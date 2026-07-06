# 12. Troubleshooting

Esta seção reúne os principais problemas operacionais da plataforma **Financial Statement Analytics Platform**, suas causas mais comuns e ações corretivas recomendadas.

---

## 🎯 Objetivo

Padronizar o diagnóstico de falhas na plataforma, reduzindo o tempo de resolução de incidentes e facilitando a manutenção do ambiente de dados.

---

## ☁️ Infraestrutura

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Falha no acesso ao ADLS | Permissões ou identidade incorreta | Validar Managed Identity, Access Connector e permissões no Storage |
| Erro ao acessar Key Vault | Secret Scope mal configurado | Verificar integração entre Databricks Secret Scope e Key Vault |
| Cluster não inicia | Falta de recursos ou configuração inválida | Validar tipo de cluster, quotas e configuração do workspace |

---

## 🗂️ Unity Catalog

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Erro ao consultar tabelas | Schema ou catálogo inexistente | Validar criação do catálogo e schemas (bronze/silver/gold) |
| Acesso negado | Permissões insuficientes | Revisar GRANTs aplicados aos grupos |
| External Location indisponível | Storage Credential inválida | Validar credencial e mapeamento no Unity Catalog |

---

## 🧪 Execução de Notebooks

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Falha na ingestão | Arquivo de origem indisponível | Validar SharePoint e credenciais do Entra ID |
| Erro ao gravar Delta | Caminho ou permissão inválida | Verificar estrutura do ADLS e permissões de escrita |
| Falha no registro no catálogo | Schema inexistente | Confirmar criação do schema no Unity Catalog |

---

## ⚙️ Orquestração (ADF)

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Pipeline falha na primeira atividade | Linked Service inválido | Testar conexão ADF ↔ Databricks |
| Notebook não executa | Caminho incorreto | Validar configuração da atividade Notebook |
| Pipeline interrompe execução | Dependências incorretas | Revisar encadeamento das atividades |
| Trigger não executa | Trigger desativado | Publicar e validar estado do trigger |

---

## 🔐 Governança

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Usuários não aparecem no Databricks | SCIM não configurado | Validar sincronização no Entra ID |
| Permissões não aplicadas | GRANT não executado | Reexecutar notebook de governança |
| Usuário sem acesso | Grupo incorreto | Validar associação ao grupo correto |

---

## 📊 Power BI / Consumo

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Falha de conexão | SQL Warehouse desligado | Iniciar o Warehouse |
| Erro de autenticação | Token expirado | Gerar novo PAT |
| Views não aparecem | Permissão insuficiente | Validar acesso ao Unity Catalog |
| Dados desatualizados | Pipeline não executado | Executar ADF e atualizar dataset |

---

## 🧊 Delta Lake

| Problema | Possível causa | Ação recomendada |
|----------|----------------|------------------|
| Sobrescrita incorreta | Overwrite indevido | Usar Time Travel ou RESTORE TABLE |
| Divergência de dados | Múltiplas versões | Consultar DESCRIBE HISTORY |
| Necessidade de auditoria | Alterações históricas | Usar VERSION AS OF |

---

## 📋 Localização de Logs

| Componente | Informações disponíveis |
|------------|------------------------|
| Azure Data Factory | Execução de pipeline, status, erros |
| Azure Databricks | Logs de notebooks e cluster |
| Unity Catalog | Auditoria de permissões e metadados |
| Delta Lake | Histórico de versões e operações |

---

## 🧭 Boas práticas de diagnóstico

Ordem recomendada para análise de incidentes:

1. Verificar execução no Azure Data Factory  
2. Analisar logs no Azure Databricks  
3. Validar dados de origem  
4. Conferir permissões no Unity Catalog  
5. Verificar tabelas Delta  
6. Testar views semânticas  
7. Consultar `DESCRIBE HISTORY` quando necessário  

---

## 🎯 Resultado esperado

Uma abordagem padronizada de troubleshooting que permite:

- rápida identificação de falhas  
- redução do tempo de resolução  
- maior previsibilidade operacional  
- estabilidade da plataforma analítica  
