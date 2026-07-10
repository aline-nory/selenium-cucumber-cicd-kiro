# Framework de Automação com Selenium + Cucumber
## Guia Completo para QA — Do Zero à Pipeline

---

## Sumário

1. [Criar o projeto Maven vazio](#capítulo-1--criar-o-projeto-maven-vazio)
2. [Configurar dependências no pom.xml](#capítulo-2--configurar-dependências-no-pomxml)
3. [Criar estrutura de diretórios e pacotes](#capítulo-3--criar-estrutura-de-diretórios-e-pacotes)
4. [FrameworkException](#capítulo-4--frameworkexception)
5. [ConfigReader e Environment](#capítulo-5--configreader-e-environment)
6. [DriverFactory e DriverManager](#capítulo-6--driverfactory-e-drivermanager)
7. [LogUtils e logback.xml](#capítulo-7--logutils-e-logbackxml)
8. [BasePage e LoginPage](#capítulo-8--basepage-e-loginpage)
9. [Feature de login + LoginSteps + TestRunner](#capítulo-9--feature-de-login--loginsteps--testrunner)
10. [UiHooks e ScreenshotUtils](#capítulo-10--uihooks-e-screenshotutils)
11. [RestClient](#capítulo-11--restclient)
12. [JsonUtils e payloads](#capítulo-12--jsonutils-e-payloads)
13. [PostService](#capítulo-13--postservice)
14. [PostRequest e PostBuilder](#capítulo-14--postrequest-e-postbuilder)
15. [Feature de API + PostSteps + ApiHooks](#capítulo-15--feature-de-api--poststeps--apihooks)
16. [JSON Schema Validation](#capítulo-16--json-schema-validation)
17. [Ambiente HML](#capítulo-17--ambiente-hml)
18. [Allure Report](#capítulo-18--allure-report)
19. [GitHub Actions (progressivo)](#capítulo-19--github-actions-progressivo)
20. [Manutenção e evolução](#capítulo-20--manutenção-e-evolução)

---

## Capítulo 1 — Criar o projeto Maven vazio

### Resultado que construiremos

Um projeto Maven funcional com a estrutura mínima que compila sem erros. Ao final, você terá um diretório reconhecido por qualquer IDE Java e pronto para receber dependências.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| PROJETO MAVEN (pom.xml)                               |  <-- AQUI
|                                                       |
|   src/test/java/    (código de teste)                 |
|   src/test/resources/ (recursos de teste)             |
+-------------------------------------------------------+
```

Estamos na fundação. Sem o Maven configurado, nada mais funciona.

### Conceito mínimo necessário

Maven é um gerenciador de build e dependências. Ele usa um arquivo `pom.xml` para saber:
- Qual versão do Java usar
- Quais bibliotecas baixar
- Como compilar e executar testes

O diretório `src/test/java` é onde ficam os testes. Diferente de projetos de aplicação, nosso framework de automação vive inteiramente em `src/test`.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `pom.xml` | Configuração do Maven |

### Construção manual passo a passo

1. Crie uma pasta chamada `selenium-cucumber-project`
2. Dentro dela, crie o arquivo `pom.xml`
3. Crie a estrutura de pastas: `src/test/java` e `src/test/resources`

No terminal:

```bash
mkdir selenium-cucumber-project
cd selenium-cucumber-project
mkdir -p src/test/java
mkdir -p src/test/resources
```

### Codigo completo final

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.framework</groupId>
    <artifactId>selenium-cucumber-project</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

</project>
```

### Explicacao do codigo

- `groupId`: identifica sua organização (como um domínio invertido)
- `artifactId`: nome do projeto
- `version`: versão atual (SNAPSHOT indica desenvolvimento)
- `packaging`: jar é o padrão para projetos Java
- `maven.compiler.source/target`: define Java 8 como versão de compilação

### Fluxo de execucao

```
Terminal: mvn validate
    |
    v
Maven lê pom.xml
    |
    v
Valida estrutura XML
    |
    v
BUILD SUCCESS (sem erros)
```

### Como executar

```bash
cd selenium-cucumber-project
mvn validate
```

### Como confirmar que funcionou

Você verá no terminal:

```
[INFO] BUILD SUCCESS
[INFO] Total time: 0.5 s
```

### Falha guiada

Remova a tag `</project>` do final do pom.xml e execute `mvn validate`. Você verá:

```
[FATAL] Non-parseable POM... Unexpected end of file
```

Isso ensina que o XML precisa estar bem-formado. Restaure a tag e tente novamente.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `mvn: command not found` | Maven não instalado | Instale Maven 3.x e adicione ao PATH |
| `Non-parseable POM` | XML malformado | Verifique tags abertas/fechadas |
| `Source option 5 is no longer supported` | Java antigo sem config | Adicione compiler.source/target |

### O que nao deve ser feito

- Não crie código em `src/main/java` — nosso framework é 100% teste
- Não use Maven 2.x — ele não suporta plugins modernos
- Não pule este passo achando que a IDE faz tudo — entender o pom.xml é essencial

### Exercicio

1. Altere o `groupId` para refletir sua empresa (ex: `com.suaempresa`)
2. Execute `mvn validate` e confirme BUILD SUCCESS
3. Tente mudar `maven.compiler.source` para `11` e valide novamente

### Checklist

- [ ] Pasta `selenium-cucumber-project` criada
- [ ] `pom.xml` com groupId, artifactId, version
- [ ] Propriedades de compilação Java 8 configuradas
- [ ] `mvn validate` retorna BUILD SUCCESS
- [ ] Estrutura `src/test/java` existe
- [ ] Estrutura `src/test/resources` existe

---

## Capítulo 2 — Configurar dependências no pom.xml

### Resultado que construiremos

Um `pom.xml` completo com todas as 12 dependências que o framework usa. Ao final, `mvn compile` baixará todas as bibliotecas e compilará sem erros.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| PROJETO MAVEN (pom.xml)                               |  <-- AQUI
|   +-- Selenium 3.141.59                               |
|   +-- Cucumber 7.18 + JUnit 4                         |
|   +-- REST Assured 4.5.1                              |
|   +-- Allure 2.24                                     |
|   +-- PicoContainer (injecao de dependencia)          |
|   +-- SLF4J + Logback (logs)                          |
|   +-- JavaFaker (dados fake)                          |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

Dependências Maven ficam dentro da tag `<dependencies>`. Cada dependência precisa de:
- `groupId` — quem publicou
- `artifactId` — nome da biblioteca
- `version` — versão exata (usamos versões fixas para reprodutibilidade)
- `scope` — `test` significa que só está disponível em `src/test`

Plugins Maven ficam em `<build><plugins>`. Eles estendem o comportamento do build.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `pom.xml` | Todas as dependências e plugins |

### Construção manual passo a passo

1. Abra o `pom.xml` criado no capítulo anterior
2. Adicione o bloco `<dependencies>` com cada biblioteca
3. Adicione o bloco `<build><plugins>` para Surefire e Allure
4. Execute `mvn compile` para baixar tudo

### Codigo completo final

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.framework</groupId>
    <artifactId>selenium-cucumber-project</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
        <selenium.version>3.141.59</selenium.version>
        <cucumber.version>7.18.0</cucumber.version>
        <junit.version>4.13.2</junit.version>
        <rest-assured.version>4.5.1</rest-assured.version>
        <allure.version>2.24.0</allure.version>
        <slf4j.version>1.7.36</slf4j.version>
        <logback.version>1.2.12</logback.version>
    </properties>

    <dependencies>
        <!-- Selenium -->
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- Cucumber -->
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-junit</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-picocontainer</artifactId>
            <version>${cucumber.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JUnit -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- REST Assured -->
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <version>${rest-assured.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>json-schema-validator</artifactId>
            <version>${rest-assured.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- Allure -->
        <dependency>
            <groupId>io.qameta.allure</groupId>
            <artifactId>allure-cucumber7-jvm</artifactId>
            <version>${allure.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.qameta.allure</groupId>
            <artifactId>allure-rest-assured</artifactId>
            <version>${allure.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- Logging -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>${slf4j.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>${logback.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JavaFaker -->
        <dependency>
            <groupId>com.github.javafaker</groupId>
            <artifactId>javafaker</artifactId>
            <version>1.0.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
                <configuration>
                    <argLine>
                        -javaagent:"${settings.localRepository}/org/aspectj/aspectjweaver/1.9.20.1/aspectjweaver-1.9.20.1.jar"
                    </argLine>
                    <systemPropertyVariables>
                        <allure.results.directory>${project.build.directory}/allure-results</allure.results.directory>
                    </systemPropertyVariables>
                </configuration>
                <dependencies>
                    <dependency>
                        <groupId>org.aspectj</groupId>
                        <artifactId>aspectjweaver</artifactId>
                        <version>1.9.20.1</version>
                    </dependency>
                </dependencies>
            </plugin>
        </plugins>
    </build>

</project>
```

### Explicacao do codigo

| Dependência | Para que serve |
|-------------|---------------|
| `selenium-java` | Controlar o navegador |
| `cucumber-java` | Escrever steps em Java |
| `cucumber-junit` | Integrar Cucumber com JUnit |
| `cucumber-picocontainer` | Injetar dependências nos steps |
| `junit` | Runner de testes |
| `rest-assured` | Testes de API REST |
| `json-schema-validator` | Validar JSON contra schema |
| `allure-cucumber7-jvm` | Relatórios Allure para UI |
| `allure-rest-assured` | Relatórios Allure para API |
| `slf4j-api` | Fachada de logging |
| `logback-classic` | Implementação de logging |
| `javafaker` | Gerar dados de teste |

O plugin `maven-surefire-plugin` executa os testes e integra o AspectJ para o Allure interceptar os steps.

### Fluxo de execucao

```
Terminal: mvn compile -DskipTests
    |
    v
Maven resolve dependencias (baixa .jar do Maven Central)
    |
    v
Compila src/test/java (ainda vazio)
    |
    v
BUILD SUCCESS
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

```
[INFO] BUILD SUCCESS
```

Verifique também que a pasta `~/.m2/repository` agora contém as bibliotecas baixadas.

### Falha guiada

Mude a versão do Selenium para `99.99.99` (inexistente):

```xml
<selenium.version>99.99.99</selenium.version>
```

Execute `mvn compile`. Você verá:

```
Could not find artifact org.seleniumhq.selenium:selenium-java:jar:99.99.99
```

Isso mostra que o Maven valida se a versão existe. Restaure para `3.141.59`.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Could not find artifact` | Versão inexistente | Confirme versão no Maven Central |
| `Failed to read artifact descriptor` | Sem internet | Verifique conexão |
| `Package does not exist` | Scope errado | Use `test` para src/test |
| `Plugin not found` | Repositório bloqueado | Verifique proxy/firewall |

### O que nao deve ser feito

- Não use `LATEST` ou `RELEASE` como versão — não é reproduzível
- Não omita o `<scope>test</scope>` — poluirá o classpath de produção
- Não misture versões de Cucumber (java, junit, picocontainer devem ter mesma versão)
- Não esqueça do AspectJ no Surefire — sem ele o Allure não funciona

### Exercicio

1. Adicione a dependência do `webdrivermanager` versão 5.5.3 (groupId: `io.github.bonigarcia`)
2. Execute `mvn dependency:tree` e identifique dependências transitivas do Selenium
3. Remova uma dependência, compile e observe o erro

### Checklist

- [ ] Todas as 12 dependências adicionadas
- [ ] Versões centralizadas em `<properties>`
- [ ] Scope `test` em todas as dependências
- [ ] Plugin Surefire configurado com AspectJ
- [ ] `mvn compile -DskipTests` retorna BUILD SUCCESS
- [ ] Nenhum warning de versão no output

---

## Capítulo 3 — Criar estrutura de diretórios e pacotes

### Resultado que construiremos

A árvore completa de pacotes Java e diretórios de recursos. Ao final, cada classe terá seu lugar definido e o projeto estará organizado para crescer.

### Onde estamos na arquitetura

```
src/test/java/
+-- runners/            <-- Ponto de entrada do Cucumber
+-- steps/
|   +-- ui/             <-- Steps de interface
|   +-- api/            <-- Steps de API
+-- pages/
|   +-- base/           <-- Page Objects base
|   +-- login/          <-- Page Objects por funcionalidade
+-- api/
|   +-- clients/        <-- Clientes HTTP
|   +-- services/       <-- Servicos de dominio
|   +-- models/         <-- POJOs de request/response
|   +-- builders/       <-- Builders para payloads
+-- hooks/              <-- Before/After do Cucumber
+-- config/             <-- Leitura de configuracao
+-- drivers/            <-- Gerenciamento do WebDriver
+-- utils/              <-- Utilitarios
+-- exceptions/         <-- Excecoes customizadas

src/test/resources/
+-- features/
|   +-- ui/             <-- Features de interface
|   +-- api/            <-- Features de API
+-- environments/       <-- Propriedades por ambiente
+-- payloads/
|   +-- posts/          <-- JSONs de request
+-- schemas/            <-- JSON Schemas
+-- testdata/           <-- Dados de teste
```

### Conceito mínimo necessário

Em Java, a estrutura de pacotes reflete a organização lógica do código. Cada pacote é um diretório. A convenção é:
- Agrupar por responsabilidade (não por tipo de arquivo)
- Manter pacotes coesos — classes no mesmo pacote colaboram
- Separar UI de API desde o início

O Cucumber encontra features pelo caminho configurado no Runner. Steps são descobertos pelo pacote declarado no `@CucumberOptions`.

### Arquivos envolvidos

Nenhum arquivo de código neste capítulo — apenas diretórios.

### Construção manual passo a passo

Execute no terminal (a partir da raiz do projeto):

```bash
# Pacotes Java
mkdir -p src/test/java/runners
mkdir -p src/test/java/steps/ui
mkdir -p src/test/java/steps/api
mkdir -p src/test/java/pages/base
mkdir -p src/test/java/pages/login
mkdir -p src/test/java/api/clients
mkdir -p src/test/java/api/services
mkdir -p src/test/java/api/models
mkdir -p src/test/java/api/builders
mkdir -p src/test/java/hooks
mkdir -p src/test/java/config
mkdir -p src/test/java/drivers
mkdir -p src/test/java/utils
mkdir -p src/test/java/exceptions

# Recursos
mkdir -p src/test/resources/features/ui
mkdir -p src/test/resources/features/api
mkdir -p src/test/resources/environments
mkdir -p src/test/resources/payloads/posts
mkdir -p src/test/resources/schemas
mkdir -p src/test/resources/testdata
```

### Codigo completo final

Não há código neste capítulo. A saída é a estrutura de diretórios mostrada acima.

Para validar, execute:

```bash
find src -type d | sort
```

Saída esperada:

```
src
src/test
src/test/java
src/test/java/api
src/test/java/api/builders
src/test/java/api/clients
src/test/java/api/models
src/test/java/api/services
src/test/java/config
src/test/java/drivers
src/test/java/exceptions
src/test/java/hooks
src/test/java/pages
src/test/java/pages/base
src/test/java/pages/login
src/test/java/runners
src/test/java/steps
src/test/java/steps/api
src/test/java/steps/ui
src/test/java/utils
src/test/resources
src/test/resources/environments
src/test/resources/features
src/test/resources/features/api
src/test/resources/features/ui
src/test/resources/payloads
src/test/resources/payloads/posts
src/test/resources/schemas
src/test/resources/testdata
```

### Explicacao do codigo

| Pacote | Responsabilidade |
|--------|-----------------|
| `runners` | Classes JUnit que disparam o Cucumber |
| `steps/ui` | Implementação dos steps de interface |
| `steps/api` | Implementação dos steps de API |
| `pages/base` | BasePage com métodos comuns (click, type, wait) |
| `pages/login` | LoginPage com elementos e ações da tela de login |
| `api/clients` | RestClient genérico para chamadas HTTP |
| `api/services` | PostService que conhece os endpoints |
| `api/models` | POJOs: PostRequest, PostResponse |
| `api/builders` | PostBuilder para criar payloads com fluent API |
| `hooks` | @Before/@After: abrir browser, tirar screenshot |
| `config` | Leitura de .properties por ambiente |
| `drivers` | Criação e gerenciamento do WebDriver |
| `utils` | LogUtils, JsonUtils, ScreenshotUtils |
| `exceptions` | FrameworkException customizada |

### Fluxo de execucao

Não há execução neste capítulo. A estrutura será populada a partir do Capítulo 4.

### Como executar

```bash
# Valide que compila (mesmo vazio)
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. O comando `find src -type d | sort` mostra todos os diretórios
2. `mvn compile -DskipTests` continua com BUILD SUCCESS
3. Sua IDE mostra a árvore de pacotes no painel lateral

### Falha guiada

Crie um arquivo `src/test/java/steps/Teste.java` com conteúdo:

```java
package steps.ui;

public class Teste {}
```

Compile. O erro será:

```
Teste.java: package steps.ui does not match directory steps
```

Isso ensina que o `package` declarado DEVE corresponder ao diretório. Mova o arquivo para `src/test/java/steps/ui/` ou mude o package.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| Package does not match directory | Arquivo no diretório errado | Mover arquivo para o pacote correto |
| Class not found | Pacote não existe | Criar o diretório correspondente |
| IDE não reconhece src/test/java | Não marcou como Test Source | Marque na IDE (Mark as Test Sources Root) |

### O que nao deve ser feito

- Não crie `src/main/java` — não temos código de produção
- Não coloque tudo em um pacote só — dificulta manutenção
- Não misture features de UI e API no mesmo diretório
- Não use nomes de pacotes com hífen ou maiúsculas

### Exercicio

1. Adicione um pacote `pages/dashboard` para uma futura página de dashboard
2. Adicione `src/test/resources/payloads/users` para um futuro endpoint de usuários
3. Verifique que a estrutura compila sem erros

### Checklist

- [ ] Todos os 14 pacotes Java criados
- [ ] Todos os 7 diretórios de resources criados
- [ ] `mvn compile -DskipTests` BUILD SUCCESS
- [ ] IDE reconhece src/test/java como source root
- [ ] IDE reconhece src/test/resources como resource root
- [ ] Nenhum arquivo de código criado ainda (apenas diretórios)

---

## Capítulo 4 — FrameworkException

### Resultado que construiremos

Uma exceção customizada que padroniza o tratamento de erros no framework. Toda falha interna (timeout, configuração ausente, driver não encontrado) será encapsulada nesta exceção.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| exceptions/                                           |
|   +-- FrameworkException.java   <-- AQUI              |
|                                                       |
| Quem usa:                                             |
|   ConfigReader, DriverFactory, BasePage, RestClient   |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

Exceções customizadas em Java estendem `RuntimeException` (unchecked) ou `Exception` (checked). Usamos `RuntimeException` porque:
- Não obriga o chamador a fazer try/catch
- Interrompe o teste imediatamente quando algo está errado
- Mantém o código dos steps limpo

Uma boa exceção customizada:
1. Aceita mensagem descritiva
2. Aceita causa original (para não perder stack trace)
3. Tem nome que expressa o domínio

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/exceptions/FrameworkException.java` | Exceção do framework |

### Construção manual passo a passo

1. Crie o arquivo `src/test/java/exceptions/FrameworkException.java`
2. Declare o pacote `exceptions`
3. Estenda `RuntimeException`
4. Crie dois construtores: um com mensagem e outro com mensagem + causa

### Codigo completo final

```java
package exceptions;

public class FrameworkException extends RuntimeException {

    public FrameworkException(String message) {
        super(message);
    }

    public FrameworkException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### Explicacao do codigo

- `extends RuntimeException`: torna a exceção unchecked (não exige throws na assinatura)
- Construtor com `String message`: para erros simples como "Propriedade X não encontrada"
- Construtor com `Throwable cause`: preserva a exceção original no stack trace
- Sem lógica adicional — é apenas um wrapper semântico

Exemplos de uso futuro:

```java
// Em ConfigReader
throw new FrameworkException("Propriedade 'base.url' nao encontrada no arquivo de configuracao");

// Em DriverFactory
throw new FrameworkException("Browser '" + browser + "' nao suportado");

// Em BasePage (com causa)
try {
    wait.until(ExpectedConditions.visibilityOf(element));
} catch (TimeoutException e) {
    throw new FrameworkException("Elemento nao visivel apos 10s: " + element, e);
}
```

### Fluxo de execucao

```
Alguma classe detecta erro
    |
    v
throw new FrameworkException("mensagem clara")
    |
    v
JUnit captura a excecao
    |
    v
Teste marca como FAILED
    |
    v
Stack trace mostra origem + mensagem
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Nenhum erro de compilação
3. O arquivo aparece em `target/test-classes/exceptions/FrameworkException.class`

### Falha guiada

Remova `extends RuntimeException` e tente usar sem try/catch:

```java
public class FrameworkException { ... }
```

Em outra classe:

```java
throw new FrameworkException("teste");
```

Erro: `Incompatible types: FrameworkException cannot be converted to Throwable`

Isso mostra que para usar `throw`, a classe DEVE estender alguma classe de Throwable.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `cannot be converted to Throwable` | Não estende Exception/RuntimeException | Adicione extends RuntimeException |
| `unreported exception` | Estendeu Exception (checked) | Mude para RuntimeException ou adicione throws |
| `package does not exist` | Diretório errado | Verifique que está em src/test/java/exceptions/ |

### O que nao deve ser feito

- Não use `Exception` genérica — perde semântica nos logs
- Não adicione lógica de negócio na exceção — ela só carrega informação
- Não crie dezenas de exceções diferentes — uma é suficiente para um framework de teste
- Não engula a causa (`catch (Exception e) { throw new FrameworkException("erro") }`) — sempre passe `e`

### Exercicio

1. Crie um método `main` temporário que faz `throw new FrameworkException("teste")`
2. Execute e observe o stack trace
3. Agora use o construtor com causa: `throw new FrameworkException("wrap", new NullPointerException())`
4. Compare os dois stack traces

### Checklist

- [ ] Arquivo em `src/test/java/exceptions/FrameworkException.java`
- [ ] Package declaration: `package exceptions;`
- [ ] Estende RuntimeException
- [ ] Construtor com String message
- [ ] Construtor com String message + Throwable cause
- [ ] Compila sem erros

---

## Capítulo 5 — ConfigReader e Environment

### Resultado que construiremos

Um sistema de configuração que lê propriedades de arquivos `.properties` baseado no ambiente ativo (dev, hml). Ao final, qualquer classe poderá obter a URL base ou credenciais chamando `Environment.get("base.url")`.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| config/                                               |
|   +-- ConfigReader.java         <-- AQUI              |
|   +-- Environment.java          <-- AQUI              |
|                                                       |
| environments/                                         |
|   +-- dev.properties            <-- AQUI              |
|   +-- hml.properties            (capitulo 17)         |
|                                                       |
| Quem usa:                                             |
|   DriverFactory, RestClient, Pages, Steps             |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**ConfigReader**: classe que carrega um arquivo `.properties` do classpath e expõe os valores. Usa `java.util.Properties` internamente.

**Environment**: fachada estática que decide QUAL arquivo carregar baseado na system property `env`. Se nenhuma for passada, usa `dev` como padrão.

Fluxo: `mvn test -Denv=hml` → Environment lê `environments/hml.properties`.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/config/ConfigReader.java` | Carrega .properties |
| `src/test/java/config/Environment.java` | Fachada estática |
| `src/test/resources/environments/dev.properties` | Config de DEV |

### Construção manual passo a passo

1. Crie `dev.properties` com as propriedades mínimas
2. Crie `ConfigReader` que recebe o nome do arquivo e carrega
3. Crie `Environment` que instancia ConfigReader com o ambiente correto
4. Teste compilando

### Codigo completo final

**src/test/resources/environments/dev.properties**

```properties
base.url=https://the-internet.herokuapp.com
api.base.url=https://jsonplaceholder.typicode.com
browser=chrome
timeout=10
headless=false
username=tomsmith
password=SuperSecretPassword!
```

**src/test/java/config/ConfigReader.java**

```java
package config;

import exceptions.FrameworkException;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigReader {

    private final Properties properties;

    public ConfigReader(String fileName) {
        properties = new Properties();
        loadProperties(fileName);
    }

    private void loadProperties(String fileName) {
        String path = "environments/" + fileName + ".properties";
        try (InputStream input = getClass().getClassLoader().getResourceAsStream(path)) {
            if (input == null) {
                throw new FrameworkException("Arquivo de configuracao nao encontrado: " + path);
            }
            properties.load(input);
        } catch (IOException e) {
            throw new FrameworkException("Erro ao ler arquivo de configuracao: " + path, e);
        }
    }

    public String getProperty(String key) {
        String value = properties.getProperty(key);
        if (value == null) {
            throw new FrameworkException("Propriedade '" + key + "' nao encontrada no arquivo de configuracao");
        }
        return value.trim();
    }

    public String getProperty(String key, String defaultValue) {
        String value = properties.getProperty(key);
        return value != null ? value.trim() : defaultValue;
    }

    public int getIntProperty(String key) {
        String value = getProperty(key);
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            throw new FrameworkException("Propriedade '" + key + "' nao e um numero valido: " + value, e);
        }
    }

    public boolean getBooleanProperty(String key) {
        return Boolean.parseBoolean(getProperty(key));
    }
}
```

**src/test/java/config/Environment.java**

```java
package config;

public class Environment {

    private static ConfigReader configReader;

    private Environment() {
        // Classe utilitaria - nao instanciar
    }

    private static ConfigReader getConfigReader() {
        if (configReader == null) {
            String env = System.getProperty("env", "dev");
            configReader = new ConfigReader(env);
        }
        return configReader;
    }

    public static String get(String key) {
        return getConfigReader().getProperty(key);
    }

    public static String get(String key, String defaultValue) {
        return getConfigReader().getProperty(key, defaultValue);
    }

    public static int getInt(String key) {
        return getConfigReader().getIntProperty(key);
    }

    public static boolean getBoolean(String key) {
        return getConfigReader().getBooleanProperty(key);
    }
}
```

### Explicacao do codigo

**ConfigReader:**
- `getResourceAsStream`: lê do classpath (dentro de src/test/resources)
- `Properties.load()`: parse chave=valor automaticamente
- `getProperty(key)` com exceção: falha rápido se configuração ausente
- `getProperty(key, default)`: para configs opcionais
- `getIntProperty/getBooleanProperty`: conversão tipada

**Environment:**
- Padrão Singleton lazy — inicializa na primeira chamada
- `System.getProperty("env", "dev")`: lê `-Denv=xxx` da linha de comando
- Construtor privado: impede instanciação
- Métodos estáticos: acesso direto sem instanciar (`Environment.get("base.url")`)

### Fluxo de execucao

```
Test Runner inicia
    |
    v
Alguma classe chama Environment.get("base.url")
    |
    v
Environment verifica se configReader existe
    |  (primeira vez: nao existe)
    v
Le System.getProperty("env") --> "dev"
    |
    v
Cria ConfigReader("dev")
    |
    v
ConfigReader abre "environments/dev.properties"
    |
    v
Retorna "https://the-internet.herokuapp.com"
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Para testar em tempo de execução (futuro): `Environment.get("base.url")` retorna a URL do dev.properties

### Falha guiada

1. Passe um ambiente inexistente: `mvn test -Denv=producao`
   - Erro: `FrameworkException: Arquivo de configuracao nao encontrado: environments/producao.properties`

2. Remova `base.url` do dev.properties e tente acessar:
   - Erro: `FrameworkException: Propriedade 'base.url' nao encontrada`

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Arquivo nao encontrado` | Nome do .properties errado | Verifique que combina com `-Denv` |
| `NullPointerException` em getResourceAsStream | Arquivo fora do classpath | Deve estar em src/test/resources |
| `Propriedade nao encontrada` | Chave escrita diferente | Compare exatamente com o .properties |
| Valor com espaços extras | Properties não trim | Nosso código já faz trim() |

### O que nao deve ser feito

- Não hardcode URLs nos steps — sempre use Environment.get()
- Não crie um Environment por classe — é singleton compartilhado
- Não coloque credenciais sensíveis de produção no .properties commitado
- Não use encoding diferente de UTF-8 no .properties

### Exercicio

1. Adicione a propriedade `api.timeout=30` no dev.properties
2. Acesse com `Environment.getInt("api.timeout")`
3. Crie uma propriedade `screenshot.on.failure=true` e acesse com `Environment.getBoolean()`

### Checklist

- [ ] `dev.properties` em `src/test/resources/environments/`
- [ ] ConfigReader lê do classpath com getResourceAsStream
- [ ] ConfigReader lança FrameworkException para arquivo/propriedade ausente
- [ ] Environment usa System.getProperty("env", "dev")
- [ ] Environment é singleton lazy (inicializa na primeira chamada)
- [ ] Métodos get, getInt, getBoolean disponíveis
- [ ] Compila sem erros

---

## Capítulo 6 — DriverFactory e DriverManager

### Resultado que construiremos

Um sistema que cria e gerencia instâncias do WebDriver. `DriverFactory` sabe COMO criar cada browser. `DriverManager` controla o ciclo de vida (criar, obter, fechar) usando ThreadLocal para segurança em execução paralela.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| drivers/                                              |
|   +-- DriverFactory.java        <-- AQUI              |
|   +-- DriverManager.java        <-- AQUI              |
|                                                       |
| Depende de:                                           |
|   config/Environment (para ler browser e headless)    |
|   exceptions/FrameworkException                       |
|                                                       |
| Quem usa:                                             |
|   hooks/UiHooks, pages/base/BasePage                  |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**DriverFactory**: Factory Pattern — encapsula a lógica de criação de objetos. Dado um nome de browser ("chrome", "firefox"), retorna o WebDriver correspondente configurado.

**DriverManager**: gerencia o ciclo de vida do driver usando `ThreadLocal<WebDriver>`. ThreadLocal garante que cada thread tem sua própria instância, permitindo execução paralela futura.

**WebDriver**: é a interface do Selenium que controla o navegador. Cada instância é um browser aberto.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/drivers/DriverFactory.java` | Cria WebDriver por browser |
| `src/test/java/drivers/DriverManager.java` | Gerencia ciclo de vida |

### Construção manual passo a passo

1. Crie `DriverFactory` com método `createDriver(String browser)`
2. Configure ChromeDriver e FirefoxDriver com opções
3. Crie `DriverManager` com ThreadLocal
4. Exponha métodos `getDriver()`, `setDriver()`, `quitDriver()`

### Codigo completo final

**src/test/java/drivers/DriverFactory.java**

```java
package drivers;

import config.Environment;
import exceptions.FrameworkException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

import java.util.concurrent.TimeUnit;

public class DriverFactory {

    private DriverFactory() {
        // Classe utilitaria - nao instanciar
    }

    public static WebDriver createDriver() {
        String browser = Environment.get("browser", "chrome");
        boolean headless = Environment.getBoolean("headless");
        int timeout = Environment.getInt("timeout");

        WebDriver driver = initDriver(browser, headless);
        configureDriver(driver, timeout);
        return driver;
    }

    private static WebDriver initDriver(String browser, boolean headless) {
        switch (browser.toLowerCase()) {
            case "chrome":
                return createChromeDriver(headless);
            case "firefox":
                return createFirefoxDriver(headless);
            default:
                throw new FrameworkException("Browser nao suportado: " + browser);
        }
    }

    private static WebDriver createChromeDriver(boolean headless) {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--window-size=1920,1080");
        if (headless) {
            options.addArguments("--headless");
        }
        return new ChromeDriver(options);
    }

    private static WebDriver createFirefoxDriver(boolean headless) {
        FirefoxOptions options = new FirefoxOptions();
        if (headless) {
            options.addArguments("--headless");
        }
        return new FirefoxDriver(options);
    }

    private static void configureDriver(WebDriver driver, int timeout) {
        driver.manage().timeouts().implicitlyWait(timeout, TimeUnit.SECONDS);
        driver.manage().window().maximize();
    }
}
```

**src/test/java/drivers/DriverManager.java**

```java
package drivers;

import org.openqa.selenium.WebDriver;

public class DriverManager {

    private static final ThreadLocal<WebDriver> driverThread = new ThreadLocal<>();

    private DriverManager() {
        // Classe utilitaria - nao instanciar
    }

    public static WebDriver getDriver() {
        return driverThread.get();
    }

    public static void setDriver(WebDriver driver) {
        driverThread.set(driver);
    }

    public static void quitDriver() {
        WebDriver driver = driverThread.get();
        if (driver != null) {
            driver.quit();
            driverThread.remove();
        }
    }
}
```

### Explicacao do codigo

**DriverFactory:**
- `createDriver()`: método público que orquestra a criação
- `initDriver()`: switch que seleciona browser — extensível para Edge, Safari
- `createChromeDriver()`: configura ChromeOptions (no-sandbox é obrigatório em CI)
- `configureDriver()`: timeout implícito e maximize — aplicados a qualquer browser
- `--disable-dev-shm-usage`: previne crash em containers com memória limitada
- `--window-size=1920,1080`: garante layout consistente em headless

**DriverManager:**
- `ThreadLocal<WebDriver>`: cada thread tem seu próprio driver
- `getDriver()`: retorna o driver da thread atual
- `setDriver()`: armazena o driver na thread atual
- `quitDriver()`: fecha o browser E limpa o ThreadLocal (evita memory leak)
- `remove()`: essencial — sem isso o ThreadLocal vaza em thread pools

### Fluxo de execucao

```
UiHooks @Before:
    |
    v
DriverFactory.createDriver()
    |
    v
Le "browser" do Environment --> "chrome"
    |
    v
Cria ChromeDriver com options
    |
    v
DriverManager.setDriver(driver)
    |
    v
[Teste executa usando DriverManager.getDriver()]
    |
    v
UiHooks @After:
    |
    v
DriverManager.quitDriver()
    |
    v
Browser fecha + ThreadLocal limpo
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS — classes compilam sem erro
2. Verificação real acontecerá no Capítulo 9 quando o primeiro teste rodar

### Falha guiada

No `dev.properties`, mude `browser=safari` e tente criar o driver (futuro):
- Erro: `FrameworkException: Browser nao suportado: safari`

Remova `--no-sandbox` e rode em CI (Docker):
- Erro: `DevToolsActivePort file doesn't exist` — Chrome precisa do no-sandbox em containers

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `WebDriverException: cannot find chromedriver` | ChromeDriver não instalado | Use WebDriverManager ou baixe manualmente |
| `session not created: version mismatch` | ChromeDriver incompatível com Chrome | Atualize para versão correspondente |
| `DevToolsActivePort` | Falta no-sandbox em CI | Adicione --no-sandbox |
| `NullPointerException em getDriver()` | setDriver nunca chamado | Verifique que Hook inicializa |
| `ThreadLocal leak` | Não chamou remove() | quitDriver() sempre faz remove() |

### O que nao deve ser feito

- Não crie WebDriver diretamente nos steps — use DriverManager
- Não use `driver.close()` — use `driver.quit()` (close fecha só a aba, quit mata o processo)
- Não esqueça de chamar `quitDriver()` no @After — browser fica aberto
- Não use ImplicitWait + ExplicitWait juntos — causa comportamento imprevisível
- Não compartilhe WebDriver entre threads sem ThreadLocal

### Exercicio

1. Adicione suporte ao Microsoft Edge (EdgeDriver + EdgeOptions)
2. Adicione um log (`System.out.println`) mostrando qual browser foi criado
3. Experimente mudar `headless=true` no dev.properties

### Checklist

- [ ] DriverFactory com factory method createDriver()
- [ ] Suporte a Chrome e Firefox com options
- [ ] Headless configurável via properties
- [ ] Timeout implícito configurável
- [ ] DriverManager com ThreadLocal
- [ ] Métodos getDriver, setDriver, quitDriver
- [ ] quitDriver faz quit() + remove()
- [ ] Compila sem erros

---

## Capítulo 7 — LogUtils e logback.xml

### Resultado que construiremos

Um sistema de logging estruturado usando SLF4J + Logback. `LogUtils` é a fachada que toda classe do framework usa para registrar informações. `logback.xml` configura formato, nível e destino dos logs.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| utils/                                                |
|   +-- LogUtils.java             <-- AQUI              |
|                                                       |
| resources/                                            |
|   +-- logback.xml               <-- AQUI              |
|                                                       |
| Quem usa:                                             |
|   TODAS as classes do framework                       |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**SLF4J**: fachada (interface) de logging. Seu código depende apenas dela.
**Logback**: implementação que faz o log aparecer no console/arquivo.

Níveis de log (do mais detalhado ao mais grave):
- `TRACE` → detalhe fino (raramente usado)
- `DEBUG` → informação de debug
- `INFO` → fluxo normal de execução
- `WARN` → algo inesperado mas não fatal
- `ERROR` → falha que requer atenção

`LogUtils` simplifica o uso: em vez de criar Logger em cada classe, você chama `LogUtils.info("mensagem")`.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/utils/LogUtils.java` | Fachada de logging |
| `src/test/resources/logback.xml` | Configuração do Logback |

### Construção manual passo a passo

1. Crie `logback.xml` em src/test/resources
2. Configure appender de console com padrão timestamp + nível + mensagem
3. Crie `LogUtils` com métodos estáticos para cada nível

### Codigo completo final

**src/test/resources/logback.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>target/logs/framework.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>target/logs/framework-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>7</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>
        </encoder>
    </appender>

    <logger name="io.restassured" level="WARN"/>
    <logger name="org.apache.http" level="WARN"/>
    <logger name="org.openqa.selenium" level="WARN"/>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>

</configuration>
```

**src/test/java/utils/LogUtils.java**

```java
package utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LogUtils {

    private static final Logger logger = LoggerFactory.getLogger("Framework");

    private LogUtils() {
        // Classe utilitaria - nao instanciar
    }

    public static void info(String message) {
        logger.info(message);
    }

    public static void info(String message, Object... args) {
        logger.info(message, args);
    }

    public static void debug(String message) {
        logger.debug(message);
    }

    public static void debug(String message, Object... args) {
        logger.debug(message, args);
    }

    public static void warn(String message) {
        logger.warn(message);
    }

    public static void warn(String message, Object... args) {
        logger.warn(message, args);
    }

    public static void error(String message) {
        logger.error(message);
    }

    public static void error(String message, Throwable throwable) {
        logger.error(message, throwable);
    }
}
```

### Explicacao do codigo

**logback.xml:**
- `CONSOLE` appender: mostra logs no terminal durante execução
- `FILE` appender: salva em `target/logs/framework.log` com rotação
- `SizeAndTimeBasedRollingPolicy`: novo arquivo por dia ou quando atingir 10MB
- `maxHistory=7`: mantém 7 dias de log
- Loggers silenciados (`WARN`): REST Assured, Apache HTTP e Selenium são verbosos — só queremos ver warnings deles
- Root level `INFO`: mostra INFO, WARN e ERROR no console

**LogUtils:**
- Logger com nome "Framework" — aparece nos logs para identificar a origem
- Varargs `Object... args`: permite placeholders como `LogUtils.info("Abrindo pagina: {}", url)`
- SLF4J usa `{}` como placeholder (mais eficiente que concatenação)
- Método `error(String, Throwable)`: loga a exceção com stack trace completo

### Fluxo de execucao

```
LogUtils.info("Navegando para: {}", url)
    |
    v
SLF4J repassa para Logback
    |
    v
Logback aplica pattern
    |
    v
Console: 14:30:05.123 [main] INFO  Framework - Navegando para: https://...
    |
    v
Arquivo: target/logs/framework.log (mesma mensagem)
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Verificação real no Capítulo 9 — logs aparecerão no console durante teste

### Falha guiada

Remova `logback.xml` do classpath e execute um teste (futuro):

```
SLF4J: Failed to load class "ch.qos.logback.classic.LoggerContext"
SLF4J: Defaulting to no-operation (NOP) logger implementation
```

Isso mostra que sem o logback.xml, SLF4J funciona mas não imprime nada.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Failed to load class LoggerContext` | logback-classic não no classpath | Verifique dependência no pom.xml |
| `No appenders found` | logback.xml fora de resources | Mova para src/test/resources/ |
| Logs não aparecem | Level muito restritivo | Mude root level para DEBUG |
| Logs excessivos de Selenium | Selenium loga em INFO | Silencie com logger level WARN |

### O que nao deve ser feito

- Não use `System.out.println` — não tem timestamp, nível ou arquivo
- Não logue dados sensíveis (senhas, tokens) em INFO — use DEBUG
- Não silencie o root em WARN — você perderá informações de fluxo
- Não crie um Logger por método — um por classe (ou um centralizado como fizemos)

### Exercicio

1. Adicione `LogUtils.info("Iniciando teste")` em um método main temporário
2. Execute e observe o formato no console
3. Mude o root level para `DEBUG` e observe mais detalhes
4. Verifique que `target/logs/framework.log` foi criado

### Checklist

- [ ] `logback.xml` em `src/test/resources/`
- [ ] Appender CONSOLE configurado
- [ ] Appender FILE com rolling policy
- [ ] Selenium/REST Assured silenciados em WARN
- [ ] LogUtils com métodos info, debug, warn, error
- [ ] Suporte a placeholders com varargs
- [ ] Compila sem erros

---

## Capítulo 8 — BasePage e LoginPage

### Resultado que construiremos

O padrão Page Object implementado em duas camadas: `BasePage` com métodos genéricos reutilizáveis (click, type, waitForElement) e `LoginPage` que herda de BasePage e mapeia a tela de login.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| pages/                                                |
|   +-- base/                                           |
|   |   +-- BasePage.java         <-- AQUI              |
|   +-- login/                                          |
|       +-- LoginPage.java        <-- AQUI              |
|                                                       |
| Depende de:                                           |
|   drivers/DriverManager                               |
|   config/Environment                                  |
|   utils/LogUtils                                      |
|   exceptions/FrameworkException                       |
|                                                       |
| Quem usa:                                             |
|   steps/ui/LoginSteps                                 |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Page Object Pattern**: cada tela da aplicação é representada por uma classe Java. A classe:
- Mapeia os elementos da tela (locators)
- Expõe ações de negócio (login, preencherUsuario)
- Encapsula detalhes de implementação (XPath, CSS)

**BasePage**: classe abstrata com métodos que QUALQUER page object precisa:
- `click(element)` — clicar com wait
- `type(element, text)` — limpar e digitar
- `waitForElement(element)` — espera explícita
- `getText(element)` — obter texto visível

Os steps nunca interagem diretamente com WebDriver ou locators.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/pages/base/BasePage.java` | Métodos genéricos |
| `src/test/java/pages/login/LoginPage.java` | Page Object do login |

### Construção manual passo a passo

1. Crie `BasePage` com WebDriver obtido do DriverManager
2. Configure WebDriverWait no construtor
3. Implemente métodos genéricos com explicit wait
4. Crie `LoginPage` estendendo BasePage
5. Mapeie elementos com By (username, password, botão, mensagem)
6. Crie métodos de ação: fillUsername, fillPassword, clickLogin, getSuccessMessage

### Codigo completo final

**src/test/java/pages/base/BasePage.java**

```java
package pages.base;

import config.Environment;
import drivers.DriverManager;
import exceptions.FrameworkException;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import utils.LogUtils;

public abstract class BasePage {

    protected WebDriver driver;
    protected WebDriverWait wait;

    protected BasePage() {
        this.driver = DriverManager.getDriver();
        int timeout = Environment.getInt("timeout");
        this.wait = new WebDriverWait(driver, timeout);
    }

    protected void click(By locator) {
        LogUtils.debug("Clicando no elemento: {}", locator);
        waitForClickable(locator).click();
    }

    protected void type(By locator, String text) {
        LogUtils.debug("Digitando '{}' no elemento: {}", text, locator);
        WebElement element = waitForVisible(locator);
        element.clear();
        element.sendKeys(text);
    }

    protected String getText(By locator) {
        String text = waitForVisible(locator).getText();
        LogUtils.debug("Texto obtido: '{}'", text);
        return text;
    }

    protected boolean isDisplayed(By locator) {
        try {
            return waitForVisible(locator).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    protected void navigateTo(String url) {
        LogUtils.info("Navegando para: {}", url);
        driver.get(url);
    }

    protected WebElement waitForVisible(By locator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        } catch (Exception e) {
            throw new FrameworkException("Elemento nao visivel apos timeout: " + locator, e);
        }
    }

    protected WebElement waitForClickable(By locator) {
        try {
            return wait.until(ExpectedConditions.elementToBeClickable(locator));
        } catch (Exception e) {
            throw new FrameworkException("Elemento nao clicavel apos timeout: " + locator, e);
        }
    }

    public String getTitle() {
        return driver.getTitle();
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }
}
```

**src/test/java/pages/login/LoginPage.java**

```java
package pages.login;

import config.Environment;
import org.openqa.selenium.By;
import pages.base.BasePage;
import utils.LogUtils;

public class LoginPage extends BasePage {

    // Locators
    private final By inputUsername = By.id("username");
    private final By inputPassword = By.id("password");
    private final By buttonLogin = By.cssSelector("button[type='submit']");
    private final By labelSuccess = By.cssSelector(".flash.success");
    private final By labelError = By.cssSelector(".flash.error");

    // Actions
    public void openLoginPage() {
        String url = Environment.get("base.url") + "/login";
        navigateTo(url);
        LogUtils.info("Pagina de login aberta");
    }

    public void fillUsername(String username) {
        type(inputUsername, username);
    }

    public void fillPassword(String password) {
        type(inputPassword, password);
    }

    public void clickLogin() {
        click(buttonLogin);
        LogUtils.info("Botao de login clicado");
    }

    public void login(String username, String password) {
        fillUsername(username);
        fillPassword(password);
        clickLogin();
    }

    public String getSuccessMessage() {
        return getText(labelSuccess);
    }

    public String getErrorMessage() {
        return getText(labelError);
    }

    public boolean isSuccessMessageDisplayed() {
        return isDisplayed(labelSuccess);
    }
}
```

### Explicacao do codigo

**BasePage:**
- `abstract class`: não pode ser instanciada diretamente — só via herança
- `DriverManager.getDriver()`: obtém o driver da thread atual (configurado pelo Hook)
- `WebDriverWait`: espera explícita que aguarda condições (visível, clicável)
- `waitForVisible/waitForClickable`: envolvem o wait com tratamento de exceção amigável
- `type()` faz `clear()` antes — garante que o campo está vazio
- Todos os métodos logam a ação — facilita debug

**LoginPage:**
- Locators como `By` constants: centralizados no topo, fáceis de atualizar
- `openLoginPage()`: monta URL completa usando Environment
- `login()`: ação composta — preenche e clica (atalho para os steps)
- `getSuccessMessage()/getErrorMessage()`: retornam texto para assertação nos steps
- Steps NUNCA veem `By.id("username")` — só veem `loginPage.fillUsername("tom")`

### Fluxo de execucao

```
LoginSteps chama loginPage.openLoginPage()
    |
    v
BasePage.navigateTo() --> driver.get(url)
    |
    v
LoginSteps chama loginPage.login("tomsmith", "SuperSecret!")
    |
    v
LoginPage.fillUsername() --> BasePage.type(inputUsername, "tomsmith")
    |
    v
BasePage.waitForVisible() --> WebDriverWait ate elemento aparecer
    |
    v
element.clear() + element.sendKeys("tomsmith")
    |
    v
LoginPage.clickLogin() --> BasePage.click(buttonLogin)
    |
    v
LoginSteps chama loginPage.getSuccessMessage()
    |
    v
BasePage.getText(labelSuccess) --> retorna texto da flash message
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Teste real no Capítulo 9

### Falha guiada

Mude o locator para um ID inexistente:

```java
private final By inputUsername = By.id("usuario_inexistente");
```

Ao executar o teste (futuro), o erro será:
```
FrameworkException: Elemento nao visivel apos timeout: By.id: usuario_inexistente
```

Isso demonstra o valor do wrap com mensagem descritiva vs. o stacktrace críptico do Selenium.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `NullPointerException` no driver | getDriver() antes de setDriver() | Hook deve inicializar primeiro |
| `StaleElementReference` | Elemento mudou no DOM | Use locator dinâmico (not cached element) |
| `ElementNotInteractable` | Elemento coberto por outro | Use waitForClickable |
| Timeout muito curto | Aplicação lenta | Aumente timeout no .properties |
| `NoSuchElementException` | Locator errado | Inspecione elemento no DevTools |

### O que nao deve ser feito

- Não exponha WebElement nos métodos públicos — encapsule na Page
- Não use Thread.sleep() — use explicit wait
- Não coloque asserts na Page Object — asserts ficam nos steps
- Não use PageFactory (@FindBy) com Selenium 3 — tem problemas com StaleElement
- Não repita locators em várias pages — se compartilham, crie um ComponentObject

### Exercicio

1. Adicione um método `isErrorMessageDisplayed()` na LoginPage
2. Crie uma `SecureAreaPage` com locator para o botão de logout
3. Na BasePage, adicione um método `selectDropdown(By locator, String visibleText)`

### Checklist

- [ ] BasePage abstrata com driver do DriverManager
- [ ] WebDriverWait configurável via Environment
- [ ] Métodos: click, type, getText, isDisplayed, navigateTo
- [ ] waitForVisible e waitForClickable com FrameworkException
- [ ] LoginPage com locators privados e ações públicas
- [ ] Métodos fillUsername, fillPassword, clickLogin, login
- [ ] getSuccessMessage e getErrorMessage
- [ ] Logging em ações principais
- [ ] Compila sem erros

---

## Capítulo 9 — Feature de login + LoginSteps + TestRunner

### Resultado que construiremos

O primeiro teste executável do framework. Uma feature Cucumber em Gherkin, a classe de steps que implementa cada passo, e o Runner que integra Cucumber com JUnit. Ao final, `mvn test` abrirá o browser e executará o cenário de login.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| features/ui/                                          |
|   +-- login.feature            <-- AQUI               |
|                                                       |
| steps/ui/                                             |
|   +-- LoginSteps.java          <-- AQUI               |
|                                                       |
| runners/                                              |
|   +-- TestRunner.java           <-- AQUI              |
|                                                       |
| testdata/                                             |
|   +-- login.json                <-- AQUI              |
|                                                       |
| Depende de:                                           |
|   pages/login/LoginPage                               |
|   drivers/DriverFactory, DriverManager                |
|   config/Environment                                  |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Feature file**: descreve o comportamento em linguagem natural (Gherkin). Usa Given/When/Then.

**Steps**: classe Java que implementa cada linha do Gherkin com `@Given`, `@When`, `@Then`.

**TestRunner**: classe JUnit com `@RunWith(Cucumber.class)` que configura onde buscar features e steps.

**PicoContainer**: injeta dependências nos steps. Se dois steps compartilham um objeto, PicoContainer resolve automaticamente.

> **IMPORTANTE**: Neste capítulo, como os Hooks ainda não existem, incluiremos código TEMPORÁRIO para abrir e fechar o browser dentro dos steps. No Capítulo 10, esse código será removido.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/resources/features/ui/login.feature` | Cenários Gherkin |
| `src/test/java/steps/ui/LoginSteps.java` | Implementação dos steps |
| `src/test/java/runners/TestRunner.java` | Configuração do Cucumber |
| `src/test/resources/testdata/login.json` | Dados de teste |

### Construção manual passo a passo

1. Crie a feature com cenários de login com sucesso e falha
2. Crie `login.json` com credenciais de teste
3. Crie `TestRunner` com @CucumberOptions
4. Crie `LoginSteps` com código temporário de setup/teardown do driver
5. Execute `mvn test`

### Codigo completo final

**src/test/resources/features/ui/login.feature**

```gherkin
@ui @login
Feature: Login no The Internet

  Como usuario do sistema
  Quero fazer login com credenciais validas
  Para acessar a area segura

  @smoke
  Scenario: Login com credenciais validas
    Given que estou na pagina de login
    When preencho o usuario "tomsmith"
    And preencho a senha "SuperSecretPassword!"
    And clico no botao de login
    Then devo ver a mensagem de sucesso

  @negative
  Scenario: Login com senha invalida
    Given que estou na pagina de login
    When preencho o usuario "tomsmith"
    And preencho a senha "senhaerrada"
    And clico no botao de login
    Then devo ver a mensagem de erro
```

**src/test/resources/testdata/login.json**

```json
{
  "validUser": {
    "username": "tomsmith",
    "password": "SuperSecretPassword!"
  },
  "invalidUser": {
    "username": "tomsmith",
    "password": "senhaerrada"
  }
}
```

**src/test/java/runners/TestRunner.java**

```java
package runners;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"steps", "hooks"},
    plugin = {
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/cucumber-reports/cucumber.json",
        "io.qameta.allure.cucumber7jvm.AllureCucumber7Jvm"
    },
    monochrome = true,
    tags = ""
)
public class TestRunner {
}
```

**src/test/java/steps/ui/LoginSteps.java** — VERSAO TEMPORARIA

```java
package steps.ui;

// =====================================================================
// VERSAO TEMPORARIA - O codigo de setup/teardown do driver sera movido
// para hooks/UiHooks.java no Capitulo 10.
// =====================================================================

import drivers.DriverFactory;
import drivers.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;
import pages.login.LoginPage;
import utils.LogUtils;

public class LoginSteps {

    private LoginPage loginPage;

    // =====================================================================
    // TEMPORARIO: Estes metodos Before/After serao removidos no Capitulo 10
    // quando criarmos UiHooks.java
    // =====================================================================
    @Before("@ui")
    public void setup() {
        LogUtils.info("=== SETUP TEMPORARIO: Iniciando browser ===");
        DriverManager.setDriver(DriverFactory.createDriver());
        loginPage = new LoginPage();
    }

    @After("@ui")
    public void teardown() {
        LogUtils.info("=== TEARDOWN TEMPORARIO: Fechando browser ===");
        DriverManager.quitDriver();
    }
    // =====================================================================
    // FIM DO CODIGO TEMPORARIO
    // =====================================================================

    @Given("que estou na pagina de login")
    public void queEstouNaPaginaDeLogin() {
        loginPage.openLoginPage();
    }

    @When("preencho o usuario {string}")
    public void preenchoOUsuario(String username) {
        loginPage.fillUsername(username);
    }

    @When("preencho a senha {string}")
    public void preenchoASenha(String password) {
        loginPage.fillPassword(password);
    }

    @When("clico no botao de login")
    public void clicoNoBotaoDeLogin() {
        loginPage.clickLogin();
    }

    @Then("devo ver a mensagem de sucesso")
    public void devoVerAMensagemDeSucesso() {
        Assert.assertTrue(
            "Mensagem de sucesso nao exibida",
            loginPage.isSuccessMessageDisplayed()
        );
        LogUtils.info("Login realizado com sucesso - mensagem de sucesso visivel");
    }

    @Then("devo ver a mensagem de erro")
    public void devoVerAMensagemDeErro() {
        String errorMessage = loginPage.getErrorMessage();
        Assert.assertTrue(
            "Mensagem de erro nao contem texto esperado",
            errorMessage.contains("Your username is invalid!")
                || errorMessage.contains("Your password is invalid!")
        );
        LogUtils.info("Mensagem de erro exibida: {}", errorMessage);
    }
}
```

### Explicacao do codigo

**login.feature:**
- `@ui @login`: tags para filtrar execução
- `@smoke`: cenário prioritário para pipeline rápida
- `Feature/Scenario`: estrutura padrão Gherkin
- Given/When/Then: setup, ação, verificação
- `{string}` no When: captura parâmetro entre aspas

**TestRunner:**
- `@RunWith(Cucumber.class)`: JUnit delega execução ao Cucumber
- `features`: caminho das features (relativo à raiz do projeto)
- `glue`: pacotes onde buscar steps E hooks
- `plugin`: formatadores de relatório
- `monochrome`: output sem cores (melhor para CI)
- `tags = ""`: executa tudo (filtrar com `-Dcucumber.filter.tags="@smoke"`)

**LoginSteps (temporário):**
- `@Before("@ui")`: executa antes de cenários com tag @ui
- `@After("@ui")`: executa depois — garante que browser fecha
- `loginPage = new LoginPage()`: cria após driver existir
- Steps são métodos simples que delegam para LoginPage
- Asserts no `@Then` — único lugar com verificações

### Fluxo de execucao

```
mvn test
    |
    v
JUnit encontra TestRunner.java
    |
    v
Cucumber le features em src/test/resources/features
    |
    v
Para cada Scenario:
    |
    v
@Before("@ui") --> cria driver
    |
    v
Given --> loginPage.openLoginPage()
    |
    v
When --> fillUsername, fillPassword, clickLogin
    |
    v
Then --> Assert.assertTrue(...)
    |
    v
@After("@ui") --> fecha driver
    |
    v
Proximo Scenario...
    |
    v
Relatorio gerado em target/cucumber-reports/
```

### Como executar

```bash
# Todos os testes
mvn test

# Apenas cenarios com tag @smoke
mvn test -Dcucumber.filter.tags="@smoke"

# Apenas login
mvn test -Dcucumber.filter.tags="@login"
```

### Como confirmar que funcionou

```
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

O Chrome abrirá (visível se headless=false), navegará para a página de login, preencherá os campos e verificará as mensagens.

### Falha guiada

1. Remova o `glue` do Runner:
   ```
   io.cucumber.junit.CucumberOptions: No backends were found. Please make sure you have a backend module on your CLASSPATH.
   ```

2. Use uma tag inexistente: `-Dcucumber.filter.tags="@naoexiste"` — 0 cenários executados

3. Mude a senha para valor errado no step e observe o Assert falhar

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `No backends were found` | glue não aponta para pacote de steps | Corrija o glue |
| `Step undefined` | Step no Gherkin não tem match em Java | Crie o método com a annotation correta |
| `Duplicate step` | Dois métodos com mesmo padrão | Remova a duplicata |
| `0 Scenarios` | Tag filtra tudo | Verifique tags ou remova filtro |
| `Cannot instantiate class` | Construtor com parâmetros sem PicoContainer | Use construtor padrão |

### O que nao deve ser feito

- Não coloque lógica de negócio nos steps — delegue para Pages
- Não use `Thread.sleep()` nos steps — Pages já fazem explicit wait
- Não hardcode dados nos steps — use parâmetros do Gherkin ou testdata
- Não esqueça de fechar o browser no @After — deixa processos zombie
- Não misture steps de UI e API no mesmo arquivo

### Exercicio

1. Adicione um cenário `Scenario: Login com usuario invalido` 
2. Filtre execução com `-Dcucumber.filter.tags="@smoke"` e confirme que só roda 1 cenário
3. Mude `headless=true` no dev.properties e observe que o Chrome não aparece

### Checklist

- [ ] Feature com cenários Given/When/Then
- [ ] Tags @ui, @login, @smoke, @negative
- [ ] TestRunner com features, glue, plugins configurados
- [ ] LoginSteps implementa todos os steps da feature
- [ ] Setup/teardown TEMPORÁRIO funciona (driver abre e fecha)
- [ ] `mvn test` executa 2 cenários com sucesso
- [ ] Relatório HTML gerado em target/cucumber-reports/
- [ ] Código temporário claramente marcado para remoção

---

## Capítulo 10 — UiHooks e ScreenshotUtils

### Resultado que construiremos

Hooks centralizados que gerenciam o ciclo de vida do browser para TODOS os testes de UI e capturam screenshots em caso de falha. Ao final, o código temporário do Capítulo 9 será removido e os steps ficarão limpos.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| hooks/                                                |
|   +-- UiHooks.java             <-- AQUI               |
|                                                       |
| utils/                                                |
|   +-- ScreenshotUtils.java     <-- AQUI               |
|                                                       |
| Depende de:                                           |
|   drivers/DriverFactory, DriverManager                |
|   utils/LogUtils                                      |
|                                                       |
| Quem usa:                                             |
|   Cucumber (automaticamente via @Before/@After)       |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Hooks** no Cucumber são métodos `@Before` e `@After` que executam antes/depois de cada cenário. Eles ficam em classes separadas dos steps para manter responsabilidades isoladas.

**Cenário com tags**: `@Before("@ui")` só executa para cenários com tag `@ui`. Isso permite ter hooks diferentes para UI e API.

**Screenshot on failure**: o `@After` recebe o objeto `Scenario`. Se `scenario.isFailed()`, capturamos screenshot e anexamos ao relatório.

**Allure attachment**: `@Attachment` do Allure salva bytes (screenshot) no relatório.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/hooks/UiHooks.java` | @Before/@After para UI |
| `src/test/java/utils/ScreenshotUtils.java` | Captura de screenshot |
| `src/test/java/steps/ui/LoginSteps.java` | Versão FINAL (sem temporário) |

### Construção manual passo a passo

1. Crie `ScreenshotUtils` com método que retorna bytes do screenshot
2. Crie `UiHooks` com @Before e @After para tag @ui
3. No @After, verifique se cenário falhou e capture screenshot
4. REMOVA o código temporário de LoginSteps
5. Execute `mvn test` e confirme que funciona igual

### Codigo completo final

**src/test/java/utils/ScreenshotUtils.java**

```java
package utils;

import drivers.DriverManager;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class ScreenshotUtils {

    private ScreenshotUtils() {
        // Classe utilitaria - nao instanciar
    }

    public static byte[] takeScreenshot() {
        WebDriver driver = DriverManager.getDriver();
        if (driver == null) {
            LogUtils.warn("Driver nulo - nao foi possivel capturar screenshot");
            return new byte[0];
        }
        LogUtils.debug("Capturando screenshot");
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }

    public static byte[] takeScreenshotIfFailed(boolean isFailed) {
        if (isFailed) {
            LogUtils.info("Cenario falhou - capturando screenshot");
            return takeScreenshot();
        }
        return new byte[0];
    }
}
```

**src/test/java/hooks/UiHooks.java**

```java
package hooks;

import drivers.DriverFactory;
import drivers.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import io.qameta.allure.Allure;
import utils.LogUtils;
import utils.ScreenshotUtils;

import java.io.ByteArrayInputStream;

public class UiHooks {

    @Before("@ui")
    public void setUp(Scenario scenario) {
        LogUtils.info("========================================");
        LogUtils.info("Iniciando cenario: {}", scenario.getName());
        LogUtils.info("========================================");
        DriverManager.setDriver(DriverFactory.createDriver());
    }

    @After("@ui")
    public void tearDown(Scenario scenario) {
        try {
            if (scenario.isFailed()) {
                byte[] screenshot = ScreenshotUtils.takeScreenshot();
                if (screenshot.length > 0) {
                    scenario.attach(screenshot, "image/png", "screenshot-falha");
                    Allure.addAttachment("Screenshot - " + scenario.getName(),
                        new ByteArrayInputStream(screenshot));
                }
                LogUtils.error("Cenario FALHOU: {}", scenario.getName());
            } else {
                LogUtils.info("Cenario PASSOU: {}", scenario.getName());
            }
        } finally {
            DriverManager.quitDriver();
            LogUtils.info("Browser fechado");
            LogUtils.info("========================================");
        }
    }
}
```

**src/test/java/steps/ui/LoginSteps.java** — VERSAO FINAL (limpa)

```java
package steps.ui;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;
import pages.login.LoginPage;
import utils.LogUtils;

public class LoginSteps {

    private final LoginPage loginPage;

    public LoginSteps() {
        this.loginPage = new LoginPage();
    }

    @Given("que estou na pagina de login")
    public void queEstouNaPaginaDeLogin() {
        loginPage.openLoginPage();
    }

    @When("preencho o usuario {string}")
    public void preenchoOUsuario(String username) {
        loginPage.fillUsername(username);
    }

    @When("preencho a senha {string}")
    public void preenchoASenha(String password) {
        loginPage.fillPassword(password);
    }

    @When("clico no botao de login")
    public void clicoNoBotaoDeLogin() {
        loginPage.clickLogin();
    }

    @Then("devo ver a mensagem de sucesso")
    public void devoVerAMensagemDeSucesso() {
        Assert.assertTrue(
            "Mensagem de sucesso nao exibida",
            loginPage.isSuccessMessageDisplayed()
        );
        LogUtils.info("Login realizado com sucesso - mensagem de sucesso visivel");
    }

    @Then("devo ver a mensagem de erro")
    public void devoVerAMensagemDeErro() {
        String errorMessage = loginPage.getErrorMessage();
        Assert.assertTrue(
            "Mensagem de erro nao contem texto esperado",
            errorMessage.contains("Your username is invalid!")
                || errorMessage.contains("Your password is invalid!")
        );
        LogUtils.info("Mensagem de erro exibida corretamente");
    }
}
```

### Explicacao do codigo

**O que mudou nos LoginSteps:**
- REMOVIDO: `@Before("@ui")` e `@After("@ui")` — agora estão em UiHooks
- REMOVIDO: imports de DriverFactory, DriverManager, After, Before
- ADICIONADO: construtor com `new LoginPage()` (funciona porque Hook executa antes)
- Steps agora são PUROS — só lógica de teste

**ScreenshotUtils:**
- `takeScreenshot()`: cast para TakesScreenshot e captura em bytes
- Verifica driver null — previne NPE se algo deu errado antes
- Retorna `byte[]` para flexibilidade (pode salvar em arquivo ou anexar)

**UiHooks:**
- `@Before("@ui")`: cria driver antes de cada cenário com tag @ui
- `@After("@ui")`: captura screenshot se falhou, depois SEMPRE fecha driver
- `try/finally`: garante que `quitDriver()` executa mesmo com exceção
- `scenario.attach()`: anexa screenshot ao relatório Cucumber
- `Allure.addAttachment()`: anexa ao relatório Allure
- Logs marcam início/fim claramente (facilita debug em execução paralela)

### Fluxo de execucao

```
Cucumber inicia Scenario (tag @ui)
    |
    v
UiHooks.setUp() --> cria driver
    |
    v
LoginSteps constructor --> new LoginPage() (driver ja existe)
    |
    v
Given/When/Then executam
    |
    v
UiHooks.tearDown()
    |
    +-- scenario.isFailed()?
    |       |
    |       +-- SIM: takeScreenshot() + attach
    |       +-- NAO: log "PASSOU"
    |
    v
DriverManager.quitDriver() (SEMPRE executa)
```

### Como executar

```bash
mvn test
```

### Como confirmar que funcionou

1. Testes passam como antes (`Tests run: 2, Failures: 0`)
2. Logs mostram "Iniciando cenario:" e "Cenario PASSOU:"
3. Remova o código temporário dos LoginSteps e confirme que ainda funciona
4. Force uma falha (mude assert) e verifique que screenshot aparece no relatório

### Falha guiada

Para verificar screenshot on failure:

1. Mude temporariamente o assert para `Assert.fail("Forçando falha")`
2. Execute `mvn test`
3. Abra `target/cucumber-reports/cucumber.html`
4. O cenário falhado terá a imagem "screenshot-falha" anexada
5. Restaure o assert original

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `NullPointerException em LoginPage()` | Hook não executou antes | Verifique tag @ui no cenário |
| Screenshot vazio | Driver já fechou | Capture ANTES de quit |
| `ClassCastException: TakesScreenshot` | Driver custom sem interface | Use driver padrão |
| Hooks duplicados | @Before em steps E em hooks | Remova do steps |
| `Cannot attach` | Scenario sem falha | Só attach quando isFailed |

### O que nao deve ser feito

- Não deixe @Before/@After nos steps — viole separação de responsabilidades
- Não capture screenshot DEPOIS de quit — driver já morreu
- Não esqueça o try/finally — se screenshot falha, quit não executaria
- Não use @Before sem tag — executaria para steps de API também
- Não faça lógica de teste no Hook — ele só gerencia infraestrutura

### Exercicio

1. Adicione log do URL atual no @After (antes de quit) para debug
2. Force uma falha e verifique o screenshot no relatório HTML
3. Adicione um `@Before("@ui")` que verifica se o driver é null antes de criar

### Checklist

- [ ] UiHooks com @Before/@After para tag @ui
- [ ] ScreenshotUtils com takeScreenshot retornando bytes
- [ ] Screenshot capturado ANTES do quit
- [ ] Screenshot anexado a Scenario e Allure
- [ ] try/finally garante quit
- [ ] LoginSteps LIMPO — sem código de infraestrutura
- [ ] Código temporário do Cap. 9 COMPLETAMENTE removido
- [ ] `mvn test` continua passando 2 cenários
- [ ] Logs mostram início/fim de cenário

---

## Capítulo 11 — RestClient

### Resultado que construiremos

Um cliente HTTP genérico usando REST Assured que encapsula GET, POST, PUT e DELETE. Qualquer service class (PostService, UserService, etc.) usará o RestClient para fazer chamadas HTTP sem conhecer detalhes do REST Assured.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| api/                                                  |
|   +-- clients/                                        |
|       +-- RestClient.java       <-- AQUI              |
|                                                       |
| Depende de:                                           |
|   config/Environment (api.base.url)                   |
|   utils/LogUtils                                      |
|                                                       |
| Quem usa:                                             |
|   api/services/PostService                            |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**REST Assured**: biblioteca Java para testes de API REST. Usa uma DSL fluente: `given().when().then()`.

**RestClient**: wrapper que:
- Configura a base URL uma vez
- Adiciona headers padrão (Content-Type, Accept)
- Expõe métodos simples: `get(path)`, `post(path, body)`, etc.
- Retorna `Response` do REST Assured para que o service valide

**RequestSpecification**: configuração reutilizável de request (base URL, headers, auth).

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/api/clients/RestClient.java` | Cliente HTTP genérico |

### Construção manual passo a passo

1. Crie `RestClient` com construtor que lê `api.base.url` do Environment
2. Crie método privado `defaultSpec()` que monta RequestSpecification
3. Implemente GET, POST, PUT, DELETE usando REST Assured
4. Cada método retorna `Response`
5. Adicione logging de request/response

### Codigo completo final

**src/test/java/api/clients/RestClient.java**

```java
package api.clients;

import config.Environment;
import io.restassured.RestAssured;
import io.restassured.filter.log.RequestLoggingFilter;
import io.restassured.filter.log.ResponseLoggingFilter;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import utils.LogUtils;

public class RestClient {

    private final String baseUrl;

    public RestClient() {
        this.baseUrl = Environment.get("api.base.url");
        LogUtils.info("RestClient inicializado com base URL: {}", baseUrl);
    }

    private RequestSpecification defaultSpec() {
        return RestAssured
            .given()
            .baseUri(baseUrl)
            .contentType(ContentType.JSON)
            .accept(ContentType.JSON)
            .filter(new RequestLoggingFilter())
            .filter(new ResponseLoggingFilter());
    }

    public Response get(String path) {
        LogUtils.info("GET {}{}", baseUrl, path);
        return defaultSpec()
            .when()
            .get(path)
            .then()
            .extract()
            .response();
    }

    public Response get(String path, String paramName, Object paramValue) {
        LogUtils.info("GET {}{} ?{}={}", baseUrl, path, paramName, paramValue);
        return defaultSpec()
            .queryParam(paramName, paramValue)
            .when()
            .get(path)
            .then()
            .extract()
            .response();
    }

    public Response post(String path, Object body) {
        LogUtils.info("POST {}{}", baseUrl, path);
        return defaultSpec()
            .body(body)
            .when()
            .post(path)
            .then()
            .extract()
            .response();
    }

    public Response put(String path, Object body) {
        LogUtils.info("PUT {}{}", baseUrl, path);
        return defaultSpec()
            .body(body)
            .when()
            .put(path)
            .then()
            .extract()
            .response();
    }

    public Response delete(String path) {
        LogUtils.info("DELETE {}{}", baseUrl, path);
        return defaultSpec()
            .when()
            .delete(path)
            .then()
            .extract()
            .response();
    }
}
```

### Explicacao do codigo

- `baseUrl`: lido do Environment uma única vez no construtor
- `defaultSpec()`: cria uma spec limpa a cada chamada (não compartilha estado entre requests)
- `ContentType.JSON`: header `Content-Type: application/json`
- `RequestLoggingFilter/ResponseLoggingFilter`: imprime request e response no console (útil para debug)
- `extract().response()`: retorna o Response completo (status, body, headers)
- Métodos retornam `Response` — quem chama decide o que validar
- `post(path, body)`: body pode ser String JSON ou POJO (REST Assured serializa automaticamente)

**Por que wrapper em vez de REST Assured direto?**
- Centraliza headers/baseUrl (DRY)
- Se mudar de REST Assured para OkHttp, muda só aqui
- Controla logging em um lugar
- Permite interceptar (auth token, retry) sem mudar services

### Fluxo de execucao

```
PostService.createPost(payload)
    |
    v
restClient.post("/posts", payload)
    |
    v
defaultSpec() --> baseUri + headers + filters
    |
    v
REST Assured envia POST https://jsonplaceholder.typicode.com/posts
    |
    v
Response retornada (status 201, body com id)
    |
    v
PostService valida status e retorna dados
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Verificação real no Capítulo 15 quando o primeiro teste de API rodar

### Falha guiada

Mude `api.base.url` para um host inexistente:

```properties
api.base.url=https://host-inexistente-xyz.com
```

Ao executar um teste (futuro):
```
java.net.UnknownHostException: host-inexistente-xyz.com
```

Isso mostra que o RestClient usa o valor do Environment fielmente.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `UnknownHostException` | URL errada | Corrija api.base.url |
| `Connection refused` | Servidor down | Verifique se API está no ar |
| `415 Unsupported Media Type` | Falta Content-Type | defaultSpec() já define JSON |
| `Serialization error` | POJO sem getters | Adicione getters ao model |
| `SSLHandshakeException` | Certificado inválido | Adicione `relaxedHTTPSValidation()` |

### O que nao deve ser feito

- Não faça validações no RestClient — ele só transporta dados
- Não compartilhe RequestSpecification entre chamadas — crie nova a cada vez
- Não hardcode URLs — sempre use Environment
- Não remova os filters de log — sem eles é impossível debugar API
- Não capture exceções de rede — deixe falhar para aparecer no relatório

### Exercicio

1. Adicione um método `patch(String path, Object body)` para operações parciais
2. Adicione um header customizado `X-Request-Id` com UUID aleatório
3. Crie um método `getWithAuth(path, token)` que adiciona header Authorization

### Checklist

- [ ] RestClient com base URL do Environment
- [ ] Métodos GET, POST, PUT, DELETE implementados
- [ ] GET com query params
- [ ] ContentType JSON em todas as requests
- [ ] Request/Response logging com filters
- [ ] Retorna Response (não faz validação)
- [ ] Compila sem erros

---

## Capítulo 12 — JsonUtils e payloads

### Resultado que construiremos

Uma classe utilitária para ler arquivos JSON do classpath e converter entre String e objetos Java. Também criaremos os arquivos de payload que representam o corpo das requisições de API.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| utils/                                                |
|   +-- JsonUtils.java           <-- AQUI               |
|                                                       |
| resources/payloads/posts/                             |
|   +-- create-post.json         <-- AQUI               |
|   +-- update-post.json         <-- AQUI               |
|                                                       |
| Depende de:                                           |
|   exceptions/FrameworkException                       |
|                                                       |
| Quem usa:                                             |
|   api/services/PostService                            |
|   steps/api/PostSteps                                 |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Payloads**: arquivos JSON que representam o corpo de uma requisição. Mantê-los em arquivos separados (não inline no código) permite:
- Reusar em cenários diferentes
- Alterar sem recompilar
- Versionar como dado de teste

**JsonUtils**: lê o arquivo JSON do classpath e retorna como String. REST Assured aceita String JSON diretamente no `body()`.

**Por que não usar ObjectMapper aqui?** REST Assured já tem serialização embutida. Para payloads simples, ler como String é mais direto. Para modelos complexos, usamos POJOs (Capítulo 14).

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/utils/JsonUtils.java` | Leitura de JSON |
| `src/test/resources/payloads/posts/create-post.json` | Payload de criação |
| `src/test/resources/payloads/posts/update-post.json` | Payload de atualização |

### Construção manual passo a passo

1. Crie os arquivos JSON de payload
2. Crie `JsonUtils` com método para ler arquivo do classpath
3. Adicione método para substituir placeholders no JSON
4. Compile e valide

### Codigo completo final

**src/test/resources/payloads/posts/create-post.json**

```json
{
  "title": "{{title}}",
  "body": "{{body}}",
  "userId": {{userId}}
}
```

**src/test/resources/payloads/posts/update-post.json**

```json
{
  "id": {{id}},
  "title": "{{title}}",
  "body": "{{body}}",
  "userId": {{userId}}
}
```

**src/test/java/utils/JsonUtils.java**

```java
package utils;

import exceptions.FrameworkException;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Scanner;

public class JsonUtils {

    private JsonUtils() {
        // Classe utilitaria - nao instanciar
    }

    public static String readJsonFile(String path) {
        LogUtils.debug("Lendo arquivo JSON: {}", path);
        try (InputStream is = JsonUtils.class.getClassLoader().getResourceAsStream(path)) {
            if (is == null) {
                throw new FrameworkException("Arquivo JSON nao encontrado no classpath: " + path);
            }
            Scanner scanner = new Scanner(is, StandardCharsets.UTF_8.name());
            scanner.useDelimiter("\\A");
            String content = scanner.hasNext() ? scanner.next() : "";
            scanner.close();
            return content;
        } catch (IOException e) {
            throw new FrameworkException("Erro ao ler arquivo JSON: " + path, e);
        }
    }

    public static String readPayload(String relativePath) {
        return readJsonFile("payloads/" + relativePath);
    }

    public static String replacePlaceholders(String json, Map<String, String> values) {
        String result = json;
        for (Map.Entry<String, String> entry : values.entrySet()) {
            String placeholder = "{{" + entry.getKey() + "}}";
            result = result.replace(placeholder, entry.getValue());
        }
        LogUtils.debug("Payload com placeholders substituidos: {}", result);
        return result;
    }

    public static String buildPayload(String relativePath, Map<String, String> values) {
        String template = readPayload(relativePath);
        return replacePlaceholders(template, values);
    }
}
```

### Explicacao do codigo

**Payloads JSON:**
- `{{title}}`, `{{body}}`, `{{userId}}`: placeholders que serão substituídos em runtime
- Placeholders com `{{}}` e não `${}` para evitar conflito com outros template engines
- `userId` sem aspas no template — é numérico

**JsonUtils:**
- `readJsonFile(path)`: lê qualquer arquivo do classpath como String
- `getResourceAsStream`: busca em `src/test/resources` (compilado para target/test-classes)
- `Scanner("\\A")`: truque para ler o InputStream inteiro como uma única String
- `readPayload(relativePath)`: atalho que prefixa `payloads/`
- `replacePlaceholders`: substituição simples de placeholders por valores
- `buildPayload`: combina leitura + substituição (usado nos steps)

**Por que Scanner e não Files.readString?** `Files.readString` é Java 11+. Estamos em Java 8.

### Fluxo de execucao

```
PostSteps precisa criar um post
    |
    v
JsonUtils.buildPayload("posts/create-post.json", Map.of(
    "title", "Meu Post",
    "body", "Conteudo...",
    "userId", "1"
))
    |
    v
readPayload() --> le template do classpath
    |
    v
replacePlaceholders() --> substitui {{title}}, {{body}}, {{userId}}
    |
    v
Retorna: {"title": "Meu Post", "body": "Conteudo...", "userId": 1}
    |
    v
restClient.post("/posts", payload)
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Verificação real no Capítulo 15

### Falha guiada

Tente ler um arquivo inexistente:

```java
JsonUtils.readJsonFile("payloads/naoexiste.json");
```

Erro: `FrameworkException: Arquivo JSON nao encontrado no classpath: payloads/naoexiste.json`

Tente esquecer um placeholder no Map:

```java
Map<String, String> values = new HashMap<>();
values.put("title", "teste");
// esqueceu body e userId
String json = JsonUtils.buildPayload("posts/create-post.json", values);
```

O JSON resultante terá `{{body}}` e `{{userId}}` literais — a API retornará erro de validação.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Arquivo nao encontrado` | Caminho errado | Verifique que está em src/test/resources |
| JSON inválido após substituição | Aspas faltando/sobrando | Verifique template (String vs número) |
| `{{placeholder}}` literal no payload | Chave não encontrada no Map | Adicione todas as chaves necessárias |
| `NullPointerException` no Map | Valor null | Valide valores antes de passar |
| Encoding errado | Caracteres especiais | Use UTF-8 (já configurado) |

### O que nao deve ser feito

- Não hardcode JSONs como String no código Java — use arquivos
- Não use `new File()` — não funciona em classpath (funciona só no filesystem)
- Não esqueça placeholders — causa erros silenciosos de parsing
- Não coloque lógica de negócio em JsonUtils — é só leitura e substituição
- Não use este approach para payloads complexos com listas dinâmicas — use Builders (Cap 14)

### Exercicio

1. Crie um payload `payloads/posts/partial-update.json` com apenas `{"title": "{{title}}"}`
2. Adicione um método `readSchema(String name)` que lê de `schemas/`
3. Crie um teste unitário que valida que `buildPayload` substitui todos os placeholders

### Checklist

- [ ] `create-post.json` com placeholders {{title}}, {{body}}, {{userId}}
- [ ] `update-post.json` com id adicional
- [ ] JsonUtils.readJsonFile lê do classpath
- [ ] JsonUtils.readPayload prefixa caminho com payloads/
- [ ] replacePlaceholders substitui todas as chaves do Map
- [ ] buildPayload combina leitura + substituição
- [ ] FrameworkException para arquivo não encontrado
- [ ] Compila sem erros

---

## Capítulo 13 — PostService

### Resultado que construiremos

Uma classe de serviço que conhece os endpoints de posts e usa o RestClient para realizar operações CRUD. Ela é a interface entre os steps de API e o RestClient genérico.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| api/services/                                         |
|   +-- PostService.java         <-- AQUI               |
|                                                       |
| Depende de:                                           |
|   api/clients/RestClient                              |
|   utils/LogUtils                                      |
|                                                       |
| Quem usa:                                             |
|   steps/api/PostSteps                                 |
+-------------------------------------------------------+

Camada de abstracoes:

  Steps (o que testar)
    |
    v
  Service (qual endpoint chamar)
    |
    v
  RestClient (como fazer HTTP)
    |
    v
  REST Assured (detalhes de protocolo)
```

### Conceito mínimo necessário

**Service Pattern**: cada recurso da API (posts, users, comments) tem uma classe service que:
- Conhece o path do endpoint (`/posts`, `/posts/{id}`)
- Chama o RestClient com o verbo correto
- Retorna o Response para o step validar

O service NÃO valida (não faz assert). Ele apenas orquestra a chamada.

**Por que Service em vez de chamada direta?**
- Se o endpoint mudar de `/posts` para `/v2/posts`, muda só aqui
- Reuso entre cenários (criar post é usado em vários testes)
- Mantém os steps focados em validação, não em construção de request

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/api/services/PostService.java` | Operações CRUD de posts |

### Construção manual passo a passo

1. Crie `PostService` com instância de RestClient
2. Defina constante com path do endpoint
3. Implemente métodos: getAllPosts, getPost, createPost, updatePost, deletePost
4. Cada método delega para o RestClient e retorna Response

### Codigo completo final

**src/test/java/api/services/PostService.java**

```java
package api.services;

import api.clients.RestClient;
import io.restassured.response.Response;
import utils.LogUtils;

public class PostService {

    private static final String POSTS_ENDPOINT = "/posts";
    private static final String POST_BY_ID_ENDPOINT = "/posts/{id}";

    private final RestClient restClient;

    public PostService() {
        this.restClient = new RestClient();
    }

    public Response getAllPosts() {
        LogUtils.info("Buscando todos os posts");
        return restClient.get(POSTS_ENDPOINT);
    }

    public Response getPostById(int id) {
        LogUtils.info("Buscando post com id: {}", id);
        String path = POST_BY_ID_ENDPOINT.replace("{id}", String.valueOf(id));
        return restClient.get(path);
    }

    public Response getPostsByUserId(int userId) {
        LogUtils.info("Buscando posts do usuario: {}", userId);
        return restClient.get(POSTS_ENDPOINT, "userId", userId);
    }

    public Response createPost(Object body) {
        LogUtils.info("Criando novo post");
        return restClient.post(POSTS_ENDPOINT, body);
    }

    public Response updatePost(int id, Object body) {
        LogUtils.info("Atualizando post com id: {}", id);
        String path = POST_BY_ID_ENDPOINT.replace("{id}", String.valueOf(id));
        return restClient.put(path, body);
    }

    public Response deletePost(int id) {
        LogUtils.info("Deletando post com id: {}", id);
        String path = POST_BY_ID_ENDPOINT.replace("{id}", String.valueOf(id));
        return restClient.delete(path);
    }
}
```

### Explicacao do codigo

- `POSTS_ENDPOINT`: path centralizado — muda uma vez, afeta todos os métodos
- `POST_BY_ID_ENDPOINT`: template com `{id}` substituído em runtime
- `RestClient` criado no construtor — um por instância de PostService
- `createPost(Object body)`: aceita String JSON (do JsonUtils) ou POJO (do PostBuilder)
- Retorna `Response` sem processar — steps decidem o que validar
- Logging em cada operação — rastreável no console

**Separação de responsabilidades:**

| Camada | Responsabilidade | Exemplo |
|--------|-----------------|---------|
| Steps | O QUE validar | `assertEquals(201, response.statusCode())` |
| Service | QUAL endpoint | `POST /posts` |
| RestClient | COMO fazer HTTP | headers, baseUrl, filters |
| REST Assured | Protocolo | HTTP/HTTPS transport |

### Fluxo de execucao

```
PostSteps: "Quando crio um novo post"
    |
    v
postService.createPost(payload)
    |
    v
restClient.post("/posts", payload)
    |
    v
REST Assured: POST https://jsonplaceholder.typicode.com/posts
    |
    v
Response: { "id": 101, "title": "...", "body": "...", "userId": 1 }
    |
    v
PostSteps: assertEquals(201, response.statusCode())
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Teste real no Capítulo 15

### Falha guiada

Mude o endpoint para path inexistente:

```java
private static final String POSTS_ENDPOINT = "/postsXYZ";
```

Ao executar o teste (futuro), a API retornará 404 e o assert de status falhará. Isso mostra a importância de centralizar o path.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| 404 Not Found | Path errado | Verifique endpoint na documentação da API |
| `NullPointerException` no body | Body null passado | Valide body antes de chamar |
| `SerializationException` | POJO sem getters | Adicione getters ao model |
| Path com `{id}` literal | Esqueceu replace | Use String.valueOf(id) |
| Timeout | API lenta | Configure timeout no REST Assured |

### O que nao deve ser feito

- Não faça asserts no Service — ele retorna, step valida
- Não crie um RestClient por método — reutilize a instância
- Não hardcode IDs — receba como parâmetro
- Não misture lógica de UI no Service — são camadas separadas
- Não retorne tipos específicos (PostResponse) aqui — faça isso no step se necessário

### Exercicio

1. Adicione um método `getPostComments(int postId)` que chama `/posts/{id}/comments`
2. Crie uma `UserService` seguindo o mesmo padrão para `/users`
3. Adicione um overload `createPost(String title, String body, int userId)` que monta JSON inline

### Checklist

- [ ] PostService com RestClient no construtor
- [ ] Constantes para endpoints
- [ ] Métodos: getAllPosts, getPostById, getPostsByUserId
- [ ] Métodos: createPost, updatePost, deletePost
- [ ] Retorna Response (sem validação)
- [ ] Logging em cada operação
- [ ] body aceita String ou Object
- [ ] Compila sem erros

---

## Capítulo 14 — PostRequest e PostBuilder

### Resultado que construiremos

Um POJO (PostRequest) que representa o corpo de um post e um Builder com fluent API para construí-lo de forma legível. O Builder também integra JavaFaker para gerar dados aleatórios automaticamente.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| api/models/                                           |
|   +-- PostRequest.java         <-- AQUI               |
|                                                       |
| api/builders/                                         |
|   +-- PostBuilder.java         <-- AQUI               |
|                                                       |
| Depende de:                                           |
|   JavaFaker (dados aleatorios)                        |
|                                                       |
| Quem usa:                                             |
|   steps/api/PostSteps                                 |
|   api/services/PostService (como body)                |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**POJO (Plain Old Java Object)**: classe simples com atributos, getters e setters. REST Assured serializa automaticamente para JSON.

**Builder Pattern**: permite construir objetos complexos passo a passo com uma API fluente:
```java
PostRequest post = new PostBuilder().withTitle("Hello").withUserId(1).build();
```

**JavaFaker**: gera dados aleatórios realistas (nomes, endereços, textos). Cada execução usa dados diferentes, o que:
- Evita colisões em APIs reais
- Descobre bugs que dados fixos não encontram
- Torna testes mais realistas

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/api/models/PostRequest.java` | POJO do request |
| `src/test/java/api/builders/PostBuilder.java` | Builder com Faker |

### Construção manual passo a passo

1. Crie `PostRequest` com title, body, userId + getters/setters
2. Crie `PostBuilder` com métodos `with*` para cada campo
3. Adicione JavaFaker no builder para valores default
4. Implemente `build()` que retorna PostRequest preenchido

### Codigo completo final

**src/test/java/api/models/PostRequest.java**

```java
package api.models;

public class PostRequest {

    private String title;
    private String body;
    private int userId;

    public PostRequest() {
        // Construtor padrao necessario para serializacao
    }

    public PostRequest(String title, String body, int userId) {
        this.title = title;
        this.body = body;
        this.userId = userId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getBody() {
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    @Override
    public String toString() {
        return "PostRequest{" +
            "title='" + title + '\'' +
            ", body='" + body + '\'' +
            ", userId=" + userId +
            '}';
    }
}
```

**src/test/java/api/builders/PostBuilder.java**

```java
package api.builders;

import api.models.PostRequest;
import com.github.javafaker.Faker;
import utils.LogUtils;

public class PostBuilder {

    private static final Faker faker = new Faker();

    private String title;
    private String body;
    private int userId;

    public PostBuilder() {
        // Valores default com Faker
        this.title = faker.book().title();
        this.body = faker.lorem().paragraph();
        this.userId = faker.number().numberBetween(1, 10);
    }

    public PostBuilder withTitle(String title) {
        this.title = title;
        return this;
    }

    public PostBuilder withBody(String body) {
        this.body = body;
        return this;
    }

    public PostBuilder withUserId(int userId) {
        this.userId = userId;
        return this;
    }

    public PostRequest build() {
        PostRequest request = new PostRequest(title, body, userId);
        LogUtils.debug("PostRequest construido: {}", request);
        return request;
    }

    // Factory methods para cenarios comuns
    public static PostRequest defaultPost() {
        return new PostBuilder().build();
    }

    public static PostRequest postForUser(int userId) {
        return new PostBuilder().withUserId(userId).build();
    }
}
```

### Explicacao do codigo

**PostRequest:**
- Construtor vazio: necessário para deserialização (Jackson/REST Assured)
- Construtor com parâmetros: conveniência para criação direta
- Getters/Setters: REST Assured usa reflexão para serializar para JSON
- `toString()`: facilita logging e debug

**PostBuilder:**
- `Faker` estático: uma instância compartilhada (thread-safe para geração simples)
- Construtor preenche TODOS os campos com valores aleatórios
- Métodos `with*` retornam `this` (fluent API — permite encadeamento)
- `build()`: cria e retorna o PostRequest final
- `defaultPost()`: factory method estático — post aleatório com uma linha
- `postForUser(userId)`: factory com override parcial

**Exemplos de uso nos steps:**

```java
// Post totalmente aleatorio
PostRequest post = PostBuilder.defaultPost();

// Post com titulo especifico, resto aleatorio
PostRequest post = new PostBuilder()
    .withTitle("Titulo do Teste")
    .build();

// Post com tudo especificado
PostRequest post = new PostBuilder()
    .withTitle("Meu Post")
    .withBody("Conteudo do post")
    .withUserId(5)
    .build();
```

### Fluxo de execucao

```
PostSteps: "Quando crio um post com titulo 'Teste'"
    |
    v
PostRequest post = new PostBuilder()
    .withTitle("Teste")
    .build();
    |
    v
Builder preenche body com faker.lorem()
Builder preenche userId com faker.number()
Builder usa "Teste" como title (override)
    |
    v
PostRequest { title="Teste", body="Lorem ipsum...", userId=7 }
    |
    v
postService.createPost(post)
    |
    v
REST Assured serializa para JSON:
{ "title": "Teste", "body": "Lorem ipsum...", "userId": 7 }
```

### Como executar

```bash
mvn compile -DskipTests
```

### Como confirmar que funcionou

1. BUILD SUCCESS
2. Verificação real no Capítulo 15

### Falha guiada

Remova o getter `getTitle()` e tente serializar com REST Assured:

```
Response body: {"body": "...", "userId": 1}
```

O campo `title` desaparece do JSON — REST Assured só serializa propriedades com getter. Isso mostra por que os getters são obrigatórios.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| Campo ausente no JSON | Getter faltando | Adicione getter para o campo |
| `null` no JSON | Setter chamado com null | Valide no builder |
| Faker gera texto enorme | Parágrafo longo demais | Use `faker.lorem().sentence()` |
| `StackOverflowError` | toString com referência circular | Não inclua relações bidirecionais |
| Builder sem reset | Valores da chamada anterior | Sempre use `new PostBuilder()` |

### O que nao deve ser feito

- Não reutilize instância de Builder — crie nova a cada post
- Não omita getters — serialização depende deles
- Não use campos públicos — quebra encapsulamento
- Não coloque lógica de validação no POJO — ele é só transporte
- Não faça Builder retornar campos opcionais como null — use valores default

### Exercicio

1. Crie um `PostResponse` com id, title, body, userId para deserialização
2. Adicione ao PostBuilder um método `withRandomTitle(int maxWords)` usando Faker
3. Crie um `UserBuilder` para um futuro endpoint de usuarios

### Checklist

- [ ] PostRequest com title, body, userId
- [ ] Construtor vazio + construtor com parâmetros
- [ ] Getters e setters para todos os campos
- [ ] toString() implementado
- [ ] PostBuilder com valores default do Faker
- [ ] Métodos with* retornando this (fluent)
- [ ] build() retorna PostRequest
- [ ] Factory methods defaultPost() e postForUser()
- [ ] Compila sem erros

---

## Capítulo 15 — Feature de API + PostSteps + ApiHooks

### Resultado que construiremos

O teste de API completo: feature Gherkin para posts, steps que chamam o PostService, e hooks específicos para API. Este capítulo já inclui o step de schema validation que será detalhado no Capítulo 16.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| features/api/                                         |
|   +-- posts.feature            <-- AQUI               |
|                                                       |
| steps/api/                                            |
|   +-- PostSteps.java           <-- AQUI               |
|                                                       |
| hooks/                                                |
|   +-- ApiHooks.java            <-- AQUI               |
|                                                       |
| Depende de:                                           |
|   api/services/PostService                            |
|   api/builders/PostBuilder                            |
|   api/models/PostRequest                              |
|   utils/JsonUtils                                     |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Testes de API** não precisam de browser. São mais rápidos, mais estáveis e devem ser a maioria dos seus testes automatizados.

**ApiHooks**: mais leves que UiHooks — apenas configuram logging e podem resetar estado entre cenários.

**Schema Validation**: valida que o JSON de resposta segue um contrato (schema). Isso garante que novos campos não foram removidos e tipos não mudaram.

A feature exercita:
- GET (listar e buscar por ID)
- POST (criar)
- PUT (atualizar)
- DELETE (remover)
- Schema validation

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/resources/features/api/posts.feature` | Cenários de API |
| `src/test/java/steps/api/PostSteps.java` | Steps de API |
| `src/test/java/hooks/ApiHooks.java` | Hooks de API |

### Construção manual passo a passo

1. Crie a feature com cenários CRUD
2. Crie `ApiHooks` com @Before/@After para tag @api
3. Crie `PostSteps` implementando cada step
4. Execute `mvn test -Dcucumber.filter.tags="@api"`

### Codigo completo final

**src/test/resources/features/api/posts.feature**

```gherkin
@api @posts
Feature: CRUD de Posts via API

  Como consumidor da API
  Quero gerenciar posts
  Para validar que a API funciona corretamente

  @smoke
  Scenario: Listar todos os posts
    When envio GET para listar posts
    Then o status code deve ser 200
    And a resposta deve conter uma lista de posts

  Scenario: Buscar post por ID
    When envio GET para buscar o post com id 1
    Then o status code deve ser 200
    And a resposta deve conter o post com id 1

  @smoke
  Scenario: Criar um novo post
    Given que tenho um payload de post valido
    When envio POST para criar o post
    Then o status code deve ser 201
    And a resposta deve conter o titulo do post criado

  Scenario: Atualizar um post existente
    Given que tenho um payload de post atualizado
    When envio PUT para atualizar o post com id 1
    Then o status code deve ser 200
    And a resposta deve conter o titulo atualizado

  Scenario: Deletar um post
    When envio DELETE para remover o post com id 1
    Then o status code deve ser 200

  @schema
  Scenario: Validar schema do post
    When envio GET para buscar o post com id 1
    Then o status code deve ser 200
    And a resposta deve estar de acordo com o schema "post-schema.json"
```

**src/test/java/hooks/ApiHooks.java**

```java
package hooks;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import utils.LogUtils;

public class ApiHooks {

    @Before("@api")
    public void setUp(Scenario scenario) {
        LogUtils.info("========================================");
        LogUtils.info("[API] Iniciando cenario: {}", scenario.getName());
        LogUtils.info("========================================");
    }

    @After("@api")
    public void tearDown(Scenario scenario) {
        if (scenario.isFailed()) {
            LogUtils.error("[API] Cenario FALHOU: {}", scenario.getName());
        } else {
            LogUtils.info("[API] Cenario PASSOU: {}", scenario.getName());
        }
        LogUtils.info("========================================");
    }
}
```

**src/test/java/steps/api/PostSteps.java**

```java
package steps.api;

import api.builders.PostBuilder;
import api.models.PostRequest;
import api.services.PostService;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;
import io.restassured.response.Response;
import org.junit.Assert;
import utils.LogUtils;

import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;

public class PostSteps {

    private final PostService postService;
    private PostRequest postRequest;
    private Response response;

    public PostSteps() {
        this.postService = new PostService();
    }

    // === GIVEN ===

    @Given("que tenho um payload de post valido")
    public void queTenhoUmPayloadDePostValido() {
        postRequest = PostBuilder.defaultPost();
        LogUtils.info("Payload criado: {}", postRequest);
    }

    @Given("que tenho um payload de post atualizado")
    public void queTenhoUmPayloadDePostAtualizado() {
        postRequest = new PostBuilder()
            .withTitle("Titulo Atualizado")
            .withBody("Body atualizado via PUT")
            .withUserId(1)
            .build();
        LogUtils.info("Payload de atualizacao criado: {}", postRequest);
    }

    // === WHEN ===

    @When("envio GET para listar posts")
    public void envioGetParaListarPosts() {
        response = postService.getAllPosts();
    }

    @When("envio GET para buscar o post com id {int}")
    public void envioGetParaBuscarPostComId(int id) {
        response = postService.getPostById(id);
    }

    @When("envio POST para criar o post")
    public void envioPostParaCriarOPost() {
        response = postService.createPost(postRequest);
    }

    @When("envio PUT para atualizar o post com id {int}")
    public void envioPutParaAtualizarPostComId(int id) {
        response = postService.updatePost(id, postRequest);
    }

    @When("envio DELETE para remover o post com id {int}")
    public void envioDeleteParaRemoverPostComId(int id) {
        response = postService.deletePost(id);
    }

    // === THEN ===

    @Then("o status code deve ser {int}")
    public void oStatusCodeDeveSer(int expectedStatus) {
        int actualStatus = response.getStatusCode();
        LogUtils.info("Status code esperado: {} | recebido: {}", expectedStatus, actualStatus);
        Assert.assertEquals(
            "Status code diferente do esperado",
            expectedStatus,
            actualStatus
        );
    }

    @Then("a resposta deve conter uma lista de posts")
    public void aRespostaDeveConterUmaListaDePosts() {
        int size = response.jsonPath().getList("$").size();
        LogUtils.info("Quantidade de posts retornados: {}", size);
        Assert.assertTrue("Lista de posts esta vazia", size > 0);
    }

    @Then("a resposta deve conter o post com id {int}")
    public void aRespostaDeveConterOPostComId(int expectedId) {
        int actualId = response.jsonPath().getInt("id");
        Assert.assertEquals("ID do post diferente", expectedId, actualId);
    }

    @Then("a resposta deve conter o titulo do post criado")
    public void aRespostaDeveConterOTituloDoPostCriado() {
        String actualTitle = response.jsonPath().getString("title");
        Assert.assertEquals(
            "Titulo do post criado nao confere",
            postRequest.getTitle(),
            actualTitle
        );
        LogUtils.info("Post criado com titulo: {}", actualTitle);
    }

    @Then("a resposta deve conter o titulo atualizado")
    public void aRespostaDeveConterOTituloAtualizado() {
        String actualTitle = response.jsonPath().getString("title");
        Assert.assertEquals(
            "Titulo atualizado nao confere",
            postRequest.getTitle(),
            actualTitle
        );
    }

    @Then("a resposta deve estar de acordo com o schema {string}")
    public void aRespostaDeveEstarDeAcordoComOSchema(String schemaFile) {
        LogUtils.info("Validando resposta contra schema: {}", schemaFile);
        response.then().assertThat()
            .body(matchesJsonSchemaInClasspath("schemas/" + schemaFile));
        LogUtils.info("Schema validation PASSOU");
    }
}
```

### Explicacao do codigo

**posts.feature:**
- `@api @posts`: tags para filtro — nunca abre browser
- Cenários cobrem todo o CRUD + schema
- Parâmetros `{int}` e `{string}` capturam valores dinâmicos
- `@smoke`: cenários prioritários para CI rápida

**ApiHooks:**
- Mais simples que UiHooks — sem driver, sem screenshot
- Apenas logging para rastreabilidade
- `@Before("@api")`: só executa para cenários com tag @api

**PostSteps:**
- `PostService` no construtor — serviço de API
- `postRequest` e `response` como estado do cenário — compartilhados entre steps
- Given prepara dados, When executa ação, Then valida resultado
- `response.jsonPath()`: acessa campos do JSON com expressão path
- Schema validation: `matchesJsonSchemaInClasspath` valida contra arquivo em resources
- Assert com mensagens descritivas — facilita diagnóstico de falha

### Fluxo de execucao

```
mvn test -Dcucumber.filter.tags="@api"
    |
    v
Cucumber encontra posts.feature
    |
    v
Para cada Scenario:
    |
    v
ApiHooks.setUp() --> log "Iniciando cenario"
    |
    v
Given --> prepara payload (PostBuilder)
    |
    v
When --> chama PostService --> RestClient --> API
    |
    v
Then --> valida status, body, schema
    |
    v
ApiHooks.tearDown() --> log resultado
```

### Como executar

```bash
# Apenas testes de API
mvn test -Dcucumber.filter.tags="@api"

# Apenas smoke (UI + API)
mvn test -Dcucumber.filter.tags="@smoke"

# Todos os testes
mvn test
```

### Como confirmar que funcionou

```
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

Nos logs, você verá as requisições HTTP (request e response) graças aos filters do RestClient.

> **Nota**: O cenário de schema validation falhará até criarmos o arquivo `post-schema.json` no Capítulo 16. Execute com `-Dcucumber.filter.tags="@api and not @schema"` até lá.

### Falha guiada

1. Mude o expected status para valor errado:
   ```
   AssertionError: Status code diferente do esperado expected:<200> but was:<201>
   ```

2. Crie post com userId null:
   ```
   PostRequest { title="...", body="...", userId=0 }
   ```
   A API aceita (jsonplaceholder é permissiva), mas uma API real retornaria 422.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Step undefined` | Texto do Gherkin não bate com annotation | Compare exatamente |
| `NullPointerException em response` | When não executou | Verifique ordem dos steps |
| `Connection refused` | API fora do ar | Verifique URL no dev.properties |
| Schema validation falha | Schema inexistente | Crie no Capítulo 16 |
| `AssertionError: Lists differ` | API mudou resposta | Atualize expectativas |

### O que nao deve ser feito

- Não misture steps de UI e API na mesma classe
- Não crie dependência entre cenários (um cria post, outro busca) — são independentes
- Não hardcode IDs que podem não existir em API real
- Não ignore o schema validation — é o contrato da API
- Não faça setup/teardown pesado no ApiHooks — API não precisa de browser

### Exercicio

1. Adicione cenário: "Buscar posts por userId"
2. Adicione cenário negativo: "Buscar post com id inexistente" (espere 404)
3. Crie uma Scenario Outline com Examples para testar vários IDs

### Checklist

- [ ] Feature com cenários CRUD (GET, POST, PUT, DELETE)
- [ ] Tags @api, @posts, @smoke, @schema
- [ ] ApiHooks com @Before/@After para @api
- [ ] PostSteps com estado compartilhado (postRequest, response)
- [ ] Validação de status code
- [ ] Validação de body com jsonPath
- [ ] Step de schema validation (usando matchesJsonSchemaInClasspath)
- [ ] `mvn test -Dcucumber.filter.tags="@api and not @schema"` passa
- [ ] Logs mostram request/response HTTP

---

## Capítulo 16 — JSON Schema Validation

### Resultado que construiremos

Um arquivo JSON Schema que define o contrato do endpoint de posts. Ao final, o cenário com tag `@schema` do Capítulo 15 passará, validando que a resposta da API segue a estrutura esperada.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| resources/schemas/                                    |
|   +-- post-schema.json         <-- AQUI               |
|                                                       |
| Quem usa:                                             |
|   steps/api/PostSteps (matchesJsonSchemaInClasspath)  |
|                                                       |
| Depende de:                                           |
|   rest-assured json-schema-validator (pom.xml)        |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**JSON Schema**: é uma especificação que define a estrutura esperada de um JSON. Funciona como um "contrato":
- Quais campos são obrigatórios
- Qual o tipo de cada campo (string, integer, array)
- Limites de valores (minLength, maximum)

**Por que validar schema?**
- Detecta regressão: se a API remove um campo, o schema falha
- Documenta o contrato: devs e QAs sabem o que esperar
- Independe de dados: valida ESTRUTURA, não VALORES

**json-schema-validator do REST Assured**: compara o body da response contra um arquivo .json schema no classpath.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/resources/schemas/post-schema.json` | Contrato do endpoint GET /posts/{id} |

### Construção manual passo a passo

1. Faça uma chamada GET /posts/1 e observe a resposta
2. Mapeie os campos e tipos no formato JSON Schema Draft-07
3. Salve em `src/test/resources/schemas/post-schema.json`
4. Execute o cenário @schema e confirme que passa

### Codigo completo final

**Resposta real de GET /posts/1 (referência):**

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati...",
  "body": "quia et suscipit\nsuscipit recusandae..."
}
```

**src/test/resources/schemas/post-schema.json**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Post",
  "description": "Schema de validacao para o recurso Post",
  "type": "object",
  "required": ["userId", "id", "title", "body"],
  "properties": {
    "userId": {
      "type": "integer",
      "description": "ID do usuario autor do post",
      "minimum": 1
    },
    "id": {
      "type": "integer",
      "description": "ID unico do post",
      "minimum": 1
    },
    "title": {
      "type": "string",
      "description": "Titulo do post",
      "minLength": 1
    },
    "body": {
      "type": "string",
      "description": "Conteudo do post",
      "minLength": 1
    }
  },
  "additionalProperties": false
}
```

**Como o step usa (já implementado no Capítulo 15):**

```java
@Then("a resposta deve estar de acordo com o schema {string}")
public void aRespostaDeveEstarDeAcordoComOSchema(String schemaFile) {
    LogUtils.info("Validando resposta contra schema: {}", schemaFile);
    response.then().assertThat()
        .body(matchesJsonSchemaInClasspath("schemas/" + schemaFile));
    LogUtils.info("Schema validation PASSOU");
}
```

### Explicacao do codigo

**JSON Schema:**
- `$schema`: versão do JSON Schema (draft-07 é amplamente suportada)
- `type: "object"`: a resposta raiz é um objeto JSON
- `required`: campos que DEVEM estar presentes (se um sumir, falha)
- `properties`: define o tipo e restrições de cada campo
- `type: "integer"`: valida que userId e id são números inteiros
- `type: "string"`: valida que title e body são textos
- `minimum: 1`: IDs devem ser positivos
- `minLength: 1`: textos não podem ser vazios
- `additionalProperties: false`: proíbe campos não declarados (schema estrito)

**Decisão de design — strict vs permissive:**
- `additionalProperties: false` → schema ESTRITO — falha se API adicionar campo novo
- `additionalProperties: true` → schema PERMISSIVO — aceita campos extras

Para testes de contrato, recomenda-se ESTRITO. Para testes de integração, pode ser PERMISSIVO.

### Fluxo de execucao

```
PostSteps: "a resposta deve estar de acordo com o schema 'post-schema.json'"
    |
    v
matchesJsonSchemaInClasspath("schemas/post-schema.json")
    |
    v
REST Assured le o schema de src/test/resources/schemas/
    |
    v
Compara body da response com o schema
    |
    v
Todos os campos presentes? Tipos corretos? Restricoes atendidas?
    |
    +-- SIM: step passa
    +-- NAO: AssertionError com detalhes do campo que violou
```

### Como executar

```bash
# Agora o cenario @schema funciona
mvn test -Dcucumber.filter.tags="@schema"

# Ou todos os de API
mvn test -Dcucumber.filter.tags="@api"
```

### Como confirmar que funcionou

```
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

Log mostrará: `Schema validation PASSOU`

### Falha guiada

1. Adicione um campo inexistente ao `required`:

```json
"required": ["userId", "id", "title", "body", "campoInexistente"]
```

Erro:
```
AssertionError: object has missing required properties (["campoInexistente"])
```

2. Mude o tipo de `userId` para `"string"`:

```json
"userId": { "type": "string" }
```

Erro:
```
AssertionError: instance type (integer) does not match any allowed primitive type (allowed: ["string"])
```

3. Remova `additionalProperties: false` e observe que o schema aceita qualquer campo extra.

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Schema file not found` | Arquivo fora do classpath | Verifique caminho em src/test/resources/schemas |
| `missing required properties` | Campo não presente na response | Atualize schema ou investigue API |
| `type does not match` | Campo com tipo diferente | Corrija tipo no schema |
| `additionalProperties` falha | Campo extra na response | Adicione ao schema ou use true |
| `null value` para campo required | API retorna null | Use `"type": ["string", "null"]` |

### O que nao deve ser feito

- Não crie schemas manualmente sem observar a API real — use uma response como base
- Não use draft-03 ou draft-04 — REST Assured suporta draft-07 melhor
- Não valide dados de negócio no schema — schema é ESTRUTURA, steps validam VALORES
- Não ignore falhas de schema — são regressões de contrato
- Não use schema genérico para todos os endpoints — cada um tem seu contrato

### Exercicio

1. Crie `schemas/posts-list-schema.json` para validar o array de GET /posts
2. Adicione constraint `"maxLength": 500` ao title e veja se a API respeita
3. Crie um schema para o endpoint de criação (POST response que tem id)

### Checklist

- [ ] `post-schema.json` em `src/test/resources/schemas/`
- [ ] Draft-07 declarado no $schema
- [ ] Campos required: userId, id, title, body
- [ ] Tipos validados: integer e string
- [ ] Restrições: minimum e minLength
- [ ] additionalProperties definido (true ou false)
- [ ] Cenário @schema passa com sucesso
- [ ] `mvn test -Dcucumber.filter.tags="@api"` sem falhas

---

## Capítulo 17 — Ambiente HML

### Resultado que construiremos

Um segundo arquivo de configuração para homologação (HML), demonstrando como o framework suporta múltiplos ambientes sem alterar código. Ao final, `mvn test -Denv=hml` usará URLs, credenciais e configurações diferentes.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| resources/environments/                               |
|   +-- dev.properties           (ja existe)            |
|   +-- hml.properties           <-- AQUI               |
|                                                       |
| config/                                               |
|   +-- ConfigReader.java        (le baseado em -Denv)  |
|   +-- Environment.java         (fachada)              |
+-------------------------------------------------------+

Fluxo:
  mvn test -Denv=hml
      |
      v
  System.getProperty("env") --> "hml"
      |
      v
  ConfigReader("hml") --> le hml.properties
      |
      v
  Environment.get("base.url") --> URL de HML
```

### Conceito mínimo necessário

**Multi-ambiente**: o mesmo código roda contra ambientes diferentes apenas mudando uma variável. Isso permite:
- Desenvolvimento local (dev) — aplicação local ou stub
- Homologação (hml) — ambiente compartilhado com equipe
- Staging (stg) — espelho de produção

Cada ambiente tem suas URLs, credenciais, timeouts e configurações de browser.

**Nenhum código muda** — apenas o parâmetro `-Denv` na linha de comando.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/resources/environments/hml.properties` | Configuração de HML |

### Construção manual passo a passo

1. Copie `dev.properties` para `hml.properties`
2. Altere as URLs para apontar para HML
3. Ajuste timeout (HML geralmente é mais lento)
4. Ajuste headless (HML geralmente roda em CI)
5. Execute com `-Denv=hml`

### Codigo completo final

**src/test/resources/environments/hml.properties**

```properties
# === Ambiente de Homologacao ===

# UI
base.url=https://the-internet.herokuapp.com
browser=chrome
timeout=15
headless=true

# API
api.base.url=https://jsonplaceholder.typicode.com
api.timeout=30

# Credenciais (diferentes de DEV em projetos reais)
username=tomsmith
password=SuperSecretPassword!

# Configuracoes de execucao
screenshot.on.failure=true
retry.count=1
```

**Comparação DEV vs HML:**

| Propriedade | DEV | HML |
|-------------|-----|-----|
| `base.url` | https://the-internet.herokuapp.com | https://the-internet.herokuapp.com |
| `browser` | chrome | chrome |
| `timeout` | 10 | 15 |
| `headless` | false | true |
| `api.timeout` | (não definido) | 30 |
| `screenshot.on.failure` | (não definido) | true |
| `retry.count` | (não definido) | 1 |

> **Nota**: Neste exemplo, as URLs são as mesmas porque usamos aplicações públicas. Em um projeto real, DEV apontaria para `http://localhost:8080` e HML para `https://hml.suaempresa.com`.

### Explicacao do codigo

**Diferenças estratégicas entre ambientes:**

- `timeout=15`: HML costuma ser mais lento (ambiente compartilhado)
- `headless=true`: em HML geralmente executamos em CI (sem monitor)
- `api.timeout=30`: APIs de HML podem ter throttling
- `retry.count=1`: permite uma retry em ambiente instável
- `screenshot.on.failure=true`: útil para debug remoto

**Como usar propriedades novas (exemplo de retry):**

```java
// Em UiHooks ou num RetryAnalyzer futuro
int retries = Environment.getInt("retry.count");
```

O método `Environment.get(key, defaultValue)` permite leitura segura:

```java
// Se a propriedade nao existe no dev.properties, usa 0
int retries = Integer.parseInt(Environment.get("retry.count", "0"));
```

### Fluxo de execucao

```
Terminal: mvn test -Denv=hml
    |
    v
Maven seta System property: env=hml
    |
    v
Environment.getConfigReader()
    |
    v
System.getProperty("env", "dev") --> "hml"
    |
    v
new ConfigReader("hml")
    |
    v
Abre environments/hml.properties
    |
    v
Properties carregadas: timeout=15, headless=true, ...
    |
    v
DriverFactory.createDriver()
    |
    v
Environment.getBoolean("headless") --> true
    |
    v
Chrome abre em modo headless
```

### Como executar

```bash
# Ambiente DEV (padrao)
mvn test

# Ambiente HML
mvn test -Denv=hml

# HML com filtro de tag
mvn test -Denv=hml -Dcucumber.filter.tags="@smoke"
```

### Como confirmar que funcionou

1. Execute com `-Denv=hml` e observe nos logs que `headless=true` foi aplicado
2. O Chrome NÃO aparece visualmente (está headless)
3. Os testes passam normalmente
4. Mude `-Denv=dev` e o Chrome aparece (headless=false)

### Falha guiada

1. Execute com ambiente inexistente:

```bash
mvn test -Denv=producao
```

Erro: `FrameworkException: Arquivo de configuracao nao encontrado: environments/producao.properties`

2. Remova `base.url` do hml.properties:

```bash
mvn test -Denv=hml
```

Erro: `FrameworkException: Propriedade 'base.url' nao encontrada no arquivo de configuracao`

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| Arquivo não encontrado | Nome errado | Verifique que hml.properties está em environments/ |
| Testes falham em HML | URLs diferentes | Verifique que a aplicação está no ar |
| Headless não funciona | ChromeDriver antigo | Atualize ChromeDriver |
| Timeout em HML | Ambiente lento | Aumente timeout no hml.properties |
| Credenciais incorretas | Usuário diferente em HML | Atualize username/password |

### O que nao deve ser feito

- Não commite credenciais de produção no repositório
- Não crie um if/else no código para cada ambiente — use .properties
- Não deixe propriedades faltando em um .properties — cause erro explícito
- Não assuma que DEV e HML têm os mesmos dados — use dados dinâmicos (Faker)
- Não ignore timeouts diferentes — HML e CI são mais lentos

### Exercicio

1. Crie um `stg.properties` para staging com headless=true e timeout=20
2. Adicione propriedade `parallel=true` no hml.properties para futuro uso
3. Execute os mesmos testes com `-Denv=dev` e `-Denv=hml` e compare os tempos

### Checklist

- [ ] `hml.properties` em `src/test/resources/environments/`
- [ ] Todas as propriedades obrigatórias presentes
- [ ] Timeout maior que DEV
- [ ] Headless = true
- [ ] `mvn test -Denv=hml` executa com sucesso
- [ ] Chrome não aparece (headless)
- [ ] Logs confirmam ambiente HML
- [ ] Propriedades extras (retry, screenshot) com valores default seguros

---

## Capítulo 18 — Allure Report

### Resultado que construiremos

Relatórios Allure visuais e interativos gerados automaticamente após execução dos testes. Ao final, `allure serve` abrirá um dashboard com gráficos, timeline, steps detalhados e screenshots de falha.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| Allure Ecosystem                                      |
|                                                       |
| pom.xml:                                              |
|   +-- allure-cucumber7-jvm (captura steps)            |
|   +-- allure-rest-assured (captura requests)          |
|   +-- aspectjweaver (intercepta annotations)          |
|                                                       |
| TestRunner.java:                                      |
|   +-- plugin: AllureCucumber7Jvm                      |
|                                                       |
| UiHooks.java:                                         |
|   +-- Allure.addAttachment (screenshots)              |
|                                                       |
| Output:                                               |
|   +-- target/allure-results/ (dados brutos)           |
|   +-- allure-report/ (HTML gerado)    <-- AQUI        |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**Allure** é um framework de relatórios que gera dashboards a partir de dados brutos. Funciona em duas fases:
1. **Coleta**: durante execução, plugins salvam JSONs em `target/allure-results/`
2. **Geração**: depois, o CLI do Allure transforma JSONs em HTML interativo

**O que já configuramos nos capítulos anteriores:**
- pom.xml: dependências allure-cucumber7-jvm + allure-rest-assured + aspectjweaver
- TestRunner: plugin `AllureCucumber7Jvm`
- UiHooks: `Allure.addAttachment` para screenshots

Falta: instalar o CLI do Allure e integrar com `allure-rest-assured` filter.

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `src/test/java/api/clients/RestClient.java` | Adicionar Allure filter |
| Configuração do Allure CLI | Gerar relatórios |

### Construção manual passo a passo

1. Instale o Allure CLI
2. Adicione o filter do Allure no RestClient
3. Execute os testes
4. Gere o relatório com `allure serve`

### Codigo completo final

**Instalação do Allure CLI (escolha uma opção):**

```bash
# Opcao 1: via npm (mais simples)
npm install -g allure-commandline

# Opcao 2: via Homebrew (macOS)
brew install allure

# Opcao 3: via Scoop (Windows)
scoop install allure
```

**Atualização em src/test/java/api/clients/RestClient.java** — adicione o import e filter:

```java
package api.clients;

import config.Environment;
import io.qameta.allure.restassured.AllureRestAssured;
import io.restassured.RestAssured;
import io.restassured.filter.log.RequestLoggingFilter;
import io.restassured.filter.log.ResponseLoggingFilter;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import utils.LogUtils;

public class RestClient {

    private final String baseUrl;

    public RestClient() {
        this.baseUrl = Environment.get("api.base.url");
        LogUtils.info("RestClient inicializado com base URL: {}", baseUrl);
    }

    private RequestSpecification defaultSpec() {
        return RestAssured
            .given()
            .baseUri(baseUrl)
            .contentType(ContentType.JSON)
            .accept(ContentType.JSON)
            .filter(new AllureRestAssured())
            .filter(new RequestLoggingFilter())
            .filter(new ResponseLoggingFilter());
    }

    public Response get(String path) {
        LogUtils.info("GET {}{}", baseUrl, path);
        return defaultSpec()
            .when()
            .get(path)
            .then()
            .extract()
            .response();
    }

    public Response get(String path, String paramName, Object paramValue) {
        LogUtils.info("GET {}{} ?{}={}", baseUrl, path, paramName, paramValue);
        return defaultSpec()
            .queryParam(paramName, paramValue)
            .when()
            .get(path)
            .then()
            .extract()
            .response();
    }

    public Response post(String path, Object body) {
        LogUtils.info("POST {}{}", baseUrl, path);
        return defaultSpec()
            .body(body)
            .when()
            .post(path)
            .then()
            .extract()
            .response();
    }

    public Response put(String path, Object body) {
        LogUtils.info("PUT {}{}", baseUrl, path);
        return defaultSpec()
            .body(body)
            .when()
            .put(path)
            .then()
            .extract()
            .response();
    }

    public Response delete(String path) {
        LogUtils.info("DELETE {}{}", baseUrl, path);
        return defaultSpec()
            .when()
            .delete(path)
            .then()
            .extract()
            .response();
    }
}
```

**A única mudança é adicionar:**
```java
import io.qameta.allure.restassured.AllureRestAssured;
```

E no `defaultSpec()`:
```java
.filter(new AllureRestAssured())
```

Isso faz o Allure capturar request e response de cada chamada API automaticamente.

### Explicacao do codigo

**Fluxo do Allure:**

```
Teste executa
    |
    +-- AllureCucumber7Jvm captura cada step (Given, When, Then)
    |
    +-- AllureRestAssured captura cada request/response HTTP
    |
    +-- Allure.addAttachment captura screenshots
    |
    v
target/allure-results/
    +-- xxxxx-result.json (um por cenario)
    +-- xxxxx-attachment.png (screenshots)
    +-- xxxxx-attachment.txt (request/response)
    |
    v
allure serve target/allure-results
    |
    v
Browser abre com dashboard interativo
```

**O que aparece no relatório:**
- Overview: gráfico de pizza (passed/failed/broken)
- Suites: agrupamento por feature
- Timeline: duração de cada cenário
- Behaviors: agrupamento por tag
- Cada cenário: steps expandíveis com timing
- Steps de API: request e response completos
- Falhas de UI: screenshot anexado

### Fluxo de execucao

```
mvn test
    |
    v
Testes executam, Allure coleta dados
    |
    v
target/allure-results/ preenchido com JSONs
    |
    v
allure serve target/allure-results
    |
    v
Allure CLI le JSONs e gera HTML
    |
    v
Browser abre em http://localhost:XXXX
    |
    v
Dashboard interativo
```

### Como executar

```bash
# 1. Execute os testes
mvn test

# 2. Gere e abra o relatorio (serve = gera + abre)
allure serve target/allure-results

# OU gere sem abrir (para CI)
allure generate target/allure-results -o target/allure-report --clean
```

### Como confirmar que funcionou

1. Após `mvn test`, a pasta `target/allure-results/` contém arquivos .json
2. `allure serve` abre o browser com o dashboard
3. Clique em um cenário e veja os steps detalhados
4. Para cenários de API, veja request/response nos attachments
5. Para cenários de UI que falharam, veja screenshot

### Falha guiada

1. Delete `target/allure-results/` e tente `allure serve`:
   ```
   Could not find any allure results
   ```

2. Remova `aspectjweaver` do pom.xml:
   - O relatório mostra cenários mas steps não aparecem detalhados

3. Remova `AllureCucumber7Jvm` do plugin no TestRunner:
   - `allure-results/` fica vazio

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `allure: command not found` | CLI não instalado | Instale via npm/brew/scoop |
| `No allure results found` | Pasta vazia | Execute mvn test antes |
| Steps não aparecem | Falta aspectjweaver | Verifique Surefire plugin no pom.xml |
| Request/Response não aparece | Falta AllureRestAssured | Adicione filter ao RestClient |
| Screenshot não aparece | Falta addAttachment | Verifique UiHooks |
| Relatório antigo | Cache | Use `--clean` no generate |

### O que nao deve ser feito

- Não commite `target/allure-results/` — é gerado a cada execução
- Não use Allure como único registro de falha — logs são mais detalhados
- Não ignore relatórios vazios — significa que a integração está quebrada
- Não remova o aspectjweaver — sem ele Allure não intercepta nada
- Não esqueça de limpar resultados antigos antes de gerar relatório

### Exercicio

1. Execute testes, abra o relatório e explore cada seção
2. Force uma falha, regenere e encontre o screenshot no relatório
3. Encontre o request/response de um teste de API no relatório
4. Adicione `@io.qameta.allure.Severity(SeverityLevel.CRITICAL)` a um step

### Checklist

- [ ] Allure CLI instalado e funcional
- [ ] AllureRestAssured adicionado ao RestClient
- [ ] `target/allure-results/` gerado após mvn test
- [ ] `allure serve` abre dashboard funcional
- [ ] Steps de UI aparecem com detalhe
- [ ] Steps de API mostram request/response
- [ ] Screenshots de falha aparecem
- [ ] Timeline mostra duração correta
- [ ] Gráfico de pizza mostra passed/failed

---

## Capítulo 19 — GitHub Actions (progressivo)

### Resultado que construiremos

Uma pipeline CI/CD que executa testes automaticamente a cada push. Construiremos o YAML em 5 versões progressivas, cada uma adicionando uma funcionalidade.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| .github/workflows/                                    |
|   +-- tests.yml                <-- AQUI               |
|                                                       |
| Pipeline:                                             |
|   Push/PR --> GitHub Actions --> Maven Test -->        |
|   Allure Report --> GitHub Pages                      |
+-------------------------------------------------------+
```

### Conceito mínimo necessário

**GitHub Actions**: CI/CD integrado ao GitHub. Um arquivo YAML define jobs que executam em runners (máquinas virtuais) da Microsoft.

**Conceitos-chave:**
- `workflow`: arquivo YAML em `.github/workflows/`
- `trigger`: evento que dispara (push, pull_request)
- `job`: conjunto de steps executados em sequência
- `step`: comando individual (checkout, setup java, mvn test)
- `runner`: máquina virtual (ubuntu-latest)
- `artifact`: arquivo salvo após execução (relatórios)

### Arquivos envolvidos

| Arquivo | Função |
|---------|--------|
| `.github/workflows/tests.yml` | Pipeline de CI |

### Construção manual passo a passo

Construiremos o YAML em 5 versões, cada uma adicionando funcionalidade:

1. **V1**: Build mínimo (só compila)
2. **V2**: Executa testes de API
3. **V3**: Adiciona testes de UI com Chrome headless
4. **V4**: Gera relatório Allure como artifact
5. **V5**: Publica Allure no GitHub Pages + notificação

---

### Codigo completo final

#### VERSAO 1 — Build mínimo

O que faz: checkout + setup Java + compile. Valida que o projeto compila.

```yaml
# .github/workflows/tests.yml — VERSAO 1
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Compile project
        run: mvn compile -DskipTests -B
```

**O que mudará na V2:** adicionar step de execução de testes.

---

#### VERSAO 2 — Testes de API

Adiciona: execução dos testes de API (não precisa de browser).

```yaml
# .github/workflows/tests.yml — VERSAO 2
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Run API tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@api" -B
```

**O que mudou da V1:**
- Job renomeado para `api-tests`
- Step `Run API tests` com filtro de tag @api
- `-Denv=hml`: usa configuração de homologação
- `-B`: modo batch (sem interatividade)

**O que mudará na V3:** adicionar job separado para testes de UI.

---

#### VERSAO 3 — Testes de UI com Chrome headless

Adiciona: job de UI com Chrome instalado no runner.

```yaml
# .github/workflows/tests.yml — VERSAO 3
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Run API tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@api" -B

  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Setup Chrome
        uses: browser-actions/setup-chrome@v1
        with:
          chrome-version: 'stable'

      - name: Run UI tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@ui" -B
```

**O que mudou da V2:**
- Job `api-tests` permanece igual
- Novo job `ui-tests` com `Setup Chrome` step
- Jobs executam EM PARALELO (independentes)
- `browser-actions/setup-chrome`: instala Chrome estável no runner

**O que mudará na V4:** relatório Allure como artifact.

---

#### VERSAO 4 — Allure Report como artifact

Adiciona: upload do relatório Allure como artifact do workflow.

```yaml
# .github/workflows/tests.yml — VERSAO 4
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Run API tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@api" -B
        continue-on-error: true

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-api
          path: target/allure-results/
          retention-days: 30

  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Setup Chrome
        uses: browser-actions/setup-chrome@v1
        with:
          chrome-version: 'stable'

      - name: Run UI tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@ui" -B
        continue-on-error: true

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-ui
          path: target/allure-results/
          retention-days: 30
```

**O que mudou da V3:**
- `continue-on-error: true`: pipeline não para em falha de teste (queremos o relatório)
- `if: always()`: upload acontece mesmo se tests falharam
- `actions/upload-artifact@v4`: salva allure-results como download
- `retention-days: 30`: mantém por 30 dias

**O que mudará na V5:** publicar no GitHub Pages + notificação.

---

#### VERSAO 5 — GitHub Pages + status badge (Final)

Adiciona: job que gera o relatório e publica no GitHub Pages.

```yaml
# .github/workflows/tests.yml — VERSAO 5 (FINAL)
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Run API tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@api" -B
        continue-on-error: true

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-api
          path: target/allure-results/
          retention-days: 30

  ui-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Java 8
        uses: actions/setup-java@v4
        with:
          java-version: '8'
          distribution: 'temurin'

      - name: Cache Maven packages
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: |
            ${{ runner.os }}-maven-

      - name: Setup Chrome
        uses: browser-actions/setup-chrome@v1
        with:
          chrome-version: 'stable'

      - name: Run UI tests
        run: mvn test -Denv=hml -Dcucumber.filter.tags="@ui" -B
        continue-on-error: true

      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-ui
          path: target/allure-results/
          retention-days: 30

  publish-report:
    needs: [api-tests, ui-tests]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Download API results
        uses: actions/download-artifact@v4
        with:
          name: allure-results-api
          path: allure-results/

      - name: Download UI results
        uses: actions/download-artifact@v4
        with:
          name: allure-results-ui
          path: allure-results/

      - name: Setup Allure CLI
        run: |
          curl -o allure.tgz -Ls https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
          tar -zxvf allure.tgz
          echo "$PWD/allure-2.24.0/bin" >> $GITHUB_PATH

      - name: Generate Allure report
        run: allure generate allure-results -o allure-report --clean

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: allure-report/

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

**O que mudou da V4:**
- `permissions`: necessárias para GitHub Pages
- Novo job `publish-report` com `needs: [api-tests, ui-tests]` (espera ambos)
- Baixa artifacts dos dois jobs
- Instala Allure CLI no runner
- Gera relatório unificado
- Publica no GitHub Pages

**Badge para o README:**

```markdown
![Tests](https://github.com/SEU-USUARIO/SEU-REPO/actions/workflows/tests.yml/badge.svg)
```

### Explicacao do codigo

**Evolução das versões:**

| Versão | Funcionalidade | Complexidade |
|--------|---------------|--------------|
| V1 | Compila | Básica |
| V2 | Testes API | + mvn test |
| V3 | Testes UI | + Chrome setup |
| V4 | Artifacts | + upload results |
| V5 | Pages | + deploy report |

**Conceitos-chave do YAML:**
- `needs`: dependência entre jobs (publish espera api e ui)
- `if: always()`: executa mesmo se job anterior falhou
- `continue-on-error: true`: não para pipeline em falha de teste
- `actions/cache`: reutiliza ~/.m2 entre execuções (economiza ~2min)
- `upload-artifact/download-artifact`: compartilha dados entre jobs
- `deploy-pages`: publica HTML estático no GitHub Pages

### Fluxo de execucao

```
Developer faz Push/PR
    |
    v
GitHub Actions dispara workflow
    |
    +--[paralelo]--+
    |              |
    v              v
api-tests       ui-tests
(~1 min)        (~3 min)
    |              |
    +-- upload     +-- upload
    |              |
    v              v
    +------+-------+
           |
           v
    publish-report
    (baixa + gera + publica)
           |
           v
    Allure Report no GitHub Pages
    https://seu-user.github.io/seu-repo/
```

### Como executar

```bash
# 1. Crie a pasta .github/workflows/
mkdir -p .github/workflows

# 2. Copie a V5 para tests.yml
# 3. Commit e push
git add .github/workflows/tests.yml
git commit -m "ci: adicionar pipeline de testes"
git push origin main

# 4. Vá em GitHub > Actions e observe a execucao
```

### Como confirmar que funcionou

1. Tab "Actions" no GitHub mostra workflow verde (ou amarelo se testes falharam)
2. Artifacts disponíveis para download
3. GitHub Pages com relatório Allure acessível via URL
4. Badge no README mostra status

### Falha guiada

1. Remova `continue-on-error: true`:
   - Se um teste falha, o job falha e artifacts não são uploaded

2. Esqueça de habilitar GitHub Pages nas Settings:
   - Deploy falha: "Pages is not enabled"

3. Use `needs: [api-tests]` sem `ui-tests`:
   - Report só terá resultados de API

### Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Permission denied` para Pages | Falta permissions no YAML | Adicione permissions block |
| `Chrome not found` | Falta setup-chrome | Adicione browser-actions/setup-chrome |
| Artifact vazio | Tests não geraram results | Verifique plugin Allure no TestRunner |
| Timeout no job | Teste travou | Adicione timeout-minutes ao job |
| Cache não funciona | Hash do pom mudou | Normal — recria na próxima execução |
| `Pages is not enabled` | Settings do repo | Habilite Pages com Source: GitHub Actions |

### O que nao deve ser feito

- Não remova `continue-on-error` — você perderá relatórios em falha
- Não execute testes UI sem setup do Chrome — falhará sem browser
- Não use `runs-on: windows-latest` sem motivo — Linux é mais rápido
- Não commite secrets no YAML — use GitHub Secrets
- Não esqueça do cache — sem ele, cada run baixa ~500MB de deps

### Exercicio

1. Adicione step de `mvn compile` antes do test (falha rápida se não compila)
2. Adicione `timeout-minutes: 10` ao job para evitar travamento
3. Crie um scheduled trigger: `schedule: - cron: '0 8 * * 1-5'` (8am seg-sex)
4. Adicione step de notificação Slack com `rtCamp/action-slack-notify@v2`

### Checklist

- [ ] `.github/workflows/tests.yml` criado
- [ ] Trigger em push e pull_request
- [ ] Java 8 configurado com temurin
- [ ] Cache de ~/.m2/repository
- [ ] Job API separado de job UI
- [ ] Chrome instalado para testes UI
- [ ] `continue-on-error: true` para não perder relatório
- [ ] Upload de allure-results como artifact
- [ ] Job de publish-report com GitHub Pages
- [ ] Badge no README

---

## Capítulo 20 — Manutenção e evolução

### Resultado que construiremos

Guias práticos para manter e expandir o framework: como adicionar novos testes, fazer code review, diagnosticar problemas e evoluir a arquitetura. Este capítulo é referência permanente para o time.

### Onde estamos na arquitetura

```
+-------------------------------------------------------+
| FRAMEWORK COMPLETO                                    |
|                                                       |
|  [Features] --> [Steps] --> [Pages/Services]          |
|                     |                                 |
|                     v                                 |
|              [Hooks] + [Utils]                        |
|                     |                                 |
|                     v                                 |
|         [Drivers] + [Config] + [Exceptions]           |
|                     |                                 |
|                     v                                 |
|         [Maven] --> [CI/CD] --> [Allure Report]       |
+-------------------------------------------------------+
```

Este capítulo não adiciona código novo. É um guia operacional.

### Conceito mínimo necessário

Um framework de automação é um organismo vivo. Ele precisa de:
- **Padrões** para que qualquer pessoa adicione testes consistentes
- **Checklists** para evitar erros recorrentes
- **Troubleshooting** para resolver problemas rapidamente
- **Estratégia de evolução** para não ficar obsoleto

### Arquivos envolvidos

Nenhum arquivo novo. Este capítulo referencia todos os existentes.

### Construção manual passo a passo

Não há construção — são guias e checklists.

---

### Codigo completo final

#### Guia 1: Adicionar um novo teste de UI

```
1. CRIE a feature file:
   src/test/resources/features/ui/<funcionalidade>.feature

2. CRIE o Page Object:
   src/test/java/pages/<funcionalidade>/<Funcionalidade>Page.java
   - Extenda BasePage
   - Mapeie locators como By constants
   - Implemente acoes de negocio

3. CRIE a classe de steps:
   src/test/java/steps/ui/<Funcionalidade>Steps.java
   - Instancie a Page no construtor
   - Implemente Given/When/Then
   - Asserts apenas no @Then

4. ADICIONE tag @ui no cenario (obrigatorio para UiHooks funcionar)

5. EXECUTE:
   mvn test -Dcucumber.filter.tags="@<sua-tag>"

6. VALIDE:
   - Teste passa localmente
   - Teste passa em headless
   - Screenshot funciona em falha
```

**Exemplo de estrutura para nova funcionalidade "Dashboard":**

```
src/test/resources/features/ui/dashboard.feature
src/test/java/pages/dashboard/DashboardPage.java
src/test/java/steps/ui/DashboardSteps.java
```

---

#### Guia 2: Adicionar um novo teste de API

```
1. CRIE (ou atualize) a feature file:
   src/test/resources/features/api/<recurso>.feature

2. CRIE o model (se necessario):
   src/test/java/api/models/<Recurso>Request.java

3. CRIE o builder (se necessario):
   src/test/java/api/builders/<Recurso>Builder.java

4. CRIE o service:
   src/test/java/api/services/<Recurso>Service.java
   - Use RestClient para chamadas HTTP
   - Retorne Response sem validar

5. CRIE o schema (se necessario):
   src/test/resources/schemas/<recurso>-schema.json

6. CRIE a classe de steps:
   src/test/java/steps/api/<Recurso>Steps.java
   - Instancie o Service no construtor
   - Valide status e body nos @Then

7. ADICIONE tag @api no cenario

8. EXECUTE:
   mvn test -Dcucumber.filter.tags="@<recurso>"
```

---

#### Guia 3: Checklist de Code Review

```
FEATURE FILE:
  [ ] Tags presentes (@ui ou @api + @funcionalidade)
  [ ] Cenarios independentes (nao dependem de ordem)
  [ ] Given/When/Then claros e sem detalhes tecnicos
  [ ] Parametros entre aspas para strings
  [ ] Sem dados sensiveis hardcoded

STEPS:
  [ ] Sem logica de negocio (delega para Page/Service)
  [ ] Sem Thread.sleep()
  [ ] Sem WebDriver direto
  [ ] Asserts apenas em @Then
  [ ] Mensagens de erro descritivas nos asserts
  [ ] Logging nas acoes principais

PAGE OBJECTS:
  [ ] Locators privados e constantes
  [ ] Metodos publicos com nomes de negocio
  [ ] Usa metodos da BasePage (click, type, waitForVisible)
  [ ] Nao tem asserts
  [ ] Nao expoe WebElement

SERVICES:
  [ ] Usa RestClient (nao REST Assured direto)
  [ ] Retorna Response sem validar
  [ ] Endpoints como constantes
  [ ] Nao faz asserts

GERAL:
  [ ] Compila sem warnings
  [ ] Testes passam localmente
  [ ] Testes passam em headless
  [ ] Nao quebra testes existentes
  [ ] Log Utils usado (nao System.out)
  [ ] FrameworkException para erros internos
```

---

#### Guia 4: Troubleshooting — 10 Erros Comuns

| # | Sintoma | Causa Provável | Solução |
|---|---------|---------------|---------|
| 1 | `NullPointerException` no driver | Hook não executou — falta tag @ui | Adicione @ui ao cenário |
| 2 | `NoSuchElementException` | Locator errado ou elemento não carregou | Verifique locator no DevTools; use explicit wait |
| 3 | `StaleElementReferenceException` | Página recarregou e referência invalidou | Use locator (By) em vez de WebElement armazenado |
| 4 | `TimeoutException` no wait | Elemento nunca apareceu | Aumente timeout ou verifique condição de visibilidade |
| 5 | `Step undefined` no Cucumber | Texto do Gherkin não bate com @Given/@When/@Then | Compare exatamente incluindo espaços e parâmetros |
| 6 | `Connection refused` na API | URL errada ou serviço fora do ar | Verifique api.base.url no .properties; teste URL no browser |
| 7 | `AssertionError: expected 200 but was 404` | Endpoint mudou ou recurso não existe | Verifique documentação da API; confirme path |
| 8 | Testes passam local mas falham no CI | Headless não configurado ou Chrome incompatível | Verifique headless=true em hml.properties; atualize ChromeDriver |
| 9 | Allure report vazio | Falta aspectjweaver ou plugin AllureCucumber | Verifique pom.xml (Surefire plugin) e TestRunner (plugins) |
| 10 | `OutOfMemoryError` em CI | Muitos testes em paralelo | Adicione `-Xmx1024m` ao argLine do Surefire |

---

#### Guia 5: Estratégia de evolução

**Curto prazo (1-3 meses):**
- Adicionar mais cenários nos endpoints existentes
- Criar Scenario Outlines com Examples para variação de dados
- Implementar retry em cenários flaky (Cucumber `@Retry` plugin)

**Médio prazo (3-6 meses):**
- Execução paralela com `cucumber-jvm-parallel-plugin` ou JUnit 5
- Page Object Components para elementos compartilhados (header, menu)
- Data-driven testing com CSV/Excel

**Longo prazo (6-12 meses):**
- Migrar para Selenium 4 + BiDi protocol
- Migrar para JUnit 5 + Cucumber 8
- Adicionar testes de performance com Gatling
- Adicionar testes de acessibilidade com axe-core
- Dockerizar execução com Selenoid/Selenium Grid

**Sinais de que o framework precisa de refactoring:**
- Mais de 5 locators duplicados entre Pages
- Steps com mais de 30 linhas
- BasePage com mais de 20 métodos
- Tempo de execução total acima de 30 minutos
- Mais de 10% de testes flaky

### Explicacao do codigo

Este capítulo não tem código novo. A "explicação" é o raciocínio por trás de cada guia:

**Por que checklists?** Reduzem erros cognitivos. Mesmo QAs experientes esquecem tags ou cometem typos em locators.

**Por que troubleshooting?** Os mesmos 10 erros respondem por 90% dos problemas do dia a dia. Ter a solução à mão economiza horas.

**Por que estratégia de evolução?** Frameworks estagnados se tornam legados. Planejar a evolução previne reescrita total.

### Fluxo de execucao

Fluxo de trabalho diário do QA com o framework:

```
1. Recebe historia/bug para automacao
    |
    v
2. Cria branch: feature/automacao-login-social
    |
    v
3. Escreve feature file (Gherkin)
    |
    v
4. Cria/atualiza Page Object ou Service
    |
    v
5. Implementa Steps
    |
    v
6. Executa localmente (mvn test -Dcucumber.filter.tags="@nova-tag")
    |
    v
7. Valida em headless (mvn test -Denv=hml ...)
    |
    v
8. Commit + Push
    |
    v
9. CI executa automaticamente
    |
    v
10. Code Review seguindo checklist
    |
    v
11. Merge para develop/main
```

### Como executar

Comandos mais usados no dia a dia:

```bash
# Rodar todos os testes
mvn test

# Rodar apenas smoke tests
mvn test -Dcucumber.filter.tags="@smoke"

# Rodar apenas API
mvn test -Dcucumber.filter.tags="@api"

# Rodar apenas UI
mvn test -Dcucumber.filter.tags="@ui"

# Rodar em HML headless
mvn test -Denv=hml

# Rodar cenario especifico por nome
mvn test -Dcucumber.filter.tags="@login"

# Gerar relatorio Allure
allure serve target/allure-results

# Limpar e recompilar
mvn clean compile -DskipTests

# Ver arvore de dependencias
mvn dependency:tree
```

### Como confirmar que funcionou

Este capítulo é validado pela prática:
1. Siga o Guia 1 e adicione um teste de UI novo
2. Siga o Guia 2 e adicione um teste de API novo
3. Faça code review usando o Guia 3
4. Resolva um problema usando o Guia 4
5. Planeje o próximo trimestre usando o Guia 5

### Falha guiada

Cenário: você adicionou um teste novo mas ele não executa.

Diagnóstico passo a passo:
1. O cenário tem tag? (`@ui` ou `@api`)
2. O glue no TestRunner inclui o pacote do step?
3. O texto do step no Gherkin bate exatamente com a annotation?
4. O arquivo está no diretório correto?
5. Compile: `mvn compile -DskipTests` dá erro?

### Erros comuns

(Consolidado no Guia 4 — Troubleshooting acima)

### O que nao deve ser feito

- Não modifique BasePage sem entender o impacto em TODAS as Pages
- Não atualize dependências sem rodar a suite completa
- Não desabilite testes flaky — corrija-os (ou marque como @known-bug)
- Não deixe código morto (steps sem feature, pages sem steps)
- Não crie "mega-steps" que fazem 10 coisas — quebre em steps menores
- Não ignore o relatório Allure — é a documentação viva do sistema

### Exercicio

1. Adicione um novo teste de UI para a página "Secure Area" (logout)
2. Adicione um novo teste de API para GET /users
3. Faça code review do seu próprio código usando o Checklist
4. Simule o erro #3 (StaleElement) e resolva
5. Crie um plano de 3 meses para evolução do framework

### Checklist

- [ ] Li e entendi todos os 5 guias
- [ ] Consigo adicionar teste UI seguindo o Guia 1
- [ ] Consigo adicionar teste API seguindo o Guia 2
- [ ] Sei usar o checklist de code review
- [ ] Conheço os 10 erros mais comuns e suas soluções
- [ ] Tenho um plano de evolução para o framework
- [ ] Toda a equipe tem acesso a esta documentação
- [ ] Pipeline CI está verde e publicando relatórios

---

## Arquitetura Final Completa

```
selenium-cucumber-project/
|
+-- pom.xml
+-- .github/workflows/tests.yml
|
+-- src/test/java/
|   +-- runners/
|   |   +-- TestRunner.java
|   |
|   +-- steps/
|   |   +-- ui/
|   |   |   +-- LoginSteps.java
|   |   +-- api/
|   |       +-- PostSteps.java
|   |
|   +-- pages/
|   |   +-- base/
|   |   |   +-- BasePage.java
|   |   +-- login/
|   |       +-- LoginPage.java
|   |
|   +-- api/
|   |   +-- clients/
|   |   |   +-- RestClient.java
|   |   +-- services/
|   |   |   +-- PostService.java
|   |   +-- models/
|   |   |   +-- PostRequest.java
|   |   +-- builders/
|   |       +-- PostBuilder.java
|   |
|   +-- hooks/
|   |   +-- UiHooks.java
|   |   +-- ApiHooks.java
|   |
|   +-- config/
|   |   +-- Environment.java
|   |   +-- ConfigReader.java
|   |
|   +-- drivers/
|   |   +-- DriverFactory.java
|   |   +-- DriverManager.java
|   |
|   +-- utils/
|   |   +-- LogUtils.java
|   |   +-- JsonUtils.java
|   |   +-- ScreenshotUtils.java
|   |
|   +-- exceptions/
|       +-- FrameworkException.java
|
+-- src/test/resources/
    +-- features/
    |   +-- ui/
    |   |   +-- login.feature
    |   +-- api/
    |       +-- posts.feature
    |
    +-- environments/
    |   +-- dev.properties
    |   +-- hml.properties
    |
    +-- payloads/
    |   +-- posts/
    |       +-- create-post.json
    |       +-- update-post.json
    |
    +-- schemas/
    |   +-- post-schema.json
    |
    +-- testdata/
    |   +-- login.json
    |
    +-- logback.xml
```

---

## Fluxo de Dependências

```
+------------------+     +------------------+     +------------------+
|    Features      |     |    TestRunner     |     |  GitHub Actions  |
|  (Gherkin)       |     |  (JUnit entry)   |     |  (CI trigger)    |
+--------+---------+     +--------+---------+     +--------+---------+
         |                         |                        |
         v                         v                        v
+--------+---------+     +--------+---------+     +--------+---------+
|     Steps        |<----|    Cucumber      |---->|    Maven         |
| (UI + API)       |     |  (orchestrator)  |     |  (build tool)    |
+--------+---------+     +------------------+     +------------------+
         |
    +----+----+
    |         |
    v         v
+---+---+ +---+---+
| Pages | |Service|
| (UI)  | | (API) |
+---+---+ +---+---+
    |         |
    v         v
+---+---+ +---+------+
|Driver | |RestClient|
|Manager| |          |
+---+---+ +---+------+
    |         |
    v         v
+---+---+ +---+------+
|Selenium| |REST      |
|(browser)| |Assured  |
+---------+ +---------+

Transversais (usados por todos):
  [Environment] [LogUtils] [FrameworkException]
```

---

*Framework construido. Testes rodando. Pipeline publicando. Agora e com voce.*
