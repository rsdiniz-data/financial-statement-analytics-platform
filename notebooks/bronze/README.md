# 🪵 Bronze (Raw Data)

A camada **Bronze** representa a primeira etapa da arquitetura **Medallion** da plataforma **Financial Statement Analytics Platform**.

Esta camada é responsável pela ingestão dos dados de origem, armazenamento inicial em formato **Delta Lake** no **Azure Data Lake Storage Gen2** e registro dos objetos no **Unity Catalog**, garantindo rastreabilidade, auditoria e preservação dos dados originais.

---

## 🎯 Objetivo

- Realizar a ingestão automatizada dos dados provenientes das fontes oficiais;
- Preservar os dados em sua estrutura original;
- Garantir rastreabilidade da origem e do processo de carga;
- Registrar metadados técnicos para auditoria e reprocessamento;
- Disponibilizar uma base confiável para processamento das camadas superiores.

---

## 📥 Fontes de Dados

Os dados são ingeridos a partir de arquivos financeiros utilizados na construção da plataforma analítica:

- **Plano de Contas**
- **Demonstração Financeira Padronizada (DFP)**

A origem dos arquivos está integrada ao ambiente corporativo através do **Microsoft SharePoint**, utilizando autenticação segura via **Microsoft Graph API**.

Fluxo de ingestão:

```text
SharePoint
     │
     ▼
Microsoft Graph API
     │
     ▼
Azure Databricks
     │
     ▼
Bronze Layer (Delta Lake)
     │
     ▼
Unity Catalog
```

---

## ⚙️ Processamento

Nesta camada são realizadas apenas transformações técnicas necessárias para disponibilização dos dados:

- Leitura dos arquivos de origem;
- Padronização inicial dos nomes das colunas;
- Conversão para estruturas Spark DataFrame;
- Inclusão de metadados de governança;
- Persistência em formato Delta Lake.

Não são aplicadas regras de negócio ou cálculos financeiros nesta etapa.

---

## 🏛️ Governança e Armazenamento

Características da implementação:

- **Processamento:** Azure Databricks + PySpark;
- **Armazenamento físico:** Azure Data Lake Storage Gen2;
- **Formato:** Delta Lake;
- **Catálogo:** Unity Catalog;
- **Segurança:** Azure Key Vault + Databricks Secrets;
- **Rastreabilidade:** Metadados técnicos de ingestão.

Metadados adicionados:

| Coluna | Descrição |
|---|---|
| `_source_file` | Arquivo de origem dos dados |
| `_ingestion_timestamp` | Data e hora da ingestão |

---

## 📓 Notebooks

Notebooks responsáveis pela ingestão da camada Bronze:

- [01_bronze_ingest_plano_conta.py](./01_bronze_ingest_plano_conta.py)
- [02_bronze_ingest_dfp.py](./02_bronze_ingest_dfp.py)

---

## 🔗 Integração com as Próximas Camadas

Após a ingestão, os dados Bronze são utilizados como fonte para os processos de tratamento e padronização da camada Silver.

Fluxo completo:

```text
Bronze
  │
  ▼
Silver
  │
  ▼
Gold
  │
  ▼
Power BI
```

---

## 📚 Documentação Relacionada

- 📄 [Arquitetura da Solução](../../docs/02_arquitetura.md)
- 📄 [Desenvolvimento do Projeto](../../docs/03_desenvolvimento.md)
- 📄 [Governança de Dados](../../docs/07_governanca.md)
- 📄 [Runbook de Implantação](../../docs/09_runbook_implantacao.md)
- 📄 [Artigo Técnico](../../docs/17_artigo_tecnico.md)

---

## 📌 Observação

A camada Bronze funciona como a fonte histórica confiável da plataforma, permitindo auditoria, rastreamento da origem dos dados e reprocessamento controlado das etapas posteriores do pipeline analítico.
