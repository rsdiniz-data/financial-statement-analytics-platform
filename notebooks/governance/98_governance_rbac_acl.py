# =========================================================
# 🔹 98_GOVERNANCE_RBAC_ACL
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Demonstrar governança de dados utilizando Unity Catalog
# - Demonstrar Role-Based Access Control (RBAC)
# - Demonstrar Access Control Lists (ACL)
# - Evidenciar segregação de acessos por perfil
# - Aplicar o princípio do menor privilégio
# - Demonstrar auditoria de permissões
#
# Pipeline:
# Microsoft Entra ID
#        ↓
# Azure Databricks
#        ↓
# Unity Catalog
#        ↓
# Bronze / Silver / Gold
#        ↓
# Views Semânticas
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/07_governanca.md → Governança de Dados
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md → Arquitetura de Governança
#
# 📄 Operação:
# - ../docs/06_operacao_plataforma.md → Auditoria e Monitoramento
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.8 Notebook 98 – Governança RBAC e ACL
#
# =========================================================


# =========================================================
# 1. CONFIGURAÇÕES (OBJETOS GOVERNADOS)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Objetos governados
# - docs/15_artigo_tecnico.md → 3.7.8.1 Configuração dos objetos
#
# Objetivo de negócio:
# - Centralizar os objetos utilizados na demonstração
# - Facilitar manutenção do ambiente
# - Padronizar referências do Unity Catalog
#
# =========================================================

CATALOG_NAME = "finance"

SCHEMA_BRONZE = "bronze"
SCHEMA_SILVER = "silver"
SCHEMA_GOLD = "gold"

D_PLANO_CONTA_TABLE = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.d_plano_conta"
)

FT_RESULTADO_TABLE = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.ft_resultado"
)

D_CALENDARIO_TABLE = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.d_calendario"
)

VW_D_PLANO_CONTA = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.vw_d_plano_conta"
)

VW_FT_RESULTADO = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.vw_ft_resultado"
)

VW_D_CALENDARIO = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.vw_d_calendario"
)


# =========================================================
# 2. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md → Monitoramento e logs
#
# Objetivo:
# - Padronizar mensagens operacionais
# - Facilitar rastreabilidade da execução
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando demonstração de Governança - Unity Catalog")


# =========================================================
# 3. PRINCÍPIO DO MENOR PRIVILÉGIO
# =========================================================
#
# Referência:
# - docs/07_governanca.md → RBAC e ACL
# - docs/15_artigo_tecnico.md → 3.7.8.2 Modelo de permissões
#
# Objetivo de negócio:
# - Garantir segregação de funções
# - Conceder apenas os privilégios necessários
# - Reduzir riscos operacionais
#
# Perfis:
#
# Data Engineers
# - Administração das camadas Bronze
# - Administração das camadas Silver
# - Administração das camadas Gold
# - CREATE
# - MODIFY
# - SELECT
#
# BI Analysts
# - Leitura das tabelas Gold
# - SELECT
#
# Business Users
# - Leitura das Views semânticas
# - SELECT
#
# =========================================================

log("Aplicando princípio do menor privilégio")


# =========================================================
# 4. EVIDÊNCIA DOS GRUPOS (RBAC)
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Gerenciamento de identidades
# - docs/15_artigo_tecnico.md → 3.7.8.3 Integração Microsoft Entra ID
#
# Objetivo de negócio:
# - Demonstrar sincronização dos grupos corporativos
# - Evidenciar utilização do Microsoft Entra ID
#
# Os grupos foram previamente criados
# no Microsoft Entra ID e sincronizados
# automaticamente com o Azure Databricks
# via SCIM.
#
# Grupos:
#
# - data_engineers
# - bi_analysts
# - business_users
#
# =========================================================

log("Consultando grupos sincronizados")

display(
    spark.sql("""
        SHOW GROUPS
    """)
)


# =========================================================
# 5. ACESSO AO CATÁLOGO
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Unity Catalog
# - docs/15_artigo_tecnico.md → 3.7.8.4 Permissões de catálogo
#
# Objetivo de negócio:
# - Permitir utilização do catálogo corporativo
# - Centralizar o acesso aos objetos governados
#
# =========================================================

log("Concedendo acesso ao catálogo corporativo")

spark.sql(f"""
GRANT USE CATALOG
ON CATALOG {CATALOG_NAME}
TO `data_engineers`
""")

spark.sql(f"""
GRANT USE CATALOG
ON CATALOG {CATALOG_NAME}
TO `bi_analysts`
""")

spark.sql(f"""
GRANT USE CATALOG
ON CATALOG {CATALOG_NAME}
TO `business_users`
""")
