package support.testEvidence;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import support.helpers.LogUtils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * Utilitário para captura e armazenamento de evidências de teste.
 */
public class ScreenshotUtils {

    private ScreenshotUtils() {}

    public static byte[] capturar(WebDriver driver) {
        if (driver instanceof TakesScreenshot) {
            return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
        }
        return new byte[0];
    }

    public static void salvarEmDisco(byte[] screenshot, String caminho) {
        try {
            File file = new File(caminho);
            file.getParentFile().mkdirs();
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(screenshot);
            }
            LogUtils.printMessage("Evidencia salva em: " + caminho);
        } catch (IOException e) {
            LogUtils.printMessage("Erro ao salvar evidencia: " + e.getMessage());
        }
    }
}
