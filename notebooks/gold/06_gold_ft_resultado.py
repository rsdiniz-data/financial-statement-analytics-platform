# =========================================================
# 🔹 06_GOLD_FT_RESULTADO
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Construção da tabela fato de resultado financeiro (ft_resultado)
# - Integração com dimensão Plano de Contas
# - Aplicação de regras dinâmicas de período
# - Filtragem de contas analíticas
# - Persistência na camada Gold (Delta Lake)
# - Registro no Unity Catalog
# - Criação de view semântica para BI
#
# Pipeline:
# Silver (Delta Lake) → Gold (Delta Lake) → Unity Catalog → BI View
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/03_desenvolvimento.md → Camada Gold e Modelagem Dimensional
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md → Modelo Dimensional e Camada Gold
#
# 📄 Governança:
# - ../docs/07_governanca.md → Unity Catalog, RBAC e Data Governance
#
# 📄 Runbook de Implantação:
# - ../docs/08_runbook_implantacao.md → Databricks Setup e Governança
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.6 Notebook 06 – Fato Resultado
#
# =========================================================


# =========================================================
# 1. IMPORTS
# =========================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window


# =========================================================
# 2. CONFIGURAÇÕES (SECRETS / GOVERNANÇA)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e Secret Scopes
# - docs/08_runbook_implantacao.md → Azure Key Vault
#

SECRET_SCOPE = "ss-finance-dre-kv"

STORAGE_ACCOUNT = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="storage-account-name"
)

SILVER_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-catalog"
)

SILVER_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-schema"
)

GOLD_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="gold-catalog"
)

GOLD_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="gold-schema"
)

RESULTADO_TABLE_NAME = "resultado"
PLANO_CONTA_TABLE_NAME = "plano_conta"

GOLD_TABLE_NAME = "ft_resultado"
SEMANTIC_VIEW_NAME = "vw_ft_resultado"


# =========================================================
# 3. PATHS E OBJETOS
# =========================================================
#
# Referência:
# - Camada Gold (Delta Lake)
#

GOLD_PATH = (
    f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{GOLD_TABLE_NAME}"
)

RESULTADO_TABLE = (
    f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{RESULTADO_TABLE_NAME}"
)

PLANO_CONTA_TABLE = (
    f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{PLANO_CONTA_TABLE_NAME}"
)

GOLD_TABLE = (
    f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{GOLD_TABLE_NAME}"
)

SEMANTIC_VIEW = (
    f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{SEMANTIC_VIEW_NAME}"
)


# =========================================================
# 4. LOG OPERACIONAL
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando publicação Gold - Fato Resultado")


# =========================================================
# 5. LEITURA DA CAMADA SILVER
# =========================================================
#
# Objetivo:
# - Consumir dados tratados e governados
#

log("Lendo tabelas da camada Silver...")

df_resultado = spark.table(RESULTADO_TABLE)
df_plano = spark.table(PLANO_CONTA_TABLE)


# =========================================================
# 6. FILTRO DE PERÍODOS RECENTES
# =========================================================
#
# Objetivo:
# - Selecionar automaticamente os últimos períodos
#

log("Selecionando últimos períodos...")

window_spec = Window.orderBy(F.col("data_referencia").desc())

df_resultado = (
    df_resultado
    .withColumn("rank_periodo", F.dense_rank().over(window_spec))
    .filter(F.col("rank_periodo") <= 3)
    .drop("rank_periodo")
)


# =========================================================
# 7. INTEGRAÇÃO COM DIMENSÃO PLANO DE CONTAS
# =========================================================
#
# Objetivo:
# - Aplicar regras contábeis da dimensão
#

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
# 8. FILTRO DE CONTAS ANALÍTICAS
# =========================================================
#
# Objetivo:
# - Manter apenas contas lançáveis
#

log("Filtrando contas analíticas...")

df_fact = df_join.filter(F.col("lancamento") == 1)


# =========================================================
# 9. MODELAGEM DA FATO
# =========================================================
#
# Objetivo:
# - Estruturar tabela fato final
#

log("Construindo modelo da fato...")

df_fact = (
    df_fact.select(
        F.col("codigo_da_conta").alias("id_conta"),
        F.col("data_referencia").alias("data"),
        F.col("valor"),
        F.col("ano")
    )
)


# =========================================================
# 10. QUALIDADE DOS DADOS
# =========================================================

df_fact = df_fact.dropDuplicates()


# =========================================================
# 11. METADADOS DE GOVERNANÇA
# =========================================================
#
# Objetivo:
# - Auditoria e rastreabilidade
#

df_fact = df_fact.withColumn(
    "_gold_timestamp",
    F.current_timestamp()
)


# =========================================================
# 12. PERSISTÊNCIA NA CAMADA GOLD
# =========================================================
#
# Objetivo:
# - Armazenamento otimizado em Delta Lake
#

log("Persistindo camada Gold...")

(
    df_fact.write
    .format("delta")
    .mode("overwrite")
    .partitionBy("ano")
    .save(GOLD_PATH)
)


# =========================================================
# 13. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Objetivo:
# - Governança centralizada
#

log("Registrando no Unity Catalog...")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {GOLD_TABLE}
USING DELTA
LOCATION '{GOLD_PATH}'
""")

spark.sql(f"REFRESH TABLE {GOLD_TABLE}")


# =========================================================
# 14. CRIAÇÃO DA VIEW SEMÂNTICA
# =========================================================
#
# Objetivo:
# - Camada amigável para BI
#

log("Criando view semântica...")

spark.sql(f"""
CREATE OR REPLACE VIEW {SEMANTIC_VIEW} AS

SELECT
    id_conta AS `ID Conta`,
    data     AS `Data`,
    valor    AS `Valor`
FROM {GOLD_TABLE}
ORDER BY data, id_conta
""")


# =========================================================
# 15. VALIDAÇÃO FINAL
# =========================================================

record_count = df_fact.count()

log(f"Registros processados: {record_count}")


# =========================================================
# 16. FINALIZAÇÃO
# =========================================================

log("Processo Gold Fato Resultado finalizado com sucesso")

print(f"Tabela: {GOLD_TABLE}")
print(f"View: {SEMANTIC_VIEW}")
print(f"Path: {GOLD_PATH}")
print(f"Registros: {record_count}")
