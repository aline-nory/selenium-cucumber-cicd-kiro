# selenium-restassured-cucumber-kiro-github-actions

![CI](https://github.com/aline-nory/selenium-restassured-cucumber-kiro-github-actions/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Maven](https://img.shields.io/badge/Maven-3.9-blue?logo=apachemaven)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Allure](https://img.shields.io/badge/Report-Allure-orange)
![Kiro AI](https://img.shields.io/badge/Generated%20with-Kiro%20AI-blueviolet)

Projeto de automação de testes **Web (UI)** e **API REST** com pipeline CI/CD. Desenvolvido com Kiro AI como portfólio de QA.

---

## Destaques do projeto

- **BDD em português** com Cucumber — cenários legíveis para qualquer pessoa do time
- **Page Object Pattern** com herança (`BasePage`) — código reutilizável e fácil de manter
- **Testes de UI** com Selenium WebDriver — validação de fluxos no navegador
- **Testes de API** com REST Assured — cobertura completa dos verbos HTTP (GET, POST, PUT, DELETE)
- **Validação de contrato** com JSON Schema — garante que a API respeita o formato esperado
- **Payloads externalizados** — requests em arquivos `.json` separados do código
- **Injeção de dependência** com PicoContainer — isolamento por cenário
- **Separação por camadas** — pages, steps, api, hooks, config, drivers, utils (padrão enterprise)
- **CI/CD com GitHub Actions** — testes executados automaticamente a cada push
- **Allure Report** — relatório interativo com gráficos, histórico e screenshots
- **Screenshots automáticas** — capturadas em cenários de falha (configurável)
- **Logging corporativo** com SLF4J + Logback — console + arquivo
- **Configuração por ambiente** — troca entre DEV/HML sem alterar código
- **Detecção automática de CI** — modo headless ativado automaticamente em servidores
- **Dados dinâmicos** com JavaFaker — geração de massa de teste em português

---

## Stack

| Tecnologia | Versão | Função |
|---|---|---|
| Java | 8 | Linguagem |
| Maven | 3.9 | Build e dependências |
| Selenium WebDriver | 3.141.59 | Automação de UI |
| Cucumber | 7.18 | BDD em português |
| JUnit | 4.13 | Runner e assertions |
| REST Assured | 4.5.1 | Automação de API REST |
| Allure Report | 2.24 | Relatório interativo |
| PicoContainer | 7.18 | Injeção de dependência |
| SLF4J + Logback | 1.7/1.2 | Logging corporativo |
| JavaFaker | 1.0.2 | Dados dinâmicos |
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
│   ├── DriverFactory.java           # Criação do Chrome (local/headless)
│   └── DriverManager.java           # ThreadLocal para paralelismo
├── utils/
│   ├── LogUtils.java                # Logging SLF4J
│   ├── JsonUtils.java               # Leitura de payloads do classpath
│   └── ScreenshotUtils.java         # Captura de evidências
└── exceptions/
    └── FrameworkException.java       # Exceção customizada do framework

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
│   ├── create-post.json             # Body de criação
│   └── update-post.json             # Body de atualização
├── schemas/
│   └── post-schema.json             # Contrato JSON da API
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

## Tags

| Tag | Tipo | Como rodar |
|---|---|---|
| `@ui` | Cenários Web (Chrome) | `mvn test -Dcucumber.filter.tags="@ui"` |
| `@api` | Cenários de API | `mvn test -Dcucumber.filter.tags="@api"` |
| `@smoke` | Validação rápida | `mvn test -Dcucumber.filter.tags="@smoke"` |
| sem filtro | Regressão completa | `mvn test` |

---

## Como executar

```bash
mvn test                                        # todos os cenários
mvn test -Dcucumber.filter.tags="@api"          # só API
mvn test -Dcucumber.filter.tags="@ui"           # só UI
mvn test -Dcucumber.filter.tags="@smoke"        # smoke
mvn test -Denvironment=hml                      # outro ambiente
```

---

## Relatórios

```bash
mvn allure:serve                                # abre Allure no navegador
mvn allure:report                               # gera em target/site/
```

| Tipo | Local |
|---|---|
| Cucumber HTML | `target/cucumber-reports/cucumber.html` |
| Allure Report | `mvn allure:serve` (interativo) |
| Log de execução | `target/test-execution.log` |
| GitHub Pages | Automático via CI |

---

## Pipeline CI/CD

O GitHub Actions executa automaticamente em cada push para `main` ou `develop`.

1. Configura Java 8, Chrome e ChromeDriver
2. Executa `mvn test` com `CI=true` (headless automático)
3. Gera e publica Allure Report no GitHub Pages
4. Publica relatório Cucumber como artefato
5. Exibe resultado JUnit inline no GitHub

---

## Evidências

- Screenshots capturadas em cenários `@ui` com falha (configurável via `screenshot.mode`)
- Embutidas no Allure Report e no `cucumber.html`
- Request/Response de API anexados automaticamente ao Allure

---

## Configuração por ambiente

```bash
mvn test                       # usa dev.properties (padrão)
mvn test -Denvironment=hml     # usa hml.properties
```

Configurações em `src/test/resources/environments/`.

---

## Validação de contrato (JSON Schema)

O cenário "Validar contrato do post" garante que a API retorna a estrutura esperada:

```json
{
  "type": "object",
  "required": ["userId", "id", "title", "body"],
  "properties": {
    "userId": { "type": "integer", "minimum": 1 },
    "id": { "type": "integer", "minimum": 1 },
    "title": { "type": "string", "minLength": 1 },
    "body": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": true
}
```

Se a API mudar a estrutura da resposta, o teste detecta a quebra de contrato imediatamente.

---

## Documentação

Consulte [DOCUMENTATION.md](DOCUMENTATION.md) para o guia técnico completo do framework.

---

## Gerado com Kiro AI

Projeto criado com [Kiro](https://kiro.dev), ambiente de desenvolvimento com IA.
