# =========================================================
# 🔹 03_SILVER_TRANSFORM_PLANO_CONTA
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Transformar dados da camada Bronze
# - Aplicar regras de padronização e enriquecimento
# - Estruturar a hierarquia contábil
# - Persistir dados tratados na camada Silver (Delta Lake)
# - Registrar tabela no Unity Catalog
#
# Pipeline:
# Bronze (Delta Lake) → Silver (Delta Lake) → Unity Catalog
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/03_desenvolvimento.md → Transformação Silver
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md → Camada Silver (Trusted Data)
#
# 📄 Governança:
# - ../docs/07_governanca.md → Unity Catalog, RBAC e Data Lineage
#
# 📄 Runbook de Implantação:
# - ../docs/08_runbook_implantacao.md → Configuração do ambiente Databricks
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.3 Notebook 03 – Transformação Silver de Plano de Contas
#
# =========================================================


# =========================================================
# 1. IMPORTS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.1 Configuração do ambiente
#
# Objetivo técnico:
# - Disponibilizar bibliotecas para processamento distribuído
# - Suportar transformações utilizando Apache Spark
#
# =========================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window


# =========================================================
# 2. CONFIGURAÇÕES (SECRETS / GOVERNANÇA)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Gestão de identidades, RBAC e Secret Scopes
# - docs/08_runbook_implantacao.md → Integração com Azure Key Vault
# - docs/15_artigo_tecnico.md → 3.7.3.1 Configuração do ambiente
#
# Objetivo de negócio:
# - Centralizar configurações da plataforma
# - Evitar exposição de informações sensíveis
# - Garantir reutilização entre ambientes
#
# =========================================================

SECRET_SCOPE = "ss-finance-dre-kv"

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

SILVER_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-catalog"
)

SILVER_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-schema"
)

TABLE_NAME = "plano_conta"


# =========================================================
# 3. PATHS E CONFIGURAÇÕES LÓGICAS
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Separação entre camadas (Storage vs Unity Catalog)
# - docs/03_desenvolvimento.md → Estrutura da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.2 Definição dos caminhos de armazenamento
#
# Objetivo técnico:
# - Separar camadas física e lógica da arquitetura
# - Garantir rastreabilidade e governança dos dados
#
# =========================================================

BRONZE_PATH = (
    f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{TABLE_NAME}"
)

SILVER_PATH = (
    f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{TABLE_NAME}"
)

BRONZE_TABLE = (
    f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.{TABLE_NAME}"
)

SILVER_TABLE = (
    f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{TABLE_NAME}"
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


log("Iniciando transformação Silver - Plano de Contas")

# =========================================================
# 5. LEITURA DA CAMADA BRONZE
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Consumo da camada Bronze
# - docs/02_arquitetura.md → Camada Silver (Trusted Data)
# - docs/15_artigo_tecnico.md → 3.7.3.3 Leitura da camada Bronze
#
# Objetivo de negócio:
# - Consumir dados previamente ingeridos
# - Evitar nova leitura da fonte original
# - Reduzir o acoplamento entre as etapas do pipeline
#
# =========================================================

log("Lendo dados da camada Bronze")

df_origem = spark.table(BRONZE_TABLE)


# =========================================================
# 6. PREPARAÇÃO DA ESTRUTURA DE PROCESSAMENTO
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.4 Preparação da estrutura de processamento
#
# Objetivo técnico:
# - Garantir determinismo durante o processamento
# - Preparar a estrutura para transformações hierárquicas
#
# =========================================================

log("Preparando estrutura de processamento")

df_origem = df_origem.orderBy("id_conta")

df = df_origem


# =========================================================
# 7. CRIAÇÃO DAS JANELAS ANALÍTICAS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Processamento distribuído
# - docs/15_artigo_tecnico.md → 3.7.3.5 Criação das janelas analíticas
#
# Objetivo técnico:
# - Criar Window Functions para processamento hierárquico
# - Suportar operações de FillDown utilizando Apache Spark
#
# =========================================================

janela_rownum = Window.orderBy("id_conta")

df = df.withColumn(
    "row_id",
    F.row_number().over(janela_rownum)
)

janela_filldown = (
    Window
    .orderBy("row_id")
    .rowsBetween(
        Window.unboundedPreceding,
        0
    )
)


# =========================================================
# 8. IDENTIFICAÇÃO DA HIERARQUIA CONTÁBIL
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Regras de transformação
# - docs/15_artigo_tecnico.md → 3.7.3.6 Identificação da hierarquia contábil
#
# Objetivo de negócio:
# - Identificar automaticamente o nível hierárquico
# - Preparar a estrutura para consolidação da DRE
#
# =========================================================

log("Identificando níveis hierárquicos")

df = df.withColumn(
    "nivel_hierarquia",
    F.size(
        F.split(
            F.col("id_conta"),
            r"\."
        )
    )
)

# =========================================================
# 9. CONSTRUÇÃO DA HIERARQUIA CONTÁBIL
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.7 Construção da hierarquia contábil
#
# Objetivo de negócio:
# - Organizar o plano de contas em níveis hierárquicos
# - Facilitar análises e consolidações financeiras
#
# =========================================================

# Nível 1

df = df.withColumn(
    "n1",
    F.when(
        F.col("nivel_hierarquia") == 2,
        F.col("descricao")
    )
)

# Nível 2

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

# Nível 3

df = df.withColumn(
    "n3",
    F.when(
        F.col("nivel_hierarquia") == 4,
        F.col("descricao")
    )
)


# =========================================================
# 10. APLICAÇÃO DO PREENCHIMENTO HIERÁRQUICO (FILLDOWN)
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações hierárquicas
# - docs/15_artigo_tecnico.md → 3.7.3.8 Aplicação do preenchimento hierárquico (FillDown)
#
# Objetivo de negócio:
# - Propagar os níveis superiores da hierarquia
# - Preservar o contexto contábil em todos os registros
#
# =========================================================

log("Aplicando FillDown hierárquico")

df = df.withColumn(
    "n1",
    F.last(
        "n1",
        ignorenulls=True
    ).over(janela_filldown)
)

df = df.withColumn(
    "n2",
    F.last(
        "n2",
        ignorenulls=True
    ).over(janela_filldown)
)

df = df.withColumn(
    "n2",
    F.when(
        F.col("n2") == "TEMP",
        F.lit(None)
    ).otherwise(
        F.col("n2")
    )
)


# =========================================================
# 11. CRIAÇÃO DO CÓDIGO DA DRE
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Regras de negócio da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.9 Criação do código da DRE
#
# Objetivo de negócio:
# - Identificar o agrupamento principal da DRE
# - Facilitar consolidações e indicadores financeiros
#
# =========================================================

df = df.withColumn(
    "cod_dre",
    F.when(
        F.col("nivel_hierarquia") == 2,
        F.col("id_conta")
    )
)

df = df.withColumn(
    "cod_dre",
    F.last(
        "cod_dre",
        ignorenulls=True
    ).over(janela_filldown)
)


# =========================================================
# 12. PADRONIZAÇÃO DOS TIPOS DE DADOS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Padronização da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.10 Padronização dos tipos de dados
#
# Objetivo de negócio:
# - Garantir consistência do esquema da camada Silver
# - Evitar incompatibilidades nas etapas seguintes do pipeline
#
# =========================================================

log("Padronizando tipos de dados")

df = (
    df
    .withColumn("id_conta", F.col("id_conta").cast("string"))
    .withColumn("descricao", F.col("descricao").cast("string"))
    .withColumn("lancamento", F.col("lancamento").cast("long"))
    .withColumn("calculado", F.col("calculado").cast("long"))
    .withColumn("cod_dre", F.col("cod_dre").cast("string"))
    .withColumn("n1", F.col("n1").cast("string"))
    .withColumn("n2", F.col("n2").cast("string"))
    .withColumn("n3", F.col("n3").cast("string"))
)

# =========================================================
# 13. CLASSIFICAÇÃO FINANCEIRA
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Regras de negócio da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.11 Classificação financeira
#
# Objetivo de negócio:
# - Padronizar o tratamento dos sinais financeiros
# - Simplificar a construção de indicadores analíticos
#
# =========================================================

df = df.withColumn(
    "tipo_indicador",
    F.when(
        F.col("cod_dre").isin(
            "3.02",
            "3.04"
        ),
        F.lit(-1)
    ).otherwise(
        F.lit(1)
    ).cast("long")
)


# =========================================================
# 14. METADADOS DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Data Lineage e auditoria
# - docs/05_entrega_valor.md → Rastreabilidade dos dados
# - docs/15_artigo_tecnico.md → 3.7.3.12 Inclusão de metadados de governança
#
# Objetivo de negócio:
# - Garantir rastreabilidade das transformações
# - Suportar auditoria e análise de Data Lineage
#
# =========================================================

df = (
    df
    .withColumn(
        "_silver_timestamp",
        F.current_timestamp()
    )
)


# =========================================================
# 15. LIMPEZA DA ESTRUTURA TEMPORÁRIA
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações da camada Silver
# - docs/15_artigo_tecnico.md → 3.7.3.13 Limpeza da estrutura temporária
#
# Objetivo técnico:
# - Remover colunas auxiliares utilizadas no processamento
# - Disponibilizar somente atributos relevantes
#
# =========================================================

df_final = df.drop(
    "nivel_hierarquia",
    "row_id"
)


# =========================================================
# 16. PERSISTÊNCIA NA CAMADA SILVER
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Silver Layer (Trusted Data)
# - docs/03_desenvolvimento.md → Persistência em formato Delta
# - docs/15_artigo_tecnico.md → 3.7.3.14 Persistência na camada Silver
#
# Objetivo de negócio:
# - Disponibilizar dados tratados na camada Trusted
# - Garantir versionamento e reutilização via Delta Lake
#
# =========================================================

log("Gravando dados na camada Silver")

df_final.write.format("delta") \
    .mode("overwrite") \
    .save(SILVER_PATH)


# =========================================================
# 17. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e governança centralizada
# - docs/15_artigo_tecnico.md → 3.7.3.14 Persistência na camada Silver
#
# Objetivo:
# - Registrar tabela governada
# - Disponibilizar dados para consumo analítico seguro
#
# =========================================================

log("Registrando tabela no Unity Catalog")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {SILVER_TABLE}
USING DELTA
LOCATION '{SILVER_PATH}'
""")

spark.sql(
    f"REFRESH TABLE {SILVER_TABLE}"
)


# =========================================================
# 18. VALIDAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Validação de cargas
# - docs/15_artigo_tecnico.md → 3.7.3.15 Validação e encerramento da execução
#
# Objetivo:
# - Garantir execução bem-sucedida do pipeline
#
# =========================================================

record_count = df_final.count()

log(f"Registros processados: {record_count}")


# =========================================================
# 19. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Encerramento operacional
# - docs/15_artigo_tecnico.md → 3.7.3.15 Validação e encerramento da execução
#
# =========================================================

log("Transformação Silver concluída com sucesso")

print(f"Tabela: {SILVER_TABLE}")
print(f"Path: {SILVER_PATH}")
print(f"Registros: {record_count}")
