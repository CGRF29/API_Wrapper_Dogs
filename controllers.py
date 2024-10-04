#Librerías
import mysql.connector
import logging
import datetime
import os
from dotenv import load_dotenv  # Importar load_dotenv

## Capa de control
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Función para configurar la conexión a la base de datos MySQL
def get_db_config():
    """
    Descripción:
    Obtiene la configuración de la base de datos dependiendo del entorno (pruebas o producción).
    Si el entorno es de prueba ('test'), se conectará a la base de datos de prueba, de lo contrario, se conectará a la base de datos de producción.

    Salida:
    - Devuelve un diccionario con la configuración de la base de datos (usuario, contraseña, host, puerto, y base de datos a usar).
    """
    # Verifica si el entorno es de pruebas
    if os.getenv('PYTHON_ENV') == 'test':  
        return {
            'user': os.getenv('MYSQL_USER'),  # Leer el usuario desde las variables de entorno
            'password': os.getenv('MYSQL_PASSWORD'),  # Leer la contraseña desde las variables de entorno
            'host': os.getenv('MYSQL_HOST'),  # Leer el host desde las variables de entorno
            'port': int(os.getenv('MYSQL_PORT')),  # Leer el puerto desde las variables de entorno
            'database': 'dog_api_test'  # Base de datos de prueba
        }
    else:
        # Configuración para el entorno de producción
        return {
            'user': os.getenv('MYSQL_USER'),  # Leer el usuario desde las variables de entorno
            'password': os.getenv('MYSQL_PASSWORD'),  # Leer la contraseña desde las variables de entorno
            'host': os.getenv('MYSQL_HOST'),  # Leer el host desde las variables de entorno
            'port': int(os.getenv('MYSQL_PORT')),  # Leer el puerto desde las variables de entorno
            'database': os.getenv('MYSQL_DATABASE')  # Leer la base de datos desde las variables de entorno
        }
    
# Función para insertar los datos de la solicitud en la base de datos
def insert_request_data(breed, image_url, timestamp, response_code):
    """
    Descripción:
    Inserta los datos de una solicitud en la base de datos. Crea una tabla 'requests' si no existe y almacena la raza solicitada, la URL de la imagen, la marca de tiempo y el código de respuesta.

    Parámetros:
    - breed (str): La raza del perro solicitada.
    - image_url (str): La URL de la imagen obtenida de la API Dog CEO.
    - response_code (int): El código de respuesta recibido de la API Dog CEO.

    Salida:
    - Inserta los datos en la base de datos y registra el resultado en un log.
    """    
    # Obtener la configuración correcta de la base de datos
    db_config = get_db_config()  
    try:
        # Establecer la conexión con la base de datos usando la configuración obtenida
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Crear la tabla 'requests' si no existe en la base de datos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS requests (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        breed VARCHAR(50),
                        image_url TEXT,
                        request_timestamp DATETIME,
                        response_code INT
                    );
                """)
                # Preparar la consulta SQL para insertar los datos
                query = """
                INSERT INTO requests (breed, image_url, request_timestamp, response_code)
                VALUES (%s, %s, %s, %s)
                """
                # Datos que se van a insertar
                values = (breed, image_url, timestamp, response_code)
                # Ejecutar la inserción de los datos en la base de datos
                cursor.execute(query, values)
                # Confirmar los cambios en la base de datos
                conn.commit()
                #print(f"Data inserted: {breed}, {image_url}, {timestamp}, {response_code}")
                
                # Registrar un log de nivel INFO con los detalles de la solicitud exitosa
                logging.info(f"Data inserted: {breed}, {image_url}, {response_code}")
    
    # Errores relacionados con la base de datos y registrarlos
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        raise  # OJO: lanza la excepción para que la prueba pueda capturarla
    
    # Errores relacionados para cualquier otro tipo de error
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

    # Asegurarse de que el cursor y la conexión se cierran al finalizar   
    finally: 
        if os.getenv('PYTHON_ENV') != 'test':      
            cursor.close()
            conn.close()
