from flask import Flask, jsonify, request
import requests
import datetime
import logging
from logging_config import setup_logging
from controllers import insert_request_data

app = Flask(__name__)
setup_logging()  # Configurar logging

# Ruta para obtener una imagen de una raza de perro específica
@app.route('/dog/breed/<breed_name>', methods=['GET'])
def get_dog_image(breed_name):
    # Construir la URL de la API Dog CEO
    api_url = f'https://dog.ceo/api/breed/{breed_name.lower()}/images/random'

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
            logging.warning(f"Breed '{breed_name}' not found (404)")
            return jsonify({
                'error': 'Invalid breed or breed not found',
                'status': 'failure'
            }), 404

    except requests.exceptions.Timeout as timeout_err:
        # Manejo de errores de tiempo de espera
        logging.error(f"Timeout error occurred: {timeout_err}")
        return jsonify({
            'error': 'Request timed out',
            'message': str(timeout_err),
            'status': 'failure'
        }), 500

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión o fallos de la API
        logging.error(f"Error connecting to Dog CEO API: {e}")
        return jsonify({
            'error': 'Error connecting to the Dog CEO API',
            'message': str(e),
            'status': 'failure'
        }), 500

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    app.run(debug=True)
