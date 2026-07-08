package steps;

import io.cucumber.java.pt.Dado;
import io.cucumber.java.pt.E;
import io.cucumber.java.pt.Então;
import io.cucumber.java.pt.Quando;
import io.restassured.response.Response;
import org.junit.Assert;
import services.PostService;
import support.communication.RestApi;
import support.environment.Environment;

import java.util.List;

/**
 * Steps de API de Posts.
 */
public class ApiPostsSteps {

    private Environment env = new Environment();
    private PostService postService = new PostService();

    @Dado("que estou consumindo a API de posts")
    public void configurarApi() {
        RestApi.setBaseUri(env.apiBasePath);
    }

    @Dado("que tenho os dados de um novo post")
    public void dadosNovoPost() {
        postService.criarPost("Post de Teste Automatizado", "Conteudo via REST Assured", 1);
    }

    @Dado("que tenho os dados de atualização do post {int}")
    public void dadosAtualizacao(int id) {
        postService.atualizarPost(id, "Titulo Atualizado", "Corpo atualizado", 1);
    }

    @Quando("busco todos os posts")
    public void getTodos() {
        postService.listarTodos();
    }

    @Quando("busco o post de ID {int}")
    public void getPorId(int id) {
        postService.buscarPorId(id);
    }

    @Quando("busco os posts do usuário {int}")
    public void getPorUsuario(int userId) {
        postService.buscarPorUsuario(userId);
    }

    @Quando("envio o novo post")
    public void enviarPost() {
        // POST já executado no @Dado
    }

    @Quando("atualizo o post {int}")
    public void atualizarPost(int id) {
        // PUT já executado no @Dado
    }

    @Quando("deleto o post {int}")
    public void deletarPost(int id) {
        postService.deletarPost(id);
    }

    @Então("o status code da resposta deve ser {int}")
    public void validarStatus(int esperado) {
        Assert.assertEquals("Status incorreto", esperado, RestApi.getStatusCode());
    }

    @E("o Content-Type da resposta deve conter {string}")
    public void validarContentType(String esperado) {
        Assert.assertTrue("Content-Type incorreto", RestApi.getContentType().contains(esperado));
    }

    @E("a resposta deve conter {int} posts")
    public void validarQuantidade(int esperada) {
        Response r = RestApi.getResponse();
        Assert.assertEquals("Quantidade incorreta", esperada, r.jsonPath().getList("$").size());
    }

    @E("o campo {string} deve ter valor inteiro {int}")
    public void validarCampoInt(String campo, int esperado) {
        Assert.assertEquals("Campo '" + campo + "' incorreto", esperado, RestApi.getResponse().jsonPath().getInt(campo));
    }

    @E("o campo {string} deve ter valor de texto {string}")
    public void validarCampoTexto(String campo, String esperado) {
        Assert.assertEquals("Campo '" + campo + "' incorreto", esperado, RestApi.getResponse().jsonPath().getString(campo));
    }

    @E("o campo {string} não deve estar vazio")
    public void validarCampoNaoVazio(String campo) {
        Object valor = RestApi.getResponse().jsonPath().get(campo);
        Assert.assertNotNull("Campo nulo", valor);
        Assert.assertNotEquals("Campo vazio", "", valor.toString().trim());
    }

    @E("todos os posts devem ter {string} igual a {int}")
    public void validarTodos(String campo, int esperado) {
        List<Integer> valores = RestApi.getResponse().jsonPath().getList(campo, Integer.class);
        Assert.assertFalse("Lista vazia", valores.isEmpty());
        for (int i = 0; i < valores.size(); i++) {
            Assert.assertEquals("Post[" + i + "] incorreto", esperado, (int) valores.get(i));
        }
    }
}
