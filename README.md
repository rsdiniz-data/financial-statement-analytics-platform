# 📊 Financial Statement Analytics Platform

> Plataforma corporativa de Engenharia de Dados para processamento, governança e disponibilização de demonstrações financeiras utilizando Microsoft Azure.

---

# 🧠 Sobre o Projeto

O **Financial Statement Analytics Platform** demonstra a implementação de uma plataforma moderna de Engenharia de Dados construída sobre o ecossistema **Microsoft Azure**, utilizando uma arquitetura **Lakehouse** baseada no padrão **Medallion Architecture**.

A solução automatiza todo o ciclo de processamento da **Demonstração do Resultado do Exercício (DRE)**, desde a ingestão de arquivos Microsoft Excel armazenados no **SharePoint Online** até a disponibilização de um modelo dimensional otimizado para ferramentas de Business Intelligence.

Durante o processamento, os dados percorrem as camadas **Bronze**, **Silver** e **Gold**, onde passam por processos de ingestão, padronização, tratamento, enriquecimento e modelagem analítica. Cada etapa foi projetada para garantir qualidade, rastreabilidade, escalabilidade e governança dos dados.

Além da implementação dos pipelines de dados, o projeto contempla diversos componentes presentes em plataformas corporativas modernas de Analytics, incluindo:

- Arquitetura Lakehouse baseada em Delta Lake;
- Processamento distribuído utilizando Apache Spark (PySpark);
- Governança centralizada com Unity Catalog;
- Controle de acesso baseado em papéis (RBAC);
- Gerenciamento seguro de credenciais com Azure Key Vault;
- Integração com Microsoft Entra ID e SharePoint Online;
- Orquestração de pipelines utilizando Azure Data Factory;
- Versionamento do código com Git e GitHub;
- Automação através de GitHub Actions;
- Aplicação de práticas de DevOps e DataOps.

Toda a solução foi concebida utilizando serviços gerenciados do Microsoft Azure, priorizando escalabilidade, segurança, reutilização de componentes e adoção das principais boas práticas de Engenharia de Dados.

---

# 🎯 Objetivo do Projeto

Demonstrar, de ponta a ponta, a implementação de uma plataforma corporativa de Engenharia de Dados para processamento de demonstrações financeiras, evidenciando a integração entre serviços do Microsoft Azure, governança de dados, automação de pipelines e arquitetura Lakehouse.

Ao longo do projeto são demonstrados conceitos e práticas utilizados em ambientes corporativos, incluindo:

- Arquitetura Medallion (Bronze, Silver e Gold);
- Processamento distribuído com Apache Spark;
- Modelagem dimensional para Analytics;
- Delta Lake e transações ACID;
- Governança de dados com Unity Catalog;
- Segurança baseada em Microsoft Entra ID, RBAC e Azure Key Vault;
- Orquestração de pipelines com Azure Data Factory;
- Versionamento utilizando Git e GitHub;
- Integração Contínua (CI) com GitHub Actions;
- Práticas de DevOps e DataOps aplicadas à Engenharia de Dados.

---

# 🚀 Principais Funcionalidades

## 📥 Ingestão de Dados

- Ingestão automatizada de arquivos Microsoft Excel armazenados no SharePoint Online;
- Integração segura utilizando Microsoft Graph API;
- Autenticação baseada em Microsoft Entra ID;
- Leitura dos arquivos diretamente em memória, sem dependência de uploads manuais.

---

## 🏗️ Plataforma de Dados

- Arquitetura Lakehouse baseada no padrão Medallion;
- Camadas Bronze, Silver e Gold;
- Processamento distribuído utilizando Azure Databricks;
- Persistência dos dados em formato Delta Lake;
- Organização lógica através do Unity Catalog.

---

## 📊 Processamento Analítico

- Transformações utilizando PySpark;
- Padronização e tratamento dos dados financeiros;
- Aplicação de regras de negócio da Demonstração do Resultado do Exercício (DRE);
- Construção de modelo dimensional para consumo analítico;
- Disponibilização das entidades para ferramentas de Business Intelligence.

---

## 🔐 Governança e Segurança

- Governança centralizada utilizando Unity Catalog;
- Controle de acesso baseado em grupos (RBAC);
- Gerenciamento seguro de credenciais através do Azure Key Vault;
- Auditoria e rastreabilidade dos pipelines;
- Data Lineage e metadados técnicos.

---

## ⚙️ Automação e Operação

- Orquestração de pipelines utilizando Azure Data Factory;
- Execução automatizada dos notebooks Databricks;
- Monitoramento operacional dos pipelines;
- Processos de validação e reprocessamento;
- Tratamento padronizado de erros e logs operacionais.

---

## 🔄 DevOps e DataOps

- Versionamento completo utilizando Git;
- Repositório centralizado no GitHub;
- Integração Contínua (CI) utilizando GitHub Actions;
- Estrutura preparada para Continuous Delivery (CD);
- Automação dos pipelines de dados;
- Aplicação de práticas de DataOps para governança, rastreabilidade e evolução contínua da plataforma.

---

## 📈 Consumo Analítico

- Publicação das tabelas da camada Gold;
- Modelo dimensional otimizado para análises financeiras;
- Integração com Power BI e outras ferramentas de Business Intelligence;
- Estrutura preparada para expansão com novas fontes de dados e indicadores analíticos.

---

# 🏗️ Arquitetura da Solução

A plataforma foi desenvolvida seguindo os princípios da **Lakehouse Architecture**, organizando o fluxo de dados em camadas independentes de responsabilidade conforme o padrão **Medallion Architecture**.

O pipeline automatiza todo o ciclo de vida dos dados, desde a ingestão de arquivos corporativos armazenados no SharePoint Online até a disponibilização de um modelo dimensional pronto para consumo por ferramentas de Business Intelligence.

Cada componente da arquitetura possui uma responsabilidade específica, permitindo maior escalabilidade, governança, reutilização e facilidade de manutenção.

```text
                           SharePoint Online
                                  │
                                  ▼
                  Azure Data Factory (Orquestração)
                                  │
                                  ▼
                      Azure Databricks (PySpark)
                                  │
                                  ▼
                  Azure Data Lake Storage Gen2
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
 Bronze Layer                Silver Layer               Gold Layer
 (Raw Data)                 (Trusted Data)            (Business Data)
      └───────────────────────────┼───────────────────────────┘
                                  ▼
                         Modelo Dimensional
                                  │
                                  ▼
                 Power BI / Ferramentas Analíticas
```

A solução integra serviços gerenciados do Microsoft Azure para construir uma plataforma moderna de Engenharia de Dados composta por:

| Componente | Responsabilidade |
|------------|------------------|
| **SharePoint Online** | Armazenamento dos arquivos financeiros de origem. |
| **Azure Data Factory** | Orquestração e automação dos pipelines de dados. |
| **Azure Databricks** | Processamento distribuído utilizando Apache Spark (PySpark). |
| **Azure Data Lake Storage Gen2** | Armazenamento físico das camadas Bronze, Silver e Gold. |
| **Delta Lake** | Armazenamento transacional com suporte a ACID Transactions, Time Travel e Versionamento. |
| **Unity Catalog** | Governança centralizada dos ativos de dados. |
| **Azure Key Vault** | Gerenciamento seguro de credenciais e segredos. |
| **Microsoft Entra ID** | Autenticação e gerenciamento de identidades. |
| **Power BI** | Consumo analítico das entidades disponibilizadas na camada Gold. |

A arquitetura foi projetada para proporcionar:

- Separação entre ingestão, transformação e consumo analítico;
- Processamento distribuído e escalável;
- Governança centralizada dos ativos de dados;
- Segurança baseada em identidade e controle de acesso;
- Rastreabilidade completa das transformações;
- Versionamento e recuperação de dados com Delta Lake;
- Reutilização das tabelas tratadas em diferentes cenários analíticos;
- Facilidade de evolução da plataforma com novas fontes de dados.

---

# 📌 Navegação

A documentação da plataforma está organizada em documentos independentes para facilitar a consulta e a rastreabilidade entre arquitetura, implementação, governança e operação.

| Documento | Descrição |
|-----------|-----------|
| 📄 [01. Visão Geral do Projeto](./docs/01_visao_geral.md) | Contexto, objetivos, justificativa, escopo e benefícios da plataforma. |
| 🏗️ [02. Arquitetura da Solução](./docs/02_arquitetura.md) | Arquitetura lógica, componentes Azure, fluxo de dados e arquitetura Medallion. |
| ⚙️ [03. Desenvolvimento do Projeto](./docs/03_desenvolvimento.md) | Implementação dos notebooks, pipelines, processamento distribuído e arquitetura das camadas Bronze, Silver e Gold. |
| 📊 [04. Modelagem Dimensional](./docs/04_modelagem_dimensional.md) | Modelo dimensional, tabelas fato, dimensões e estrutura analítica da camada Gold. |
| 🗂️ [05. Dicionário de Dados](./docs/05_dicionario_dados.md) | Descrição das tabelas, colunas, tipos de dados e regras de negócio. |
| 🖥️ [06. Operação da Plataforma](./docs/06_operacao_plataforma.md) | Execução dos pipelines, monitoramento, validações operacionais e administração da solução. |
| 🔐 [07. Governança de Dados](./docs/07_governanca.md) | Unity Catalog, RBAC, ACL, SCIM, Data Lineage, segurança e gerenciamento de credenciais. |
| 🚀 [08. Runbook de Implantação](./docs/08_runbook_implantacao.md) | Provisionamento da infraestrutura, configuração do ambiente e implantação da plataforma. |
| 🛠️ [09. Runbook Operacional](./docs/09_runbook_operacional.md) | Procedimentos operacionais, manutenção, monitoramento e suporte da solução. |
| 🏷️ [10. Padrão de Nomenclatura](./docs/10_padrao_nomenclatura.md) | Convenções de nomenclatura para recursos Azure, Databricks, pipelines e objetos de dados. |
| ✅ [11. Checklist de Implantação](./docs/11_checklist_implantacao.md) | Lista de verificação para validação da implantação da plataforma. |
| 🧯 [12. Troubleshooting](./docs/12_troubleshooting.md) | Diagnóstico e resolução dos principais cenários de falha. |
| 💡 [13. Entrega de Valor](./docs/13_entrega_valor.md) | Benefícios técnicos, operacionais e de negócio proporcionados pela solução. |
| 📑 [14. Apêndice A – Inventário dos Recursos da Plataforma](./docs/14_inventario.md) | Inventário dos recursos Azure, Databricks, Data Factory, Unity Catalog e GitHub. |
| 📘 [15. Artigo Técnico](./docs/15_artigo_tecnico.md) | Documentação técnica consolidada contendo arquitetura, implementação, decisões de projeto e boas práticas adotadas durante o desenvolvimento da plataforma. |

---

# 📄 Documentação Técnica

Além da documentação modular disponível na pasta **docs**, o projeto disponibiliza um documento técnico consolidado que reúne toda a implementação da plataforma em um único material.

O documento apresenta, de forma integrada:

- Visão geral da solução;
- Arquitetura da plataforma;
- Desenvolvimento dos notebooks em PySpark;
- Modelagem dimensional;
- Governança e segurança;
- Operação da plataforma;
- Runbooks de implantação e operação;
- Inventário dos recursos Azure;
- Implementação do modelo analítico;
- Boas práticas de Engenharia de Dados, DevOps e DataOps.

Este material estabelece a rastreabilidade entre os requisitos do projeto, as decisões arquiteturais e a implementação técnica da solução.

📄 **[Acessar documentação técnica completa](./docs/15_artigo_tecnico.md)**

---
