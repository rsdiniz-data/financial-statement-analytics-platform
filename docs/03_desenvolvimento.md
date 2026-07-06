# 3. Desenvolvimento do Projeto

## 🔄 Fluxo de Desenvolvimento

O desenvolvimento da plataforma foi estruturado em etapas independentes, seguindo a Arquitetura Medallion e as boas práticas de Engenharia de Dados.

1. Ingestão dos dados (Bronze)
2. Transformação e padronização (Silver)
3. Modelagem dimensional (Gold)
4. Orquestração dos pipelines
5. Consumo analítico no Power BI

---

## 📥 Ingestão (Bronze)

Responsável por:

* Leitura automatizada dos arquivos Excel no SharePoint Online
* Persistência dos dados brutos em tabelas Delta
* Padronização técnica de colunas
* Inclusão de metadados de ingestão e rastreabilidade

### 🔗 Notebooks

👉 [01_bronze_ingest_plano_conta.py](../notebooks/bronze/01_bronze_ingest_plano_conta.py)

👉 [02_bronze_ingest_dfp.py](../notebooks/bronze/02_bronze_ingest_dfp.py)

---

## 🥈 Transformações (Silver)

### 📊 Plano de Contas

Responsável por:

* Padronização dos dados
* Estruturação hierárquica do plano de contas
* Classificação das contas contábeis
* Preparação para modelagem dimensional

### 🔗 Notebook

👉 [03_silver_transform_plano_conta.py](../notebooks/silver/03_silver_transform_plano_conta.py)

---

### 📈 Resultado Financeiro

Responsável por:

* Limpeza e padronização dos dados
* Transformação Unpivot
* Conversão de valores financeiros
* Criação de atributos temporais
* Preparação da tabela fato

### 🔗 Notebook

👉 [04_silver_transform_resultado.py](../notebooks/silver/04_silver_transform_resultado.py)

---

## 🥇 Modelagem (Gold)

### 📊 Dimensão Plano de Contas

Responsável por:

* Construção da dimensão contábil
* Publicação no Unity Catalog
* Criação de view semântica

### 🔗 Notebook

👉 [05_gold_d_plano_conta.py](../notebooks/gold/05_gold_d_plano_conta.py)

---

### 📈 Fato Resultado

Responsável por:

* Construção da tabela fato
* Integração com as dimensões
* Particionamento para otimização
* Publicação da camada analítica

### 🔗 Notebook

👉 [06_gold_ft_resultado.py](../notebooks/gold/06_gold_ft_resultado.py)

---

### 📅 Dimensão Calendário

Responsável por:

* Geração automática do calendário
* Criação de atributos temporais
* Publicação no Unity Catalog
* Disponibilização para análises temporais

### 🔗 Notebook

👉 [07_gold_d_calendario.py](../notebooks/gold/07_gold_d_calendario.py)

---

## 🔐 Governança

Além dos pipelines de dados, foram desenvolvidos notebooks específicos para demonstrar recursos de governança e confiabilidade da plataforma.

### 🔗 Notebooks

👉 [98_governance_rbac_acl.py](../notebooks/governance/98_governance_rbac_acl.py)

👉 [99_delta_lake_acid_demo.py](../notebooks/governance/99_delta_lake_acid_demo.py)

---

## ⚙️ Orquestração

A execução dos notebooks é automatizada pelo **Azure Data Factory**, garantindo o processamento sequencial entre as camadas da arquitetura.

Fluxo de execução:

```text
01_bronze_ingest_plano_conta
        ↓
02_bronze_ingest_dfp
        ↓
03_silver_transform_plano_conta
        ↓
04_silver_transform_resultado
        ↓
05_gold_d_plano_conta
        ↓
06_gold_ft_resultado
        ↓
07_gold_d_calendario
```

### 🚀 Características

* Execução automatizada dos notebooks
* Dependência entre etapas
* Agendamento por gatilhos (Triggers)
* Monitoramento centralizado das execuções
* Reprocessamento em caso de falhas

---

## 📊 Consumo Analítico

Os dados publicados na camada **Gold** são disponibilizados por meio do **Unity Catalog** e consumidos diretamente por **Ferramentas de BI**, preservando as regras de negócio implementadas durante o processamento.

### ✅ Benefícios

* Modelo dimensional centralizado
* Views semânticas para BI
* Dados governados e padronizados
* Separação entre processamento e visualização
* Reutilização por múltiplos dashboards
