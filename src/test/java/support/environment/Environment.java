package support.environment;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Carrega configurações de ambiente a partir do config.properties.
 * Permite execução em diferentes ambientes via Maven: mvn test -Denvironment=HQA
 */
public class Environment {

    public String environment;
    public String domain;
    public String apiBasePath;
    public String baseUrl;

    private static Properties config;
    public static String projectPath = System.getProperty("user.dir");

    static {
        config = getPropertiesFromFile(projectPath + File.separator + "config.properties");
    }

    public static String ambiente_DEV = config.getProperty("url_DEV");
    public static String ambiente_HQA = config.getProperty("url_HQA");
    public static String api_DEV = config.getProperty("api_DEV");
    public static String api_HQA = config.getProperty("api_HQA");

    public Environment() {
        setupEnvironment();
    }

    private void setupEnvironment() {
        if (System.getProperty("environment") != null) {
            environment = System.getProperty("environment");
        } else {
            environment = config.getProperty("environment");
        }

        switch (environment) {
            case "DEV":
                baseUrl = ambiente_DEV;
                apiBasePath = api_DEV;
                break;
            case "HQA":
                baseUrl = ambiente_HQA;
                apiBasePath = api_HQA;
                break;
            default:
                baseUrl = ambiente_DEV;
                apiBasePath = api_DEV;
        }

        domain = config.getProperty("domain");
    }

    public String getProperty(String key) {
        return config.getProperty(key);
    }

    private static Properties getPropertiesFromFile(String filePath) {
        Properties properties = new Properties();
        try (FileInputStream input = new FileInputStream(filePath)) {
            properties.load(input);
        } catch (IOException e) {
            throw new RuntimeException("Erro ao carregar config.properties: " + e.getMessage());
        }
        return properties;
    }
}
