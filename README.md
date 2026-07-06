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
| 📄 [01 - Visão Geral](./docs/01_visao_geral.md) | Contexto, objetivos e benefícios da plataforma |
| 🏗️ [02 - Arquitetura da Solução](./docs/02_arquitetura.md) | Arquitetura lógica e componentes da plataforma |
| ☁️ [03 - Infraestrutura Azure](./docs/03_infraestrutura_azure.md) | Recursos provisionados no Microsoft Azure |
| ⚙️ [04 - Azure Databricks](./docs/04_databricks.md) | Organização do Workspace, Catálogos e Notebooks |
| 🗄️ [05 - Data Lake](./docs/05_data_lake.md) | Estrutura de armazenamento e camadas Bronze, Silver e Gold |
| 📊 [06 - Modelo Dimensional](./docs/06_modelo_dimensional.md) | Modelagem analítica e entidades da camada Gold |
| 🔄 [07 - Azure Data Factory](./docs/07_data_factory.md) | Orquestração dos pipelines |
| 🔐 [08 - Segurança e Governança](./docs/08_seguranca_governanca.md) | Unity Catalog, RBAC, ACL, SCIM e Key Vault |
| ⚡ [09 - Delta Lake](./docs/09_delta_lake.md) | ACID, Time Travel, Version History e Restore |
| 🚀 [10 - CI/CD](./docs/10_cicd.md) | GitHub, GitHub Actions e versionamento |
| 📈 [11 - Power BI](./docs/11_power_bi.md) | Integração com ferramentas analíticas |
| 📖 [12 - Guia de Implantação](./docs/12_implantacao.md) | Provisionamento do ambiente |
| 📑 [13 - Inventário da Plataforma](./docs/13_inventario.md) | Recursos e convenções utilizadas |

---

# 📄 Documentação Técnica

Além da documentação modular disponível na pasta **docs**, o projeto disponibiliza um documento técnico consolidado contendo toda a arquitetura da solução, decisões de projeto, implementação dos pipelines e boas práticas adotadas durante o desenvolvimento.

📄 **[Acessar documentação técnica](./docs/14_artigo_tecnico.md)**

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
