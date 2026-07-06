# 7. Governança de Dados

> A plataforma adota mecanismos de governança para garantir segurança, controle de acesso, rastreabilidade e integridade dos dados ao longo de todo o pipeline analítico.

---

## 👥 Gerenciamento de Identidades

O acesso aos recursos é centralizado no **Microsoft Entra ID**, com sincronização automática de grupos para o **Azure Databricks** via **SCIM**.

### Grupos de acesso

| Grupo | Responsabilidade |
|--------|------------------|
| `data_engineers` | Desenvolvimento e administração da plataforma |
| `bi_analysts` | Consumo das tabelas da camada Gold |
| `business_users` | Consumo das views semânticas |

---

## 🗂️ Governança com Unity Catalog

O **Unity Catalog** centraliza o gerenciamento dos ativos de dados da plataforma.

### Recursos governados

- Catálogo
- Schemas
- Tabelas
- Views
- Permissões
- Metadados

### Entidades publicadas

- `d_plano_conta`
- `ft_resultado`
- `d_calendario`
- `vw_d_plano_conta`
- `vw_ft_resultado`
- `vw_d_calendario`

---

## 🔒 Controle de Acesso (RBAC e ACL)

A plataforma utiliza **Role-Based Access Control (RBAC)** e **Access Control Lists (ACL)** para aplicar o princípio do menor privilégio.

| Grupo | Permissões |
|--------|------------|
| `data_engineers` | Administração completa da plataforma |
| `bi_analysts` | Leitura das tabelas Gold |
| `business_users` | Leitura das views semânticas |

🔗 Script:

👉 [98_governance_rbac_acl.py](../notebooks/governance/98_governance_rbac_acl.py)

---

## 🛡️ Integridade com Delta Lake

O **Delta Lake** fornece recursos que garantem consistência, auditoria e recuperação das informações.

### Funcionalidades implementadas

- Transações ACID
- Histórico de versões (History)
- Time Travel
- Restore Table
- Auditoria das alterações

🔗 Script:

👉 [99_delta_lake_acid_demo.py](../notebooks/governance/99_delta_lake_acid_demo.py)

---

## 📊 Arquitetura de Governança

A estratégia de governança integra identidade, armazenamento, catálogo e controle de acesso.

```text
Microsoft Entra ID
        │
        ▼
Grupos Corporativos
        │
        ▼
SCIM Provisioning
        │
        ▼
Azure Databricks
        │
        ▼
Unity Catalog
        │
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
 ▼              ▼              ▼
Bronze        Silver         Gold
                              │
                              ▼
                      Views Semânticas
                              │
                              ▼
                         Power BI
```

A estratégia de permissões segue a seguinte organização:

```text
data_engineers
│
├── Bronze
├── Silver
├── Gold
├── CREATE
├── MODIFY
└── SELECT

bi_analysts
│
├── Gold Tables
└── SELECT

business_users
│
├── Semantic Views
└── SELECT
```

---

## ✅ Benefícios

- Controle de acesso centralizado
- Governança unificada dos ativos de dados
- Segregação de responsabilidades
- Auditoria das alterações
- Recuperação de versões anteriores
- Maior segurança e rastreabilidade
- Preparação para ambientes corporativos escaláveis
