# =========================================================
# 🔹 06_GOLD_INGEST_FT_RESULTADO
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Construir tabela fato ft_resultado
# - Aplicar regra dinâmica dos últimos 3 períodos
# - Integrar com plano de contas (dimensão)
# - Filtrar apenas contas analíticas
# - Persistir camada Gold particionada por ano
# - Publicar tabela no Unity Catalog
# - Expor view semântica para BI
#
# Pipeline:
# Silver → Gold (Delta Table + View)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.6 Notebook 06 – Ingestão Gold de ftResultado
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Gold (Fact Table)
#   ../docs/02_arquitetura.md → Modelo Dimensional (Star Schema)
# =========================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# =========================================================
# 1. PATHS E OBJETOS
# =========================================================
# Referência:
# - 3.7.6.1 → Leitura das camadas Silver
# - docs/02_arquitetura.md → Camada Silver / Gold

GOLD_PATH = "/Volumes/finance_dre/gold/dre_volume/ft_resultado"

GOLD_TABLE = "finance_dre.gold.ft_resultado"
GOLD_VIEW = "finance_dre.gold.ftResultado"

# =========================================================
# 2. LOG
# =========================================================

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando Gold ft_resultado (Hybrid Pattern)")

# =========================================================
# 3. LEITURA DAS CAMADAS SILVER
# =========================================================
# Referência:
# - 3.7.6.1 → Consumo das camadas Silver

df_resultado = spark.read.format("delta").load(
    "/Volumes/finance_dre/silver/dre_volume/resultado"
)

df_plano = spark.read.format("delta").load(
    "/Volumes/finance_dre/silver/dre_volume/plano_conta"
)

# =========================================================
# 4. FILTRO DINÂMICO - ÚLTIMOS 3 PERÍODOS
# =========================================================
# Referência:
# - 3.7.6.2 → Filtro dinâmico de períodos
# - docs/05_entrega_valor.md → Automação e escalabilidade

window_data = Window.orderBy(F.col("data_referencia").desc())

df_resultado_filtrado = (
    df_resultado
    .withColumn(
        "rank_data",
        F.dense_rank().over(window_data)
    )
    .filter(F.col("rank_data") <= 3)
    .drop("rank_data")
)

# =========================================================
# 5. JOIN COM PLANO DE CONTAS
# =========================================================
# Referência:
# - 3.7.6.3 → Integração com Plano de Contas

df_join = (
    df_resultado_filtrado.alias("r")
    .join(
        df_plano.select("id_conta", "lancamento").alias("p"),
        F.col("r.codigo_da_conta") == F.col("p.id_conta"),
        "left"
    )
)

# =========================================================
# 6. MODELO BASE DA FATO
# =========================================================
# Referência:
# - 3.7.6.4 → Construção da estrutura da fato

df_base = df_join.select(
    F.col("r.codigo_da_conta").alias("id_conta"),
    F.col("r.data_referencia").alias("data"),
    F.col("r.valor"),
    F.col("r.ano"),
    F.col("p.lancamento")
)

# =========================================================
# 7. FILTRO DE NEGÓCIO (CONTAS ANALÍTICAS)
# =========================================================
# Referência:
# - 3.7.6.5 → Regra de contas analíticas

df_base = df_base.filter(F.col("lancamento") == 1)

# =========================================================
# 8. MODELO FINAL DA FATO
# =========================================================
# Referência:
# - 3.7.6.6 → Modelagem física final

df_final = df_base.drop("lancamento")

# =========================================================
# 9. GRAVAÇÃO GOLD FÍSICA (VOLUME)
# =========================================================
# Referência:
# - 3.7.6.7 → Persistência física da Gold

log("Gravando Gold físico (Delta Volume)...")

df_final.write \
    .mode("overwrite") \
    .format("delta") \
    .partitionBy("ano") \
    .save(GOLD_PATH)

# =========================================================
# 10. PUBLICAÇÃO GOLD (UNITY CATALOG)
# =========================================================
# Referência:
# - 3.7.6.8 → Publicação governada

log("Publicando tabela Gold no Unity Catalog...")

df_final.write \
    .mode("overwrite") \
    .format("delta") \
    .partitionBy("ano") \
    .saveAsTable(GOLD_TABLE)

# =========================================================
# 11. VIEW SEMÂNTICA (BI LAYER)
# =========================================================
# Referência:
# - 3.7.6.9 → Criação da view semântica

log("Criando view semântica...")

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_VIEW} AS
SELECT
    id_conta AS `ID Conta`,
    data     AS `Data`,
    valor    AS `Valor`
FROM {GOLD_TABLE}
ORDER BY
    `Data`,
    `ID Conta`
""")

# =========================================================
# 12. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.6.10 → Estratégia Hybrid Enterprise

log("Gold ft_resultado finalizado com sucesso")
