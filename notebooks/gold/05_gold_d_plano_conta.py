# =========================================================
# 🔹 05_GOLD_D_PLANO_CONTA
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Publicar a dimensão Plano de Contas na camada Gold
# - Aplicar modelagem dimensional
# - Disponibilizar dimensão corporativa para análises
# - Persistir dados em Delta Lake
# - Registrar tabela no Unity Catalog
# - Criar View Semântica para consumo por ferramentas de BI
#
# Pipeline:
# Silver (Delta Lake) → Gold (Delta Lake)
# → Unity Catalog → Semantic View → BI
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/03_desenvolvimento.md → Publicação Gold da Dimensão Plano de Contas
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md → Camada Gold (Business Data)
#
# 📄 Governança:
# - ../docs/07_governanca.md → Unity Catalog e Data Lineage
#
# 📄 Operação:
# - ../docs/06_operacao_plataforma.md → Monitoramento e Publicação das Camadas
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.5 Notebook 05 – Publicação Gold da Dimensão Plano de Contas
#
# =========================================================


# =========================================================
# 1. IMPORTS
# =========================================================

from pyspark.sql import functions as F


# =========================================================
# 2. CONFIGURAÇÕES (SECRETS / GOVERNANÇA)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e Governança
# - docs/15_artigo_tecnico.md → 3.7.5.1 Configuração do ambiente
#
# Objetivo de negócio:
# - Centralizar configurações da plataforma
# - Utilizar parâmetros armazenados no Azure Key Vault
# - Garantir segurança e padronização do ambiente
#
# =========================================================

SECRET_SCOPE = "ss-finance-dre-kv"

STORAGE_ACCOUNT = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="storage-account-name"
)

SILVER_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-catalog"
)

SILVER_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="silver-schema"
)

GOLD_CATALOG = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="gold-catalog"
)

GOLD_SCHEMA = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key="gold-schema"
)

SILVER_TABLE_NAME = "plano_conta"

GOLD_TABLE_NAME = "d_plano_conta"

SEMANTIC_VIEW_NAME = "vw_d_plano_conta"


# =========================================================
# 3. PATHS E CONFIGURAÇÕES LÓGICAS
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camadas Silver e Gold
# - docs/03_desenvolvimento.md → Publicação Gold
# - docs/15_artigo_tecnico.md → 3.7.5.1 Configuração do ambiente
#
# Objetivo técnico:
# - Definir origem lógica e destino físico
# - Separar armazenamento do catálogo governado
#
# =========================================================

GOLD_PATH = (
    f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{GOLD_TABLE_NAME}"
)

SILVER_TABLE = (
    f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{SILVER_TABLE_NAME}"
)

GOLD_TABLE = (
    f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{GOLD_TABLE_NAME}"
)

SEMANTIC_VIEW = (
    f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{SEMANTIC_VIEW_NAME}"
)


# =========================================================
# 4. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Monitoramento e Logs
#
# Objetivo:
# - Padronizar mensagens de execução
# - Facilitar auditoria e troubleshooting
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando publicação Gold - Dimensão Plano de Contas")


# =========================================================
# 5. LEITURA DA CAMADA SILVER
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Camada Silver (dados tratados)
# - docs/02_arquitetura.md → Fluxo Silver → Gold
# - docs/15_artigo_tecnico.md → 3.7.5.2 Consumo da camada Silver
#
# Objetivo de negócio:
# - Consumir dados já tratados e validados
# - Garantir desacoplamento da camada de ingestão
# - Reutilizar estrutura confiável para modelagem dimensional
#
# =========================================================

log("Lendo dados da camada Silver...")

df_silver = spark.table(SILVER_TABLE)


# =========================================================
# 6. MODELAGEM DIMENSIONAL
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Modelagem dimensional
# - docs/02_arquitetura.md → Camada Gold (Business Layer)
# - docs/15_artigo_tecnico.md → 3.7.5.2 Modelagem da dimensão
#
# Objetivo de negócio:
# - Estruturar dimensão contábil corporativa
# - Preservar hierarquia analítica
# - Garantir padronização para consumo em BI
#
# =========================================================

log("Aplicando modelagem dimensional...")

df_gold = (
    df_silver
    .select(
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
)


# =========================================================
# 7. CONTROLE DE QUALIDADE DA DIMENSÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Qualidade de dados
# - docs/03_desenvolvimento.md → Regras de consistência
# - docs/15_artigo_tecnico.md → 3.7.5.3 Controle de qualidade
#
# Objetivo de negócio:
# - Garantir unicidade da dimensão
# - Evitar duplicidade de chaves analíticas
# - Assegurar consistência em joins analíticos
#
# =========================================================

log("Aplicando controle de qualidade...")

df_gold = df_gold.dropDuplicates(["id_conta"])


# =========================================================
# 8. METADADOS DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Data lineage e auditoria
# - docs/05_entrega_valor.md → Rastreabilidade
# - docs/15_artigo_tecnico.md → 3.7.5.2 Metadados de governança
#
# Objetivo de negócio:
# - Registrar momento da publicação na camada Gold
# - Suportar auditoria e rastreabilidade ponta a ponta
#
# =========================================================

df_gold = df_gold.withColumn(
    "_gold_timestamp",
    F.current_timestamp()
)

# =========================================================
# 9. GRAVAÇÃO NA CAMADA GOLD
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camada Gold (Business Data)
# - docs/03_desenvolvimento.md → Persistência em Delta Lake
# - docs/15_artigo_tecnico.md → 3.7.5.4 Persistência na Gold
#
# Objetivo de negócio:
# - Persistir dimensão contábil corporativa
# - Disponibilizar dados otimizados para consumo analítico
# - Garantir versionamento via Delta Lake
#
# =========================================================

log("Gravando dados na camada Gold...")

(
    df_gold.write
           .format("delta")
           .mode("overwrite")
           .save(GOLD_PATH)
)


# =========================================================
# 10. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e governança centralizada
# - docs/15_artigo_tecnico.md → 3.7.5.4 Registro no catálogo
#
# Objetivo de negócio:
# - Tornar a tabela governada e rastreável
# - Centralizar acesso corporativo aos dados
# - Habilitar controle de permissões (RBAC)
#
# =========================================================

log("Registrando tabela no Unity Catalog...")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {GOLD_TABLE}
USING DELTA
LOCATION '{GOLD_PATH}'
""")

spark.sql(f"""
REFRESH TABLE {GOLD_TABLE}
""")


# =========================================================
# 11. VALIDAÇÃO FINAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Validação de cargas
# - docs/15_artigo_tecnico.md → 3.7.5.6 Validação final
#
# Objetivo de negócio:
# - Garantir integridade da publicação
# - Validar volume de registros processados
# - Suportar monitoramento operacional
#
# =========================================================

record_count = df_gold.count()

log(f"Quantidade de registros: {record_count}")

# =========================================================
# 12. CRIAÇÃO DA VIEW SEMÂNTICA
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camada semântica para BI
# - docs/03_desenvolvimento.md → Camada de consumo analítico
# - docs/15_artigo_tecnico.md → 3.7.5.5 View semântica
#
# Objetivo de negócio:
# - Simplificar o consumo por ferramentas de BI
# - Traduzir nomes técnicos para linguagem de negócio
# - Reduzir necessidade de transformações na camada de consumo
#
# =========================================================

log("Criando view semântica...")

spark.sql(f"""
CREATE OR REPLACE VIEW {SEMANTIC_VIEW} AS

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
# 13. FINALIZAÇÃO DO PROCESSO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Encerramento operacional
# - docs/15_artigo_tecnico.md → 3.7.5.6 Finalização do processo
#
# Objetivo de negócio:
# - Encerrar execução com rastreabilidade completa
# - Expor artefatos gerados
# - Facilitar monitoramento e auditoria
#
# =========================================================

log("Gold Dimensão Plano de Contas finalizado com sucesso")

print(f"Tabela Gold: {GOLD_TABLE}")
print(f"View Semântica: {SEMANTIC_VIEW}")
print(f"Path Gold: {GOLD_PATH}")
print(f"Registros processados: {record_count}")
