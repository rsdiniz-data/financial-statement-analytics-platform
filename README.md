# 📊 Financial Statement Analytics Platform

> Plataforma corporativa de Engenharia de Dados para processamento, governança e análise de demonstrações financeiras utilizando Microsoft Azure.

---

# 🧠 Visão Geral

O **Financial Statement Analytics Platform** é um projeto de Engenharia de Dados desenvolvido para demonstrar a construção de uma plataforma moderna de dados sobre o ecossistema Microsoft Azure, aplicando conceitos de Lakehouse, DataOps e Analytics Engineering.

A solução automatiza a ingestão, o processamento, a governança e a disponibilização de dados da **Demonstração do Resultado do Exercício (DRE)**, transformando arquivos Microsoft Excel armazenados no SharePoint Online em um modelo analítico dimensional otimizado para ferramentas de Business Intelligence.

Durante o processamento, os dados percorrem um pipeline estruturado segundo a **Arquitetura Medallion**, passando pelas camadas **Bronze**, **Silver** e **Gold**, onde são progressivamente refinados até se tornarem conjuntos de dados confiáveis, governados e preparados para análises corporativas.

Além dos pipelines de dados, o projeto demonstra a implementação de diversos componentes presentes em uma plataforma corporativa de dados, incluindo governança centralizada, controle de acesso baseado em papéis, gerenciamento seguro de credenciais, integração contínua, orquestração de pipelines, versionamento de código e recursos avançados do Delta Lake para garantir integridade, rastreabilidade e confiabilidade dos dados.

Toda a arquitetura foi concebida utilizando serviços gerenciados do Microsoft Azure, priorizando escalabilidade, segurança, reutilização de componentes e adoção das principais boas práticas de Engenharia de Dados.

---

> **Objetivo do projeto**
>
> Demonstrar, de ponta a ponta, a implementação de uma plataforma moderna de Engenharia de Dados para processamento de informações financeiras, utilizando serviços nativos do Microsoft Azure e seguindo as melhores práticas de arquitetura, governança, automação e DataOps.
