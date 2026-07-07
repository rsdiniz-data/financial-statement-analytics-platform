# 6. Operação da Plataforma

## 🎯 Objetivo

Descrever o funcionamento operacional da plataforma após a implantação, desde a execução dos pipelines até a disponibilização dos dados para consumo analítico.

---

## 🔄 Fluxo Operacional

O processamento é executado de forma automatizada pelo **Azure Data Factory**, que orquestra os notebooks do **Azure Databricks** seguindo a Arquitetura Medallion.

```text
Azure Data Factory
        │
        ▼
     Bronze
        │
        ▼
     Silver
        │
        ▼
      Gold
        │
        ▼
 Unity Catalog
        │
        ▼
Views Semânticas
        │
        ▼
    Power BI
```

Esse fluxo garante que os dados sejam processados e publicados de forma consistente para consumo analítico.

---

## 🪵 Processamento das Camadas

Cada camada possui uma responsabilidade específica dentro da plataforma.

| Camada     | Responsabilidade                                            |
| ---------- | ----------------------------------------------------------- |
| **Bronze** | Ingestão e armazenamento dos dados brutos                   |
| **Silver** | Limpeza, padronização e aplicação das regras de negócio     |
| **Gold**   | Modelagem dimensional e publicação das entidades analíticas |

Durante o processamento são executadas atividades de leitura, transformação, validação e gravação em tabelas Delta governadas.

---

## 📊 Publicação dos Dados

Após o processamento da camada Gold, os dados são disponibilizados em dois níveis:

### Camada Física

* Tabelas Delta Lake
* Azure Data Lake Storage Gen2

### Camada Lógica

* Tabelas registradas no Unity Catalog
* Views semânticas para consumo analítico

### Entidades Publicadas

* `d_plano_conta`
* `ft_resultado`
* `d_calendario`
* `vw_d_plano_conta`
* `vw_ft_resultado`
* `vw_d_calendario`

---

## 📈 Consumo Analítico

As ferramentas de Business Intelligence acessam os dados por meio das **views semânticas** publicadas no **Unity Catalog**, utilizando o **SQL Warehouse** do Azure Databricks.

Essa abordagem desacopla a camada de visualização da estrutura física do Data Lake, preservando as regras de negócio implementadas na plataforma.

---

## 📡 Monitoramento

A operação é monitorada pelo **Azure Data Factory**, permitindo acompanhar a execução dos pipelines e identificar possíveis falhas.

### Informações monitoradas

* Status das execuções
* Tempo de processamento
* Histórico dos pipelines
* Execução dos notebooks
* Mensagens de erro e reprocessamentos

Além disso, os notebooks registram logs operacionais para auxiliar auditorias e atividades de troubleshooting.

---

## 🔄 Atualização dos Dados

A atualização da plataforma ocorre automaticamente a cada execução do pipeline orquestrado pelo Azure Data Factory.

Cada execução realiza:

* Ingestão dos arquivos de origem
* Atualização das camadas Bronze, Silver e Gold
* Publicação das tabelas no Unity Catalog
* Atualização das views semânticas
* Disponibilização dos dados para o Power BI

---

## 🔗 Rastreabilidade

### 📄 Documentação relacionada

* ⚙️ [Desenvolvimento do Projeto](./03_desenvolvimento.md)
* 🔐 [Governança de Dados](./07_governanca.md)
* 🚀 [Runbook Operacional](./09_runbook_operacional.md)
* 🧯 [Troubleshooting](./12_troubleshooting.md)
* 📘 [Artigo Técnico](./15_artigo_tecnico.md)
