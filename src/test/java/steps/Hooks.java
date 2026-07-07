package steps;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Hooks do Cucumber: gerencia o ciclo de vida do WebDriver.
 *
 * Detecta automaticamente se está rodando em ambiente CI/CD (GitHub Actions,
 * Jenkins, GitLab CI) e ativa o modo headless sem precisar alterar o código.
 *
 * Variáveis de ambiente reconhecidas como CI:
 *   - CI=true          (GitHub Actions, GitLab CI, CircleCI)
 *   - JENKINS_URL      (Jenkins)
 */
public class Hooks {

    /**
     * Caminho local do ChromeDriver.
     * Pode ser sobrescrito pela variável de ambiente CHROME_DRIVER_PATH.
     * Valor padrão: C:\chromedriver\chromedriver-win64\chromedriver.exe
     *
     * Para customizar sem alterar o código:
     *   set CHROME_DRIVER_PATH=C:\seu\caminho\chromedriver.exe
     */
    private static final String CHROME_DRIVER_PATH_LOCAL =
            System.getenv("CHROME_DRIVER_PATH") != null
                    ? System.getenv("CHROME_DRIVER_PATH")
                    : "C:\\chromedriver\\chromedriver-win64\\chromedriver.exe";

    private static final ThreadLocal<WebDriver> driverThreadLocal = new ThreadLocal<WebDriver>();

    @Before
    public void iniciarNavegador() {
        boolean emCI = System.getenv("CI") != null || System.getenv("JENKINS_URL") != null;

        // Em CI o chromedriver fica no PATH (instalado pelo workflow)
        // Localmente aponta para o executável fixo
        if (!emCI) {
            System.setProperty("webdriver.chrome.driver", CHROME_DRIVER_PATH_LOCAL);
        }

        ChromeOptions options = new ChromeOptions();

        if (emCI) {
            // Modo headless obrigatório em servidores sem interface gráfica
            options.addArguments("--headless=new");
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");
            options.addArguments("--disable-gpu");
            options.addArguments("--window-size=1920,1080");
        } else {
            // Localmente abre o navegador normalmente
            options.addArguments("--start-maximized");
        }

        options.addArguments("--disable-notifications");
        options.addArguments("--remote-allow-origins=*");

        driverThreadLocal.set(new ChromeDriver(options));
    }

    @After
    public void encerrarNavegador(Scenario scenario) {
        WebDriver driver = getDriver();

        if (scenario.isFailed() && driver instanceof TakesScreenshot) {
            byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            scenario.attach(screenshot, "image/png", "Screenshot - " + scenario.getName());
        }

        if (driver != null) {
            driver.quit();
            driverThreadLocal.remove();
        }
    }

    public static WebDriver getDriver() {
        return driverThreadLocal.get();
    }
}
