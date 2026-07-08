package services;

import support.communication.RestApi;
import support.helpers.LogUtils;

/**
 * Classe de serviço para o endpoint /posts.
 * Encapsula as chamadas de API relacionadas a Posts.
 */
public class PostService {

    public void listarTodos() {
        RestApi.get("/posts");
    }

    public void buscarPorId(int id) {
        RestApi.get("/posts/" + id);
    }

    public void buscarPorUsuario(int userId) {
        RestApi.get("/posts?userId=" + userId);
    }

    public void criarPost(String title, String body, int userId) {
        String json = "{\"title\":\"" + title + "\",\"body\":\"" + body + "\",\"userId\":" + userId + "}";
        RestApi.setBody(json);
        RestApi.post("/posts");
    }

    public void atualizarPost(int id, String title, String body, int userId) {
        String json = "{\"id\":" + id + ",\"title\":\"" + title + "\",\"body\":\"" + body + "\",\"userId\":" + userId + "}";
        RestApi.setBody(json);
        RestApi.put("/posts/" + id);
    }

    public void deletarPost(int id) {
        RestApi.delete("/posts/" + id);
    }
}
