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

Os dados publicados na camada **Gold** são disponibilizados por meio do **Unity Catalog** e consumidos diretamente pelo **Power BI**, preservando as regras de negócio implementadas durante o processamento.

### ✅ Benefícios

* Modelo dimensional centralizado
* Views semânticas para BI
* Dados governados e padronizados
* Separação entre processamento e visualização
* Reutilização por múltiplos dashboards

























# 3. Desenvolvimento do Projeto

## 🔄 Pipeline

1. Ingestão (Excel → Bronze)
2. Tratamento (Silver - PySpark)
3. Modelagem (Gold - PySpark)
4. Consumo (Ferramentas de BI)

---

## 📥 Ingestão (Bronze)

Responsável por:

* Leitura dos arquivos financeiros em Excel
* Persistência dos dados brutos no Data Lake
* Padronização técnica inicial
* Inclusão de metadados de rastreabilidade

🔗 Rastreabilidade:  
👉 [01_bronze_ingest_plano_conta.py](../notebooks/bronze/01_bronze_ingest_plano_conta.py)  
👉 [02_bronze_ingest_dfp.py](../notebooks/bronze/02_bronze_ingest_dfp.py)

---

## 🥈 Transformações (Silver - PySpark)

### 📊 PlanoConta

🔗 Script:
👉 [03_silver_ingest_plano_conta.py](../notebooks/silver/03_silver_ingest_plano_conta.py)

Responsável por:

* Padronização dos dados
* Estruturação hierárquica da DRE
* Criação dos níveis N1, N2 e N3
* Classificação financeira
* Preparação da dimensão contábil

---

### 📈 Resultado

🔗 Script:
👉 [04_silver_ingest_resultado.py](../notebooks/silver/04_silver_ingest_resultado.py)

Regras aplicadas:

* Unpivot de colunas de exercícios
* Conversão de valores financeiros
* Padronização estrutural
* Criação de atributos temporais
* Preparação para integração analítica

---

## 🥇 Modelagem (Gold - PySpark)

### 📊 dPlanoConta

🔗 Script:
👉 [05_gold_ingest_d_plano_conta.py](../notebooks/gold/05_gold_ingest_d_plano_conta.py)

Regras:

* Construção da dimensão contábil
* Publicação no Unity Catalog
* Criação de view semântica
* Estruturação hierárquica da DRE

---

### 📈 ftResultado

🔗 Script:
👉 [06_gold_ingest_ft_resultado.py](../notebooks/gold/06_gold_ingest_ft_resultado.py)

Regras:

* Join com dimensão dPlanoConta
* Filtro de contas analíticas
* Estruturação da tabela fato
* Particionamento por ano
* Publicação governada

---

### 📅 dCalendario

🔗 Script:
👉 [07_gold_ingest_d_calendario.py](../notebooks/gold/07_gold_ingest_d_calendario.py)

Regras:

* Geração automática do calendário
* Criação de atributos temporais
* Publicação no Unity Catalog
* Exposição de view semântica

---

## ⚙️ Orquestração

Pipeline executado de forma encadeada:

1. Ingestão Bronze
2. Processamento Silver
3. Publicação Gold

Execução pode ser realizada via notebooks, workflows ou jobs agendados.

---

## 📊 Consumo

Ferramentas de BI conectadas à camada Gold governada no Unity Catalog, utilizando dados tratados, modelados e preparados para consumo analítico.
