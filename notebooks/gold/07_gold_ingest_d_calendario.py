# =========================================================
# 🔹 07_GOLD_INGEST_D_CALENDARIO
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Construir dimensão calendário
# - Gerar intervalo completo de datas dinamicamente
# - Garantir consistência temporal com a fato ft_resultado
# - Persistir camada física Gold (Delta)
# - Publicar no Unity Catalog
# - Expor view semântica para BI
#
# Pipeline:
# Gold Fact → Gold Dimension (Calendar)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.7 Notebook 07 – Ingestão Gold de dCalendario
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Gold (Dimensão)
#   ../docs/02_arquitetura.md → Modelo Dimensional (Star Schema)
# =========================================================

from pyspark.sql import functions as F

# =========================================================
# 1. PATHS E OBJETOS UNITY CATALOG
# =========================================================
# Referência:
# - 3.7.7.1 → Leitura da fato ft_resultado

FT_RESULTADO_TABLE = "finance_dre.gold.ft_resultado"

GOLD_PATH = "/Volumes/finance_dre/gold/dre_volume/d_calendario"

CALENDAR_TABLE = "finance_dre.gold.d_calendario"
CALENDAR_VIEW = "finance_dre.gold.dCalendario"

# =========================================================
# 2. LOG
# =========================================================

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando Gold d_calendario (Hybrid Pattern)")

# =========================================================
# 3. LEITURA DA FATO
# =========================================================
# Referência:
# - 3.7.7.1 → Fonte de dados (ft_resultado)
# - docs/02_arquitetura.md → Camada Gold Fact

df_ft = spark.table(FT_RESULTADO_TABLE)

# =========================================================
# 4. IDENTIFICAÇÃO DO INTERVALO DE DATAS
# =========================================================
# Referência:
# - 3.7.7.2 → Intervalo dinâmico de datas

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

# =========================================================
# 5. AJUSTE PARA ANOS COMPLETOS
# =========================================================
# Referência:
# - 3.7.7.3 → Ajuste de anos completos

start_date = f"{min_date.year}-01-01"
end_date = f"{max_date.year}-12-31"

# =========================================================
# 6. GERAÇÃO DO CALENDÁRIO
# =========================================================
# Referência:
# - 3.7.7.4 → Sequence + Explode

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
# 7. ATRIBUTOS TEMPORAIS
# =========================================================
# Referência:
# - 3.7.7.5 → Criação de atributos temporais

df_calendar = (
    df_calendar
    .withColumn("ano", F.year("data"))
    .withColumn("mes", F.initcap(F.date_format("data", "MMM")))
    .withColumn("mes_num", F.month("data"))
)

# =========================================================
# 8. GRAVAÇÃO GOLD FÍSICA (VOLUME)
# =========================================================
# Referência:
# - 3.7.7.6 → Persistência física

log("Gravando Gold físico (Delta Volume)...")

df_calendar.write \
    .mode("overwrite") \
    .format("delta") \
    .save(GOLD_PATH)

# =========================================================
# 9. PUBLICAÇÃO GOLD (UNITY CATALOG)
# =========================================================
# Referência:
# - 3.7.7.7 → Publicação governada

log("Publicando tabela Gold no Unity Catalog...")

df_calendar.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable(CALENDAR_TABLE)

# =========================================================
# 10. VIEW SEMÂNTICA (BI LAYER)
# =========================================================
# Referência:
# - 3.7.7.8 → Camada semântica

log("Criando view semântica dCalendario...")

spark.sql(f"""
CREATE OR REPLACE VIEW {CALENDAR_VIEW} AS
SELECT
    data     AS `Data`,
    ano      AS `Ano`,
    mes      AS `Mes`,
    mes_num  AS `Mes_Num`
FROM {CALENDAR_TABLE}
ORDER BY `Data`
""")

# =========================================================
# 11. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.7.9 → Finalização do processo

log("Gold d_calendario finalizado com sucesso")
