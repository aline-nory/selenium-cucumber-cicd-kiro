package hooks;

import config.Environment;
import drivers.DriverFactory;
import drivers.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.WebDriver;
import utils.LogUtils;
import utils.ScreenshotUtils;

/**
 * Hooks para cenarios @ui.
 * Environment injetado via PicoContainer - mesma instancia compartilhada
 * com os demais steps/hooks do cenario (evita reler o .properties varias vezes).
 */
public class UiHooks {

    private final Environment env;

    public UiHooks(Environment env) {
        this.env = env;
    }

    @Before(value = "@ui", order = 0)
    public void logScenario(Scenario scenario) {
        LogUtils.info("=== [UI] " + scenario.getName() + " ===");
    }

    @Before(value = "@ui", order = 1)
    public void openBrowser() {
        // Sempre cria um driver novo por cenario para evitar estado residual
        // de um cenario anterior que falhou de forma inesperada.
        DriverManager.quit();

        String browser = env.get("browser", "chrome");
        int pageLoad = env.getInt("timeout.pageLoad", 30);

        DriverFactory factory = new DriverFactory();
        WebDriver driver = factory.create(browser);

        // Nao definimos implicitlyWait: a BasePage usa explicit waits (WebDriverWait)
        // para toda interacao com elementos. Misturar implicit + explicit causa
        // tempos de espera duplicados e comportamento nao-deterministico.
        driver.manage().timeouts().pageLoadTimeout(pageLoad, java.util.concurrent.TimeUnit.SECONDS);
        DriverManager.setDriver(driver);
    }

    @After(value = "@ui")
    public void closeBrowser(Scenario scenario) {
        WebDriver driver = DriverManager.getDriver();
        if (driver == null) return;

        String mode = env.get("screenshot.mode", "failure_only");
        boolean shouldCapture = "always".equals(mode) || scenario.isFailed();

        if (shouldCapture) {
            byte[] screenshot = ScreenshotUtils.capture(driver);
            if (screenshot.length > 0) {
                String status = scenario.isFailed() ? "FALHA" : "SUCESSO";
                scenario.attach(screenshot, "image/png", status + " - " + scenario.getName());
                LogUtils.info("Screenshot [" + status + "]");
            }
        }

        DriverManager.quit();
        LogUtils.info("=== Navegador encerrado ===");
    }
}
