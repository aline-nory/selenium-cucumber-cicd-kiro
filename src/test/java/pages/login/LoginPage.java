package pages.login;

import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import pages.base.BasePage;
import utils.LogUtils;

/**
 * Page Object da pagina de Login.
 */
public class LoginPage extends BasePage {

    private final By usernameField = By.name("username");
    private final By passwordField = By.name("password");
    private final By loginButton   = By.cssSelector("button[type='submit']");
    private final By errorMessage  = By.cssSelector(".orangehrm-login-form .oxd-alert-content-text");

    public LoginPage(WebDriver driver, int explicitWaitSeconds) {
        super(driver, explicitWaitSeconds);
    }

    public void open(String url) {
        navigate(url);
        waitUntilLoaded();
    }

    public void fillUsername(String username) {
        type(usernameField, username);
    }

    public void fillPassword(String password) {
        type(passwordField, password);
    }

    public void clickLogin() {
        click(loginButton);
    }

    public String getErrorMessage() {
        return getText(errorMessage);
    }

    /**
     * Verifica se a mensagem de erro esta visivel sem estourar TimeoutException.
     */
    public boolean isErrorMessageDisplayed() {
        try {
            wait.until(ExpectedConditions.visibilityOfElementLocated(errorMessage));
            return true;
        } catch (TimeoutException e) {
            LogUtils.warn("Timeout aguardando mensagem de erro ficar visivel");
            return false;
        }
    }

    /**
     * Confirma que a pagina de login carregou (campo username visivel).
     * Chamado internamente por open() para falhar cedo caso a pagina nao renderize.
     */
    private void waitUntilLoaded() {
        try {
            wait.until(ExpectedConditions.visibilityOfElementLocated(usernameField));
        } catch (TimeoutException e) {
            throw new IllegalStateException(
                    "LoginPage nao carregou: campo username nao ficou visivel dentro do timeout", e);
        }
    }
}
