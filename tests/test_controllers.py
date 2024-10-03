import pytest
import os
import mysql.connector
from controllers import insert_request_data
from unittest.mock import patch

# Configurar el entorno de pruebas antes de ejecutar las pruebas
@pytest.fixture(scope='session', autouse=True)
def set_test_env():
    os.environ['PYTHON_ENV'] = 'test'  # Configurar el entorno de pruebas

# Fixture para configurar y limpiar la base de datos antes de cada prueba
@pytest.fixture(scope='function')
def setup_database():
    # Configuración de la base de datos de prueba
    db_config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'port': 3306,
        'database': 'dog_api_test'  # Base de datos de prueba
    }

    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute("""                   
        CREATE TABLE IF NOT EXISTS requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            breed VARCHAR(50),
            image_url TEXT,
            request_timestamp DATETIME,
            response_code INT
        );
    """)

    # Limpiar la tabla antes de cada prueba
    cursor.execute("DELETE FROM requests")
    conn.commit()

    # Devolver la conexión y el cursor para usarlos en las pruebas
    yield cursor

    # Cerrar el cursor y la conexión después de la prueba
    cursor.close()
    conn.close()

def test_insert_request_data(setup_database):
    # Valores de prueba
    breed = 'hound'
    image_url = 'https://images.dog.ceo/breeds/hound/image.jpg'
    response_code = 200

    # Ejecutar la función insert_request_data
    insert_request_data(breed, image_url, response_code)

    # Verificar que los datos fueron insertados en la base de datos de pruebas
    print("Realizando consulta para verificar inserción")
    setup_database.execute("SELECT * FROM requests WHERE breed = %s", (breed,))
    result = setup_database.fetchone()

    print(f"Resultado de la consulta: {result}")  # Depuración

    assert result is not None, f"No se encontró ningún registro para la raza {breed}"
    assert result[1] == breed
    assert result[2] == image_url
    assert result[3] is not None
    assert result[4] == response_code
"""
def test_insert_request_data_database_error(setup_database):
    # Simular un error de conexión a la base de datos
    with patch('mysql.connector.connect', side_effect=mysql.connector.Error("Connection Error")):
        # Ejecutar la función y verificar que maneje la excepción
        try:
            insert_request_data('hound', 'https://images.dog.ceo/breeds/hound/image.jpg', 200)
            assert False, "Expected an exception but none was raised."
        except mysql.connector.Error as e:
            assert str(e) == "Connection Error"
"""