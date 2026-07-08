package support.communication;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import support.helpers.LogUtils;

import static io.restassured.RestAssured.given;

/**
 * Classe utilitária para comunicação REST.
 * Centraliza chamadas HTTP (GET, POST, PUT, DELETE).
 */
public class RestApi {

    private static Response response;
    private static RequestSpecification request;

    public static void setBaseUri(String baseUri) {
        RestAssured.baseURI = baseUri;
        request = given()
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);
    }

    public static void setBody(String body) {
        request = request.body(body);
    }

    public static void get(String endpoint) {
        LogUtils.printMessage("GET " + RestAssured.baseURI + endpoint);
        response = request.when().get(endpoint).then().extract().response();
    }

    public static void post(String endpoint) {
        LogUtils.printMessage("POST " + RestAssured.baseURI + endpoint);
        response = request.when().post(endpoint).then().extract().response();
    }

    public static void put(String endpoint) {
        LogUtils.printMessage("PUT " + RestAssured.baseURI + endpoint);
        response = request.when().put(endpoint).then().extract().response();
    }

    public static void delete(String endpoint) {
        LogUtils.printMessage("DELETE " + RestAssured.baseURI + endpoint);
        response = request.when().delete(endpoint).then().extract().response();
    }

    public static int getStatusCode() {
        return response.getStatusCode();
    }

    public static String getContentType() {
        return response.getContentType();
    }

    public static Response getResponse() {
        return response;
    }
}
