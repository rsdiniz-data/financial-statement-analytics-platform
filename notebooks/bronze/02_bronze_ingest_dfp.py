# =========================================================
# 🔹 02_BRONZE_INGEST_DFP
# Projeto: DRE | Medallion Architecture Databricks
#
# Objetivo:
# - Ler arquivo fonte Excel (DFP.xlsx)
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
#   3.7.2 Notebook 02 – Ingestão Bronze de DFP
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
# - 3.7.2.1 → Definição dos caminhos (Paths)
# - docs/02_arquitetura.md → Camada Bronze (Raw Data)
#
# Negócio:
# Centraliza o acesso aos arquivos financeiros e elimina dependência de diretórios locais.

SOURCE_PATH = "/Volumes/finance_dre/source/raw_files/DFP.xlsx"
TARGET_PATH = "/Volumes/finance_dre/bronze/dre_volume/dfp"

# =========================================================
# 2. LOG
# =========================================================
# Referência:
# - 3.7.2 → Estrutura padrão de logging operacional

def log(msg):
    print(f"[INFO] {msg}")

log("Iniciando ingestão Bronze - DFP")

# =========================================================
# 3. FUNÇÃO DE PADRONIZAÇÃO DE COLUNAS
# =========================================================
# Referência:
# - 3.7.2.2 → Criação da função de padronização
# - 3.7.2.3 → Tratamento de quebras de linha nos cabeçalhos
#
# Regras:
# - lowercase
# - snake_case
# - remoção de acentos
# - remoção de caracteres especiais
# - remoção de quebras de linha (\n, \r)
#
# Negócio:
# Garante consistência estrutural no dataset financeiro e evita problemas de compatibilidade no Spark.

def normalize_column_name(col_name):

    # remove espaços laterais
    col_name = col_name.strip()

    # remove quebras de linha
    col_name = col_name.replace("\n", " ")
    col_name = col_name.replace("\r", " ")

    # remove acentos
    col_name = unicodedata.normalize("NFKD", col_name)
    col_name = col_name.encode("ascii", "ignore").decode("utf-8")

    # lowercase
    col_name = col_name.lower()

    # substitui caracteres especiais por underscore
    col_name = re.sub(r"[^a-z0-9]", "_", col_name)

    # remove underscores duplicados
    col_name = re.sub(r"_+", "_", col_name)

    # remove underscore início/fim
    col_name = col_name.strip("_")

    return col_name

# =========================================================
# 4. LEITURA DO EXCEL (PANDAS)
# =========================================================
# Referência:
# - 3.7.2.4 → Leitura do arquivo Excel
# - docs/02_arquitetura.md → Camada Bronze (Raw Data)
#
# Negócio:
# Permite ingestão controlada de demonstrativos financeiros em formato Excel.

log("Lendo arquivo Excel...")

pdf = pd.read_excel(
    SOURCE_PATH,
    engine="openpyxl"
)

# =========================================================
# 5. PADRONIZAÇÃO DE COLUNAS
# =========================================================
# Referência:
# - 3.7.2.5 → Padronização das colunas
#
# Negócio:
# Padroniza a estrutura técnica do dataset antes da entrada no Data Lake.

pdf.columns = [
    normalize_column_name(col)
    for col in pdf.columns
]

# =========================================================
# 6. CONVERSÃO PARA SPARK
# =========================================================
# Referência:
# - 3.7.2.6 → Conversão para Spark DataFrame
#
# Negócio:
# Permite processamento distribuído e integração com Delta Lake.

log("Convertendo para Spark DataFrame...")

df = spark.createDataFrame(pdf)

# =========================================================
# 7. METADADOS DE GOVERNANÇA
# =========================================================
# Referência:
# - 3.7.2.7 → Inclusão de metadados de governança
# - docs/05_entrega_valor.md → Rastreabilidade e auditoria
#
# Negócio:
# Garante auditoria, rastreabilidade e suporte a reprocessamentos futuros.

df = (
    df
    .withColumn(
        "_source_file",
        F.lit("DFP.xlsx")
    )
    .withColumn(
        "_ingestion_timestamp",
        F.current_timestamp()
    )
)

# =========================================================
# 8. GRAVAÇÃO NA BRONZE (DELTA)
# =========================================================
# Referência:
# - 3.7.2.8 → Gravação na Bronze em formato Delta
# - docs/02_arquitetura.md → Camada Bronze (Raw Data)
#
# Negócio:
# Cria camada raw estruturada preparada para transformação na Silver.

log("Gravando Delta Bronze...")

df.write \
    .mode("overwrite") \
    .format("delta") \
    .save(TARGET_PATH)

# =========================================================
# 9. FINALIZAÇÃO
# =========================================================
# Referência:
# - 3.7.2.9 → Finalização do processo

log("Bronze DFP finalizado com sucesso")
