import pytest
from app import app
import requests
import logging
from app import setup_logging
from unittest.mock import patch

@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    setup_logging()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_dog_image_real_api(client):
    # Hacer una solicitud real al endpoint que llama a la API Dog CEO
    response = client.get('/dog/breed/hound')
    json_data = response.get_json()

    # Verificar la respuesta
    assert response.status_code == 200
    assert json_data['breed'] == 'hound'
    assert json_data['image_url'] is not None
    assert json_data['status'] == 'success'

def test_get_dog_image_invalid_breed(client, caplog):
    with caplog.at_level(logging.WARNING):
        response = client.get('/dog/breed/invalid_breed')
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid breed or breed not found'
        # Verificar que el log de advertencia fue generado
        assert "Breed 'invalid_breed' not found" in caplog.text

def test_get_dog_image_api_timeout(client, mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)
    response = client.get('/dog/breed/hound')
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data['error'] == 'Request timed out'

def test_get_dog_image_api_failure(client):
    # Simular una excepción en la llamada a la API
    with patch('requests.get', side_effect=requests.exceptions.RequestException("API request failed")):
        response = client.get('/dog/breed/hound')
        json_data = response.get_json()
        assert response.status_code == 500
        assert json_data['error'] == 'Error connecting to the Dog CEO API'
        assert json_data['message'] == 'API request failed'