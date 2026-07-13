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
- **Configuração por ambiente** — troca entre DEV/HML sem alterar código, com override via variável de ambiente (pronto para GitHub Secrets)
- **Detecção automática de CI** — modo headless ativado automaticamente em servidores
- **Reexecução automática de falhas** — mitiga flakiness ao depender de serviços públicos de terceiros (JSONPlaceholder, OrangeHRM demo)

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
| Jackson Databind | 2.15.2 | Leitura/edição de payloads JSON |
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
│   └── services/
│       └── PostService.java         # Lógica de negócio /posts
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
│   ├── JsonUtils.java               # Leitura/edição de payloads JSON do classpath
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

## Pré-requisitos locais

- Java 8, Maven 3.9+ e Google Chrome instalados.
- **ChromeDriver** compatível com a versão do Chrome instalado — baixe em
  [chrome-for-testing](https://googlechromelabs.github.io/chrome-for-testing/) e aponte a variável de ambiente:
  ```bash
  # Windows
  set CHROME_DRIVER_PATH=C:\chromedriver\chromedriver.exe
  # Linux/Mac
  export CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
  ```
  Sem essa variável, os cenários `@ui` falham com uma mensagem explicando o que falta.
  Em CI (`CI=true`), o Chrome roda headless e o ChromeDriver já vem instalado pelo workflow — nada a configurar.
- Testes `@api` não precisam de Chrome/ChromeDriver.

## Como executar

```bash
mvn test                                        # todos os cenários
mvn test -Dcucumber.filter.tags="@api"          # só API
mvn test -Dcucumber.filter.tags="@ui"           # só UI
mvn test -Dcucumber.filter.tags="@smoke"        # smoke
mvn test -Denvironment=hml                      # outro ambiente
```

Cenários com falha são reexecutados automaticamente uma vez (`rerunFailingTestsCount`) antes de reportar
falha definitiva — mitiga instabilidade transitória dos serviços públicos usados como alvo (JSONPlaceholder, OrangeHRM demo).

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

O GitHub Actions executa automaticamente em cada push para `main`/`develop` e em pull requests para `main`,
em dois jobs separados (princípio do menor privilégio — só o job de publicação tem permissão de escrita):

**Job `testes`** (permissão apenas de leitura + `checks: write`)
1. Configura Java 8 e instala Chrome + ChromeDriver compatível (`browser-actions/setup-chrome`)
2. Executa `mvn test` com `CI=true` (headless automático)
3. Publica relatório Cucumber e resultados Allure como artefatos, e o resumo JUnit inline no GitHub

**Job `publicar-relatorio`** (permissão de escrita — só roda em push para `main`)
4. Baixa os resultados Allure do job de testes
5. Gera e publica o Allure Report no GitHub Pages

Ações de terceiros são fixadas em versões imutáveis (nunca `@master`), e o job de publicação
nunca roda em pull requests — uma PR não pode sobrescrever o relatório público.

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

### Credenciais

Os valores em `dev.properties`/`hml.properties` (ex. `senha.admin`) são as credenciais públicas do
[demo do OrangeHRM](https://opensource-demo.orangehrmlive.com/) — não são segredos reais, por isso ficam
no repositório para facilitar rodar o projeto localmente sem nenhuma configuração extra.

Qualquer chave pode ser sobrescrita por variável de ambiente sem tocar nos arquivos: `senha.admin` vira
`SENHA_ADMIN` (ver `ConfigReader`). Em um projeto real, aponte essas variáveis para GitHub Secrets / um
gerenciador de segredos (Vault, AWS Secrets Manager) em vez de manter valores reais em `.properties`.

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
