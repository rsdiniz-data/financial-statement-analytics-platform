# 📦 Apêndice A — Inventário dos Recursos da Plataforma

Este apêndice consolida todos os recursos utilizados na solução **Financial Statement Analytics Platform**, organizados por categoria para facilitar rastreabilidade, manutenção e evolução da arquitetura.

---

## 🏗️ Infraestrutura

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Resource Group | grp | grp-finance-dev | Azure | Agrupamento dos recursos |
| Storage Account | st | stfinancedl002 | Azure | Data Lake (ADLS Gen2) |
| Container Bronze | co | bronze | Azure | Dados brutos |
| Container Silver | co | silver | Azure | Dados tratados |
| Container Gold | co | gold | Azure | Dados analíticos |
| Container Unity Catalog | co | unitycatalog | Azure | Metastore |
| Metastore Root | dir | metastore-root | Azure | Raiz do Unity Catalog |

---

## 🔐 Segurança e Identidade

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| App Registration (ADLS) | app | app-databricks-adls-access | Entra ID | Acesso ao Storage |
| App Registration (SharePoint) | app | app-databricks-sharepoint-ingestion | Entra ID | Ingestão externa |
| Access Connector | ac | ac-finance-databricks | Azure | Managed Identity |
| Key Vault | kv | kv-finance-dev-011 | Azure | Gestão de segredos |
| Secret Scope | ss | ss-finance-dre-kv | Databricks | Integração com Key Vault |

---

## 🧠 Plataforma de Dados

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Databricks Workspace | ws | ws-finance-databricks-dev | Azure | Ambiente analítico |
| Cluster | clu | clu-finance-dre-dev | Databricks | Processamento Spark |
| SQL Warehouse | sqlw | sqlw-finance-dev | Databricks | Consumo SQL / Power BI |

---

## 🧩 Governança (Unity Catalog)

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Storage Credential | sc | sc-finance-dre | Databricks | Acesso ao ADLS |
| External Location (Bronze) | el | el-bronze-finance | Databricks | Camada Bronze |
| External Location (Silver) | el | el-silver-finance | Databricks | Camada Silver |
| External Location (Gold) | el | el-gold-finance | Databricks | Camada Gold |
| External Location (Metastore) | el | el-metastore-root | Databricks | Root UC |
| Catalog | cat | finance | Databricks | Catálogo corporativo |
| Schema Bronze | sch | bronze | Databricks | Camada Bronze |
| Schema Silver | sch | silver | Databricks | Camada Silver |
| Schema Gold | sch | gold | Databricks | Camada Gold |

---

## ⚙️ Orquestração (Azure Data Factory)

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Linked Service | ls | ls-databricks-dre | ADF | Conexão com Databricks |
| Pipeline | pl | pl-orchestrator-dre | ADF | Orquestração principal |
| Notebook Activity | nb | nb_01_bronze_ingest | ADF | Execução de notebooks |
| Trigger | trg | trg-pl-orchestrator-dre | ADF | Agendamento |
| Retry Policy | rp | retry-3 | ADF | Resiliência |

---

## 📓 Notebooks (Databricks)

### Validação
- 01_sharepoint_connection_test  
- 02_key_vault_validation  
- 03_adls_connection_test  
- 04_unity_catalog_validation  

### Bronze
- 01_bronze_ingest_plano_conta  
- 02_bronze_ingest_dfp  

### Silver
- 03_silver_transform_plano_conta  
- 04_silver_transform_resultado  

### Gold
- 05_gold_d_plano_conta  
- 06_gold_ft_resultado  
- 07_gold_d_calendario  

### Governança
- 98_governance_rbac_acl  
- 99_delta_lake_acid_demo  

---

## 📊 BI e Consumo

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| View Semântica | vw | vw_d_plano_conta | Unity Catalog | Consumo analítico |
| View Semântica | vw | vw_ft_resultado | Unity Catalog | Consumo analítico |
| View Semântica | vw | vw_d_calendario | Unity Catalog | Consumo analítico |
| Dataset Power BI | ds | Financial Statement Analytics | Power BI | Modelo analítico |

---

## 👥 Governança de Acesso

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Grupo | grp | data_engineers | Entra ID | Engenharia de dados |
| Grupo | grp | bi_analysts | Entra ID | BI |
| Grupo | grp | business_users | Entra ID | Negócio |
| SCIM Provisioning | scim | Databricks SCIM | Entra ID | Sincronização automática |

---

## 🔄 DevOps

| Recurso | Prefixo | Exemplo | Plataforma | Finalidade |
|----------|----------|----------|-------------|-------------|
| Repository | repo | financial-statement-analytics-platform | GitHub | Código-fonte |
| GitHub Actions | gha | ci_cd.yml | GitHub | CI/CD |

---

## 🎯 Resultado

Este inventário garante:

- Padronização completa da plataforma  
- Rastreabilidade dos recursos  
- Facilidade de manutenção e troubleshooting  
- Apoio à evolução da arquitetura  
- Visão centralizada do ecossistema de dados




| Ordem | Categoria | Recurso | Prefixo | Exemplo | Plataforma | Objetivo | Observações | Seção do Documento | Referência |
| 1 | Infraestrutura | Resource Group | grp | grp-finance-dev | Azure Portal | Agrupar recursos do projeto | Ambiente de desenvolvimento | 8. Runbook de Implantação | 8.2 Provisionamento da infraestrutura |

