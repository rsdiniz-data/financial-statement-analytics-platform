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
