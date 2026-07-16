# 📖 Glossário Técnico

Este glossário reúne os principais conceitos, tecnologias, serviços e termos utilizados ao longo da documentação da **Financial Statement Analytics Platform**.

Seu objetivo é servir como material de apoio para facilitar a compreensão da arquitetura da solução, dos componentes implementados e das tecnologias empregadas durante o desenvolvimento da plataforma de Engenharia de Dados.

Sempre que aplicável, cada definição apresenta também sua utilização dentro do projeto.

---

# A

## 🔹 ACID (Atomicity, Consistency, Isolation and Durability)

Conjunto de propriedades que garantem a confiabilidade das transações em bancos de dados.

No **Delta Lake**, as propriedades ACID asseguram que todas as operações de escrita ocorram de forma consistente, mesmo diante de falhas ou execuções simultâneas.

### Aplicação no projeto

As funcionalidades ACID são demonstradas no notebook:

- `99_delta_lake_acid_demo.py`

São apresentados recursos como:

- Version History
- Time Travel
- Restore Table
- Controle transacional das tabelas Delta

---

## 🔹 Access Control List (ACL)

Mecanismo utilizado para controlar permissões de acesso sobre objetos específicos da plataforma, como:

- Catálogos
- Schemas
- Tabelas
- Views
- Volumes

As ACLs complementam o modelo RBAC, permitindo um controle granular das permissões concedidas aos usuários e grupos.

### Aplicação no projeto

As permissões são implementadas no Unity Catalog utilizando comandos SQL como:

```sql
GRANT SELECT ON TABLE finance.gold.ft_resultado TO `bi_analysts`;
```

O gerenciamento das permissões é demonstrado no notebook:

- `98_governance_rbac_acl.py`

---

## 🔹 Apache Spark

Framework distribuído para processamento de grandes volumes de dados.

O Apache Spark permite executar operações paralelas sobre conjuntos massivos de dados, oferecendo alta escalabilidade e desempenho.

Entre suas principais características estão:

- Processamento distribuído
- Computação em memória
- APIs para múltiplas linguagens
- Integração nativa com Delta Lake

### Aplicação no projeto

Todo o processamento das camadas Bronze, Silver e Gold é realizado utilizando Apache Spark através do Azure Databricks.

---

## 🔹 Apache Parquet

Formato colunar de armazenamento otimizado para processamento analítico.

Entre suas principais vantagens destacam-se:

- Alta taxa de compressão
- Leitura seletiva de colunas
- Excelente desempenho em consultas analíticas

### Aplicação no projeto

Embora as tabelas sejam persistidas em formato **Delta Lake**, internamente o Delta utiliza arquivos Apache Parquet como mecanismo físico de armazenamento.

---

## 🔹 Azure Data Factory (ADF)

Serviço de integração e orquestração de dados da Microsoft Azure.

Permite construir pipelines responsáveis por coordenar a execução de diferentes atividades de processamento.

### Aplicação no projeto

O Azure Data Factory é responsável por:

- executar os notebooks do Azure Databricks;
- controlar a sequência do pipeline;
- monitorar execuções;
- registrar logs operacionais;
- automatizar o processamento da plataforma.

---

## 🔹 Azure Data Lake Storage Gen2 (ADLS Gen2)

Serviço de armazenamento escalável da Microsoft Azure utilizado como Data Lake da solução.

O ADLS Gen2 oferece:

- armazenamento distribuído;
- integração nativa com Spark;
- controle de acesso;
- alta disponibilidade;
- suporte a grandes volumes de dados.

### Aplicação no projeto

Armazena todas as camadas da arquitetura:

- Bronze
- Silver
- Gold

Também hospeda o diretório utilizado pelo Unity Catalog.

---

## 🔹 Azure Databricks

Plataforma analítica baseada em Apache Spark destinada ao desenvolvimento de pipelines de dados, processamento distribuído e Analytics Engineering.

O Azure Databricks oferece recursos como:

- notebooks colaborativos;
- clusters Spark gerenciados;
- integração com Azure Data Lake;
- Unity Catalog;
- Delta Lake;
- SQL Warehouse.

### Aplicação no projeto

Todos os notebooks da plataforma foram desenvolvidos e executados no Azure Databricks.

---

## 🔹 Azure Key Vault

Serviço da Microsoft Azure destinado ao armazenamento seguro de credenciais, chaves criptográficas, certificados e segredos.

O serviço permite eliminar credenciais armazenadas diretamente no código-fonte.

### Aplicação no projeto

Os notebooks recuperam automaticamente informações sensíveis, como:

- Client ID
- Client Secret
- Tenant ID
- Storage Account
- SharePoint IDs
- Unity Catalog

Todas essas informações são obtidas por meio da integração entre Databricks Secrets e Azure Key Vault.

---

# B

## 🔹 Bronze Layer

Primeira camada da Arquitetura Medallion.

Seu objetivo é preservar os dados provenientes das fontes praticamente em seu formato original, realizando apenas transformações técnicas mínimas.

Entre elas:

- padronização dos nomes das colunas;
- inclusão de metadados;
- armazenamento em Delta Lake.

### Aplicação no projeto

Nesta plataforma, a camada Bronze realiza a ingestão automatizada dos arquivos:

- PlanoContas.xlsx
- DFP.xlsx

Os dados são persistidos no schema:

```text
finance.bronze
```

---

## 🔹 Business Intelligence (BI)

Conjunto de técnicas, metodologias e ferramentas destinadas à transformação de dados em informações para apoio à tomada de decisão.

Ferramentas de BI normalmente consomem modelos dimensionais e indicadores consolidados.

### Aplicação no projeto

A camada Gold disponibiliza tabelas e views preparadas para consumo por ferramentas de Business Intelligence, como:

- Microsoft Power BI
- Azure Databricks SQL Warehouse
- outras ferramentas compatíveis com SQL.

---

# C

## 🔹 Catálogo (Unity Catalog)

Estrutura lógica responsável pela organização dos ativos de dados dentro do Azure Databricks.

O catálogo agrupa:

- schemas;
- tabelas;
- views;
- volumes;
- permissões.

### Aplicação no projeto

A solução utiliza o catálogo corporativo:

```text
finance
```

Organizado nos seguintes schemas:

- bronze
- silver
- gold

---

## 🔹 CI/CD (Continuous Integration / Continuous Delivery)

Conjunto de práticas voltadas à automação do desenvolvimento, validação e entrega de software.

Essas práticas reduzem atividades manuais e aumentam a qualidade das entregas.

### Aplicação no projeto

O pipeline automatizado implementado com GitHub Actions executa:

- validação da estrutura do repositório;
- validação da documentação;
- organização dos notebooks;
- empacotamento dos artefatos;
- simulação do processo de publicação da plataforma.

---

## 🔹 Cluster

Conjunto de recursos computacionais utilizado para executar aplicações distribuídas no Apache Spark.

No Azure Databricks, o cluster é responsável por fornecer capacidade de processamento para os notebooks.

### Aplicação no projeto

Todos os notebooks das camadas Bronze, Silver, Gold e Governança são executados sobre um cluster Spark configurado no Azure Databricks.

---

# D

## 🔹 Data Lake

Repositório centralizado utilizado para armazenar dados estruturados, semiestruturados e não estruturados.

O Data Lake permite armazenar grandes volumes de informação preservando a granularidade dos dados.

### Aplicação no projeto

A camada física da plataforma é implementada utilizando:

- Azure Data Lake Storage Gen2.

---

## 🔹 Data Lineage

Capacidade de rastrear toda a trajetória dos dados, desde sua origem até seu consumo analítico.

Inclui informações como:

- origem;
- transformações;
- destino;
- responsáveis;
- histórico de processamento.

### Aplicação no projeto

O projeto implementa Data Lineage através de:

- metadados de ingestão;
- Unity Catalog;
- logs operacionais;
- histórico das tabelas Delta.

---

## 🔹 DataOps

Conjunto de práticas destinadas à automação, monitoramento, padronização e governança dos pipelines de dados.

O objetivo é tornar o ciclo de vida dos dados mais confiável, repetível e escalável.

### Aplicação no projeto

As principais práticas de DataOps demonstradas são:

- Arquitetura Medallion;
- automação dos pipelines;
- notebooks especializados;
- governança dos dados;
- monitoramento operacional;
- versionamento;
- rastreabilidade das cargas.

---

## 🔹 Delta Lake

Camada de armazenamento transacional construída sobre o Apache Parquet.

O Delta Lake adiciona recursos avançados como:

- transações ACID;
- Time Travel;
- Version History;
- Restore Table;
- otimizações de desempenho;
- controle de concorrência.

### Aplicação no projeto

Todas as tabelas das camadas Bronze, Silver e Gold são persistidas em formato Delta Lake.

---

## 🔹 DevOps

Conjunto de práticas que integra desenvolvimento de software e operações por meio da automação dos processos de entrega.

O DevOps busca aumentar a qualidade das entregas, reduzir atividades manuais e facilitar a evolução contínua das aplicações.

### Aplicação no projeto

O projeto demonstra práticas de DevOps por meio de:

- Git;
- GitHub;
- GitHub Actions;
- integração contínua;
- organização do repositório;
- documentação versionada;
- automação de validações.

# G

## 🔹 Git

Sistema distribuído de controle de versões utilizado para registrar, rastrear e gerenciar alterações realizadas em arquivos ao longo do desenvolvimento de um projeto.

O Git permite que diferentes desenvolvedores trabalhem simultaneamente sobre a mesma base de código, mantendo o histórico completo de alterações.

Entre suas principais funcionalidades destacam-se:

- versionamento distribuído;
- criação de branches;
- controle de merges;
- histórico de alterações;
- recuperação de versões anteriores.

### Aplicação no projeto

Todo o código-fonte da plataforma é versionado utilizando Git, incluindo:

- documentação técnica;
- notebooks Databricks;
- workflows do GitHub Actions;
- imagens e diagramas;
- scripts auxiliares;
- arquivos de configuração.

---

## 🔹 GitHub

Plataforma de hospedagem de repositórios Git utilizada para armazenamento, colaboração e gerenciamento do código-fonte.

Além do versionamento, o GitHub oferece recursos como:

- Pull Requests;
- Issues;
- GitHub Actions;
- Wiki;
- gerenciamento de releases;
- controle de permissões.

### Aplicação no projeto

O projeto é mantido em um repositório GitHub, que centraliza:

- documentação completa da solução;
- notebooks desenvolvidos em PySpark;
- workflow de CI/CD;
- diagramas da arquitetura;
- estrutura da plataforma.

---

## 🔹 GitHub Actions

Serviço de automação integrado ao GitHub utilizado para implementação de pipelines de Integração Contínua (CI) e Entrega Contínua (CD).

Os workflows são definidos por arquivos YAML armazenados na pasta:

```text
.github/workflows/
```

### Aplicação no projeto

O projeto implementa um workflow responsável por:

- validar a estrutura do repositório;
- verificar a documentação técnica;
- validar a organização dos notebooks;
- gerar um pacote da solução;
- simular o processo de publicação da plataforma;
- apresentar um resumo da execução do pipeline.

---

# L

## 🔹 Lakehouse

Arquitetura moderna de dados que combina características de um Data Lake com funcionalidades tradicionalmente encontradas em Data Warehouses.

Essa abordagem permite unir:

- armazenamento escalável;
- processamento distribuído;
- governança centralizada;
- consultas analíticas de alto desempenho.

### Aplicação no projeto

Toda a plataforma foi desenvolvida seguindo o conceito de Lakehouse, utilizando:

- Azure Data Lake Storage Gen2;
- Azure Databricks;
- Delta Lake;
- Unity Catalog.

---

## 🔹 Medallion Architecture

Arquitetura de processamento de dados baseada em múltiplas camadas de refinamento progressivo.

Cada camada possui responsabilidades específicas durante o pipeline.

### Camadas utilizadas

| Camada | Finalidade |
|----------|------------|
| Bronze | Ingestão dos dados |
| Silver | Tratamento e padronização |
| Gold | Disponibilização para consumo analítico |

### Aplicação no projeto

Toda a solução segue a Arquitetura Medallion para garantir:

- separação de responsabilidades;
- qualidade dos dados;
- governança;
- reutilização das entidades analíticas.

---

# M

## 🔹 Microsoft Entra ID

Serviço de gerenciamento de identidades e controle de acesso da Microsoft Azure.

É responsável pela autenticação de usuários, aplicações e serviços corporativos.

Entre seus principais recursos destacam-se:

- autenticação centralizada;
- gerenciamento de grupos;
- autenticação multifator (MFA);
- App Registrations;
- integração com serviços Azure.

### Aplicação no projeto

O Microsoft Entra ID é utilizado para:

- autenticação da Microsoft Graph API;
- gerenciamento dos grupos corporativos;
- integração com Azure Databricks;
- sincronização de usuários via SCIM.

---

## 🔹 Microsoft Graph API

Interface REST disponibilizada pela Microsoft para acesso programático aos serviços do Microsoft 365.

Permite consultar e manipular recursos como:

- SharePoint Online;
- OneDrive;
- Microsoft Teams;
- Outlook;
- usuários e grupos.

### Aplicação no projeto

Os notebooks da camada Bronze utilizam a Microsoft Graph API para realizar automaticamente o download dos arquivos armazenados no SharePoint Online.

A autenticação é realizada utilizando OAuth 2.0.

---

## 🔹 Modelo Dimensional

Modelo de organização de dados voltado para consultas analíticas e construção de indicadores de negócio.

Normalmente é composto por:

- tabelas fato;
- tabelas dimensão;
- relacionamentos otimizados para análise.

### Aplicação no projeto

A camada Gold implementa um modelo dimensional baseado em Star Schema contendo:

- dimensão Plano de Contas;
- dimensão Calendário;
- fato Resultado Financeiro.

Esse modelo serve como base para construção de dashboards e indicadores financeiros.

---

## 🔹 Microsoft SharePoint Online

Serviço colaborativo da Microsoft utilizado para armazenamento e compartilhamento de documentos corporativos.

Além da interface web, seus arquivos podem ser acessados programaticamente através da Microsoft Graph API.

### Aplicação no projeto

O SharePoint Online representa a principal fonte de dados da plataforma.

Os arquivos:

- PlanoContas.xlsx
- DFP.xlsx

são consumidos automaticamente durante a ingestão da camada Bronze, eliminando a necessidade de uploads manuais.
