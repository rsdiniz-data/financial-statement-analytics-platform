# 🥇 Gold (Business Data)

Camada responsável pela modelagem e disponibilização dos dados para consumo analítico.

---

## 🎯 Objetivo

- Estruturar dados no modelo dimensional (Star Schema)
- Aplicar regras de negócio da DRE
- Disponibilizar dados prontos para consumo analítico
- Publicar entidades governadas no Unity Catalog

---

## 📓 Notebooks

- [05_gold_ingest_d_plano_conta.py](./05_gold_ingest_d_plano_conta.py)
- [06_gold_ingest_ft_resultado.py](./06_gold_ingest_ft_resultado.py)
- [07_gold_ingest_d_calendario.py](./07_gold_ingest_d_calendario.py)
  
---

## ⚙️ Processamento

Nesta camada são aplicadas:

- Criação de dimensões e tabelas fato
- Integração entre fatos e dimensões
- Aplicação de regras de negócio financeiras
- Filtragem de contas analíticas
- Criação de calendário analítico
- Publicação em Delta Lake e Unity Catalog

---

## ⭐ Modelo

- Dimensão: dPlanoConta
- Fato: ftResultado
- Dimensão temporal: dCalendario

---

## 🔗 Integração

Detalhes completos:

👉 [Desenvolvimento](../../docs/03_desenvolvimento.md)
