# selenium-restassured-cucumber-kiro-github-actions

![CI](https://github.com/aline-nory/selenium-restassured-cucumber-kiro-github-actions/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Maven](https://img.shields.io/badge/Maven-3.9-blue?logo=apachemaven)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Allure](https://img.shields.io/badge/Report-Allure-orange)
![Kiro AI](https://img.shields.io/badge/Generated%20with-Kiro%20AI-blueviolet)

Projeto de automação de testes **Web (UI)** e **API REST**, com pipeline **CI/CD** via GitHub Actions e relatórios Allure.

---

## Stack

| Tecnologia | Versão | Função |
|---|---|---|
| Java | 8 | Linguagem |
| Maven | 3.9 | Build e gerenciamento de dependências |
| Selenium WebDriver | 3.141.59 | Automação de UI no Chrome |
| Cucumber | 7.18 | BDD — cenários em português |
| JUnit | 4.13 | Runner e assertions |
| REST Assured | 4.5.1 | Automação de API REST |
| Allure Report | 2.24 | Relatórios visuais com evidências |
| PicoContainer | 7.18 | Injeção de dependência |
| SLF4J + Logback | 1.7/1.2 | Logging corporativo |
| JavaFaker | 1.0.2 | Dados dinâmicos de teste |
| GitHub Actions | - | Pipeline CI/CD |

---

## Estrutura do projeto

```
src/test/java/
├── runners/
│   └── TestRunner.java              # Ponto de entrada Cucumber + JUnit
├── steps/
│   ├── ui/
│   │   └── LoginSteps.java         # Steps de UI
│   └── api/
│       └── PostSteps.java           # Steps de API
├── pages/
│   ├── base/
│   │   └── BasePage.java            # Classe abstrata (ações comuns)
│   └── login/
│       └── LoginPage.java           # Page Object do login
├── api/
│   ├── clients/
│   │   └── RestClient.java          # Cliente HTTP com Allure attachments
│   ├── services/
│   │   └── PostService.java         # Lógica de negócio /posts
│   ├── models/
│   │   └── PostRequest.java         # POJO de request
│   └── builders/
│       └── PostBuilder.java         # Builder com Faker
├── hooks/
│   ├── UiHooks.java                 # Ciclo de vida WebDriver (@ui)
│   └── ApiHooks.java                # Setup de API (@api)
├── config/
│   ├── Environment.java             # Gerenciamento de ambiente
│   └── ConfigReader.java            # Leitura de .properties
├── drivers/
│   ├── DriverFactory.java           # Criação do Chrome
│   └── DriverManager.java           # ThreadLocal (paralelo)
├── utils/
│   ├── LogUtils.java                # Logging SLF4J
│   ├── JsonUtils.java               # Leitura de payloads
│   └── ScreenshotUtils.java         # Captura de tela
└── exceptions/
    └── FrameworkException.java       # Exceção customizada

src/test/resources/
├── features/
│   ├── ui/
│   │   └── login.feature            # Cenários de UI (OrangeHRM)
│   └── api/
│       └── posts.feature            # Cenários de API (JSONPlaceholder)
├── environments/
│   ├── dev.properties               # Configuração DEV
│   └── hml.properties               # Configuração HML
├── payloads/posts/
│   ├── create-post.json             # Body POST
│   └── update-post.json             # Body PUT
├── schemas/
│   └── post-schema.json             # Contrato JSON Schema
└── logback.xml                      # Configuração de logging
```

---

## Cenários de teste

### UI — Login (OrangeHRM Demo)

- Login com credenciais válidas
- Login com senha incorreta
- Login com múltiplas credenciais inválidas (Scenario Outline)

### API — Posts (JSONPlaceholder)

- `GET /posts` — listar todos os posts
- `GET /posts/{id}` — buscar por ID
- `GET /posts?userId=1` — filtrar por usuário
- `POST /posts` — criar novo post
- `PUT /posts/{id}` — atualizar post
- `DELETE /posts/{id}` — deletar post
- `GET /posts/9999` — recurso inexistente (404)
- Validação de contrato (JSON Schema)

---

## Como executar

### Pré-requisitos

- Java 8 JDK instalado
- Maven 3.8+ instalado
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

### Executar via Maven

```bash
mvn test                                    # todos os testes
mvn test -Dcucumber.filter.tags="@api"      # apenas API
mvn test -Dcucumber.filter.tags="@ui"       # apenas UI
mvn test -Dcucumber.filter.tags="@smoke"    # smoke tests
mvn test -Denvironment=hml                  # ambiente HML
```

### Tags disponíveis

| Tag | Descrição |
|---|---|
| `@ui` | Cenários Web (abre Chrome) |
| `@api` | Cenários de API (sem navegador) |
| `@smoke` | Cenários críticos |

---

## Relatórios

```bash
# Allure Report (abre no navegador)
mvn allure:serve

# Cucumber HTML
target/cucumber-reports/cucumber.html

# Log de execução
target/test-execution.log
```

---

## Pipeline CI/CD

O GitHub Actions executa os testes automaticamente em cada:
- **Push** para `main` ou `develop`
- **Pull Request** para `main`
- **Execução manual** pela aba Actions

### O que o pipeline faz

1. Faz checkout do código
2. Configura Java 8
3. Instala Chrome e ChromeDriver (versão compatível)
4. Executa `mvn test` com `CI=true` (ativa headless automático)
5. Gera e publica Allure Report no GitHub Pages
6. Publica relatório Cucumber como artefato
7. Exibe resultado JUnit inline no GitHub

> Os testes de UI rodam em modo **headless** automaticamente no CI.
> Localmente o Chrome abre normalmente.

---

## Ambientes

Configurações separadas por ambiente em `src/test/resources/environments/`:

```bash
mvn test                       # usa dev.properties (padrão)
mvn test -Denvironment=hml     # usa hml.properties
```

---

## Documentação

Consulte [DOCUMENTATION.md](DOCUMENTATION.md) para o guia técnico completo do framework.

---

## Gerado com Kiro AI

Este projeto foi criado com o auxílio do **[Kiro](https://kiro.dev)**, um ambiente de desenvolvimento com IA.
