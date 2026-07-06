# =========================================================
# 🔹 04_SILVER_TRANSFORM_RESULTADO
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Ler dados financeiros da camada Bronze
# - Aplicar limpeza e padronização
# - Transformar estrutura Wide em formato Long
# - Persistir dados tratados na camada Silver
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
# - ../docs/07_governanca.md → Unity Catalog, RBAC e Governança de Dados
#
# 📄 Runbook de Implantação:
# - ../docs/08_runbook_implantacao.md → Configuração do Azure Databricks
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.4 Notebook 04 – Transformação Silver de Resultado
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
# - docs/07_governanca.md → Gestão de identidades, RBAC e Secret Scopes
# - docs/08_runbook_implantacao.md → Integração com Azure Key Vault
#
# Objetivo de negócio:
# - Centralizar parâmetros do ambiente
# - Evitar configuração fixa no código
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

BRONZE_TABLE_NAME = "dfp"

SILVER_TABLE_NAME = "resultado"


# =========================================================
# 3. PATHS E CONFIGURAÇÕES LÓGICAS
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Separação entre camadas Medallion
# - docs/03_desenvolvimento.md → Estrutura da camada Silver
#
# Objetivo técnico:
# - Separar armazenamento físico da camada lógica
# - Garantir governança via Unity Catalog
#
# =========================================================

BRONZE_PATH = (
    f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{BRONZE_TABLE_NAME}"
)

SILVER_PATH = (
    f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net/"
    f"{SILVER_TABLE_NAME}"
)

BRONZE_TABLE = (
    f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.{BRONZE_TABLE_NAME}"
)

SILVER_TABLE = (
    f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{SILVER_TABLE_NAME}"
)


# =========================================================
# 4. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Monitoramento e logs
#
# Objetivo:
# - Padronizar rastreabilidade da execução
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando transformação Silver - Resultado")


# =========================================================
# 5. LEITURA DA CAMADA BRONZE
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camada Bronze (Raw Data)
# - docs/03_desenvolvimento.md → Transformação Silver
# - docs/15_artigo_tecnico.md → 3.7.4.1 Leitura da camada Bronze
#
# Objetivo de negócio:
# - Consumir dados previamente ingeridos
# - Eliminar dependência da fonte SharePoint
# - Utilizar tabela governada pelo Unity Catalog
#
# =========================================================

log("Lendo dados da camada Bronze")

df_origem = spark.table(BRONZE_TABLE)


# =========================================================
# 6. LIMPEZA E PADRONIZAÇÃO INICIAL
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações Silver
# - docs/15_artigo_tecnico.md → 3.7.4.2 Limpeza e padronização inicial
#
# Objetivo de negócio:
# - Garantir consistência estrutural
# - Eliminar registros inválidos
# - Preparar os dados para transformação analítica
#
# =========================================================

log("Aplicando limpeza e padronização")

df_limpo = (
    df_origem
    .withColumn(
        "codigo_da_conta",
        F.trim(
            F.col("codigo_da_conta")
        )
    )
    .withColumn(
        "descricao_da_conta",
        F.trim(
            F.col("descricao_da_conta")
        )
    )
)

df_limpo = df_limpo.filter(
    F.col("codigo_da_conta").isNotNull()
)

df_limpo = df_limpo.filter(
    F.col("codigo_da_conta") != ""
)

df_limpo = df_limpo.dropDuplicates()

# =========================================================
# 7. IDENTIFICAÇÃO DAS COLUNAS DE EXERCÍCIO
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformação Silver
# - docs/15_artigo_tecnico.md → 3.7.4.3 Identificação dinâmica das colunas de exercício
#
# Objetivo de negócio:
# - Identificar automaticamente novos exercícios financeiros
# - Eliminar dependência de anos fixos no código
# - Tornar o pipeline resiliente à evolução da base de dados
#
# =========================================================

log("Identificando colunas de exercício")

period_columns = [
    column
    for column in df_limpo.columns
    if (
        "exercicio" in column.lower()
        and "31_12_" in column.lower()
    )
]

if not period_columns:
    raise ValueError(
        "Nenhuma coluna de exercício encontrada. "
        f"Colunas disponíveis: {df_limpo.columns}"
    )

log(f"Colunas de exercício encontradas: {len(period_columns)}")

for column in period_columns:
    log(f" - {column}")


# =========================================================
# 8. TRANSFORMAÇÃO ESTRUTURAL (WIDE → LONG)
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camada Silver (Trusted Data)
# - docs/03_desenvolvimento.md → Transformações analíticas
# - docs/15_artigo_tecnico.md → 3.7.4.4 Transformação estrutural (Wide → Long)
#
# Objetivo de negócio:
# - Converter colunas de exercícios em registros
# - Facilitar análises temporais
# - Preparar os dados para modelagem dimensional
#
# =========================================================

log("Executando transformação Wide → Long")

df_unpivot = (
    df_limpo
    .unpivot(
        ids=[
            "codigo_da_conta",
            "descricao_da_conta"
        ],
        values=period_columns,
        variableColumnName="periodo_origem",
        valueColumnName="valor_bruto"
    )
)


# =========================================================
# 9. CRIAÇÃO DA DATA DE REFERÊNCIA
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações Silver
# - docs/15_artigo_tecnico.md → 3.7.4.5 Criação da data de referência
#
# Objetivo de negócio:
# - Padronizar representação temporal
# - Preparar integração com dimensão calendário
# - Eliminar colunas auxiliares utilizadas na transformação
#
# =========================================================

log("Criando data de referência")

df_unpivot = (
    df_unpivot
    .withColumn(
        "ano_referencia",
        F.regexp_extract(
            F.col("periodo_origem"),
            r"31_12_(\d{4})",
            1
        )
    )
    .withColumn(
        "data_referencia",
        F.to_date(
            F.concat(
                F.lit("31/12/"),
                F.col("ano_referencia")
            ),
            "dd/MM/yyyy"
        )
    )
    .drop(
        "ano_referencia",
        "periodo_origem"
    )
)


# =========================================================
# 10. TRATAMENTO DOS VALORES FINANCEIROS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Padronização de dados financeiros
# - docs/15_artigo_tecnico.md → 3.7.4.6 Tratamento dos valores financeiros
#
# Objetivo de negócio:
# - Padronizar formato monetário
# - Garantir precisão dos cálculos financeiros
# - Preparar valores para processamento analítico
#
# =========================================================

log("Tratando valores financeiros")

df_tratado = (
    df_unpivot
    .withColumn(
        "valor_bruto",
        F.trim(
            F.col("valor_bruto").cast("string")
        )
    )
    .withColumn(
        "valor_bruto",
        F.when(
            F.col("valor_bruto").isin(
                "",
                "-",
                "null",
                "None"
            ),
            None
        ).otherwise(
            F.col("valor_bruto")
        )
    )
    .withColumn(
        "valor_bruto",
        F.regexp_replace(
            F.col("valor_bruto"),
            r"\.",
            ""
        )
    )
    .withColumn(
        "valor_bruto",
        F.regexp_replace(
            F.col("valor_bruto"),
            ",",
            "."
        )
    )
    .withColumn(
        "valor_bruto",
        F.regexp_replace(
            F.col("valor_bruto"),
            r"^\((.*)\)$",
            r"-\1"
        )
    )
)


# =========================================================
# 11. CONVERSÃO DE TIPOS E ATRIBUTOS TEMPORAIS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Transformações Silver
# - docs/02_arquitetura.md → Camada Silver (Trusted Data)
# - docs/15_artigo_tecnico.md → 3.7.4.7 Conversão de tipos e criação de atributos temporais
#
# Objetivo de negócio:
# - Garantir consistência do modelo analítico
# - Padronizar tipos de dados para consumo pelas camadas seguintes
# - Criar atributos temporais para consultas e particionamento
#
# =========================================================

log("Aplicando tipagem e criando atributos temporais")

df_resultado = (
    df_tratado
    .withColumn(
        "codigo_da_conta",
        F.col("codigo_da_conta").cast("string")
    )
    .withColumn(
        "descricao_da_conta",
        F.col("descricao_da_conta").cast("string")
    )
    .withColumn(
        "data_referencia",
        F.to_date(
            F.col("data_referencia"),
            "dd/MM/yyyy"
        )
    )
    .withColumn(
        "valor",
        F.col("valor_bruto").cast("double")
    )
    .withColumn(
        "ano",
        F.year("data_referencia")
    )
    .drop("valor_bruto")
)


# =========================================================
# 12. CONTROLE DE QUALIDADE DOS DADOS
# =========================================================
#
# Referência:
# - docs/03_desenvolvimento.md → Qualidade de dados
# - docs/06_operacao_plataforma.md → Validação de cargas
# - docs/15_artigo_tecnico.md → 3.7.4.8 Controle de qualidade dos dados
#
# Objetivo de negócio:
# - Garantir consistência da camada Silver
# - Remover registros inválidos
# - Eliminar duplicidades antes da persistência
#
# =========================================================

log("Executando validações de qualidade")

df_resultado = df_resultado.filter(
    F.col("valor").isNotNull()
)

df_resultado = df_resultado.dropDuplicates()


# =========================================================
# 13. METADADOS DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Data Lineage e auditoria
# - docs/05_entrega_valor.md → Rastreabilidade dos dados
# - docs/15_artigo_tecnico.md → 3.7.4.9 Inclusão de metadados de governança
#
# Objetivo de negócio:
# - Registrar o momento da transformação
# - Suportar auditoria e reprocessamentos
# - Facilitar rastreabilidade dos dados
#
# =========================================================

df_resultado = (
    df_resultado
    .withColumn(
        "_silver_timestamp",
        F.current_timestamp()
    )
)


# =========================================================
# 14. PERSISTÊNCIA NA CAMADA SILVER
# =========================================================
#
# Referência:
# - docs/02_arquitetura.md → Camada Silver (Trusted Data)
# - docs/03_desenvolvimento.md → Persistência em formato Delta
# - docs/15_artigo_tecnico.md → 3.7.4.10 Persistência da camada Silver
#
# Objetivo de negócio:
# - Persistir dados tratados em formato Delta Lake
# - Otimizar consultas por meio de particionamento
# - Disponibilizar dados confiáveis para a camada Gold
#
# =========================================================

log("Gravando dados na camada Silver")

(
    df_resultado.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("ano")
        .save(SILVER_PATH)
)

# =========================================================
# 15. REGISTRO NO UNITY CATALOG
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog e governança centralizada
# - docs/15_artigo_tecnico.md → 3.7.4.10 Persistência da camada Silver
#
# Objetivo de negócio:
# - Registrar tabela governada no Unity Catalog
# - Centralizar o acesso aos dados tratados
# - Disponibilizar o dataset para consumo analítico
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
# 16. VALIDAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Validação de cargas
# - docs/15_artigo_tecnico.md → 3.7.4.11 Finalização do processo
#
# Objetivo de negócio:
# - Validar a persistência dos dados
# - Registrar indicadores operacionais da execução
# - Confirmar a conclusão bem-sucedida do pipeline
#
# =========================================================

record_count = df_resultado.count()

log(f"Registros processados: {record_count}")


# =========================================================
# 17. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Encerramento operacional
# - docs/15_artigo_tecnico.md → 3.7.4.11 Finalização do processo
#
# Objetivo:
# - Registrar o encerramento da execução
# - Disponibilizar informações para monitoramento e troubleshooting
#
# =========================================================

log("Transformação Silver concluída com sucesso")

print(f"Tabela: {SILVER_TABLE}")
print(f"Path: {SILVER_PATH}")
print(f"Registros: {record_count}")
