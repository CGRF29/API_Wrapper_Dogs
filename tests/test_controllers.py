#Librerias
import pytest
import os
import datetime
import mysql.connector
import logging
from app import setup_logging
from controllers import insert_request_data, get_db_config
from unittest.mock import patch

@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    """
    Descripción:
    Configura el sistema de logging para las pruebas.
        - Utiliza la función 'setup_logging' para establecer la configuración de logs que se utilizarán durante la ejecución de las pruebas.
    """
    setup_logging(testing=True)

# Configurar el entorno de pruebas antes de ejecutar las pruebas
@pytest.fixture(scope='session', autouse=True)
def set_test_env():
    os.environ['PYTHON_ENV'] = 'test'  # Configurar el entorno de pruebas

# Fixture para configurar y limpiar la base de datos antes de cada prueba
@pytest.fixture(scope='function')
def setup_database():
    """
    Descripción:
    Configura una base de datos MySQL de prueba y asegura que esté limpia antes de cada prueba. 
    Crea la tabla 'requests' si no existe, y limpia cualquier dato previo para asegurar un entorno limpio.

    Salida:
    - Devuelve un cursor de la base de datos para interactuar con ella durante las pruebas.
    """
    #wait_for_db()  # Esperar hasta que la base de datos esté lista
    db_config = get_db_config()
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
    """
    Descripción:
    Prueba que verifica la inserción de datos en la base de datos. Inserta una solicitud en la tabla 'requests' y luego verifica que los datos se hayan guardado correctamente.

    Parámetros:
    - setup_database: El cursor de la base de datos proporcionado por el fixture 'setup_database'.

    Salida:
    - No devuelve nada, solo utiliza asserts para verificar que los datos se hayan insertado correctamente.
    """
    
    # Valores de prueba
    breed = 'hound'
    image_url = 'https://images.dog.ceo/breeds/hound/image.jpg'
    response_code = 200
    timestamp = datetime.datetime.now()


    # Ejecutar la función insert_request_data
    insert_request_data(breed, image_url,timestamp, response_code)

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

def test_insert_request_data_database_error(setup_database,caplog):
    """
    Descripción:
    Prueba que simula un error de conexión a la base de datos para verificar que la función insert_request_data maneje correctamente las excepciones de conexión.

    Parametro:
    - setup_database: El cursor de la base de datos proporcionado por el fixture 'setup_database'.

    Salida:
    - No devuelve nada, solo utiliza asserts para verificar que el error fue manejado correctamente.
    """
    # Simular un error de conexión a la base de datos
    with patch('mysql.connector.connect', side_effect=mysql.connector.Error("Connection Error")):
        # Ejecutar la función y verificar que maneje la excepción
        try:
            timestamp = datetime.datetime.now()
            insert_request_data('beagle', 'https://images.dog.ceo/breeds/beagle/image.jpg',timestamp, 200)
            assert False, "Expected an exception but none was raised."
        except mysql.connector.Error as e:
            assert str(e) == "Connection Error"

