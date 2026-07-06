# 🪵 Bronze (Raw Data)

Camada responsável pela ingestão e armazenamento dos dados brutos no Data Lake.

---

## 🎯 Objetivo

- Preservar os dados na forma original  
- Garantir rastreabilidade da origem  
- Servir como base para processamento nas camadas superiores  

---

## 📥 Ingestão

Os dados são ingeridos a partir de arquivos financeiros utilizados no projeto:

- Plano de Contas  
- Demonstração de Resultado (DRE / DFP)  

A persistência é realizada em formato Delta Lake dentro do Data Lake.

---

## ⚙️ Processamento

Nesta camada:

- Não há aplicação de regras de negócio  
- Transformações são mínimas  
- O foco está na leitura, padronização inicial e persistência dos dados brutos  

---

## 📓 Notebooks

- [01_bronze_ingest_plano_conta.py](./01_bronze_ingest_plano_conta.py)  
- [02_bronze_ingest_dfp.py](./02_bronze_ingest_dfp.py)
  
---

## 🔗 Integração

A ingestão e arquitetura do pipeline são descritas em:

👉 [Desenvolvimento do Projeto](../../docs/03_desenvolvimento.md)

---

## 📌 Observação

A camada Bronze representa a origem confiável dos dados dentro da arquitetura Medallion, permitindo reprocessamentos e rastreabilidade completa ao longo do pipeline analítico.
