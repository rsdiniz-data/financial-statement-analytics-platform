# 8. DevOps, DataOps e Versionamento

> A plataforma adota práticas modernas de **DevOps**, **DataOps** e **versionamento de código** para garantir rastreabilidade, padronização, automação e qualidade durante todo o ciclo de desenvolvimento da solução.

---

## 🌿 Versionamento do Código

Todo o código-fonte do projeto é mantido em um repositório **Git** hospedado no **GitHub**, permitindo controle de versões, rastreabilidade das alterações e evolução contínua da plataforma.

### Artefatos versionados

- Documentação técnica
- Notebooks Databricks
- Workflows do GitHub Actions
- Diagramas e imagens da solução
- Scripts auxiliares
- Arquivos de configuração

### Benefícios

- Histórico completo das alterações
- Facilidade para auditoria
- Colaboração entre desenvolvedores
- Recuperação de versões anteriores
- Evolução contínua da plataforma

---

## 🚀 Práticas de DevOps

A solução incorpora práticas de DevOps para padronizar o desenvolvimento, reduzir atividades manuais e aumentar a qualidade das entregas.

### Práticas implementadas

- Versionamento do código com Git
- Repositório centralizado no GitHub
- Organização padronizada do projeto
- Documentação integrada ao código-fonte
- Automação das validações com GitHub Actions

### Benefícios

- Maior padronização do projeto
- Redução de erros operacionais
- Facilidade de manutenção
- Integração entre documentação e código
- Maior previsibilidade durante a evolução da plataforma

---

## 🔄 Práticas de DataOps

Os pipelines foram desenvolvidos seguindo princípios de DataOps, promovendo maior confiabilidade, repetibilidade e governança dos processos de Engenharia de Dados.

### Práticas implementadas

- Arquitetura Medallion
- Organização dos pipelines por camadas
- Notebooks especializados por responsabilidade
- Processamento automatizado
- Monitoramento das execuções
- Governança de dados
- Rastreabilidade das cargas
- Padronização das transformações

### Benefícios

- Maior qualidade dos dados
- Processos reprodutíveis
- Facilidade para manutenção
- Escalabilidade da solução
- Operação simplificada da plataforma

---

## 🔁 Continuous Integration (CI)

O projeto utiliza **GitHub Actions** para executar automaticamente um pipeline de **Integração Contínua (Continuous Integration)** sempre que ocorre um **push** ou uma **Pull Request** direcionada para a branch principal do repositório.

Durante a execução do workflow são realizadas validações automáticas da estrutura da solução.

### Validações executadas

- Estrutura do repositório
- Documentação técnica
- Organização dos notebooks
- Diretório de imagens
- Estrutura dos workflows

Também são apresentadas estatísticas sobre a organização dos notebooks das camadas **Bronze**, **Silver**, **Gold** e **Governança**, facilitando a validação da arquitetura da plataforma.

---

## 📦 Empacotamento da Solução

Após a conclusão das validações, o workflow gera automaticamente um pacote contendo os principais artefatos do projeto.

### Artefatos incluídos

- Documentação técnica
- Notebooks
- Imagens
- Arquivos principais do repositório

### Benefícios

- Organização dos artefatos
- Facilidade para distribuição da solução
- Preparação para futuras publicações
- Padronização das entregas

---

## 🚀 Continuous Delivery (CD)

Como etapa final do workflow, é executada uma simulação do processo de publicação da plataforma, representando a sequência lógica de disponibilização dos principais componentes da arquitetura.

### Componentes simulados

- Azure Data Lake Storage Gen2
- Azure Databricks
- Unity Catalog
- Azure Data Factory
- Delta Lake
- Camada semântica para ferramentas de Business Intelligence

Embora o projeto não realize a implantação automática da infraestrutura em Azure, essa etapa demonstra como um processo de **Continuous Delivery** pode ser estruturado para suportar futuras evoluções da plataforma.

---

## ⚙️ GitHub Actions

A automação do repositório é realizada através do **GitHub Actions**, responsável pela execução do workflow de validação, empacotamento e simulação do pipeline de entrega.

### Estrutura

```text
.github/
└── workflows/
    └── ci-cd-financial-platform.yml
```

### Jobs implementados

| Job | Objetivo |
|------|----------|
| `validate-platform` | Validação da estrutura do repositório, documentação, notebooks e imagens |
| `package-platform` | Empacotamento dos principais artefatos do projeto |
| `publish-platform` | Simulação da publicação da plataforma e dos principais serviços Azure |
| `pipeline-summary` | Consolidação dos resultados e apresentação do resumo da execução |

### Fluxo do workflow

```text
Git Push / Pull Request
            │
            ▼
     GitHub Actions
            │
            ▼
 validate-platform
            │
            ▼
 package-platform
            │
            ▼
 publish-platform
            │
            ▼
 pipeline-summary
```

---

## 📊 Pipeline Automatizado

O workflow implementado demonstra uma abordagem moderna para validação e organização de projetos de Engenharia de Dados.

### Principais funcionalidades

- Validação automática da estrutura do projeto
- Verificação da documentação técnica
- Organização dos notebooks
- Empacotamento dos artefatos
- Simulação do processo de publicação
- Consolidação dos resultados da execução

---

## ✅ Práticas Demonstradas

Ao longo do workflow automatizado são evidenciadas as seguintes competências e práticas:

- Git
- GitHub
- GitHub Actions
- Continuous Integration (CI)
- Continuous Delivery (CD)
- DevOps
- DataOps
- Versionamento de código
- Documentação como código
- Automação de validações
- Empacotamento de artefatos
- Organização de projetos de Engenharia de Dados

---

## 📈 Benefícios

A adoção conjunta de práticas de **DevOps**, **DataOps** e **versionamento** proporciona diversos benefícios para a plataforma.

- Maior qualidade das entregas
- Padronização do desenvolvimento
- Automação das validações
- Rastreabilidade completa das alterações
- Organização dos artefatos do projeto
- Facilidade para manutenção e evolução contínua
- Preparação para pipelines corporativos de CI/CD
- Demonstração de boas práticas modernas de Engenharia de Dados
