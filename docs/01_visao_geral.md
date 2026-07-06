# 1. Visão Geral do Projeto

## 🎯 Contexto

O **Financial Statement Analytics Platform** demonstra a construção de uma plataforma moderna de Engenharia de Dados utilizando serviços do **Microsoft Azure** para automatizar a ingestão, o processamento, a governança e a disponibilização de informações financeiras.

A solução processa dados da **Demonstração do Resultado do Exercício (DRE)** a partir de arquivos Microsoft Excel armazenados no **SharePoint Online**, organizando o pipeline segundo a **Arquitetura Medallion** (Bronze, Silver e Gold) até a publicação de um modelo dimensional otimizado para ferramentas de Business Intelligence.

Além dos pipelines de dados, o projeto implementa práticas modernas de governança, segurança, DataOps e automação, utilizando serviços nativos da plataforma Azure.

---

## 🎯 Objetivos

O projeto foi desenvolvido com os seguintes objetivos:

* Construir uma plataforma de dados baseada em arquitetura Lakehouse.

* Automatizar a ingestão de dados financeiros provenientes do SharePoint Online.

* Implementar processamento distribuído utilizando Azure Databricks e Apache Spark.

* Organizar os dados nas camadas Bronze, Silver e Gold.

* Disponibilizar um modelo dimensional otimizado para análises financeiras.

* Implementar governança e controle de acesso utilizando Unity Catalog.

* Automatizar a orquestração dos pipelines com Azure Data Factory.

* Aplicar práticas de DevOps e DataOps utilizando GitHub e GitHub Actions.

---



## 💡 Justificativa

Organizações que utilizam planilhas eletrônicas como fonte de informações financeiras enfrentam desafios relacionados à padronização, rastreabilidade, segurança e escalabilidade dos processos analíticos.

Para solucionar esse cenário, foi desenvolvida uma arquitetura baseada em **Lakehouse**, separando claramente as etapas de ingestão, transformação e consumo dos dados.

Essa abordagem aumenta a confiabilidade das informações, fortalece a governança dos dados e prepara a plataforma para evolução e integração com novos cenários analíticos.

---

## 🚀 Benefícios da Solução

A arquitetura implementada proporciona diversos benefícios técnicos e operacionais, entre eles:

* Automação dos pipelines de dados.

* Arquitetura escalável baseada em Lakehouse.

* Governança centralizada com Unity Catalog.

* Segurança baseada em RBAC, ACL e Microsoft Entra ID.

* Armazenamento transacional com Delta Lake.

* Rastreabilidade através de Time Travel e Version History.

* Processamento distribuído com Apache Spark.

* Integração com Power BI para consumo analítico.

---

## 🛠️ Plataforma Tecnológica


| Categoria        | Tecnologia                                |
| ---------------- | ----------------------------------------- |
| Cloud            | Microsoft Azure                           |
| Armazenamento    | Azure Data Lake Storage Gen2              |
| Processamento    | Azure Databricks (Apache Spark / PySpark) |
| Governança       | Unity Catalog                             |
| Formato de Dados | Delta Lake                                |
| Orquestração     | Azure Data Factory                        |
| Segurança        | Microsoft Entra ID + Azure Key Vault      |
| DevOps           | GitHub + GitHub Actions                   |
| Analytics        | Power BI                                  |

---

A plataforma adota a **Arquitetura Medallion**, estruturando o Data Lake nas camadas Bronze, Silver e Gold, enquanto a camada Gold disponibiliza um modelo dimensional otimizado para análises corporativas.

---

## 🔗 Rastreabilidade


* 🏗️ [Arquitetura da Solução](./02_arquitetura.md)

* ⚙️ [Desenvolvimento do Projeto](./03_desenvolvimento.md)

* 📊 [Modelagem Dimensional](./04_modelagem_dimensional.md)

* 🗂️ [Dicionário de Dados](./05_dicionario_dados.md)

* 🖥️ [Operação da Plataforma](./06_operacao_plataforma.md)

* 🔐 [Governança de Dados](./07_governanca.md)

* 🚀 [Runbook de Implantação](./08_runbook_implantacao.md)

* 🛠️ [Runbook Operacional](./09_runbook_operacional.md)

* 🏷️ [Padrão de Nomenclatura](./10_padrao_nomenclatura.md)

* ✅ [Checklist de Implantação](./11_checklist_implantacao.md)

* 🧯 [Troubleshooting](./12_troubleshooting.md)

* 💡 [Entrega de Valor](./13_entrega_valor.md)

* 📑 [Apêndice A – Inventário dos Recursos da Plataforma](./14_inventario.md)

* 📘 [Artigo Técnico Completo](./15_artigo_tecnico.md)
