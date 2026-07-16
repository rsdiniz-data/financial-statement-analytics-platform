# 📝 17. Artigo Técnico — Financial Statement Analytics Platform

Este artigo apresenta a construção da solução **Financial Statement Analytics Platform**, uma arquitetura analítica moderna baseada em **Azure Databricks, Azure Data Factory, Delta Lake e Medallion Architecture**, aplicada ao processamento e análise de demonstrações financeiras.

---

## 🔗 Acesso ao artigo

👉 [Ler no LinkedIn](https://www.linkedin.com/...)

---

## 🧠 Principais temas abordados

- Arquitetura Lakehouse com padrão Medallion (Bronze, Silver e Gold)  
- Orquestração de pipelines com Azure Data Factory  
- Processamento de dados com PySpark no Azure Databricks  
- Modelagem dimensional para análise financeira (DRE)  
- Uso do Delta Lake com garantias ACID e Time Travel  
- Governança de dados com Unity Catalog e RBAC  
- Camada semântica para consumo analítico em BI  
- Integração com Microsoft Power BI  

---

## 🔄 Relação com este repositório

Este repositório contém a **implementação completa da solução apresentada no artigo**, incluindo:

- Pipelines de ingestão, transformação e publicação (Bronze, Silver e Gold)  
- Notebooks organizados por camada e governança  
- Estrutura de tabelas dimensionais e fato  
- Publicação e governança via Unity Catalog  
- Views semânticas para consumo analítico  
- Orquestração automatizada no Azure Data Factory  
- Integração com Power BI via SQL Warehouse  

---

## 🎯 Objetivo do Artigo

Demonstrar a construção de uma plataforma moderna de dados financeiros, conectando arquitetura, engenharia de dados e consumo analítico em uma solução escalável, governada e automatizada em ambiente Azure.
