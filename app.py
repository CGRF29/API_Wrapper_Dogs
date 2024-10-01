from flask import Flask, jsonify, request
import requests
import datetime
import mysql.connector

app = Flask(__name__)

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
    
    finally:
        cursor.close()
        conn.close()

# Ruta para obtener una imagen de una raza de perro específica
@app.route('/dog/breed/<breed_name>', methods=['GET'])
def get_dog_image(breed_name):
    # Construir la URL de la API Dog CEO
    api_url = f'https://dog.ceo/api/breed/{breed_name}/images/random'

    try:
        # Hacer la solicitud GET a la API externa
        response = requests.get(api_url)
        data = response.json()

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200 and data['status'] == 'success':
            image_url = data['message']
            timestamp = datetime.datetime.now()

            # Llamar a la función para insertar los datos en la base de datos
            insert_request_data(breed_name, image_url, response.status_code)

            # Devolver la respuesta con la URL de la imagen
            return jsonify({
                'breed': breed_name,
                'image_url': image_url,
                'request_timestamp': timestamp,
                'status': 'success'
            }), 200
        else:
            # Manejar el caso donde la raza no es válida
            return jsonify({
                'error': 'Invalid breed or breed not found',
                'status': 'failure'
            }), 404

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión o fallos de la API
        return jsonify({
            'error': 'Error connecting to the Dog CEO API',
            'message': str(e),
            'status': 'failure'
        }), 500

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    app.run(debug=True)
