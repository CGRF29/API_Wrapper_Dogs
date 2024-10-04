# Librerías
import pytest
from app import app
import requests
import logging
from app import setup_logging
from unittest.mock import patch

@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    """
    Descripción:
    Configura el sistema de logging para las pruebas.
        - Utiliza la función 'setup_logging' para establecer la configuración de logs que se utilizarán durante la ejecución de las pruebas.
    """
    setup_logging()

@pytest.fixture
def client():
    """
    Descripción:
    Crea un cliente de pruebas para la aplicación Flask.
    - Esto permite simular solicitudes HTTP a la aplicación sin necesidad de levantar un servidor real.
    """
    with app.test_client() as client:
        yield client

def test_get_dog_image_real_api(client):
    """
    Descripción:
    Prueba que realiza una solicitud real a la API Dog CEO a través del endpoint `/dog/breed/<dog_breed>`.
    - Verifica que la respuesta de la API tenga un código de estado 200 y que contenga una URL válida de una imagen.

    Parametro:
    - client: El cliente de pruebas Flask proporcionado por el fixture.

    Salida:
    - No devuelve nada. Utiliza asserts para verificar que la respuesta sea correcta.
    """
    
    # Hacer una solicitud real al endpoint que llama a la API Dog CEO
    response = client.get('/dog/breed/beagle')
    json_data = response.get_json()
    # Verificar la respuesta
    assert response.status_code == 200
    #assert json_data['breed'] == 'beagle'
    assert json_data['image_url'] is not None
    assert json_data['status'] == 'success'

def test_get_dog_image_invalid_breed(client, caplog):
    """
    Descripción:
    Prueba que verifica el manejo de una raza inválida.
    - Envía una solicitud a la API con una raza inexistente y verifica que la respuesta sea un error 404.
    - También comprueba que se registre una advertencia en los logs.

    Parámetros:
    - client: El cliente de pruebas Flask proporcionado por el fixture.
    - caplog: Herramienta de pytest para capturar y verificar los mensajes de log.

    Salida:
    - No devuelve nada. Utiliza asserts para verificar la respuesta y los logs generados.
    """
    with caplog.at_level(logging.WARNING):
        response = client.get('/dog/breed/invalid_breed')
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid breed or breed not found'
        # Verificar que el log de advertencia fue generado
        assert "Breed 'invalid_breed' not found" in caplog.text

def test_get_dog_image_api_timeout(client, mocker):
    """
    Descripción:
    Prueba que simula un tiempo de espera (timeout) al hacer la solicitud a la API externa.
    - Verifica que la respuesta devuelva un código 500 y que se registre un mensaje de error de timeout.

    Parámetros:
    - client: El cliente de pruebas Flask proporcionado por el fixture.
    - mocker: Herramienta de pytest utilizada para simular resultados en las funciones.

    Salida:
    - No devuelve nada. Utiliza asserts para verificar la respuesta y el mensaje de error devuelto.
    """
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)
    response = client.get('/dog/breed/hound')
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data['error'] == 'Request timed out'

def test_get_dog_image_api_failure(client):
    """
    Descripción:
    Esta prueba unitaria simula un fallo en la conexión a la API externa (Dog CEO) y verifica que la API interna
    maneje correctamente el error y devuelva el código de estado HTTP 500 junto con un mensaje de error adecuado.
    
    Parametro:
    - client: El cliente de pruebas proporcionado por Flask, que se utiliza para simular solicitudes HTTP sin 
              necesidad de levantar un servidor real.

    Salida:
    - No devuelve ningún valor. La función utiliza 'assert' para validar lo siguiente:
        - El código de estado HTTP debe ser 500 (Internal Server Error).
        - El campo 'error' en la respuesta JSON debe contener el mensaje: 'Error connecting to the Dog CEO API'.
        - El campo 'message' en la respuesta JSON debe contener el mensaje de error simulado: 'API request failed'.
    """
    # Simular una excepción en la llamada a la API
    with patch('requests.get', side_effect=requests.exceptions.RequestException("API request failed")):
        response = client.get('/dog/breed/hound')
        json_data = response.get_json()
        assert response.status_code == 500
        assert json_data['error'] == 'Error connecting to the Dog CEO API'
        assert json_data['message'] == 'API request failed'