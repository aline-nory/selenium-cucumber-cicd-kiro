package drivers;

import org.openqa.selenium.WebDriver;

/**
 * Gerencia o WebDriver via ThreadLocal.
 * Isso mantem o gerenciamento de driver seguro caso a execucao paralela seja
 * habilitada no futuro (ex.: migrando o runner para o Cucumber JUnit Platform Engine
 * com cucumber.execution.parallel.enabled=true) - hoje o TestRunner roda tudo em serie.
 */
public class DriverManager {

    private static final ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    private DriverManager() {}

    public static WebDriver getDriver() {
        return driver.get();
    }

    public static void setDriver(WebDriver webDriver) {
        driver.set(webDriver);
    }

    public static void quit() {
        WebDriver d = driver.get();
        if (d != null) {
            d.quit();
            driver.remove();
        }
    }
}
