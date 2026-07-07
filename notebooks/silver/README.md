# 🥈 Silver (Trusted Data)

Camada responsável pelo tratamento, padronização e enriquecimento dos dados financeiros provenientes da camada Bronze.

Nesta etapa, os dados brutos são transformados em estruturas confiáveis e preparadas para consumo analítico e construção das entidades corporativas da camada Gold.

---

## 🎯 Objetivo

- Garantir qualidade e consistência dos dados financeiros
- Aplicar transformações técnicas e regras estruturais
- Padronizar atributos para processamento analítico
- Preparar entidades confiáveis para modelagem dimensional
- Disponibilizar dados tratados para publicação na camada Gold

---

## 📥 Origem dos Dados

Os dados são consumidos exclusivamente da camada Bronze:

- Dados do Plano de Contas
- Dados financeiros da Demonstração de Resultado (DFP / DRE)

A leitura é realizada através de tabelas Delta Lake registradas no Unity Catalog.

---

## 📓 Notebooks

- [03_silver_ingest_plano_conta.py](./03_silver_ingest_plano_conta.py)  
- [04_silver_ingest_resultado.py](./04_silver_ingest_resultado.py)  

---

## ⚙️ Processamento

Nesta camada são aplicadas transformações técnicas necessárias para criação das estruturas analíticas:

### 📘 Plano de Contas

- Leitura da tabela Bronze
- Padronização dos atributos contábeis
- Tratamento da hierarquia de contas
- Normalização dos campos de classificação
- Preparação da dimensão contábil

Resultado:
