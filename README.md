# selenium-cucumber-cicd-kiro

![CI](https://github.com/aline-nory/selenium-cucumber-cicd-kiro/actions/workflows/testes.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-8-orange?logo=java)
![Maven](https://img.shields.io/badge/Maven-3.9-blue?logo=apachemaven)
![Selenium](https://img.shields.io/badge/Selenium-3.141-green?logo=selenium)
![Cucumber](https://img.shields.io/badge/Cucumber-7.18-brightgreen?logo=cucumber)
![REST Assured](https://img.shields.io/badge/REST_Assured-4.5-teal)
![Kiro AI](https://img.shields.io/badge/Generated%20with-Kiro%20AI-blueviolet)

Projeto de automação de testes desenvolvido com **Kiro AI**, cobrindo testes **Web (UI)** e **API REST**, com pipeline **CI/CD** via GitHub Actions.

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
| GitHub Actions | - | Pipeline CI/CD |

---

## Estrutura do projeto

```
selenium-cucumber-cicd-kiro/
├── .github/
│   └── workflows/
│       └── testes.yml          # Pipeline CI/CD
├── src/
│   └── test/
│       ├── java/
│       │   ├── pages/
│       │   │   └── LoginPage.java       # Page Object
│       │   ├── steps/
│       │   │   ├── Hooks.java           # Ciclo de vida WebDriver
│       │   │   ├── LoginSteps.java      # Steps de UI
│       │   │   └── ApiSteps.java        # Steps de API
│       │   └── runner/
│       │       └── RunnerTest.java      # JUnit Runner
│       └── resources/
│           ├── features/
│           │   ├── login.feature        # Cenários de UI (OrangeHRM)
│           │   └── api_posts.feature    # Cenários de API (JSONPlaceholder)
│           └── cucumber.properties
├── pom.xml
└── executar-testes.bat         # Script para execução local (Windows)
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

---

## Como executar localmente (Windows)

### Pré-requisitos
- Java 8 JDK instalado
- Maven instalado (ou use o script abaixo)
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

### Executar todos os testes
```bat
executar-testes.bat
```

### Executar por categoria
```bat
executar-testes.bat api    # apenas testes de API
executar-testes.bat ui     # apenas testes de UI
```

### Executar via Maven diretamente
```bat
mvn test
mvn test -Dcucumber.features=src/test/resources/features/api_posts.feature
mvn test -Dcucumber.filter.tags="@smoke"
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
5. Publica o relatório HTML como artefato
6. Exibe resultado JUnit inline no GitHub

> Os testes de UI rodam em modo **headless** automaticamente no CI.
> Localmente o Chrome abre normalmente.

---

## Relatórios

Após a execução os relatórios ficam disponíveis em:
- `target/cucumber-reports/cucumber.html` — relatório visual
- `target/cucumber-reports/cucumber.json` — para integrações
- `target/cucumber-reports/cucumber.xml` — formato JUnit (Jenkins/GitHub)

No CI os relatórios são publicados como artefatos na aba **Actions** do GitHub.

---

## Gerado com Kiro AI

Este projeto foi criado com o auxílio do **[Kiro](https://kiro.dev)**, um ambiente de desenvolvimento com IA que gera, refatora e executa código diretamente no editor.
