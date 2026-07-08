package steps;

import io.cucumber.java.pt.Dado;
import io.cucumber.java.pt.Então;
import io.cucumber.java.pt.Quando;
import org.junit.Assert;
import pages.LoginPage;
import support.environment.Environment;
import support.hooks.WebHooks;

/**
 * Steps de Login.
 */
public class LoginSteps {

    private LoginPage loginPage;
    private Environment env = new Environment();

    @Dado("que estou na página de login")
    public void abrirLogin() {
        loginPage = new LoginPage(WebHooks.getDriver());
        loginPage.abrirPagina(env.baseUrl);
    }

    @Quando("faço login como administrador")
    public void loginAdmin() {
        loginPage.preencherUsuario(env.getProperty("usuario.admin"));
        loginPage.preencherSenha(env.getProperty("senha.admin"));
        loginPage.clicarLogin();
    }

    @Quando("faço login com usuário {string} e senha {string}")
    public void loginComCredenciais(String usuario, String senha) {
        loginPage.preencherUsuario(usuario);
        loginPage.preencherSenha(senha);
        loginPage.clicarLogin();
    }

    @Quando("faço login com usuário {string} e senha incorreta")
    public void loginComSenhaIncorreta(String usuario) {
        loginPage.preencherUsuario(usuario);
        loginPage.preencherSenha(env.getProperty("senha.invalida"));
        loginPage.clicarLogin();
    }

    @Então("devo ser redirecionado para a página inicial")
    public void validarDashboard() {
        Assert.assertTrue("Nao redirecionou para o dashboard", loginPage.estaNoDashboard());
    }

    @Então("devo ver a mensagem de erro {string}")
    public void validarMensagemErro(String esperada) {
        Assert.assertEquals("Mensagem incorreta", esperada, loginPage.obterMensagemErro());
    }
}
