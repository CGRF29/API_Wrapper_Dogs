import mysql.connector
import logging
import datetime
import os

## Control layer
# Configuración de la conexión a la base de datos MySQL
# Configuración de la base de datos basada en el entorno
def get_db_config():
    if os.getenv('PYTHON_ENV') == 'test':  # Verifica si estamos en el entorno de pruebas
        return {
            'user': 'root',
            'password': 'password',
            'host': 'localhost',
            'port': 3306,
            'database': 'dog_api_test'  # Base de datos de prueba
        }
    else:
        return {
            'user': 'root',
            'password': 'password',
            'host': 'localhost',
            'port': 3306,
            'database': 'dog_api'  # Base de datos de producción
        }

def insert_request_data(breed, image_url, response_code):
    db_config = get_db_config()  # Obtener la configuración correcta de la base de datos
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:

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

                query = """
                INSERT INTO requests (breed, image_url, request_timestamp, response_code)
                VALUES (%s, %s, %s, %s)
                """
                timestamp = datetime.datetime.now()
                values = (breed, image_url, timestamp, response_code)

                cursor.execute(query, values)
                conn.commit()
                #print(f"Data inserted: {breed}, {image_url}, {timestamp}, {response_code}")
                
                # Log de nivel INFO para solicitudes exitosas
                logging.info(f"Data inserted: {breed}, {image_url}, {response_code}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        logging.error(f"Database error: {err}")

    except Exception as e:
        # Log de nivel ERROR para cualquier otro tipo de error
        logging.error(f"Unexpected error: {e}")

    finally:
        cursor.close()
        conn.close()
