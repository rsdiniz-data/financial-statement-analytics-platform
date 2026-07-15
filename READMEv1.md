# 📊 Financial Statement Analytics Platform

> Plataforma corporativa de Engenharia de Dados para processamento, governança e análise de demonstrações financeiras utilizando Microsoft Azure.

---

# 🧠 Sobre o Projeto

O **Financial Statement Analytics Platform** é um projeto de Engenharia de Dados desenvolvido para demonstrar a construção de uma plataforma moderna de dados sobre o ecossistema Microsoft Azure, aplicando conceitos de Lakehouse, DataOps e Analytics Engineering.

A solução automatiza a ingestão, o processamento, a governança e a disponibilização de dados da **Demonstração do Resultado do Exercício (DRE)**, transformando arquivos Microsoft Excel armazenados no SharePoint Online em um modelo analítico dimensional otimizado para ferramentas de Business Intelligence.

Durante o processamento, os dados percorrem um pipeline estruturado segundo a **Arquitetura Medallion**, passando pelas camadas **Bronze**, **Silver** e **Gold**, onde são progressivamente refinados até se tornarem conjuntos de dados confiáveis, governados e preparados para análises corporativas.

Além dos pipelines de dados, o projeto demonstra a implementação de diversos componentes presentes em uma plataforma corporativa de dados, incluindo governança centralizada, controle de acesso baseado em papéis, gerenciamento seguro de credenciais, integração contínua, orquestração de pipelines, versionamento de código e recursos avançados do Delta Lake para garantir integridade, rastreabilidade e confiabilidade dos dados.

Toda a arquitetura foi concebida utilizando serviços gerenciados do Microsoft Azure, priorizando escalabilidade, segurança, reutilização de componentes e adoção das principais boas práticas de Engenharia de Dados.

---

> **Objetivo do projeto**
>
> Demonstrar, de ponta a ponta, a implementação de uma plataforma moderna de Engenharia de Dados para processamento de informações financeiras, utilizando serviços nativos do Microsoft Azure e seguindo as melhores práticas de arquitetura, governança, automação e DataOps.

---

# 🚀 Principais Funcionalidades

- 📥 Ingestão automatizada de arquivos Microsoft Excel armazenados no SharePoint Online.
- 🏗️ Arquitetura Lakehouse baseada no padrão Medallion (Bronze, Silver e Gold).
- ⚡ Processamento distribuído utilizando Apache Spark (PySpark) no Azure Databricks.
- 📊 Construção de modelo dimensional otimizado para análises financeiras.
- 🗄️ Armazenamento transacional com Delta Lake.
- 🔐 Governança centralizada utilizando Unity Catalog.
- 👥 Controle de acesso baseado em grupos corporativos (RBAC e ACL).
- 🔑 Gerenciamento seguro de credenciais através do Azure Key Vault.
- 🔄 Orquestração de pipelines utilizando Azure Data Factory.
- 📈 Integração com ferramentas de Business Intelligence, como Power BI.
- 🔍 Rastreabilidade, versionamento e recuperação de dados utilizando recursos avançados do Delta Lake.
- 🚀 Aplicação de práticas de DevOps e DataOps com GitHub e GitHub Actions.

---

# 🏗️ Arquitetura da Solução

A plataforma foi desenvolvida seguindo o conceito de **Lakehouse Architecture**, organizando o fluxo de dados em múltiplas camadas independentes de responsabilidade.

O pipeline automatiza desde a ingestão dos arquivos financeiros até a disponibilização de um modelo analítico pronto para consumo por ferramentas de Business Intelligence.

```text
                     SharePoint Online
                              │
                              ▼
                  Azure Data Factory (Ingestão)
                              │
                              ▼
               Azure Data Lake Storage Gen2
                              │
                              ▼
                  Azure Databricks (PySpark)
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      Bronze Layer       Silver Layer        Gold Layer
   (Raw Data)         (Trusted Data)     (Business Data)
          └───────────────────┼───────────────────┘
                              ▼
                    Modelo Dimensional
                              │
                              ▼
              Power BI / Ferramentas Analíticas
```

A arquitetura foi projetada para proporcionar:

- Separação entre ingestão, transformação e consumo analítico;
- Escalabilidade para novas fontes de dados;
- Governança centralizada dos ativos de dados;
- Alta rastreabilidade das transformações;
- Reutilização das tabelas tratadas em diferentes cenários analíticos.

---

# 📌 Navegação

A documentação completa da plataforma está organizada em documentos independentes para facilitar a navegação e a consulta.

| Documento | Descrição |
|-----------|-----------|
| 📄 [Visão Geral do Projeto](./docs/01_visao_geral.md) | Contexto, objetivos, justificativa e benefícios da plataforma. |
| 🏗️ [Arquitetura da Solução](./docs/02_arquitetura.md) | Arquitetura lógica, componentes da plataforma e fluxo de dados. |
| ⚙️ [Desenvolvimento do Projeto](./docs/03_desenvolvimento.md) | Implementação da solução, organização dos notebooks, pipelines de dados e processamento nas camadas Bronze, Silver e Gold. |
| 📊 [Modelagem Dimensional](./docs/04_modelagem_dimensional.md) | Modelo dimensional, dimensões, fatos, relacionamentos e estrutura analítica da camada Gold. |
| 🗂️ [Dicionário de Dados](./docs/05_dicionario_dados.md) | Descrição das tabelas, colunas, tipos de dados e regras de negócio implementadas. |
| 🖥️ [Operação da Plataforma](./docs/06_operacao_plataforma.md) | Execução dos pipelines, monitoramento, validações operacionais e administração da plataforma. |
| 🔐 [Governança de Dados](./docs/07_governanca.md) | Governança de dados, segurança, Unity Catalog, RBAC, ACL, SCIM e gerenciamento de credenciais. |
| 🚀 [Runbook de Implantação](./docs/08_runbook_implantacao.md) | Procedimentos para provisionamento da infraestrutura, configuração do ambiente e implantação da solução. |
| 🛠️ [Runbook Operacional](./docs/09_runbook_operacional.md) | Procedimentos operacionais, manutenção, monitoramento e suporte da plataforma. |
| 🏷️ [Padrão de Nomenclatura](./docs/10_padrao_nomenclatura.md) | Convenções de nomenclatura adotadas para recursos Azure, Databricks, pipelines e objetos de dados. |
| ✅ [Checklist de Implantação](./docs/11_checklist_implantacao.md) | Lista de verificação para validação da implantação completa da plataforma. |
| 🧯 [Troubleshooting](./docs/12_troubleshooting.md) | Diagnóstico, resolução de problemas e tratamento dos principais cenários de falha. |
| 💡 [Entrega de Valor](./docs/13_entrega_valor.md) | Benefícios técnicos, operacionais e de negócio proporcionados pela arquitetura da solução. |
| 📑 [Apêndice A – Inventário dos Recursos da Plataforma](./docs/14_inventario.md) | Relação completa dos recursos provisionados no Azure, Azure Databricks, Azure Data Factory, Unity Catalog e GitHub, incluindo convenções de nomenclatura, finalidade e localização de cada artefato. |

---

# 📄 Documentação Técnica

Além da documentação modular disponível na pasta **docs**, o projeto disponibiliza um documento técnico consolidado contendo a arquitetura completa da solução, decisões de projeto, implementação dos pipelines, governança, segurança e boas práticas adotadas durante o desenvolvimento.

📄 **[Acessar documentação técnica](./docs/15_artigo_tecnico.md)**

---

# 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
|------------|------------|
| Cloud Platform | Microsoft Azure |
| Armazenamento | Azure Data Lake Storage Gen2 |
| Processamento | Azure Databricks |
| Engine | Apache Spark / PySpark |
| Formato de Dados | Delta Lake |
| Governança | Unity Catalog |
| Orquestração | Azure Data Factory |
| Gerenciamento de Segredos | Azure Key Vault |
| Identidade | Microsoft Entra ID |
| Versionamento | Git |
| Repositório | GitHub |
| CI/CD | GitHub Actions |
| Linguagens | Python, SQL |
| Consumo Analítico | Power BI |

---

# 📚 Documentação

Este repositório reúne toda a documentação necessária para compreender, implantar e evoluir a plataforma.

Entre os principais assuntos abordados estão:

- Arquitetura Lakehouse
- Arquitetura Medallion
- Provisionamento da infraestrutura Azure
- Organização do Azure Databricks
- Azure Data Lake Storage Gen2
- Unity Catalog
- Azure Data Factory
- Azure Key Vault
- Microsoft Entra ID
- Governança de Dados
- Segurança (RBAC, ACL e SCIM)
- Delta Lake
- Modelagem Dimensional
- Processamento distribuído com Apache Spark
- Integração com Power BI
- GitHub e GitHub Actions
- Boas práticas de Engenharia de Dados
- DataOps e automação de pipelines

---

# 📁 Estrutura do Repositório

```text
financial-statement-analytics-platform/
│
├── data/
│   ├── raw/
│   └── sample/
│
├── docs/
│
├── images/
│
├── notebooks/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── shared/
│
├── infrastructure/
│
├── pipelines/
│
├── scripts/
│
├── .github/
│   └── workflows/
│
├── .gitignore
├── LICENSE
└── README.md
```

O repositório está organizado para separar claramente os componentes da plataforma, facilitando a manutenção, a evolução da solução e a navegação entre infraestrutura, pipelines, notebooks e documentação técnica.
