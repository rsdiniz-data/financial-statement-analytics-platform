# 11. Padrão de Nomenclatura

> A plataforma adota convenções de nomenclatura para padronizar a identificação dos recursos de infraestrutura, processamento, governança e consumo analítico.

---

## 🎯 Objetivos

A padronização tem como objetivos:

- Facilitar a identificação dos recursos
- Padronizar a organização da plataforma
- Simplificar administração e manutenção
- Apoiar automações e implantação
- Melhorar a legibilidade da arquitetura

---

## 🏗️ Convenção Geral

Formato adotado:

```text
<prefixo>-<domínio>-<projeto>-<ambiente>
```

Exemplos:

| Recurso | Exemplo |
|----------|----------|
| Resource Group | `grp-finance-dev` |
| Databricks Workspace | `ws-finance-databricks-dev` |
| Azure Data Factory | `adf-finance-dev-001` |
| Cluster | `clu-finance-dre-dev` |
| Key Vault | `kv-finance-dev-001` |

---

## 🔤 Prefixos dos Recursos

| Prefixo | Recurso |
|----------|----------|
| `grp` | Resource Group |
| `st` | Storage Account |
| `app` | App Registration |
| `ac` | Access Connector |
| `ws` | Databricks Workspace |
| `adf` | Azure Data Factory |
| `clu` | Cluster |
| `cat` | Unity Catalog |
| `sch` | Schema |
| `el` | External Location |
| `kv` | Key Vault |
| `ss` | Secret Scope |
| `ls` | Linked Service |
| `pl` | Pipeline |
| `trg` | Trigger |
| `sqlw` | SQL Warehouse |
| `repo` | Repositório GitHub |
| `gha` | GitHub Actions |

---

## 🗄️ Objetos do Data Lakehouse

### Tabelas Dimensionais

Prefixo:

```text
d_
```

Exemplos:

- `d_plano_conta`
- `d_calendario`

### Tabelas Fato

Prefixo:

```text
ft_
```

Exemplo:

- `ft_resultado`

### Views Semânticas

Prefixo:

```text
vw_
```

Exemplos:

- `vw_d_plano_conta`
- `vw_ft_resultado`
- `vw_d_calendario`

### Schemas

- `bronze`
- `silver`
- `gold`

---

## 📒 Convenção dos Notebooks

Formato:

```text
NN_<camada>_<objeto>
```

Exemplos:

- `01_bronze_ingest_plano_conta`
- `02_bronze_ingest_dfp`
- `03_silver_transform_plano_conta`
- `04_silver_transform_resultado`
- `05_gold_d_plano_conta`
- `06_gold_ft_resultado`
- `07_gold_d_calendario`
- `98_governance_rbac_acl`
- `99_delta_lake_acid_demo`

---

## ⚙️ Convenção da Orquestração

| Recurso | Exemplo |
|----------|----------|
| Linked Service | `ls-databricks-dre` |
| Pipeline | `pl-orchestrator-dre` |
| Trigger | `trg-pl-orchestrator-dre` |

As atividades do pipeline seguem a nomenclatura dos notebooks correspondentes.

---

## 👥 Convenção de Governança

| Grupo | Finalidade |
|--------|------------|
| `data_engineers` | Administração e desenvolvimento |
| `bi_analysts` | Consumo das tabelas Gold |
| `business_users` | Consumo das views semânticas |

---

## 📋 Inventário da Plataforma

A relação completa dos recursos provisionados está disponível em:

👉 [Apêndice A – Inventário dos Recursos da Plataforma](./14_inventario.md)
