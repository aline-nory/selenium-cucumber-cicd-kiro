package utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import exceptions.FrameworkException;

import java.io.IOException;
import java.io.InputStream;
import java.util.Scanner;

/**
 * Utilitario para leitura e edicao de payloads JSON do classpath.
 */
public class JsonUtils {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private JsonUtils() {}

    /**
     * Carrega um arquivo JSON do classpath.
     * @param path caminho relativo (ex: "payloads/posts/create-post.json")
     */
    public static String load(String path) {
        InputStream input = JsonUtils.class.getClassLoader().getResourceAsStream(path);
        if (input == null) {
            throw new FrameworkException("Arquivo JSON nao encontrado: " + path);
        }
        try (Scanner scanner = new Scanner(input, "UTF-8")) {
            return scanner.useDelimiter("\\A").next();
        }
    }

    /**
     * Retorna uma copia do JSON com um campo inteiro sobrescrito.
     * Usa parsing real (Jackson) em vez de substituicao de texto,
     * para nao depender da formatacao exata do arquivo fonte.
     */
    public static String setIntField(String json, String field, int value) {
        try {
            ObjectNode node = (ObjectNode) MAPPER.readTree(json);
            node.put(field, value);
            return MAPPER.writeValueAsString(node);
        } catch (IOException e) {
            throw new FrameworkException("Erro ao editar campo '" + field + "' do JSON", e);
        }
    }
}
