# =========================================================
# 🔹 04_SILVER_INGEST_RESULTADO
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Ler dados financeiros da Bronze (Delta)
# - Aplicar limpeza e padronização
# - Transformar estrutura wide em formato analítico (long)
# - Persistir dados tratados na Silver
#
# Pipeline:
# Bronze (Delta) → Silver (Delta)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.4 Notebook 04 – Ingestão Silver de Resultado
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Silver (Trusted Data)
# =========================================================

from pyspark.sql import functions as F

# =========================================================
# 1. PATHS
# =========================================================
# Referência:
# - 3.7.4.1 → Leitura da camada Bronze
# - docs/02_arquitetura.md → Fluxo Bronze → Silver

BRONZE_PATH = "/Volumes/finance_dre/bronze/dre_volume/dfp"
SILVER_PATH = "/Volumes/finance_dre/silver/dre_volume/resultado"

# =========================================================
# 2. LOG
# =========================================================
# Referência:
# - 3.7.4.8 → Persistência e observabilidade

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando transformação Silver - Resultado")

# =========================================================
# 3. LEITURA DA BRONZE (DELTA)
# =========================================================
# Referência:
# - 3.7.4.1 → Leitura da camada Bronze

df_origem = spark.read.format("delta").load(BRONZE_PATH)

# =========================================================
# 4. LIMPEZA PRÉVIA
# =========================================================
# Referência:
# - 3.7.4.2 → Limpeza e padronização inicial
#
# Objetivo:
# - remover inconsistências e registros inválidos

df_limpo = (
    df_origem
    .withColumn("codigo_da_conta", F.trim(F.col("codigo_da_conta")))
    .withColumn("descricao_da_conta", F.trim(F.col("descricao_da_conta")))
)

df_limpo = df_limpo.filter(
    F.col("codigo_da_conta").isNotNull() &
    (F.col("codigo_da_conta") != "")
)

df_limpo = df_limpo.filter(
    F.coalesce(
        F.col("penultimo_exercicio_01_01_2021_a_31_12_2021"),
        F.col("ultimo_exercicio_01_01_2022_a_31_12_2022"),
        F.col("penultimo_exercicio_01_01_2023_a_31_12_2023"),
        F.col("ultimo_exercicio_01_01_2024_a_31_12_2024")
    ).isNotNull()
)

df_limpo = df_limpo.dropDuplicates()

# =========================================================
# 5. UNPIVOT (WIDE → LONG)
# =========================================================
# Referência:
# - 3.7.4.3 → Transformação estrutural (Wide → Long)
#
# Objetivo:
# - transformar colunas de períodos em linhas

expr_unpivot = """
stack(
    4,
    '31/12/2021', penultimo_exercicio_01_01_2021_a_31_12_2021,
    '31/12/2022', ultimo_exercicio_01_01_2022_a_31_12_2022,
    '31/12/2023', penultimo_exercicio_01_01_2023_a_31_12_2023,
    '31/12/2024', ultimo_exercicio_01_01_2024_a_31_12_2024
) as (data_referencia, valor_bruto)
"""

df_unpivot = df_limpo.selectExpr(
    "codigo_da_conta",
    "descricao_da_conta",
    expr_unpivot
)

# =========================================================
# 6. TRATAMENTO DOS VALORES
# =========================================================
# Referência:
# - 3.7.4.4 → Tratamento dos valores financeiros

df_tratado = (
    df_unpivot
    .withColumn("valor_bruto", F.trim(F.col("valor_bruto").cast("string")))
    .withColumn(
        "valor_bruto",
        F.when(
            F.col("valor_bruto").isin("", "-", "null", "None"),
            None
        ).otherwise(F.col("valor_bruto"))
    )
    .withColumn("valor_bruto", F.regexp_replace(F.col("valor_bruto"), r"\.", ""))
    .withColumn("valor_bruto", F.regexp_replace(F.col("valor_bruto"), ",", "."))
    .withColumn(
        "valor_bruto",
        F.regexp_replace(F.col("valor_bruto"), r"^\((.*)\)$", r"-\1")
    )
)

# =========================================================
# 7. TIPAGEM E ATRIBUTOS TEMPORAIS
# =========================================================
# Referência:
# - 3.7.4.5 → Conversão de tipos e atributos temporais

df_resultado = (
    df_tratado
    .withColumn("codigo_da_conta", F.col("codigo_da_conta").cast("string"))
    .withColumn("descricao_da_conta", F.col("descricao_da_conta").cast("string"))
    .withColumn("data_referencia", F.to_date(F.col("data_referencia"), "dd/MM/yyyy"))
    .withColumn("valor", F.col("valor_bruto").cast("double"))
    .withColumn("ano", F.year(F.col("data_referencia")))
    .drop("valor_bruto")
)

# =========================================================
# 8. LIMPEZA FINAL
# =========================================================
# Referência:
# - 3.7.4.6 → Limpeza final e qualidade de dados

df_resultado = df_resultado.filter(F.col("valor").isNotNull())
df_resultado = df_resultado.dropDuplicates()

# =========================================================
# 9. METADADOS SILVER
# =========================================================
# Referência:
# - 3.7.4.7 → Metadados de governança

df_resultado = df_resultado.withColumn(
    "_silver_timestamp",
    F.current_timestamp()
)

# =========================================================
# 10. GRAVAÇÃO SILVER (DELTA)
# =========================================================
# Referência:
# - 3.7.4.8 → Persistência da camada Silver

log("Gravando camada Silver...")

df_resultado.write \
    .mode("overwrite") \
    .format("delta") \
    .partitionBy("ano") \
    .save(SILVER_PATH)

# =========================================================
# 11. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.4.8 → Encerramento do pipeline

log("Silver Resultado finalizado com sucesso")
