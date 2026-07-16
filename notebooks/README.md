# ☁️ Notebooks (Azure Databricks)

Esta pasta reúne os notebooks desenvolvidos em **PySpark** no **Azure Databricks**, responsáveis pela implementação dos pipelines de engenharia de dados da plataforma **Financial Statement Analytics Platform**.

A organização segue a **Arquitetura Medallion (Bronze, Silver e Gold)**, permitindo a separação das etapas de ingestão, tratamento e disponibilização dos dados para consumo analítico.

Todos os notebooks utilizam recursos nativos do ecossistema Azure, como **Azure Data Lake Storage Gen2**, **Delta Lake**, **Unity Catalog**, **Azure Key Vault** e **Databricks Secrets**, garantindo governança, rastreabilidade, segurança e escalabilidade.

---

# 🧱 Camadas da Arquitetura

## 🪵 Bronze (Raw Data)

Responsável pela ingestão dos dados provenientes das fontes de origem.

Principais atividades:

- Ingestão automatizada dos arquivos de origem;
- Persistência dos dados em formato Delta Lake;
- Inclusão de metadados de governança;
- Registro das tabelas no Unity Catalog;
- Preservação dos dados originais para auditoria e reprocessamento.

👉 [Ver camada Bronze](./bronze/README.md)

---

## 🥈 Silver (Trusted Data)

Responsável pelo tratamento técnico e padronização dos dados.

Principais atividades:

- Limpeza e padronização dos dados;
- Aplicação de regras técnicas e validações;
- Estruturação dos dados para modelagem analítica;
- Inclusão de metadados adicionais de rastreabilidade;
- Publicação de tabelas tratadas no Unity Catalog.

👉 [Ver camada Silver](./silver/README.md)

---

## 🥇 Gold (Business Data)

Responsável pela construção da camada analítica utilizada pelas ferramentas de Business Intelligence.

Principais atividades:

- Construção das dimensões e tabelas fato;
- Aplicação da modelagem dimensional;
- Criação de views semânticas para consumo analítico;
- Publicação das tabelas governadas no Unity Catalog;
- Disponibilização da camada para integração com Power BI.

👉 [Ver camada Gold](./gold/README.md)

---

# 🔄 Fluxo dos Dados

```text
SharePoint
      │
      ▼
Bronze (Raw)
      │
      ▼
Silver (Trusted)
      │
      ▼
Gold (Business)
      │
      ▼
Ferramentas de BI
```

---

# 🔗 Integração com a Documentação

Para compreender toda a arquitetura da solução e os pipelines implementados, consulte:

- 📄 [Arquitetura da Solução](../docs/02_arquitetura.md)
- 📄 [Desenvolvimento do Projeto](../docs/03_desenvolvimento.md)
- 📄 [Governança de Dados](../docs/07_governanca.md)
- 📄 [Runbook de Implantação](../docs/09_runbook_implantacao.md)
- 📄 [Artigo Técnico](../docs/17_artigo_tecnico.md)
