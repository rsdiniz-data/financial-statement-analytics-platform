# 2. Arquitetura da Solução

## 🎯 Objetivo

Construir uma arquitetura moderna de engenharia de dados no Databricks, garantindo escalabilidade, governança e rastreabilidade ao longo de todo o pipeline, desde a ingestão até o consumo analítico.

A solução segue o padrão **Medallion Architecture**, separando claramente as etapas de ingestão, tratamento e consumo de dados.

---

## 🧱 Visão Geral da Arquitetura

A arquitetura foi implementada em ambiente Databricks, utilizando:

- Data Lakehouse como base arquitetural  
- Delta Lake para armazenamento transacional  
- PySpark para processamento distribuído  
- Unity Catalog para governança e controle de acesso  
- Databricks Workflows para orquestração  

Fluxo principal:

Arquivos Excel → Bronze → Silver → Gold → Ferramentas de BI

📷 ![Arquitetura](../images/arquitetura.png)

---

## 🪵 Bronze (Raw Data)
### 🎯 Objetivo

Armazenar os dados brutos provenientes da fonte, garantindo rastreabilidade e possibilidade de reprocessamento.

### 📥 Características

- Ingestão de arquivos Excel
- Padronizações técnicas mínimas (nomes e estrutura)
- Inclusão de metadados de governança
- Persistência em Delta Lake (Volumes Databricks)
- Camada sem regras de negócio

### 📦 Artefatos

- `plano_conta`
- `dfp`

---

## 🥈 Silver (Trusted Data)
### 🎯 Objetivo

Transformar os dados brutos em estruturas confiáveis, padronizadas e analíticas.

### 🔧 Características

- Limpeza e padronização dos dados
- Aplicação de regras de qualidade
- Estruturação hierárquica do plano de contas
- Transformação de dados financeiros (unpivot)
- Criação de atributos derivados
- Preparação para modelagem analítica

### 📦 Artefatos

- `plano_conta (tratado)`
- `resultado (analítico e temporal)`

---

## 🥇 Gold (Business Data)
### 🎯 Objetivo

Disponibilizar dados prontos para consumo analítico, organizados em modelo dimensional.

### 📊 Características

- Modelagem dimensional (Star Schema)
- Publicação em tabelas Delta governadas
- Criação de views semânticas para BI
- Otimização para consultas analíticas
- Integração direta com ferramentas de visualização

### 📦 Tabelas

- `d_plano_conta`
- `ft_resultado`
- `d_calendario`

---

## ⭐ Modelo Dimensional

A camada Gold segue um modelo dimensional estruturado:

- **Fato:** `ft_resultado`
- **Dimensão:** `d_plano_conta`
- **Dimensão:** `d_calendario`

---

## 🔗 Relacionamentos

d_plano_conta (1) → (N) ft_resultado  
d_calendario  (1) → (N) ft_resultado  

📷 ![Modelo](../images/modelo_dimensional.png)

---

## 🔄 Pipeline de Dados

Fluxo completo da solução:

Arquivos Excel → Bronze → Silver → Gold → Ferramentas de BI

⚙️ Características

- Orquestração via Databricks Workflows
- Execução sequencial entre camadas
- Processamento reprodutível e escalável
- Separação clara entre ingestão e transformação
- Publicação automatizada das tabelas Gold

---

## 🔗 Rastreabilidade
### 🪵 Bronze
- [01_bronze_ingest_plano_conta.py](../notebooks/bronze/01_bronze_ingest_plano_conta.py)
- [02_bronze_ingest_dfp.py](../notebooks/bronze/02_bronze_ingest_dfp.py)

### 🥈 Silver
- [03_silver_ingest_plano_conta.py](../notebooks/silver/03_silver_ingest_plano_conta.py)
- [04_silver_ingest_resultado.py](../notebooks/silver/04_silver_ingest_resultado.py)

### 🥇 Gold
- [05_gold_ingest_d_plano_conta.py](../notebooks/gold/05_gold_ingest_d_plano_conta.py)
- [06_gold_ingest_ft_resultado.py](../notebooks/gold/06_gold_ingest_ft_resultado.py)
- [07_gold_ingest_d_calendario.py](../notebooks/gold/07_gold_ingest_d_calendario.py)
