# selenium-restassured-cucumber-kiro-github-actions

![CI](https://github.com/aline-nory/selenium-restassured-cucumber-kiro-github-actions/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Maven](https://img.shields.io/badge/Maven-3.9-blue?logo=apachemaven)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Allure](https://img.shields.io/badge/Report-Allure-orange)

Framework profissional de automacao de testes UI + API com arquitetura enterprise, pipeline CI/CD e relatorios Allure.

---

## Arquitetura

```
                 Feature (.feature)
                        |
                   Step Layer
                        |
           -------------------------
           |                       |
       UI Layer               API Layer
           |                       |
     Page Objects           Services / Client
           |                       |
      Selenium              REST Assured
           |
     Infrastructure
           |
  Config / Drivers / Logs / Reports / CI
```

---

## Destaques

- **Separacao UI / API** — steps, features e camadas isoladas por tipo
- **Injecao de Dependencia** — PicoContainer (uma instancia por cenario)
- **Page Object Pattern** — BasePage + heranca por funcionalidade
- **Service + Client** — camada de negocio separada do HTTP
- **Models + Builders** — objetos tipados com Faker para dados dinamicos
- **Configuracao por ambiente** — arquivos .properties por ambiente (dev/hml)
- **Logging corporativo** — SLF4J + Logback (console + arquivo)
- **Excecoes customizadas** — FrameworkException com contexto claro
- **Allure Report** — request/response anexados automaticamente
- **Screenshots configuraveis** — failure_only ou always
- **CI/CD** — GitHub Actions com Chrome headless
- **JSON Schema validation** — contrato de API garantido

---

## Estrutura do projeto

```
src/test/java/
├── runners/
│   └── TestRunner.java
├── steps/
│   ├── ui/
│   │   └── LoginSteps.java
│   └── api/
│       └── PostSteps.java
├── pages/
│   ├── base/
│   │   └── BasePage.java
│   └── login/
│       └── LoginPage.java
├── api/
│   ├── clients/
│   │   └── RestClient.java
│   ├── services/
│   │   └── PostService.java
│   ├── models/
│   │   └── PostRequest.java
│   └── builders/
│       └── PostBuilder.java
├── hooks/
│   ├── UiHooks.java
│   └── ApiHooks.java
├── config/
│   ├── Environment.java
│   └── ConfigReader.java
├── drivers/
│   ├── DriverFactory.java
│   └── DriverManager.java
├── utils/
│   ├── LogUtils.java
│   ├── JsonUtils.java
│   └── ScreenshotUtils.java
└── exceptions/
    └── FrameworkException.java

src/test/resources/
├── features/
│   ├── ui/
│   │   └── login.feature
│   └── api/
│       └── posts.feature
├── environments/
│   ├── dev.properties
│   └── hml.properties
├── payloads/
│   └── posts/
│       ├── create-post.json
│       └── update-post.json
├── schemas/
│   └── post-schema.json
├── testdata/
│   └── login.json
└── logback.xml
```

---

## Comandos

```bash
mvn test                                    # todos os cenarios
mvn test -Dcucumber.filter.tags="@smoke"    # smoke
mvn test -Dcucumber.filter.tags="@api"      # apenas API
mvn test -Dcucumber.filter.tags="@ui"       # apenas UI
mvn test -Denvironment=hml                  # ambiente HML
mvn allure:serve                            # relatorio Allure
```

---

## Stack

| Tecnologia | Versao | Funcao |
|---|---|---|
| Java | 8 | Linguagem |
| Maven | 3.9 | Build |
| Selenium | 3.141.59 | Automacao UI |
| Cucumber | 7.18 | BDD |
| JUnit | 4.13 | Runner |
| REST Assured | 4.5.1 | Automacao API |
| Allure | 2.24 | Relatorios |
| PicoContainer | 7.18 | Injecao de dependencia |
| SLF4J + Logback | 1.7/1.2 | Logging |
| JavaFaker | 1.0.2 | Dados dinamicos |
| GitHub Actions | - | CI/CD |

---

## Pipeline CI/CD

O GitHub Actions executa automaticamente em cada push:
1. Java 8 + Chrome + ChromeDriver configurados
2. `mvn test` com `CI=true` (headless)
3. Allure Report publicado no GitHub Pages
4. Artefatos Cucumber disponiveis

---

## Configuracao por ambiente

```
resources/environments/
├── dev.properties    <- padrao
└── hml.properties    <- mvn test -Denvironment=hml
```

Hierarquia de credenciais:
1. `dev.properties` — credenciais de teste (commitavel)
2. Variaveis de ambiente — CI/CD (GitHub Secrets)
3. Secrets Manager — producao (nunca no codigo)

---

## Documentacao completa

Consulte o arquivo [DOCUMENTATION.md](DOCUMENTATION.md) para o guia tecnico completo com 42 capitulos cobrindo toda a arquitetura, implementacao e boas praticas.
