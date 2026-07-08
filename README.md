# selenium-restassured-cucumber-kiro-github-actions

![CI](https://github.com/aline-nory/selenium-restassured-cucumber-kiro-github-actions/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Allure](https://img.shields.io/badge/Report-Allure-orange)

Framework de automação de testes Web e API com Cucumber BDD, pipeline CI/CD e relatórios Allure.

---

## Tecnologias

| Tecnologia | Versão |
|---|---|
| Java | 8 |
| Maven | 3.9 |
| Selenium WebDriver | 3.141.59 |
| Cucumber | 7.18.0 |
| JUnit | 4.13.2 |
| REST Assured | 4.5.1 |
| Allure Report | 2.24.0 |
| PicoContainer | 7.18.0 |
| SLF4J + Logback | 1.7 / 1.2 |
| JavaFaker | 1.0.2 |
| GitHub Actions | — |

---

## Pré-requisitos

- JDK 8 instalado (`java -version`)
- Maven 3.8+ instalado (`mvn -version`)
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome

---

## Como executar

```bash
# Todos os testes
mvn test

# Apenas API
mvn test -Dcucumber.filter.tags="@api"

# Apenas UI
mvn test -Dcucumber.filter.tags="@ui"

# Apenas smoke
mvn test -Dcucumber.filter.tags="@smoke"

# Outro ambiente
mvn test -Denvironment=hml
```

---

## Relatórios

```bash
# Allure (abre no navegador)
mvn allure:serve

# Cucumber HTML
target/cucumber-reports/cucumber.html

# Log de execução
target/test-execution.log
```

---

## Estrutura

```
src/test/java/
├── runners/TestRunner.java
├── steps/
│   ├── ui/LoginSteps.java
│   └── api/PostSteps.java
├── pages/
│   ├── base/BasePage.java
│   └── login/LoginPage.java
├── api/
│   ├── clients/RestClient.java
│   ├── services/PostService.java
│   ├── models/PostRequest.java
│   └── builders/PostBuilder.java
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
│   ├── ui/login.feature
│   └── api/posts.feature
├── environments/
│   ├── dev.properties
│   └── hml.properties
├── payloads/posts/
│   ├── create-post.json
│   └── update-post.json
├── schemas/post-schema.json
└── logback.xml
```

---

## Tags

| Tag | Descrição |
|---|---|
| `@ui` | Testes de interface (abre Chrome) |
| `@api` | Testes de API (sem navegador) |
| `@smoke` | Cenários críticos |

---

## Ambientes

```bash
# Padrão: dev
mvn test

# Homologação
mvn test -Denvironment=hml
```

Configurações em `src/test/resources/environments/dev.properties` e `hml.properties`.

---

## CI/CD

GitHub Actions executa automaticamente em push para `main`/`develop`. Relatório Allure publicado no GitHub Pages.

---

## Documentação

Consulte [DOCUMENTATION.md](DOCUMENTATION.md) para o guia completo do framework.
