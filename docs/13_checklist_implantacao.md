# 13. Checklist de Implantação

Checklist utilizado para validar a correta implantação da plataforma **Financial Statement Analytics Platform**, cobrindo infraestrutura, segurança, governança, processamento, orquestração e consumo analítico.

---

## 🎯 Objetivo

Garantir que todos os componentes da solução estejam corretamente configurados antes da execução do pipeline, reduzindo riscos operacionais e falhas em produção.

---

## ☁️ Infraestrutura Azure

| Item | Verificação | Status |
|------|------------|--------|
| Resource Group criado | ☐ | |
| Storage Account (ADLS Gen2) criada | ☐ | |
| Containers Bronze, Silver, Gold e Unity Catalog criados | ☐ | |
| Diretório `metastore-root` criado | ☐ | |
| Azure Databricks Workspace criado | ☐ | |
| Azure Data Factory criado | ☐ | |
| Azure Key Vault criado | ☐ | |
| Access Connector criado | ☐ | |
| SQL Warehouse criado | ☐ | |

---

## 🔐 Segurança e Identidade

| Item | Verificação | Status |
|------|------------|--------|
| App Registration (ADLS) criada | ☐ | |
| App Registration (SharePoint) criada | ☐ | |
| Permissões no Storage configuradas | ☐ | |
| Managed Identity configurada | ☐ | |
| Key Vault com segredos disponíveis | ☐ | |
| Secret Scope criado no Databricks | ☐ | |
| Secret Scope integrado ao Key Vault | ☐ | |

---

## 🗂️ Unity Catalog

| Item | Verificação | Status |
|------|------------|--------|
| Metastore configurado | ☐ | |
| Storage Credential criada | ☐ | |
| External Locations (Bronze/Silver/Gold) criadas | ☐ | |
| Catalog criado | ☐ | |
| Schemas (bronze, silver, gold) criados | ☐ | |

---

## 🧪 Validação do Ambiente

| Item | Verificação | Status |
|------|------------|--------|
| Notebook de teste SharePoint executado | ☐ | |
| Notebook de validação Key Vault executado | ☐ | |
| Notebook de validação ADLS executado | ☐ | |
| Notebook de validação Unity Catalog executado | ☐ | |

---

## 📒 Notebooks Publicados

### Bronze

| Notebook | Status |
|----------|--------|
| 01_bronze_ingest_plano_conta | ☐ |
| 02_bronze_ingest_dfp | ☐ |

### Silver

| Notebook | Status |
|----------|--------|
| 03_silver_transform_plano_conta | ☐ |
| 04_silver_transform_resultado | ☐ |

### Gold

| Notebook | Status |
|----------|--------|
| 05_gold_d_plano_conta | ☐ |
| 06_gold_ft_resultado | ☐ |
| 07_gold_d_calendario | ☐ |

### Governança

| Notebook | Status |
|----------|--------|
| 98_governance_rbac_acl | ☐ |
| 99_delta_lake_acid_demo | ☐ |

---

## 🗃️ Estruturas de Dados

| Item | Verificação | Status |
|------|------------|--------|
| Tabelas Bronze publicadas | ☐ | |
| Tabelas Silver publicadas | ☐ | |
| Dimensão `d_plano_conta` publicada | ☐ | |
| Fato `ft_resultado` publicada | ☐ | |
| Dimensão `d_calendario` publicada | ☐ | |

---

## 🧭 Camada Semântica

| Item | Verificação | Status |
|------|------------|--------|
| vw_d_plano_conta criada | ☐ | |
| vw_ft_resultado criada | ☐ | |
| vw_d_calendario criada | ☐ | |

---

## 🔐 Governança

| Item | Verificação | Status |
|------|------------|--------|
| Grupo `data_engineers` criado | ☐ | |
| Grupo `bi_analysts` criado | ☐ | |
| Grupo `business_users` criado | ☐ | |
| SCIM configurado | ☐ | |
| Sincronização validada | ☐ | |
| RBAC aplicado | ☐ | |
| ACLs configuradas | ☐ | |

---

## ⚙️ Orquestração

| Item | Verificação | Status |
|------|------------|--------|
| Linked Service Databricks criado | ☐ | |
| Pipeline `pl-orchestrator-dre` criado | ☐ | |
| Atividades configuradas | ☐ | |
| Dependências entre notebooks definidas | ☐ | |
| Retry Policy configurada | ☐ | |
| Trigger agendado criado | ☐ | |
| Pipeline publicado no ADF | ☐ | |

---

## 📊 Integração Power BI

| Item | Verificação | Status |
|------|------------|--------|
| SQL Warehouse ativo | ☐ | |
| Server Hostname obtido | ☐ | |
| HTTP Path obtido | ☐ | |
| Personal Access Token criado | ☐ | |
| Conexão estabelecida | ☐ | |
| Views carregadas | ☐ | |
| Modelo dimensional validado | ☐ | |

---

## 🔎 Validação Operacional

| Item | Verificação | Status |
|------|------------|--------|
| Pipeline executado com sucesso | ☐ | |
| Logs disponíveis no ADF | ☐ | |
| Dados publicados no Unity Catalog | ☐ | |
| Views disponíveis para consumo | ☐ | |
| Dashboard atualizado no Power BI | ☐ | |
| Testes de leitura validados | ☐ | |

---

## ✅ Critério de Aceite

A implantação é considerada concluída quando **todos os itens estiverem validados**, garantindo que a plataforma esteja:

- operacional  
- governada  
- escalável  
- pronta para consumo analítico  
- integrada ao Power BI  
