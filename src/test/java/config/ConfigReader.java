package config;

import exceptions.FrameworkException;
import utils.LogUtils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Le arquivos .properties do classpath.
 *
 * Cada chave pode ser sobrescrita por variavel de ambiente: "base.url" vira "BASE_URL"
 * (pontos -&gt; underscore, maiusculo). Em CI/CD, use isso para injetar valores via
 * GitHub Secrets sem tocar nos arquivos .properties.
 */
public class ConfigReader {

    private final Properties props = new Properties();

    public ConfigReader(String fileName) {
        try (InputStream input = getClass().getClassLoader().getResourceAsStream(fileName)) {
            if (input == null) {
                throw new FrameworkException("Arquivo nao encontrado no classpath: " + fileName);
            }
            props.load(input);
        } catch (IOException e) {
            throw new FrameworkException("Erro ao carregar " + fileName, e);
        }
    }

    public String get(String key) {
        String envKey = key.replace(".", "_").toUpperCase();
        String envValue = System.getenv(envKey);
        if (envValue != null) {
            LogUtils.debug("Config '" + key + "' resolvida via variavel de ambiente " + envKey);
            return envValue;
        }
        return props.getProperty(key);
    }

    public String get(String key, String defaultValue) {
        String value = get(key);
        return value != null ? value : defaultValue;
    }

    public int getInt(String key, int defaultValue) {
        String value = get(key);
        return value != null ? Integer.parseInt(value) : defaultValue;
    }
}
