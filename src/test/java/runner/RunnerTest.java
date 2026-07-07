package runner;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.BeforeClass;
import org.junit.runner.RunWith;

/**
 * Runner principal do Cucumber com JUnit.
 *
 * Como executar:
 *   - Pela IDE:    clique com botão direito → Run As → JUnit Test
 *   - Pelo Maven:  mvn test
 *   - Só API:      mvn test -Dcucumber.features=src/test/resources/features/api_posts.feature
 *   - Por tag:     mvn test -Dcucumber.filter.tags="@smoke"
 */
@RunWith(Cucumber.class)
@CucumberOptions(
    // Todos os arquivos .feature (UI + API)
    features = "src/test/resources/features",

    // Pacote dos Step Definitions e Hooks
    glue = "steps",

    // Relatórios gerados em target/cucumber-reports/
    plugin = {
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/cucumber-reports/cucumber.json",
        "junit:target/cucumber-reports/cucumber.xml"
    },

    snippets = CucumberOptions.SnippetType.CAMELCASE,
    monochrome = true
)
public class RunnerTest {

    /**
     * Configura o truststore customizado antes de qualquer teste.
     *
     * Necessário em ambientes onde um proxy SSL (ex: antivírus corporativo)
     * intercepta conexões HTTPS e o Java 8 rejeita os certificados substituídos.
     * O arquivo ~/.maven-cacerts deve conter o certificado raiz do proxy importado.
     *
     * Em CI (GitHub Actions) este truststore não existe e não é necessário,
     * pois o Java no Linux tem cacerts atualizados e sem interferência de proxy.
     */
    @BeforeClass
    public static void configurarSSL() {
        // Só aplica o truststore customizado se o arquivo existir (ambiente local)
        String cacertsPath = System.getProperty("user.home") + "/.maven-cacerts";
        if (new java.io.File(cacertsPath).exists()) {
            System.setProperty("javax.net.ssl.trustStore", cacertsPath);
            System.setProperty("javax.net.ssl.trustStorePassword", "changeit");
        }
    }
}
