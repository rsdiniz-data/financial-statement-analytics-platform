# 4. Modelagem Dimensional

## 🎯 Objetivo

Disponibilizar os dados financeiros em uma estrutura otimizada para consultas analíticas, utilizando um modelo dimensional que facilite a construção de indicadores, dashboards e relatórios.

A modelagem foi implementada na camada **Gold** da Arquitetura Medallion, utilizando **Delta Lake** para armazenamento e **Unity Catalog** para governança dos ativos analíticos.

---

## ⭐ Modelo Dimensional

A solução adota o padrão **Star Schema**, composto por uma tabela fato central e dimensões responsáveis pelo contexto analítico dos dados.

### 📦 Entidades

| Entidade        | Tipo     | Descrição                                        |
| --------------- | -------- | ------------------------------------------------ |
| `ft_resultado`  | Fato     | Valores financeiros da Demonstração do Resultado |
| `d_plano_conta` | Dimensão | Estrutura hierárquica do plano de contas         |
| `d_calendario`  | Dimensão | Atributos temporais para análises                |

📷 ![Modelo](../images/modelo_dimensional.png)

---

## 📊 Tabela Fato

### 📈 ft_resultado

Responsável por armazenar os indicadores financeiros utilizados nas análises.

### Principais características

* Valores financeiros da DRE
* Integração com a dimensão de contas
* Particionamento por ano
* Dados preparados para consultas analíticas

---

## 📚 Dimensões

### 📊 d_plano_conta

Disponibiliza a estrutura hierárquica do plano de contas utilizada nas análises financeiras.

**Principais atributos:**

* Código da conta
* Descrição
* Hierarquia da DRE (N1, N2 e N3)
* Código DRE
* Tipo de indicador

---

### 📅 d_calendario

Disponibiliza os atributos temporais utilizados nas análises e filtros de período.

**Principais atributos:**

* Data
* Ano
* Mês
* Número do mês

---

## 🔗 Relacionamentos

O modelo dimensional possui os seguintes relacionamentos:

```text
d_plano_conta (1) ──────► (N) ft_resultado

d_calendario  (1) ──────► (N) ft_resultado
```

Essa estrutura permite análises financeiras por conta contábil, período e diferentes níveis de agregação.

---

## 🧩 Camada Semântica

Além das tabelas físicas, a solução disponibiliza **views semânticas** para simplificar o consumo dos dados pelas ferramentas de Business Intelligence.

### Views

* `vw_d_plano_conta`
* `vw_ft_resultado`
* `vw_d_calendario`

As views abstraem detalhes técnicos do modelo físico e padronizam o acesso aos dados analíticos.

---

## 🚀 Benefícios

A modelagem dimensional proporciona:

* Estrutura otimizada para consultas analíticas
* Separação entre fatos e dimensões
* Melhor desempenho em agregações
* Reutilização das dimensões em diferentes análises
* Integração simplificada com Power BI
* Consistência das regras de negócio
* Escalabilidade para evolução da plataforma

---

## 🔗 Rastreabilidade

### 📄 Documentação relacionada

* 🏗️ [Arquitetura da Solução](./02_arquitetura.md)
* ⚙️ [Desenvolvimento do Projeto](./03_desenvolvimento.md)
* 📊 [Dicionário de Dados](./05_dicionario_dados.md)
* 📘 [Artigo Técnico](./17_artigo_tecnico.md)

### 💻 Notebooks

👉 [05_gold_d_plano_conta.py](../notebooks/gold/05_gold_d_plano_conta.py)

👉 [06_gold_ft_resultado.py](../notebooks/gold/06_gold_ft_resultado.py)

👉 [07_gold_d_calendario.py](../notebooks/gold/07_gold_d_calendario.py)
