# =========================================================
# 🔹 03_SILVER_INGEST_PLANO_CONTA
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Ler dados da Bronze (Delta)
# - Aplicar transformações técnicas
# - Estruturar hierarquia contábil
# - Persistir dados tratados na Silver
#
# Pipeline:
# Bronze (Delta) → Silver (Delta)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.3 Notebook 03 – Ingestão Silver de PlanoConta
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Silver (Trusted Data)
# =========================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =========================================================
# 1. PATHS
# =========================================================
# Referência:
# - 3.7.3.1 → Definição dos caminhos (Paths)
# - docs/02_arquitetura.md → Camadas Bronze → Silver

BRONZE_PATH = "/Volumes/finance_dre/bronze/dre_volume/plano_conta"
SILVER_PATH = "/Volumes/finance_dre/silver/dre_volume/plano_conta"

# =========================================================
# 2. LOG
# =========================================================
# Referência:
# - 3.7.3.15 → Finalização e observabilidade do pipeline

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando transformação Silver - Plano de Contas")

# =========================================================
# 3. LEITURA DA BRONZE (DELTA)
# =========================================================
# Referência:
# - 3.7.3.2 → Leitura da camada Bronze
# - docs/02_arquitetura.md → Fluxo Bronze → Silver
#
# Objetivo:
# - Reutilizar dados ingeridos sem reprocessar fonte original

df_origem = spark.read.format("delta").load(BRONZE_PATH)

# =========================================================
# 4. DATAFRAME BASE
# =========================================================
# Referência:
# - 3.7.3.3 → Criação do DataFrame base
#
# Características herdadas da Bronze:
# - lowercase
# - snake_case
# - sem acentos

df = df_origem

# =========================================================
# 5. ORDENAÇÃO
# =========================================================
# Referência:
# - 3.7.3.4 → Ordenação dos registros
#
# Objetivo:
# - Garantir determinismo no processamento hierárquico

df = df.orderBy(F.col("id_conta"))

janela_rownum = Window.orderBy(F.col("id_conta"))

df = df.withColumn(
    "row_id",
    F.row_number().over(janela_rownum)
)

janela_filldown = Window.orderBy("row_id").rowsBetween(
    Window.unboundedPreceding,
    0
)

# =========================================================
# 6. IDENTIFICAÇÃO DA HIERARQUIA
# =========================================================
# Referência:
# - 3.7.3.6 → Identificação da hierarquia contábil
#
# Regra:
# - quantidade de níveis baseada em split por "."

df = df.withColumn(
    "nivel_hierarquia",
    F.size(
        F.split(F.col("id_conta"), r"\.")
    )
)

# ---------------------------------------------------------
# Nível 1
# ---------------------------------------------------------
# Referência: 3.7.3.7 → Coluna n1

df = df.withColumn(
    "n1",
    F.when(
        F.col("nivel_hierarquia") == 2,
        F.col("descricao")
    )
)

# ---------------------------------------------------------
# Nível 2
# ---------------------------------------------------------
# Referência: 3.7.3.7 → Coluna n2

df = df.withColumn(
    "n2",
    F.when(
        F.col("nivel_hierarquia") == 3,
        F.col("descricao")
    ).when(
        F.col("nivel_hierarquia") == 2,
        F.lit("TEMP")
    )
)

# ---------------------------------------------------------
# Nível 3
# ---------------------------------------------------------
# Referência: 3.7.3.7 → Coluna n3

df = df.withColumn(
    "n3",
    F.when(
        F.col("nivel_hierarquia") == 4,
        F.col("descricao")
    )
)

# =========================================================
# 7. FILLDOWN HIERÁRQUICO
# =========================================================
# Referência:
# - 3.7.3.8 → Aplicação do FillDown hierárquico
# - docs/03_desenvolvimento.md → Window Functions

df = df.withColumn(
    "n1",
    F.last("n1", ignorenulls=True).over(janela_filldown)
)

df = df.withColumn(
    "n2",
    F.last("n2", ignorenulls=True).over(janela_filldown)
)

df = df.withColumn(
    "n2",
    F.when(F.col("n2") == "TEMP", F.lit(None)).otherwise(F.col("n2"))
)

# =========================================================
# 8. CRIAÇÃO DO cod_dre
# =========================================================
# Referência:
# - 3.7.3.9 → Criação da coluna cod_dre

df = df.withColumn(
    "cod_dre",
    F.when(
        F.col("nivel_hierarquia") == 2,
        F.col("id_conta")
    )
)

df = df.withColumn(
    "cod_dre",
    F.last("cod_dre", ignorenulls=True).over(janela_filldown)
)

# =========================================================
# 9. TIPAGEM
# =========================================================
# Referência:
# - 3.7.3.10 → Aplicação de tipagem

df = (
    df
    .withColumn("cod_dre", F.col("cod_dre").cast("string"))
    .withColumn("id_conta", F.col("id_conta").cast("string"))
    .withColumn("descricao", F.col("descricao").cast("string"))
    .withColumn("lancamento", F.col("lancamento").cast("long"))
    .withColumn("calculado", F.col("calculado").cast("long"))
    .withColumn("n1", F.col("n1").cast("string"))
    .withColumn("n2", F.col("n2").cast("string"))
    .withColumn("n3", F.col("n3").cast("string"))
)

# =========================================================
# 10. CLASSIFICAÇÃO FINANCEIRA
# =========================================================
# Referência:
# - 3.7.3.11 → Classificação financeira

df = df.withColumn(
    "tipo_indicador",
    F.when(
        F.col("cod_dre").isin("3.02", "3.04"),
        F.lit(-1)
    ).otherwise(F.lit(1)).cast("long")
)

# =========================================================
# 11. METADADOS SILVER
# =========================================================
# Referência:
# - 3.7.3.12 → Metadados Silver

df = df.withColumn(
    "_silver_timestamp",
    F.current_timestamp()
)

# =========================================================
# 12. LIMPEZA FINAL
# =========================================================
# Referência:
# - 3.7.3.13 → Limpeza final

df_final = df.drop(
    "nivel_hierarquia",
    "row_id"
)

# =========================================================
# 13. GRAVAÇÃO SILVER (DELTA)
# =========================================================
# Referência:
# - 3.7.3.14 → Persistência na Silver

log("Gravando camada Silver...")

df_final.write \
    .mode("overwrite") \
    .format("delta") \
    .save(SILVER_PATH)

# =========================================================
# 14. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.3.15 → Finalização do processo

log("Silver PlanoConta finalizado com sucesso")
