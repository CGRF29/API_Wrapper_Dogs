import mysql.connector
import logging
import datetime

## Control layer
# Configuración de la conexión a la base de datos MySQL
db_config = {
    'user': 'root',  # Cambia esto si tu usuario de MySQL es diferente
    'password': 'password',  # Cambia por la contraseña de tu usuario
    'host': 'localhost',
    'port':3306,
    'database': 'dog_api'
}

def insert_request_data(breed, image_url, response_code):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO requests (breed, image_url, request_timestamp, response_code)
        VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.datetime.now()
        values = (breed, image_url, timestamp, response_code)

        cursor.execute(query, values)
        conn.commit()
        print(f"Data inserted: {breed}, {image_url}, {timestamp}, {response_code}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        logging.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()
