package support.helpers;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Utilitário de log para execução dos testes.
 */
public class LogUtils {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");

    private LogUtils() {}

    public static void printMessage(String message) {
        System.out.println("[" + LocalDateTime.now().format(formatter) + "] " + message);
    }
}
