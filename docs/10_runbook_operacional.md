# 10. Runbook Operacional

> Este runbook reúne os principais procedimentos para operação, monitoramento e manutenção da plataforma após sua implantação.

---

## ▶️ Execução do Pipeline

O processamento pode ser iniciado de duas formas:

- Execução automática por agendamento
- Execução manual via Azure Data Factory

Fluxo de execução:

1. Bronze
2. Silver
3. Gold

📷 ![Pipeline Operacional](../images/adf_pipeline.png)

---

## 📊 Monitoramento

Acompanhe as execuções pelo Azure Data Factory.

Principais indicadores:

- Status da execução
- Horário de início e término
- Tempo de processamento
- Execução dos notebooks
- Mensagens de erro
- Tentativas de reprocessamento (Retry)

---

## ✅ Validação das Cargas

Após cada execução, verifique:

- Tabelas Bronze atualizadas
- Tabelas Silver atualizadas
- Tabelas Gold publicadas
- Views semânticas disponíveis
- Quantidade de registros processados
- Logs de execução dos notebooks

---

## 🔄 Atualização dos Dados

Após a conclusão do pipeline:

- As tabelas do Unity Catalog são atualizadas
- As views semânticas refletem os novos dados
- O Power BI pode ser atualizado com um **Refresh** do conjunto de dados

---

## ♻️ Reprocessamento

Em caso de inconsistências:

- Corrigir os dados de origem
- Executar novamente o pipeline completo

Como as tabelas utilizam **Delta Lake**, os dados são substituídos de forma controlada, mantendo a consistência entre as camadas.

---

## 🛡️ Auditoria e Recuperação

O Delta Lake permite:

- Consultar o histórico das tabelas (History)
- Acessar versões anteriores (Time Travel)
- Restaurar versões (Restore)

🔗 Script:

👉 [99_delta_lake_acid_demo.py](../notebooks/governance/99_delta_lake_acid_demo.py)

---

## 👥 Administração de Acessos

O gerenciamento de usuários é realizado pelo **Microsoft Entra ID**, com sincronização automática via **SCIM**.

As permissões são aplicadas aos grupos:

- `data_engineers`
- `bi_analysts`
- `business_users`

---

## 🔧 Manutenção Preventiva

Recomenda-se verificar periodicamente:

- Funcionamento do agendamento
- Disponibilidade do Azure Databricks
- SQL Warehouse
- Validade dos PATs
- Sincronização SCIM
- Permissões no Unity Catalog
- Utilização do Azure Data Lake Storage

---

## 🎯 Resultado Esperado

A operação da plataforma deve garantir:

- Execução automatizada dos pipelines
- Monitoramento centralizado
- Atualização consistente das camadas
- Governança dos acessos
- Auditoria e rastreabilidade
- Recuperação rápida de incidentes
- Disponibilização contínua dos dados para ferramentas de BI
