# 🥈 Silver (Trusted Data)

Camada responsável pelo tratamento, padronização e estruturação dos dados analíticos.

---

## 🎯 Objetivo

- Limpar e padronizar os dados  
- Aplicar regras técnicas e estruturais  
- Organizar os dados para modelagem analítica  
- Preparar as entidades para consumo na camada Gold  

---

## 📓 Notebooks

- [03_silver_ingest_plano_conta.py](./03_silver_ingest_plano_conta.py)  
- [04_silver_ingest_resultado.py](./04_silver_ingest_resultado.py)  

---

## ⚙️ Processamento

Nesta camada são aplicadas:

- Limpeza e padronização dos dados  
- Conversão de tipos de dados  
- Estruturação hierárquica do plano de contas  
- Transformação de dados wide → long (unpivot)  
- Tratamento de valores financeiros  
- Preparação para joins e modelagem dimensional  

---

## 🔗 Integração

Detalhes do pipeline e das transformações:

👉 [Desenvolvimento do Projeto](../../docs/03_desenvolvimento.md)
