# =========================================================
# 🔹 99_DELTA_LAKE_ACID_DEMO
# Projeto: Financial Statement Analytics Platform
#
# Objetivo:
# - Demonstrar as propriedades ACID do Delta Lake
# - Evidenciar o versionamento automático das tabelas Delta
# - Demonstrar auditoria nativa através do Transaction Log
# - Demonstrar consultas históricas (Time Travel)
# - Demonstrar restauração de versões (Restore Table)
# - Evidenciar mecanismos de governança e recuperação de dados
#
# Arquitetura:
#
#                 Delta Lake
#                      │
#                      ▼
#         Tabela Oficial (ft_resultado)
#                      │
#               Cópia para Demonstração
#                      │
#                      ▼
#             ft_resultado_demo
#                      │
#      ┌───────────────┼────────────────┐
#      ▼               ▼                ▼
# DESCRIBE HISTORY  VERSION AS OF  RESTORE TABLE
#
# Recursos demonstrados:
# - Delta Lake
# - ACID Transactions
# - Transaction Log
# - DESCRIBE HISTORY
# - VERSION AS OF
# - RESTORE TABLE
# - Time Travel
# - Auditoria Nativa
#
# 🔗 Rastreabilidade:
#
# 📄 Documento técnico:
# - ../docs/07_governanca.md
#   Delta Lake, ACID, Time Travel e Auditoria
#
# 📄 Arquitetura:
# - ../docs/02_arquitetura.md
#   Arquitetura Lakehouse e Delta Lake
#
# 📄 Operação da Plataforma:
# - ../docs/06_operacao_plataforma.md
#   Monitoramento e recuperação operacional
#
# 📄 Artigo técnico:
# - ../docs/17_artigo_tecnico.md
#   3.7 Desenvolvimento dos notebooks em PySpark
#   3.7.9 Notebook 99 – Demonstração dos recursos ACID do Delta Lake
#
# =========================================================


# =========================================================
# 1. CONFIGURAÇÃO DO AMBIENTE
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Garantias transacionais do Delta Lake (ACID)
#
# - docs/02_arquitetura.md
#   → Camada Gold e Delta Lake
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.1 Configuração do ambiente
#
# Objetivo técnico:
# - Centralizar os objetos utilizados na demonstração
# - Preservar a tabela oficial da solução
#
# Objetivo de negócio:
# - Isolar os testes da plataforma analítica
# - Evitar alterações sobre os dados corporativos
# - Facilitar manutenção do notebook
#
# =========================================================

CATALOG_NAME = "finance"

SCHEMA_GOLD = "gold"

SOURCE_TABLE = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.ft_resultado"
)

DEMO_TABLE = (
    f"{CATALOG_NAME}.{SCHEMA_GOLD}.ft_resultado_demo"
)


# =========================================================
# 2. LOG OPERACIONAL
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
# - Facilitar acompanhamento da demonstração
# - Melhorar rastreabilidade operacional
#
# =========================================================

def log(message):
    print(f"[INFO] {message}")


log("Iniciando demonstração dos recursos ACID do Delta Lake")


# =========================================================
# 3. PREPARAÇÃO DO AMBIENTE DE DEMONSTRAÇÃO
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Garantias transacionais do Delta Lake
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.2 Preparação do ambiente de demonstração
#
# Objetivo técnico:
# - Criar uma tabela temporária de demonstração
# - Preservar a tabela oficial da camada Gold
#
# Objetivo de negócio:
# - Executar testes sem impactar os dados corporativos
# - Isolar operações de escrita e recuperação
#
# Fluxo:
#
# ft_resultado
#        │
#        ▼
# ft_resultado_demo
#
# =========================================================

log("Preparando ambiente de demonstração")

spark.sql(f"""
DROP TABLE IF EXISTS {DEMO_TABLE}
""")

spark.sql(f"""
CREATE TABLE {DEMO_TABLE}
AS
SELECT *
FROM {SOURCE_TABLE}
""")

log("Tabela de demonstração criada com sucesso")


# =========================================================
# 4. HISTÓRICO DE TRANSAÇÕES (DESCRIBE HISTORY)
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Histórico de versões (Table History)
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.3 Histórico de transações
#
# Objetivo técnico:
# - Consultar o Transaction Log do Delta Lake
# - Evidenciar o histórico de operações da tabela
#
# Objetivo de negócio:
# - Disponibilizar rastreabilidade das alterações
# - Apoiar auditorias e processos de conformidade
#
# Informações apresentadas:
#
# - Version
# - Operation
# - User
# - Timestamp
# - Operation Metrics
#
# =========================================================

log("Consultando histórico de transações da tabela Delta")

display(

    spark.sql(f"""
    DESCRIBE HISTORY {DEMO_TABLE}
    """)

)

# =========================================================
# 5. VALIDAÇÃO DA VERSÃO ATUAL
# =========================================================
#
# Objetivo:
# - Registrar quantidade atual de registros
#
# =========================================================

current_count = (
    spark.table(DEMO_TABLE)
         .count()
)

print(f"Registros atuais: {current_count}")

# =========================================================
# 6. SIMULAÇÃO DE TRANSAÇÃO ACID
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Garantias transacionais do Delta Lake (ACID)
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.4 Simulação de transação ACID
#
# Objetivo técnico:
# - Gerar uma nova versão da tabela Delta
# - Evidenciar o versionamento automático
#
# Objetivo de negócio:
# - Demonstrar a consistência transacional
# - Evidenciar que cada alteração gera uma
#   nova versão auditável da tabela
#
# Operação executada:
#
# OVERWRITE
#
# Resultado esperado:
#
# Version 0 → Version 1
#
# =========================================================

log("Executando transação ACID (OVERWRITE)")

(
    spark.table(DEMO_TABLE)
         .limit(10)
         .write
         .mode("overwrite")
         .saveAsTable(DEMO_TABLE)
)

# =========================================================
# 7. VALIDAÇÃO APÓS A TRANSAÇÃO
# =========================================================
#
# Objetivo:
# - Registrar quantidade de registros após overwrite
#
# =========================================================

updated_count = (
    spark.table(DEMO_TABLE)
         .count()
)

print(f"Registros após overwrite: {updated_count}")


# =========================================================
# 8. HISTÓRICO APÓS A TRANSAÇÃO
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Histórico de versões (Table History)
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.4 Simulação de transação ACID
#
# Objetivo técnico:
# - Validar a criação de uma nova versão
# - Consultar novamente o Transaction Log
#
# Objetivo de negócio:
# - Evidenciar auditoria automática
# - Demonstrar rastreabilidade das alterações
#
# Informações esperadas:
#
# - New Version
# - Operation = WRITE
# - Timestamp
# - User
#
# =========================================================

log("Consultando histórico atualizado da tabela Delta")

display(

    spark.sql(f"""
    DESCRIBE HISTORY {DEMO_TABLE}
    """)

)


# =========================================================
# 9. CONSULTA HISTÓRICA (TIME TRAVEL)
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Time Travel
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.5 Consulta histórica (Time Travel)
#
# Objetivo técnico:
# - Consultar uma versão anterior da tabela
# - Demonstrar snapshots históricos
#
# Objetivo de negócio:
# - Permitir reprodução de cenários antigos
# - Apoiar auditorias
# - Facilitar investigações sobre alterações
#
# Recurso utilizado:
#
# VERSION AS OF
#
# =========================================================

log("Consultando versão histórica da tabela")

display(

    spark.sql(f"""
    SELECT *
    FROM {DEMO_TABLE}
    VERSION AS OF 0
    """)

)


# =========================================================
# 10. RESTORE TABLE
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Restore Table
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.6 Restauração de versões
#
# Objetivo técnico:
# - Restaurar a versão original da tabela
# - Demonstrar rollback transacional
#
# Objetivo de negócio:
# - Recuperar rapidamente alterações incorretas
# - Evidenciar mecanismos de recuperação
#   nativos do Delta Lake
#
# Operação executada:
#
# RESTORE TABLE
#
# Resultado esperado:
#
# Recuperação da Version 0
#
# =========================================================

log("Restaurando versão original da tabela")

spark.sql(f"""
RESTORE TABLE {DEMO_TABLE}
TO VERSION AS OF 0
""")

# =========================================================
# 11. VALIDAÇÃO DO RESTORE
# =========================================================
#
# Objetivo:
# - Confirmar recuperação da versão original
#
# =========================================================

restored_count = (
    spark.table(DEMO_TABLE)
         .count()
)

print(f"Registros após restore: {restored_count}")


# =========================================================
# 12. HISTÓRICO FINAL DAS TRANSAÇÕES
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Auditoria das alterações
#
# - docs/06_operacao_plataforma.md
#   → Monitoramento operacional
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.7 Evidências das funcionalidades do Delta Lake
#
# Objetivo técnico:
# - Evidenciar o registro da operação RESTORE
# - Validar o histórico completo da tabela
#
# Objetivo de negócio:
# - Disponibilizar evidências da auditoria nativa
# - Demonstrar rastreabilidade das operações executadas
#
# =========================================================

log("Consultando histórico final da tabela")

display(

    spark.sql(f"""
    DESCRIBE HISTORY {DEMO_TABLE}
    """)

)

# =========================================================
# 13. EVIDÊNCIAS DAS FUNCIONALIDADES DO DELTA LAKE
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Garantias transacionais do Delta Lake
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.7 Evidências das funcionalidades do Delta Lake
#
# Objetivo técnico:
# - Consolidar os recursos demonstrados
# - Validar o funcionamento das funcionalidades do Delta Lake
#
# Objetivo de negócio:
# - Evidenciar a robustez da plataforma analítica
# - Demonstrar mecanismos de auditoria, recuperação e integridade
#
# Funcionalidades validadas:
#
# - DESCRIBE HISTORY
# - Versionamento Automático
# - Time Travel
# - Restore Table
# - Transações ACID
# - Auditoria Nativa
#
# =========================================================

log("Validando funcionalidades do Delta Lake")

print("=" * 60)
print(" DELTA LAKE - VALIDAÇÃO FINAL")
print("=" * 60)

print("✓ DESCRIBE HISTORY")
print("✓ Versionamento Automático (Version AS OF)")
print("✓ Time Travel")
print("✓ Restore Table")
print("✓ ACID Transactions")
print("✓ Auditoria Nativa")

print("-" * 60)
print(f"Tabela de origem: {SOURCE_TABLE}")
print(f"Tabela de demonstração: {DEMO_TABLE}")
print(f"Registros originais: {current_count}")
print(f"Registros restaurados: {restored_count}")
print("-" * 60)


# =========================================================
# 14. LIMPEZA DO AMBIENTE
# =========================================================
#
# Referência:
# - docs/06_operacao_plataforma.md
#   → Administração e limpeza do ambiente
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.8 Limpeza e encerramento
#
# Objetivo técnico:
# - Remover objetos temporários utilizados na demonstração
#
# Objetivo de negócio:
# - Manter o ambiente organizado
# - Evitar acúmulo de tabelas temporárias
# - Preservar apenas os dados oficiais da plataforma
#
# =========================================================

log("Removendo tabela temporária de demonstração")

spark.sql(f"""
DROP TABLE IF EXISTS {DEMO_TABLE}
""")


# =========================================================
# 15. FINALIZAÇÃO
# =========================================================
#
# Referência:
# - docs/07_governanca.md
#   → Garantias transacionais do Delta Lake
#
# - docs/06_operacao_plataforma.md
#   → Encerramento operacional
#
# - docs/17_artigo_tecnico.md
#   → 3.7.9.8 Limpeza e encerramento
#
# Objetivo de negócio:
# - Confirmar a conclusão da demonstração
# - Evidenciar a utilização dos recursos avançados do Delta Lake
# - Registrar o encerramento da execução do notebook
#
# =========================================================

log("Demonstração dos recursos do Delta Lake concluída com sucesso")

print("Notebook 99 finalizado com sucesso.")
