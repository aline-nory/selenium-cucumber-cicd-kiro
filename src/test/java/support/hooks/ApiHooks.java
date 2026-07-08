package support.hooks;

import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import support.environment.Environment;
import support.helpers.LogUtils;

/**
 * Hooks para cenários de API (@api).
 */
public class ApiHooks {

    private Environment env;

    public ApiHooks() {
        env = new Environment();
    }

    @Before(value = "@api", order = 0)
    public void setupApi(Scenario scenario) {
        LogUtils.printMessage("Iniciando cenario API: " + scenario.getName());
    }
}
