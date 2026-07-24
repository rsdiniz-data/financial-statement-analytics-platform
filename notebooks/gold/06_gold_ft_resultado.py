# =========================================================
# 🔹 06_GOLD_FT_RESULTADO
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Publicar a tabela fato ft_resultado na camada Gold
# - Integrar dados financeiros tratados (Silver) com Plano de Contas
# - Aplicar regra dinâmica dos períodos mais recentes
# - Filtrar contas analíticas
# - Persistir tabela governada no Unity Catalog
# - Criar view semântica para BI
#
# Pipeline:
# Silver (Delta Lake) → Gold (Delta Lake) → Unity Catalog → BI View
#
# 🔗 Rastreabilidade:
# 📄 Documento técnico:
#   ../docs/03_desenvolvimento.md → Camada Gold e Modelagem Dimensional
#
# 📄 Arquitetura:
#   ../docs/02_arquitetura.md → Modelo Dimensional e Camada Gold
#
# 📄 Governança:
#   ../docs/07_governanca.md → Unity Catalog, RBAC e Data Governance
#
# 📄 Artigo técnico:
#   ../docs/17_artigo_tecnico.md
#   3.7.6 Notebook 06 – Publicação Gold da Tabela Fato de Resultado
# =========================================================


# =========================================================
# 1. IMPORTS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.1 Configuração do ambiente
# - docs/03_desenvolvimento.md → Transformações Gold
#
# Objetivo técnico:
# - Disponibilizar bibliotecas para processamento distribuído
# =========================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window


# =========================================================
# 2. CONFIGURAÇÕES (SECRETS / GOVERNANÇA)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Secret Scopes e RBAC
# - docs/08_runbook_implantacao.md → Key Vault e Databricks Setup
#
# Objetivo:
# - Centralizar configurações sensíveis
# - Evitar exposição de credenciais
# =========================================================

SECRET_SCOPE = "ss-finance-dre-kv"

STORAGE_ACCOUNT = dbutils.secrets.get(scope=SECRET_SCOPE, key="storage-account-name")

SILVER_CATALOG = dbutils.secrets.get(scope=SECRET_SCOPE, key="silver-catalog")
SILVER_SCHEMA  = dbutils.secrets.get(scope=SECRET_SCOPE, key="silver-schema")

GOLD_CATALOG = dbutils.secrets.get(scope=SECRET_SCOPE, key="gold-catalog")
GOLD_SCHEMA  = dbutils.secrets.get(scope=SECRET_SCOPE, key="gold-schema")

RESULTADO_TABLE_NAME     = "resultado"
PLANO_CONTA_TABLE_NAME   = "plano_conta"
GOLD_TABLE_NAME          = "ft_resultado"
SEMANTIC_VIEW_NAME       = "vw_ft_resultado"


# =========================================================
# 3. PATHS E OBJETOS LÓGICOS
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Separação entre camadas física e lógica
#
# Objetivo:
# - Definir caminhos físicos (ADLS) e lógicos (Unity Catalog)
# =========================================================

GOLD_PATH = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net/{GOLD_TABLE_NAME}"

RESULTADO_TABLE   = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{RESULTADO_TABLE_NAME}"
PLANO_CONTA_TABLE = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{PLANO_CONTA_TABLE_NAME}"

GOLD_TABLE        = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{GOLD_TABLE_NAME}"
SEMANTIC_VIEW     = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{SEMANTIC_VIEW_NAME}"


# =========================================================
# 4. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Monitoramento e logs
#
# Objetivo:
# - Padronizar rastreabilidade de execução
# =========================================================

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando publicação Gold - Fato Resultado")


# =========================================================
# 5. LEITURA DAS TABELAS SILVER
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Consumo da camada Silver
# - docs/17_artigo_tecnico.md → 3.7.6.1 Leitura das tabelas Silver
#
# Objetivo:
# - Consumir dados tratados e governados
# =========================================================

log("Lendo tabelas da camada Silver...")

df_resultado = spark.table(RESULTADO_TABLE)
df_plano     = spark.table(PLANO_CONTA_TABLE)


# =========================================================
# 6. IDENTIFICAÇÃO DINÂMICA DOS ÚLTIMOS PERÍODOS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.2 Identificação dinâmica dos períodos
#
# Objetivo:
# - Selecionar automaticamente os 3 períodos mais recentes
# =========================================================

log("Identificando períodos mais recentes...")

window_periodo = Window.orderBy(F.col("data_referencia").desc())

df_resultado = (
    df_resultado
    .withColumn("rank_periodo", F.dense_rank().over(window_periodo))
    .filter(F.col("rank_periodo") <= 3)
    .drop("rank_periodo")
)


# =========================================================
# 7. INTEGRAÇÃO COM DIMENSÃO PLANO DE CONTAS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.3 Integração com Plano de Contas
#
# Objetivo:
# - Enriquecer dados financeiros com atributos contábeis
# =========================================================

log("Integrando com Plano de Contas...")

df_join = (
    df_resultado.alias("r")
    .join(
        df_plano.select("id_conta", "lancamento").alias("p"),
        F.col("r.codigo_da_conta") == F.col("p.id_conta"),
        "left"
    )
)


# =========================================================
# 8. FILTRAGEM DE CONTAS ANALÍTICAS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.4 Filtragem das contas analíticas
#
# Objetivo:
# - Manter apenas contas lançáveis (lancamento = 1)
# =========================================================

log("Filtrando contas analíticas...")

df_fact = df_join.filter(F.col("lancamento") == 1)


# =========================================================
# 9. MODELAGEM DA TABELA FATO
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.5 Modelagem da tabela fato
#
# Objetivo:
# - Estruturar fato enxuta e otimizada para BI
# =========================================================

log("Modelando tabela fato...")

df_fact = (
    df_fact
    .select(
        F.col("codigo_da_conta").alias("id_conta"),
        F.col("data_referencia").alias("data"),
        F.col("valor"),
        F.col("ano")
    )
)


# =========================================================
# 10. CONTROLE DE QUALIDADE E METADADOS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.6 Controle de qualidade e metadados
#
# Objetivo:
# - Remover duplicidades
# - Registrar timestamp técnico
# =========================================================

df_fact = df_fact.dropDuplicates()

df_fact = df_fact.withColumn("_gold_timestamp", F.current_timestamp())


# =========================================================
# 11. PERSISTÊNCIA NA CAMADA GOLD
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.7 Persistência Gold
#
# Objetivo:
# - Persistir tabela fato em Delta Lake
# - Particionar fisicamente por ano
# =========================================================

log("Gravando dados na camada Gold...")

(
    df_fact.write
           .format("delta")
           .mode("overwrite")
           .partitionBy("ano")
           .save(GOLD_PATH)
)


# =========================================================
# 12. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.8 Publicação no Unity Catalog
#
# Objetivo:
# - Registrar tabela governada
# =========================================================

log("Registrando tabela no Unity Catalog...")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {GOLD_TABLE}
USING DELTA
LOCATION '{GOLD_PATH}'
""")

spark.sql(f"REFRESH TABLE {GOLD_TABLE}")


# =========================================================
# 13. CRIAÇÃO DA VIEW SEMÂNTICA
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.9 View semântica
#
# Objetivo:
# - Disponibilizar camada amigável para BI
# =========================================================

log("Criando view semântica...")

spark.sql(f"""
CREATE OR REPLACE VIEW {SEMANTIC_VIEW} AS
SELECT
    id_conta AS `ID Conta`,
    data     AS `Data`,
    valor    AS `Valor`
FROM {GOLD_TABLE}
ORDER BY Data, ID Conta
""")


# =========================================================
# 14. VALIDAÇÃO FINAL
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.10 Finalização
#
# Objetivo:
# - Validar execução e registrar indicadores
# =========================================================

record_count = df_fact.count()
log(f"Registros processados: {record_count}")


# =========================================================
# 15. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.6.10 Finalização

log("Publicação Gold concluída com sucesso")

print(f"Tabela Gold: {GOLD_TABLE}")
print(f"View Semântica: {SEMANTIC_VIEW}")
print(f"Path Gold: {GOLD_PATH}")
print(f"Registros: {record_count}")
