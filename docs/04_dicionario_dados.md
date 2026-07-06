# 4. Dicionário de Dados

> Este dicionário descreve as tabelas da camada Gold, preparadas para consumo analítico por ferramentas de visualização e outros consumidores de dados.

---

## 📊 d_plano_conta

| Coluna            | Tipo    | Descrição                                      | Relacionamentos                     |
|-------------------|----------|------------------------------------------------|------------------------------------|
| `id_conta`        | STRING   | Código identificador da conta contábil         | 1:N → `ft_resultado[id_conta]`      |
| `descricao`       | STRING   | Nome da conta contábil                         | -                                  |
| `lancamento`      | LONG     | Indicador de conta analítica ou sintética      | -                                  |
| `calculado`       | LONG     | Indicador auxiliar de cálculo                  | -                                  |
| `n1`              | STRING   | Grupo principal da DRE                         | -                                  |
| `n2`              | STRING   | Subgrupo contábil                              | -                                  |
| `n3`              | STRING   | Conta analítica detalhada                      | -                                  |
| `cod_dre`          | STRING   | Código principal da DRE                        | -                                  |
| `tipo_indicador`   | LONG     | Classificação financeira da conta              | -                                  |

🔗 Script:  
👉 [05_gold_ingest_d_plano_conta.py](../notebooks/gold/05_gold_ingest_d_plano_conta.py)

---

## 📈 ft_Resultado

| Coluna        | Tipo     | Descrição                              | Relacionamentos                     |
|----------------|----------|----------------------------------------|------------------------------------|
| `id_conta`     | STRING   | Conta contábil associada ao valor      | N:1 → `d_plano_conta[id_conta]`      |
| `data`         | DATE     | Data de referência financeira          | N:1 → `d_calendario[data]`          |
| `valor`        | DOUBLE   | Valor monetário da DRE                 | -                                  |

🔗 Script:  
👉 [06_gold_ingest_ft_resultado.py](../notebooks/gold/06_gold_ingest_ft_resultado.py)

---

## 📅 d_calendario

| Coluna       | Tipo    | Descrição                               | Relacionamentos                |
|--------------|----------|-----------------------------------------|--------------------------------|
| `data`       | DATE     | Data utilizada nas análises temporais   | 1:N → `ft_resultado[data]`      |
| `ano`        | LONG     | Ano da data                             | -                              |
| `mes`        | STRING   | Nome abreviado do mês                   | -                              |
| `mes_num`    | LONG     | Número do mês para ordenação            | -                              |

🔗 Script:  
👉 [07_gold_ingest_d_calendario.py](../notebooks/gold/07_gold_ingest_d_calendario.py)
