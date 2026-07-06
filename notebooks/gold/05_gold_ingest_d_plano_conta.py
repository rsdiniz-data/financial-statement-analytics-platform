# =========================================================
# 🔹 05_GOLD_INGEST_D_PLANO_CONTA
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Publicar dimensão d_plano_conta na camada Gold
# - Disponibilizar estrutura governada no Unity Catalog
# - Criar camada semântica para consumo em BI
# - Manter cópia física para auditoria e reprocessamento
#
# Pipeline:
# Silver (Delta) → Gold (Delta + UC + View)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.5 Notebook 05 – Ingestão Gold de dPlanoConta
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Gold (Business Data)
#   ../docs/02_arquitetura.md → Modelo Semântico (BI Views)
# =========================================================

from pyspark.sql import functions as F

# =========================================================
# 1. PATHS (FÍSICO + GOVERNANÇA)
# =========================================================
# Referência:
# - 3.7.5.1 → Leitura da camada Silver
# - docs/02_arquitetura.md → Camada Silver / Gold

SILVER_PATH = "/Volumes/finance_dre/silver/dre_volume/plano_conta"

GOLD_PATH = "/Volumes/finance_dre/gold/dre_volume/d_plano_conta"
GOLD_TABLE = "finance_dre.gold.d_plano_conta"
GOLD_VIEW = "finance_dre.gold.dPlanoConta"

# =========================================================
# 2. LOG
# =========================================================

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando Gold d_plano_conta (Hybrid Pattern)")

# =========================================================
# 3. LEITURA SILVER (DELTA)
# =========================================================
# Referência:
# - 3.7.5.1 → Consumo da camada Silver
# - docs/02_arquitetura.md → Bronze → Silver → Gold

df = spark.read.format("delta").load(SILVER_PATH)

# =========================================================
# 4. MODELAGEM DA DIMENSÃO GOLD
# =========================================================
# Referência:
# - 3.7.5.2 → Modelagem da dimensão contábil
# - docs/02_arquitetura.md → Modelo Dimensional

df_gold = df.select(
    "id_conta",
    "descricao",
    "lancamento",
    "calculado",
    "n1",
    "n2",
    "n3",
    "cod_dre",
    "tipo_indicador",
    "_source_file",
    "_ingestion_timestamp",
    "_silver_timestamp"
)

# =========================================================
# 5. GRAVAÇÃO GOLD FÍSICA (AUDITORIA / BACKUP)
# =========================================================
# Referência:
# - 3.7.5.3 → Persistência física da Gold
# - docs/05_entrega_valor.md → Reprocessamento e auditoria

log("Gravando Gold físico (Delta Volume)...")

df_gold.write \
    .mode("overwrite") \
    .format("delta") \
    .save(GOLD_PATH)

# =========================================================
# 6. PUBLICAÇÃO GOLD GOVERNADA (UNITY CATALOG)
# =========================================================
# Referência:
# - 3.7.5.4 → Publicação governada
# - docs/02_arquitetura.md → Camada Gold governada

log("Publicando Gold no Unity Catalog...")

df_gold.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable(GOLD_TABLE)

# =========================================================
# 7. VIEW SEMÂNTICA (BI LAYER)
# =========================================================
# Referência:
# - 3.7.5.5 → Criação da view semântica
# - docs/02_arquitetura.md → Camada de Consumo (BI)

log("Criando camada semântica (BI View)...")

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_VIEW} AS
SELECT
    id_conta            AS `ID Conta`,
    descricao           AS `Descrição`,
    lancamento          AS `Lançamento`,
    calculado           AS `Calculado`,
    n1                  AS `N1`,
    n2                  AS `N2`,
    n3                  AS `N3`,
    cod_dre             AS `CodDRE`,
    tipo_indicador      AS `TipoIndicador`
FROM {GOLD_TABLE}
""")

# =========================================================
# 8. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.5.6 → Estratégia Hybrid Enterprise

log("Gold d_plano_conta finalizado (Hybrid Enterprise Ready)")
