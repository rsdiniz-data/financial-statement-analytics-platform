# =========================================================
# 🔹 07_GOLD_D_CALENDARIO
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Publicar a dimensão d_calendario na camada Gold
# - Gerar calendário corporativo dinâmico baseado na fato ft_resultado
# - Garantir consistência temporal entre fatos e dimensões
# - Registrar tabela governada no Unity Catalog
# - Criar view semântica para BI
#
# Pipeline:
# Gold Fact → Gold Dimension → Semantic View
#
# 🔗 Rastreabilidade:
# 📄 Documento técnico:
#   ../docs/03_desenvolvimento.md → Camada Gold
#
# 📄 Arquitetura:
#   ../docs/02_arquitetura.md → Modelo Dimensional
#
# 📄 Governança:
#   ../docs/07_governanca.md → Unity Catalog, RBAC e Data Governance
#
# 📄 Artigo técnico:
#   ../docs/17_artigo_tecnico.md
#   3.7.7 Notebook 07 – Publicação Gold da Dimensão Calendário
# =========================================================


# =========================================================
# 1. IMPORTS
# =========================================================
#
# Objetivo técnico:
# - Disponibilizar bibliotecas Spark para modelagem temporal
# =========================================================

from pyspark.sql import functions as F


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

GOLD_CATALOG = dbutils.secrets.get(scope=SECRET_SCOPE, key="gold-catalog")
GOLD_SCHEMA  = dbutils.secrets.get(scope=SECRET_SCOPE, key="gold-schema")

FACT_TABLE_NAME     = "ft_resultado"
DIM_TABLE_NAME      = "d_calendario"
SEMANTIC_VIEW_NAME  = "vw_d_calendario"


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

FACT_TABLE = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{FACT_TABLE_NAME}"
DIM_TABLE  = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{DIM_TABLE_NAME}"
SEMANTIC_VIEW = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{SEMANTIC_VIEW_NAME}"

GOLD_PATH = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net/{DIM_TABLE_NAME}"


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

log("Iniciando publicação Gold - Dimensão Calendário")


# =========================================================
# 5. LEITURA DA TABELA FATO
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.1 Leitura da tabela fato
#
# Objetivo:
# - Utilizar intervalo temporal real da fato ft_resultado
# =========================================================

log("Lendo tabela fato...")

df_ft = spark.table(FACT_TABLE)


# =========================================================
# 6. VALIDAÇÃO DA FATO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Validação de cargas
#
# Objetivo:
# - Garantir existência de registros antes da geração da dimensão
# =========================================================

if df_ft.limit(1).count() == 0:
    raise ValueError(f"A tabela {FACT_TABLE} está vazia.")


# =========================================================
# 7. IDENTIFICAÇÃO DO INTERVALO DE DATAS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.2 Identificação do intervalo de datas
#
# Objetivo:
# - Obter menor e maior data disponível na fato
# =========================================================

log("Identificando intervalo temporal...")

date_range = (
    df_ft
    .agg(
        F.min("data").alias("min_date"),
        F.max("data").alias("max_date")
    )
    .collect()[0]
)

min_date = date_range["min_date"]
max_date = date_range["max_date"]

if min_date is None or max_date is None:
    raise ValueError("Não foi possível identificar o intervalo de datas.")


# =========================================================
# 8. AJUSTE PARA ANOS COMPLETOS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.3 Ajuste para anos completos
#
# Objetivo:
# - Garantir cobertura integral dos anos no calendário
# =========================================================

start_date = f"{min_date.year}-01-01"
end_date   = f"{max_date.year}-12-31"

log(f"Calendário gerado de {start_date} até {end_date}")


# =========================================================
# 9. GERAÇÃO DA DIMENSÃO CALENDÁRIO
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.4 Geração da dimensão calendário
#
# Objetivo:
# - Criar uma linha por dia utilizando sequence() + explode()
# =========================================================

log("Gerando calendário...")

df_calendar = spark.sql(f"""
SELECT
    explode(
        sequence(
            to_date('{start_date}'),
            to_date('{end_date}'),
            interval 1 day
        )
    ) AS data
""")


# =========================================================
# 10. CRIAÇÃO DOS ATRIBUTOS TEMPORAIS
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.5 Criação dos atributos temporais
#
# Objetivo:
# - Disponibilizar atributos analíticos derivados da data
# =========================================================

df_calendar = (
    df_calendar
    .withColumn("ano", F.year("data"))
    .withColumn("mes", F.date_format("data", "MMM"))
    .withColumn("mes_num", F.month("data"))
)


# =========================================================
# 11. METADADOS DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.6 Inclusão de metadados
#
# Objetivo:
# - Registrar timestamp técnico da publicação Gold
# =========================================================

df_calendar = df_calendar.withColumn("_gold_timestamp", F.current_timestamp())


# =========================================================
# 12. PERSISTÊNCIA NA CAMADA GOLD
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.7 Persistência Gold
#
# Objetivo:
# - Persistir dimensão em Delta Lake (modo overwrite)
# =========================================================

log("Gravando dados na camada Gold...")

(
    df_calendar.write
               .format("delta")
               .mode("overwrite")
               .save(GOLD_PATH)
)


# =========================================================
# 13. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.8 Publicação no Unity Catalog
#
# Objetivo:
# - Registrar tabela governada
# =========================================================

log("Registrando tabela no Unity Catalog...")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {DIM_TABLE}
USING DELTA
LOCATION '{GOLD_PATH}'
""")

spark.sql(f"REFRESH TABLE {DIM_TABLE}")


# =========================================================
# 14. CRIAÇÃO DA VIEW SEMÂNTICA
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.9 View semântica
#
# Objetivo:
# - Disponibilizar camada amigável para BI
# =========================================================

log("Criando view semântica...")

spark.sql(f"""
CREATE OR REPLACE VIEW {SEMANTIC_VIEW} AS
SELECT
    data     AS `Data`,
    ano      AS `Ano`,
    mes      AS `Mes`,
    mes_num  AS `Mes_Num`
FROM {DIM_TABLE}
ORDER BY Data
""")


# =========================================================
# 15. VALIDAÇÃO FINAL
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.10 Finalização
#
# Objetivo:
# - Validar execução e registrar indicadores
# =========================================================

record_count = df_calendar.count()
log(f"Registros processados: {record_count}")


# =========================================================
# 16. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/17_artigo_tecnico.md → 3.7.7.10 Finalização

log("Dimensão Calendário publicada com sucesso")

print(f"Tabela Gold: {DIM_TABLE}")
print(f"View Semântica: {SEMANTIC_VIEW}")
print(f"Path Gold: {GOLD_PATH}")
print(f"Registros: {record_count}")
