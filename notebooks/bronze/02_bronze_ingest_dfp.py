# =========================================================
# 🔹 02_BRONZE_INGEST_DFP
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Ingestão automatizada do DFP.xlsx (SharePoint)
# - Padronização técnica mínima
# - Persistência na camada Bronze (Delta Lake)
# - Registro no Unity Catalog
#
# Pipeline:
# SharePoint → Bronze (Delta Lake) → Unity Catalog
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/03_desenvolvimento.md → Ingestão Bronze
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md → Camada Bronze (Raw Data / Ingestão)
#
# 📄 Governança:
# - ../docs/07_governanca.md → Unity Catalog, RBAC e Secrets Management
#
# 📄 Runbook de Implantação:
# - ../docs/08_runbook_implantacao.md → Key Vault, Secrets Scope e Databricks Setup
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.2 Notebook 02 – Ingestão Bronze de DFP
#
# =========================================================


# =========================================================
# 0. INSTALAÇÃO DE DEPENDÊNCIAS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Ingestão Bronze (pré-processamento técnico)
# - docs/08_runbook_implantacao.md → Configuração de ambiente Databricks
# - docs/15_artigo_tecnico.md → 3.7.2.1 Gerenciamento de dependências
#
# Objetivo técnico:
# - Garantir suporte à leitura de arquivos Excel
# - Habilitar integração com Microsoft Graph API
#
# =========================================================

%pip install openpyxl pandas requests

dbutils.library.restartPython()


# =========================================================
# 1. IMPORTS
# =========================================================

import re
import unicodedata
import requests
import pandas as pd

from io import BytesIO
from pyspark.sql import functions as F


# =========================================================
# 2. CONFIGURAÇÕES (SECRETS / GOVERNANÇA)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Gestão de identidades, RBAC e Secret Scopes
# - docs/08_runbook_implantacao.md → Integração com Azure Key Vault
# - docs/15_artigo_tecnico.md → 3.7.2.2 Configuração do ambiente
#
# Objetivo de negócio:
# - Centralizar credenciais no Azure Key Vault
# - Evitar exposição de secrets no código
# - Garantir governança e segurança
#
# =========================================================

SECRET_SCOPE = "ss-finance-dre-kv"

SPO_TENANT_ID = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="spo-tenant-id"
)

SPO_CLIENT_ID = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="spo-client-id"
)

SPO_CLIENT_SECRET = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="spo-client-secret"
)

SITE_ID = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="sharepoint-site-id"
)

ITEM_ID = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="dfp-item-id"
)

STORAGE_ACCOUNT = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="storage-account-name"
)

BRONZE_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="bronze-catalog"
)

BRONZE_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="bronze-schema"
)

TABLE_NAME = "dfp"

SOURCE_FILE_NAME = "DFP.xlsx"


# =========================================================
# 3. PATHS E CONFIGURAÇÕES LÓGICAS
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Separação entre camadas (Storage vs Unity Catalog)
# - docs/03_desenvolvimento.md → Estrutura da camada Bronze
# - docs/15_artigo_tecnico.md → 3.7.2.3 Definição de caminhos
#
# Objetivo técnico:
# - Separar camada física (ADLS) da camada lógica (Unity Catalog)
# - Garantir rastreabilidade e governança dos dados
#
# =========================================================

TARGET_PATH = (
    f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{TABLE_NAME}"
)

FULL_TABLE_NAME = (
    f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.{TABLE_NAME}"
)


# =========================================================
# 4. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Monitoramento e logs
#
# Objetivo:
# - Padronizar rastreabilidade de execução
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando ingestão Bronze - DFP")

# =========================================================
# 5. PADRONIZAÇÃO DE COLUNAS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações técnicas na camada Bronze
# - docs/02_arquitetura.md → Padronização mínima (Bronze Layer)
# - docs/15_artigo_tecnico.md → 3.7.2.4 Padronização de colunas
#
# Objetivo de negócio:
# - Garantir consistência entre fontes de dados
# - Evitar inconsistências no Spark/Delta/Unity Catalog
#
# =========================================================

def normalize_column_name(column_name):

    column_name = str(column_name).strip()

    column_name = column_name.replace("\n", " ")
    column_name = column_name.replace("\r", " ")

    column_name = (
        unicodedata
        .normalize("NFKD", column_name)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    column_name = column_name.lower()

    column_name = re.sub(
        r"[^a-z0-9]",
        "_",
        column_name
    )

    column_name = re.sub(
        r"_+",
        "_",
        column_name
    )

    return column_name.strip("_")


# =========================================================
# 6. AUTENTICAÇÃO SHAREPOINT (MICROSOFT GRAPH)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Controle de acesso e autenticação
# - docs/08_runbook_implantacao.md → App Registration e OAuth2
# - docs/15_artigo_tecnico.md → 3.7.2.6 Autenticação SharePoint
#
# Objetivo de negócio:
# - Garantir ingestão automatizada da fonte oficial (SharePoint)
# - Eliminar dependência de arquivos manuais
#
# =========================================================

log("Autenticando no Microsoft Graph")

token_url = (
    f"https://login.microsoftonline.com/"
    f"{SPO_TENANT_ID}/oauth2/v2.0/token"
)

token_payload = {
    "grant_type": "client_credentials",
    "client_id": SPO_CLIENT_ID,
    "client_secret": SPO_CLIENT_SECRET,
    "scope": "https://graph.microsoft.com/.default"
}

token_response = requests.post(
    token_url,
    data=token_payload
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}


# =========================================================
# 7. DOWNLOAD E LEITURA DO ARQUIVO
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Ingestão de dados externos
# - docs/02_arquitetura.md → Integração de fontes (SharePoint → Bronze)
# - docs/15_artigo_tecnico.md → 3.7.2.7 Leitura do arquivo
#
# Objetivo técnico:
# - Carregar dados diretamente em memória
# - Evitar arquivos temporários e reduzir I/O
#
# =========================================================

log("Baixando arquivo do SharePoint")

download_url = (
    f"https://graph.microsoft.com/v1.0/"
    f"sites/{SITE_ID}/drive/items/{ITEM_ID}/content"
)

response = requests.get(
    download_url,
    headers=headers
)

response.raise_for_status()


# =========================================================
# 8. LEITURA DO EXCEL
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Ingestão Bronze (Excel → Pandas → Spark)
# - docs/15_artigo_tecnico.md → 3.7.2.7 Leitura do arquivo
#
# Objetivo:
# - Ler arquivo em memória sem persistência local
#
# =========================================================

log("Lendo arquivo Excel")

pdf = pd.read_excel(
    BytesIO(response.content),
    engine="openpyxl"
)


# =========================================================
# 9. PADRONIZAÇÃO DAS COLUNAS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Padronização técnica de dados
#
# Objetivo:
# - Normalizar nomes de colunas para padrão técnico
#
# =========================================================

pdf.columns = [
    normalize_column_name(col)
    for col in pdf.columns
]


# =========================================================
# 10. CONVERSÃO PARA SPARK DATAFRAME
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Uso de Spark na camada Bronze
# - docs/03_desenvolvimento.md → Processamento distribuído
# - docs/15_artigo_tecnico.md → 3.7.2.8 Conversão para Spark
#
# Objetivo de negócio:
# - Habilitar processamento distribuído
# - Preparar dados para Delta Lake
#
# =========================================================

log("Convertendo para Spark DataFrame")

df = spark.createDataFrame(pdf)


# =========================================================
# 11. METADADOS DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Data lineage e auditoria
# - docs/05_entrega_valor.md → Rastreabilidade dos dados
# - docs/15_artigo_tecnico.md → 3.7.2.9 Metadados de governança
#
# Objetivo de negócio:
# - Garantir rastreabilidade (origem e timestamp)
# - Suportar auditoria e reprocessamento
#
# =========================================================

df = (
    df
    .withColumn("_source_file", F.lit(SOURCE_FILE_NAME))
    .withColumn("_ingestion_timestamp", F.current_timestamp())
)


# =========================================================
# 12. PERSISTÊNCIA NA CAMADA BRONZE
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Bronze Layer (Delta Lake)
# - docs/03_desenvolvimento.md → Persistência em formato Delta
# - docs/15_artigo_tecnico.md → 3.7.2.10 Persistência na Bronze
#
# Objetivo de negócio:
# - Armazenar dados raw estruturados
# - Garantir versionamento e reprocessamento via Delta Lake
#
# =========================================================

log("Gravando dados na camada Bronze")

df.write.format("delta") \
    .mode("overwrite") \
    .save(TARGET_PATH)


# =========================================================
# 13. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e governança centralizada
# - docs/15_artigo_tecnico.md → 3.7.2.10 Persistência na Bronze
#
# Objetivo:
# - Registrar tabela governada
# - Disponibilizar para consumo analítico seguro
#
# =========================================================

log("Registrando tabela no Unity Catalog")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {FULL_TABLE_NAME}
USING DELTA
LOCATION '{TARGET_PATH}'
""")

spark.sql(
    f"REFRESH TABLE {FULL_TABLE_NAME}"
)

# =========================================================
# 14. VALIDAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Validação de cargas
# - docs/15_artigo_tecnico.md → 3.7.2.11 Validação e encerramento
#
# Objetivo:
# - Garantir execução bem-sucedida do pipeline
#
# =========================================================

record_count = df.count()

log(f"Registros carregados: {record_count}")


# =========================================================
# 15. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Encerramento operacional
# - docs/15_artigo_tecnico.md → 3.7.2.11 Validação e encerramento
#
# =========================================================

log("Ingestão Bronze concluída com sucesso")

print(f"Tabela: {FULL_TABLE_NAME}")
print(f"Path: {TARGET_PATH}")
print(f"Registros: {record_count}")
