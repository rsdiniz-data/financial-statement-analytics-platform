# 🛡️ Governance

Camada responsável pela implementação dos mecanismos de governança, segurança e confiabilidade da plataforma de dados.

Nesta etapa são demonstrados recursos corporativos relacionados ao controle de acesso, gerenciamento de permissões, governança centralizada através do Unity Catalog e funcionalidades avançadas do Delta Lake, evidenciando práticas adotadas em ambientes modernos de Engenharia de Dados.

---

## 🎯 Objetivo

- Demonstrar governança centralizada utilizando Unity Catalog
- Implementar controle de acesso baseado em papéis (RBAC)
- Aplicar permissões utilizando ACLs
- Simular cenários corporativos de autorização de usuários e grupos
- Demonstrar recursos avançados do Delta Lake
- Evidenciar transações ACID
- Demonstrar Time Travel e versionamento de dados
- Validar mecanismos de auditoria e rastreabilidade

---

## 📓 Notebooks

- [98_governance_rbac_acl.py](./98_governance_rbac_acl.py)
- [99_delta_lake_acid_demo.py](./99_delta_lake_acid_demo.py)

---

# 🔐 Governança de Dados

A governança da plataforma é implementada utilizando os recursos nativos do Azure Databricks e Unity Catalog.

---

## 📘 Governança com Unity Catalog

Responsável pelo gerenciamento centralizado dos ativos de dados da plataforma.

### Processos aplicados

- Criação do catálogo corporativo
- Organização em Schemas (Bronze, Silver e Gold)
- Gerenciamento centralizado dos objetos
- Controle de permissões sobre tabelas e views
- Governança unificada dos ativos de dados

### Objetos governados

```text
finance.bronze.*
finance.silver.*
finance.gold.*
```

---

## 👥 Controle de Acesso (RBAC e ACL)

Responsável pela definição das permissões de acesso aos recursos da plataforma.

### Processos aplicados

- Criação de grupos de segurança
- Concessão de privilégios utilizando GRANT
- Revogação de permissões utilizando REVOKE
- Controle de acesso em nível de catálogo
- Controle de acesso em nível de schema
- Controle de acesso em nível de tabela
- Aplicação do princípio do menor privilégio (Least Privilege)

### Recursos demonstrados

- Unity Catalog
- RBAC (Role-Based Access Control)
- ACL (Access Control Lists)
- Privilégios sobre tabelas
- Privilégios sobre schemas
- Privilégios sobre catálogos

---

# 🧪 Recursos Avançados do Delta Lake

O notebook **99_delta_lake_acid_demo.py** demonstra funcionalidades avançadas do Delta Lake utilizadas em ambientes corporativos.

---

## 🔄 Transações ACID

São realizadas operações controladas de escrita e atualização sobre tabelas Delta para demonstrar as propriedades ACID.

### Funcionalidades demonstradas

- Atomicidade
- Consistência
- Isolamento
- Durabilidade

---

## 🕒 Time Travel

Demonstra a capacidade de consultar versões anteriores de uma tabela Delta.

### Processos aplicados

- Consulta por número de versão
- Consulta por timestamp
- Recuperação de estados anteriores
- Comparação entre versões

---

## 🗂️ Versionamento de Dados

Cada alteração realizada na tabela gera automaticamente uma nova versão do conjunto de dados.

### Recursos demonstrados

- Histórico de versões
- Evolução dos dados
- Auditoria das alterações
- Recuperação de versões anteriores

---

## 📜 Histórico de Operações

Utilização do comando:

```sql
DESCRIBE HISTORY finance.gold.ft_resultado
```

para consulta do histórico completo de modificações realizadas na tabela Delta.

São apresentadas informações como:

- versão
- operação executada
- usuário responsável
- timestamp
- métricas da operação

---

# 🧱 Características da Camada Governance

Esta camada demonstra os principais recursos corporativos relacionados à governança de dados e segurança da informação.

Principais características:

- Unity Catalog
- Governança centralizada
- Controle de acesso baseado em papéis (RBAC)
- ACLs para objetos de dados
- Auditoria e Data Lineage
- Gerenciamento de privilégios
- Delta Lake ACID Transactions
- Time Travel
- Versionamento automático
- Histórico de operações
- Rastreabilidade completa dos dados

---

# 🔗 Integração

Detalhes sobre arquitetura, governança e implementação podem ser encontrados na documentação da plataforma:

- 👉 [Arquitetura da Solução](../../docs/02_arquitetura.md)
- 👉 [Desenvolvimento do Projeto](../../docs/03_desenvolvimento.md)
- 👉 [Governança de Dados](../../docs/07_governanca.md)
- 👉 [Artigo Técnico](../../docs/15_artigo_tecnico.md)

---

# 📌 Observação

Os notebooks desta pasta possuem finalidade demonstrativa e evidenciam recursos normalmente encontrados em plataformas corporativas de Engenharia de Dados.

Além da implementação das políticas de governança e segurança através do Unity Catalog, também são apresentados mecanismos avançados do Delta Lake, como transações ACID, versionamento automático, Time Travel e histórico de operações, reforçando aspectos fundamentais de confiabilidade, auditoria e rastreabilidade em arquiteturas modernas baseadas em Lakehouse.
