package support.webDriver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Fábrica de WebDriver.
 * Inicializa o navegador de acordo com o ambiente (local ou CI).
 */
public class DriverFactory {

    private static final boolean EM_CI =
            System.getenv("CI") != null || System.getenv("JENKINS_URL") != null;

    public WebDriver init_driver(String browserName) {
        switch (browserName.toLowerCase()) {
            case "chrome":
                return criarChrome();
            default:
                throw new IllegalArgumentException("Navegador nao suportado: " + browserName);
        }
    }

    private WebDriver criarChrome() {
        if (!EM_CI) {
            String path = System.getenv("CHROME_DRIVER_PATH") != null
                    ? System.getenv("CHROME_DRIVER_PATH")
                    : "C:\\chromedriver\\chromedriver-win64\\chromedriver.exe";
            System.setProperty("webdriver.chrome.driver", path);
        }

        ChromeOptions options = new ChromeOptions();

        if (EM_CI) {
            options.addArguments("--headless=new", "--no-sandbox",
                    "--disable-dev-shm-usage", "--window-size=1920,1080");
        } else {
            options.addArguments("--start-maximized");
        }

        options.addArguments("--disable-notifications", "--remote-allow-origins=*");
        return new ChromeDriver(options);
    }
}
