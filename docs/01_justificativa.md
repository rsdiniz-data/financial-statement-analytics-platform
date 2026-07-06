# 1. Justificativa do Projeto

## 🎯 Problema

Empresas frequentemente disponibilizam demonstrativos financeiros em arquivos Excel, criando desafios relacionados à governança, padronização e escalabilidade analítica.

Nesse cenário, surgem limitações como:

- Dependência de arquivos manuais para consumo analítico  
- Dificuldade de rastreabilidade e governança dos dados  
- Acoplamento entre fonte, transformação e visualização  
- Reprocessamentos complexos e pouco escaláveis  
- Baixa padronização entre camadas analíticas  
- Limitação para expansão do pipeline e inclusão de novos períodos  

Além disso, soluções baseadas apenas em ferramentas de visualização tendem a concentrar transformações no BI, reduzindo eficiência operacional e reutilização dos dados.

---

## 💡 Solução

Desenvolver uma arquitetura moderna de engenharia de dados utilizando Databricks e padrão Medallion (Bronze, Silver e Gold), separando claramente ingestão, transformação e consumo analítico.

A solução implementada contempla:

- Ingestão centralizada de arquivos financeiros Excel  
- Armazenamento em arquitetura Lakehouse  
- Processamento distribuído com PySpark  
- Estruturação em camadas Bronze, Silver e Gold  
- Persistência transacional utilizando Delta Lake  
- Governança via Unity Catalog  
- Orquestração automatizada com Databricks Workflows  
- Disponibilização analítica através de views semânticas para BI  

Essa abordagem aumenta governança, rastreabilidade, escalabilidade e reutilização dos dados, além de preparar a solução para evolução futura e integração com múltiplos cenários analíticos.

---

## 🔗 Rastreabilidade

- 🏗️ [Arquitetura Medallion](./02_arquitetura.md)  
- ⚙️ [Desenvolvimento técnico do pipeline](./03_desenvolvimento.md)  
- 📘 [Artigo técnico completo](./06_artigo_tecnico.md)  
- 📊 [Dicionário de dados](./04_dicionario_dados.md)  

### 📂 Notebooks do Projeto

#### Bronze
- 🪵 `01_bronze_ingest_plano_conta`
- 🪵 `02_bronze_ingest_dfp`

#### Silver
- 📥 `03_silver_ingest_plano_conta`
- 📊 `04_silver_ingest_resultado`

#### Gold
- 🧱 `05_gold_ingest_d_plano_conta`
- 🔄 `06_gold_ingest_ft_resultado`
- 📅 `07_gold_ingest_d_calendario`
