package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Page Object da página de Login.
 */
public class LoginPage extends BasePage {

    private final By campoUsuario = By.name("username");
    private final By campoSenha   = By.name("password");
    private final By botaoLogin   = By.cssSelector("button[type='submit']");
    private final By mensagemErro = By.cssSelector(".oxd-alert-content-text");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public void abrirPagina(String url) {
        navegar(url);
    }

    public void preencherUsuario(String usuario) {
        preencher(campoUsuario, usuario);
    }

    public void preencherSenha(String senha) {
        preencher(campoSenha, senha);
    }

    public void clicarLogin() {
        clicar(botaoLogin);
    }

    public String obterMensagemErro() {
        return obterTexto(mensagemErro);
    }

    public boolean estaNoDashboard() {
        return urlContem("/dashboard");
    }
}
