package pages.dashboard;

import org.openqa.selenium.WebDriver;
import pages.base.BasePage;

/**
 * Page Object mínimo da página Dashboard.
 * Responsável apenas por validar que o usuário chegou ao dashboard após login.
 */
public class DashboardPage extends BasePage {

    public DashboardPage(WebDriver driver, int explicitWaitSeconds) {
        super(driver, explicitWaitSeconds);
    }

    public boolean isOnDashboard() {
        return urlContains("/dashboard");
    }
}
