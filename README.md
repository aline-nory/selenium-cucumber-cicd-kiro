# selenium-cucumber-kiro-github-actions

![CI](https://github.com/aline-nory/selenium-cucumber-kiro-github-actions/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Maven](https://img.shields.io/badge/Maven-3.9-blue?logo=apachemaven)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Kiro AI](https://img.shields.io/badge/Generated%20with-Kiro%20AI-blueviolet)

Projeto de automacao de testes Web (UI) e API REST com pipeline CI/CD via GitHub Actions. Desenvolvido com Kiro AI.

---

## Stack

| Tecnologia | Versao | Funcao |
|---|---|---|
| Java | 8 | Linguagem |
| Maven | 3.9 | Build e dependencias |
| Selenium WebDriver | 3.141.59 | Automacao de UI |
| Cucumber | 7.18 | BDD em portugues |
| JUnit | 4.13 | Runner e assertions |
| REST Assured | 4.5.1 | Automacao de API REST |
| GitHub Actions | - | Pipeline CI/CD |

---

## Estrutura do projeto

```
src/test/java/
├── pages/                          # Page Objects
│   ├── BasePage.java               # Classe base (acoes comuns)
│   └── LoginPage.java             # PO da tela de login
├── services/                       # Servicos de API
│   └── PostService.java           # Chamadas do endpoint /posts
├── steps/                          # Step Definitions
│   ├── LoginSteps.java            # Steps de UI
│   └── ApiPostsSteps.java        # Steps de API
├── support/
│   ├── communication/             # Comunicacao HTTP
│   │   └── RestApi.java           # Wrapper REST Assured
│   ├── environment/               # Configuracoes de ambiente
│   │   └── Environment.java      # Leitura do config.properties
│   ├── helpers/                   # Utilitarios
│   │   └── LogUtils.java         # Log formatado
│   ├── hooks/                     # Hooks do Cucumber
│   │   ├── WebHooks.java         # Ciclo de vida WebDriver (@ui)
│   │   └── ApiHooks.java         # Setup de API (@api)
│   ├── testEvidence/              # Evidencias de teste
│   │   └── ScreenshotUtils.java  # Captura de screenshots
│   └── webDriver/                 # Fabrica de drivers
│       └── DriverFactory.java    # Criacao Chrome/headless
└── Runner.java                    # Runner principal

src/test/resources/
└── features/
    ├── login.feature              # Cenarios de UI
    └── api_posts.feature          # Cenarios de API

config.properties                  # Configuracoes por ambiente (raiz)
```

---

## Tags

| Tag | Tipo | Como rodar |
|---|---|---|
| `@ui` | Cenarios Web (Chrome) | `mvn test -Dcucumber.filter.tags="@ui"` |
| `@api` | Cenarios de API | `mvn test -Dcucumber.filter.tags="@api"` |
| `@smoke` | Validacao rapida | `mvn test -Dcucumber.filter.tags="@smoke"` |
| sem filtro | Regressao completa | `mvn test` |

---

## Como executar

```bat
mvn test                                        # tudo
mvn test -Dcucumber.filter.tags="@api"          # so API
mvn test -Dcucumber.filter.tags="@ui"           # so UI
mvn test -Dcucumber.filter.tags="@smoke"        # smoke
mvn test -Denvironment=HQA                      # outro ambiente
```

---

## Pipeline CI/CD

O GitHub Actions executa automaticamente em cada push para `main` ou `develop`.

O que o pipeline faz:
1. Configura Java 8, Chrome e ChromeDriver
2. Executa `mvn test` com `CI=true` (headless automatico)
3. Publica relatorio Cucumber como artefato
4. Exibe resultado JUnit inline no GitHub

---

## Evidencias

- Screenshots capturadas automaticamente em todos os cenarios `@ui`
- Embutidas no relatorio `target/cucumber-reports/cucumber.html`
- Cenarios com sucesso: screenshot do estado final
- Cenarios com falha: screenshot do momento do erro

---

## Gerado com Kiro AI

Projeto criado com [Kiro](https://kiro.dev), ambiente de desenvolvimento com IA.
