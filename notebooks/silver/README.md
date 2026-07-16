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

- [03_silver_transform_plano_conta.py](./03_silver_transform_plano_conta.py)  
- [04_silver_transform_resultado.py](./04_silver_transform_resultado.py)  

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

finance.silver.plano_conta


---

### 📊 Resultado Financeiro (DRE)

- Leitura dos dados financeiros da camada Bronze
- Tratamento de períodos e referências temporais
- Transformação de estrutura horizontal para vertical (unpivot)
- Conversão e padronização dos valores financeiros
- Preparação dos dados para relacionamento com Plano de Contas

Resultado:

finance.silver.resultado


---

## 🧱 Características da Camada Silver

A camada Silver representa o nível de dados confiáveis (*Trusted Data*) da plataforma.

Principais características:

- Persistência em formato Delta Lake
- Controle de qualidade dos dados
- Estruturas padronizadas
- Dados preparados para regras de negócio
- Registro e governança através do Unity Catalog

---

## 🔗 Integração

Detalhes sobre arquitetura, transformações e fluxo de dados:

👉 [Desenvolvimento do Projeto](../../docs/03_desenvolvimento.md)

---

## 📌 Observação

A camada Silver atua como ponte entre os dados brutos da Bronze e as entidades analíticas da Gold.

Seu objetivo é garantir que os dados financeiros estejam tratados, padronizados e confiáveis antes da aplicação das regras de negócio e disponibilização para ferramentas de BI.
