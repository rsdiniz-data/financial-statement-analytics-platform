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
