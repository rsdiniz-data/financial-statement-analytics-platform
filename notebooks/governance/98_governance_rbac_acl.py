# =========================================================
# 🔹 98_GOVERNANCE_RBAC_ACL
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Demonstrar a governança de dados utilizando Unity Catalog
# - Implementar controle de acesso baseado em papéis (RBAC)
# - Implementar listas de controle de acesso (ACL)
# - Aplicar o princípio do menor privilégio (Least Privilege)
# - Evidenciar a segregação de acessos entre perfis
# - Validar as permissões através de auditoria
#
# Arquitetura:
#
# Microsoft Entra ID
#          │
#          ▼
#   Grupos Corporativos
#          │
#          ▼
# Azure Databricks
#          │
#          ▼
#   Unity Catalog
#          │
#   ┌──────┼──────┐
#   ▼      ▼      ▼
# Bronze Silver Gold
#                 │
#                 ▼
#         Views Semânticas
#
# Recursos demonstrados:
# - Unity Catalog
# - Microsoft Entra ID
# - RBAC
# - ACL
# - GRANT
# - SHOW GRANTS
# - Governança de Dados
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/07_governanca.md
#   RBAC, ACL, Unity Catalog e Auditoria
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md
#   Arquitetura Lakehouse e Governança
#
# 📄 Operação da Plataforma:
# - ../docs/06_operacao_plataforma.md
#   Auditoria e administração da plataforma
#
# 📄 Artigo técnico:
# - ../docs/15_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.8 Notebook 98 – Governança, RBAC e ACL
#
# =========================================================


# =========================================================
# 0. CONFIGURAÇÕES DE GOVERNANÇA
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Objetos governados
# - docs/02_arquitetura.md → Unity Catalog
# - docs/15_artigo_tecnico.md
#   → 3.7.8.1 Gerenciamento de dependências
#
# Objetivo técnico:
# - Centralizar os objetos administrados
# - Facilitar manutenção da política de segurança
#
# Objetivo de negócio:
# - Padronizar a administração dos objetos
# - Simplificar futuras evoluções da governança
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
# 1. LOG OPERACIONAL
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md
#   → Monitoramento e rastreabilidade operacional
#
# Objetivo técnico:
# - Padronizar mensagens de execução
#
# Objetivo de negócio:
# - Facilitar acompanhamento operacional
# - Melhorar rastreabilidade das atividades
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando demonstração de governança")


# =========================================================
# 2. PRINCÍPIO DO MENOR PRIVILÉGIO
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso (RBAC e ACL)
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.2 Princípio do menor privilégio
#
# Objetivo técnico:
# - Aplicar Least Privilege Principle
#
# Objetivo de negócio:
# - Reduzir riscos operacionais
# - Garantir segregação entre perfis
# - Preservar integridade dos dados
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
# - Consumo das tabelas Gold
# - SELECT
#
# Business Users
# - Consumo das Views Semânticas
# - SELECT
#
# =========================================================

log("Aplicando princípio do menor privilégio")


# =========================================================
# 3. VALIDAÇÃO DOS GRUPOS (RBAC)
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Gerenciamento de identidades
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.3 Evidências da estrutura RBAC
#
# Objetivo técnico:
# - Validar sincronização dos grupos
# - Confirmar integração com Microsoft Entra ID
#
# Objetivo de negócio:
# - Centralizar administração dos acessos
# - Reduzir manutenção manual
#
# Grupos esperados:
#
# - data_engineers
# - bi_analysts
# - business_users
#
# =========================================================

log("Validando grupos sincronizados")

display(

    spark.sql("""

    SHOW GROUPS

    """)

)


# =========================================================
# 4. CONCESSÃO DE ACESSO AO CATÁLOGO
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso ao Unity Catalog
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.4 Concessão de acesso ao catálogo
#
# Objetivo técnico:
# - Permitir utilização do catálogo corporativo
#
# Objetivo de negócio:
# - Disponibilizar acesso controlado
# - Preservar a estrutura lógica da plataforma
#
# =========================================================

log("Concedendo acesso ao catálogo")

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

# =========================================================
# 5. CONCESSÃO DE ACESSO AOS SCHEMAS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso (RBAC e ACL)
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.4 Concessão de acesso ao catálogo e aos schemas
#
# Objetivo técnico:
# - Permitir navegação no schema Gold
# - Restringir acesso apenas aos consumidores autorizados
#
# Objetivo de negócio:
# - Controlar o acesso à estrutura lógica do ambiente
# - Preservar a organização do Unity Catalog
#
# =========================================================

log("Concedendo acesso aos schemas")

spark.sql(f"""
GRANT USE SCHEMA
ON SCHEMA {CATALOG_NAME}.{SCHEMA_GOLD}
TO `bi_analysts`
""")

spark.sql(f"""
GRANT USE SCHEMA
ON SCHEMA {CATALOG_NAME}.{SCHEMA_GOLD}
TO `business_users`
""")


# =========================================================
# 6. ACL PARA DATA ENGINEERS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso (RBAC e ACL)
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.5 Aplicação das ACLs
#
# Objetivo técnico:
# - Conceder privilégios administrativos
# - Permitir manutenção das camadas do Lakehouse
#
# Objetivo de negócio:
# - Garantir autonomia ao time de Engenharia de Dados
# - Centralizar administração da plataforma
#
# Permissões concedidas:
#
# Bronze
# - ALL PRIVILEGES
#
# Silver
# - ALL PRIVILEGES
#
# Gold
# - ALL PRIVILEGES
#
# =========================================================

log("Aplicando ACL para Data Engineers")

spark.sql(f"""
GRANT ALL PRIVILEGES
ON SCHEMA {CATALOG_NAME}.{SCHEMA_BRONZE}
TO `data_engineers`
""")

spark.sql(f"""
GRANT ALL PRIVILEGES
ON SCHEMA {CATALOG_NAME}.{SCHEMA_SILVER}
TO `data_engineers`
""")

spark.sql(f"""
GRANT ALL PRIVILEGES
ON SCHEMA {CATALOG_NAME}.{SCHEMA_GOLD}
TO `data_engineers`
""")

# =========================================================
# 7. ACL PARA BI ANALYSTS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso às tabelas analíticas
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.5 Aplicação das ACLs
#
# Objetivo técnico:
# - Permitir acesso somente às tabelas analíticas
# - Impedir alterações na camada Gold
#
# Objetivo de negócio:
# - Disponibilizar dados confiáveis para análise
# - Preservar integridade das tabelas corporativas
#
# Objetos autorizados:
#
# - d_plano_conta
# - ft_resultado
# - d_calendario
#
# Permissão:
#
# SELECT
#
# =========================================================

log("Aplicando ACL para BI Analysts")

spark.sql(f"""
GRANT SELECT
ON TABLE {D_PLANO_CONTA_TABLE}
TO `bi_analysts`
""")

spark.sql(f"""
GRANT SELECT
ON TABLE {FT_RESULTADO_TABLE}
TO `bi_analysts`
""")

spark.sql(f"""
GRANT SELECT
ON TABLE {D_CALENDARIO_TABLE}
TO `bi_analysts`
""")


# =========================================================
# 8. ACL PARA BUSINESS USERS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Controle de acesso às Views Semânticas
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.5 Aplicação das ACLs
#
# Objetivo técnico:
# - Restringir acesso às Views Semânticas
# - Ocultar a complexidade do modelo físico
#
# Objetivo de negócio:
# - Disponibilizar informações consolidadas
# - Simplificar o consumo dos dados
# - Reduzir riscos de utilização incorreta
#
# Views autorizadas:
#
# - vw_d_plano_conta
# - vw_ft_resultado
# - vw_d_calendario
#
# Permissão:
#
# SELECT
#
# =========================================================

log("Aplicando ACL para Business Users")

spark.sql(f"""
GRANT SELECT
ON VIEW {VW_D_PLANO_CONTA}
TO `business_users`
""")

spark.sql(f"""
GRANT SELECT
ON VIEW {VW_FT_RESULTADO}
TO `business_users`
""")

spark.sql(f"""
GRANT SELECT
ON VIEW {VW_D_CALENDARIO}
TO `business_users`
""")

# =========================================================
# 9. AUDITORIA DO CATÁLOGO E DOS SCHEMAS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Auditoria de permissões
#
# - docs/06_operacao_plataforma.md
#   → Monitoramento operacional
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.6 Evidências de auditoria
#
# Objetivo técnico:
# - Validar as permissões concedidas
# - Evidenciar a configuração do Unity Catalog
#
# Objetivo de negócio:
# - Disponibilizar evidências da governança aplicada
# - Facilitar auditorias e processos de conformidade
#
# Objetos auditados:
#
# - Catálogo
# - Schema Bronze
# - Schema Silver
# - Schema Gold
#
# =========================================================

log("Consultando permissões do catálogo")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON CATALOG {CATALOG_NAME}
    """)

)

log("Consultando permissões do schema Bronze")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON SCHEMA {CATALOG_NAME}.{SCHEMA_BRONZE}
    """)

)

log("Consultando permissões do schema Silver")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON SCHEMA {CATALOG_NAME}.{SCHEMA_SILVER}
    """)

)

log("Consultando permissões do schema Gold")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON SCHEMA {CATALOG_NAME}.{SCHEMA_GOLD}
    """)

)


# =========================================================
# 10. AUDITORIA DAS TABELAS ANALÍTICAS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Auditoria das tabelas publicadas
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.6 Evidências de auditoria
#
# Objetivo técnico:
# - Validar permissões aplicadas às tabelas Gold
#
# Objetivo de negócio:
# - Garantir rastreabilidade dos acessos
# - Confirmar aderência às políticas RBAC
#
# Tabelas auditadas:
#
# - d_plano_conta
# - ft_resultado
# - d_calendario
#
# =========================================================

log("Consultando permissões da tabela d_plano_conta")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON TABLE {D_PLANO_CONTA_TABLE}
    """)

)

log("Consultando permissões da tabela ft_resultado")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON TABLE {FT_RESULTADO_TABLE}
    """)

)

log("Consultando permissões da tabela d_calendario")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON TABLE {D_CALENDARIO_TABLE}
    """)

)

# =========================================================
# 11. AUDITORIA DAS VIEWS SEMÂNTICAS
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Governança das Views Semânticas
#
# - docs/15_artigo_tecnico.md
#   → 3.7.8.6 Evidências de auditoria
#
# Objetivo técnico:
# - Validar permissões das Views Semânticas
#
# Objetivo de negócio:
# - Confirmar que usuários de negócio
#   acessam apenas os objetos destinados
#   ao consumo analítico
#
# Views auditadas:
#
# - vw_d_plano_conta
# - vw_ft_resultado
# - vw_d_calendario
#
# =========================================================

log("Consultando permissões da view vw_d_plano_conta")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON VIEW {VW_D_PLANO_CONTA}
    """)

)

log("Consultando permissões da view vw_ft_resultado")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON VIEW {VW_FT_RESULTADO}
    """)

)

log("Consultando permissões da view vw_d_calendario")

display(

    spark.sql(f"""
    SHOW GRANTS
    ON VIEW {VW_D_CALENDARIO}
    """)

)

# =========================================================
# 12. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/07_governanca.md → Modelo de Governança
# - docs/06_operacao_plataforma.md → Encerramento operacional
# - docs/15_artigo_tecnico.md → 3.7.8.7 Evidências da governança aplicada
#
# Objetivo de negócio:
# - Confirmar a aplicação da política de governança
# - Evidenciar os mecanismos de segurança implementados
# - Registrar a conclusão da demonstração de RBAC e ACL
#
# =========================================================

log("Governança demonstrada com sucesso")

print("=" * 60)
print(" GOVERNANÇA DE DADOS - VALIDAÇÃO FINAL")
print("=" * 60)

print("✓ Unity Catalog")
print("✓ Microsoft Entra ID (SCIM)")
print("✓ RBAC (Role-Based Access Control)")
print("✓ ACL (Access Control Lists)")
print("✓ Least Privilege Principle")
print("✓ Segregação de Acessos")
print("✓ Governança Corporativa")
print("✓ Auditoria de Permissões")

print("-" * 60)
print(f"Catálogo: {CATALOG_NAME}")
print(f"Schemas governados: {SCHEMA_BRONZE}, {SCHEMA_SILVER}, {SCHEMA_GOLD}")
print("-" * 60)

print("Notebook 98 finalizado com sucesso.")
