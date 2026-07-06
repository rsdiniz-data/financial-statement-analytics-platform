# =========================================================
# 🔹 01_BRONZE_INGEST_PLANO_CONTA
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Ler arquivo fonte Excel (PlanoContas.xlsx)
# - Aplicar padronização técnica mínima
# - Persistir dados raw estruturados na Bronze
#
# Pipeline:
# Source (Excel) → Bronze (Delta)
#
# 🔗 Rastreabilidade:
# - Documento técnico: ../docs/03_desenvolvimento.md
# - Artigo: ../docs/06_artigo_tecnico.md   
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.1 Notebook 01 – Ingestão Bronze de PlanoConta
#
# - Arquitetura:
#   ../docs/02_arquitetura.md → Camada Bronze (Raw Data)
#
# =========================================================

%pip install openpyxl pandas
dbutils.library.restartPython()

import re
import unicodedata
import pandas as pd

from pyspark.sql import functions as F

# =========================================================
# 1. PATHS
# =========================================================
# Referência:
# - 3.7.1.1 → Definição dos caminhos (Paths)
# - docs/02_arquitetura.md → Bronze (Raw Data)
#
# Objetivo:
# - Centralizar acesso ao arquivo fonte no Data Lake
# - Garantir rastreabilidade via Unity Catalog

SOURCE_PATH = "/Volumes/finance_dre/source/raw_files/PlanoContas.xlsx"
TARGET_PATH = "/Volumes/finance_dre/bronze/dre_volume/plano_conta"

# =========================================================
# 2. LOG
# =========================================================
# Referência:
# - 3.7.1 → Desenvolvimento do pipeline Bronze
#
# Objetivo:
# - Monitorar execução do processo de ingestão

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando ingestão Bronze - Plano de Contas")

# =========================================================
# 3. FUNÇÃO DE PADRONIZAÇÃO DE COLUNAS
# =========================================================
# Referência:
# - 3.7.1.2 → Criação da função de padronização
# - docs/02_arquitetura.md → Camada Bronze (padronização técnica)
#
# Regras:
# - lowercase
# - snake_case
# - sem acentos
# - sem caracteres especiais
#
# Exemplo:
# "Descrição Conta" → "descricao_conta"
#
# Objetivo:
# - Garantir consistência entre fontes e evitar inconsistências no Spark/Delta

def normalize_column_name(col_name):

    col_name = col_name.strip()

    # remove acentos
    col_name = unicodedata.normalize("NFKD", col_name)
    col_name = col_name.encode("ascii", "ignore").decode("utf-8")

    # lowercase
    col_name = col_name.lower()

    # substitui caracteres especiais
    col_name = re.sub(r"[^a-z0-9]", "_", col_name)

    # remove múltiplos underscores
    col_name = re.sub(r"_+", "_", col_name)

    # remove underscores laterais
    col_name = col_name.strip("_")

    return col_name

# =========================================================
# 4. LEITURA DO EXCEL (PANDAS)
# =========================================================
# Referência:
# - 3.7.1.3 → Leitura do arquivo Excel
# - docs/02_arquitetura.md → Bronze (Ingestão de fontes Excel)
#
# Objetivo:
# - Ingestão controlada de arquivo financeiro corporativo
# - Base inicial do pipeline

log("Lendo arquivo Excel...")

pdf = pd.read_excel(
    SOURCE_PATH,
    engine="openpyxl"
)

# =========================================================
# 5. PADRONIZAÇÃO DAS COLUNAS
# =========================================================
# Referência:
# - 3.7.1.4 → Padronização das colunas
#
# Objetivo:
# - Garantir estrutura consistente antes da entrada no Data Lake

pdf.columns = [
    normalize_column_name(col)
    for col in pdf.columns
]

# =========================================================
# 6. CONVERSÃO PARA SPARK DATAFRAME
# =========================================================
# Referência:
# - 3.7.1.5 → Conversão para Spark DataFrame
# - docs/02_arquitetura.md → Uso de PySpark na camada Bronze
#
# Objetivo:
# - Habilitar processamento distribuído
# - Integração com Delta Lake

log("Convertendo para Spark DataFrame...")

df = spark.createDataFrame(pdf)

# =========================================================
# 7. METADADOS DE GOVERNANÇA
# =========================================================
# Referência:
# - 3.7.1.6 → Inclusão de metadados de governança
# - docs/05_entrega_valor.md → Governança e rastreabilidade
#
# Objetivo:
# - Auditoria
# - Rastreabilidade
# - Suporte a reprocessamento

df = (
    df
    .withColumn("_source_file", F.lit("PlanoContas.xlsx"))
    .withColumn("_ingestion_timestamp", F.current_timestamp())
)

# =========================================================
# 8. GRAVAÇÃO NA BRONZE (DELTA)
# =========================================================
# Referência:
# - 3.7.1.7 → Gravação na Bronze em formato Delta
# - docs/02_arquitetura.md → Bronze (Delta Lake / Volumes)
#
# Objetivo técnico:
# - Persistir dados raw estruturados
# - Garantir versionamento e reprocessamento
#
# Objetivo de negócio:
# - Centralizar dados confiáveis para próximas camadas

log("Gravando Delta Bronze...")

df.write \
    .mode("overwrite") \
    .format("delta") \
    .save(TARGET_PATH)

# =========================================================
# 9. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.1.8 → Finalização do processo
#
# Objetivo:
# - Encerrar execução com rastreabilidade operacional

log("Bronze PlanoConta finalizado com sucesso")
