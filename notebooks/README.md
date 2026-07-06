# ☁️ Notebooks (Data Lake)

Esta pasta organiza os notebooks do projeto seguindo o padrão Medallion (Bronze, Silver e Gold).

O objetivo é estruturar o pipeline de dados em camadas independentes, garantindo governança, rastreabilidade e preparação para consumo analítico.

---

## 🧱 Camadas

### 🪵 Bronze (Raw Data)

- Ingestão dos dados brutos
- Persistência inicial no Data Lake
- Preservação da origem dos dados

👉 [Ver camada Bronze](./bronze/README.md)

---

### 🥈 Silver (Trusted Data)

- Padronização e limpeza dos dados
- Aplicação de regras técnicas
- Estruturação para modelagem analítica

👉 [Ver camada Silver](./silver/README.md)

---

### 🥇 Gold (Business Data)

- Construção das entidades analíticas
- Modelagem dimensional
- Publicação para consumo em BI

👉 [Ver camada Gold](./gold/README.md)

---

## 🔗 Integração com Documentação

Para visão completa da arquitetura e do pipeline:

👉 [Desenvolvimento do Projeto](../docs/03_desenvolvimento.md)
