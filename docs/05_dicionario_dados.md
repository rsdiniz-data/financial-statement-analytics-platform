# 5. Dicionário de Dados

> Este dicionário apresenta as principais tabelas da camada **Gold**, disponibilizadas para consumo analítico por ferramentas de Business Intelligence e demais consumidores de dados.

---

## 📊 d_plano_conta

Dimensão responsável pela estrutura hierárquica do plano de contas da DRE, utilizada para classificação e análise dos indicadores financeiros.

| Coluna           | Tipo   | Descrição                                 | Relacionamentos                |
| ---------------- | ------ | ----------------------------------------- | ------------------------------ |
| `id_conta`       | STRING | Código identificador da conta contábil    | 1:N → `ft_resultado[id_conta]` |
| `descricao`      | STRING | Descrição da conta contábil               | -                              |
| `lancamento`     | LONG   | Indicador de conta analítica ou sintética | -                              |
| `calculado`      | LONG   | Indicador auxiliar para cálculos          | -                              |
| `n1`             | STRING | Primeiro nível da hierarquia da DRE       | -                              |
| `n2`             | STRING | Segundo nível da hierarquia da DRE        | -                              |
| `n3`             | STRING | Terceiro nível da hierarquia da DRE       | -                              |
| `cod_dre`        | STRING | Código de classificação da DRE            | -                              |
| `tipo_indicador` | LONG   | Classificação do indicador financeiro     | -                              |

### 🔗 Notebook

👉 [05_gold_d_plano_conta.py](../notebooks/gold/05_gold_d_plano_conta.py)

---

## 📈 ft_resultado

Tabela fato responsável por armazenar os valores financeiros da Demonstração do Resultado, servindo como base para consultas e indicadores analíticos.

| Coluna     | Tipo   | Descrição                              | Relacionamentos                 |
| ---------- | ------ | -------------------------------------- | ------------------------------- |
| `id_conta` | STRING | Conta contábil associada ao lançamento | N:1 → `d_plano_conta[id_conta]` |
| `data`     | DATE   | Data de referência do exercício        | N:1 → `d_calendario[data]`      |
| `valor`    | DOUBLE | Valor financeiro da DRE                | -                               |

### 🔗 Notebook

👉 [06_gold_ft_resultado.py](../notebooks/gold/06_gold_ft_resultado.py)

---

## 📅 d_calendario

Dimensão temporal utilizada para organização cronológica das análises e indicadores financeiros.

| Coluna    | Tipo   | Descrição                             | Relacionamentos            |
| --------- | ------ | ------------------------------------- | -------------------------- |
| `data`    | DATE   | Data utilizada nas análises temporais | 1:N → `ft_resultado[data]` |
| `ano`     | LONG   | Ano da data de referência             | -                          |
| `mes`     | STRING | Nome abreviado do mês                 | -                          |
| `mes_num` | LONG   | Número do mês para ordenação          | -                          |

### 🔗 Notebook

👉 [07_gold_d_calendario.py](../notebooks/gold/07_gold_d_calendario.py)

---

## 🔗 Rastreabilidade

### 📄 Documentação relacionada

* 🏗️ [Arquitetura da Solução](./02_arquitetura.md)
* ⭐ [Modelagem Dimensional](./04_modelagem_dimensional.md)
* 🖥️ [Operação da Plataforma](./06_operacao_plataforma.md)
* 📘 [Artigo Técnico](./15_artigo_tecnico.md)
