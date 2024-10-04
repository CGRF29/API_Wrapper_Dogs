#Librerías
from flask import Flask, jsonify, request
import requests
import datetime
import logging
from logging_config import setup_logging 
from controllers import insert_request_data 
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
# Configurar logging a través de una función externa definida en logging_config.py
setup_logging() 
""" 
# Configurar el limitador
limiter = Limiter(
    get_remote_address,  # Función para obtener la dirección IP del cliente
    default_limits=["200 per day", "1 per hour"]  # Límites por defecto
)
"""
# Ruta para obtener una imagen de una raza de perro específica
@app.route('/dog/breed/<breed_name>', methods=['GET'])
#@limiter.limit("1 per minute")  # Limitar a 10 solicitudes por minuto por dirección IP
def get_dog_image(breed_name):
    """
    Descripción:
    Endpoint que obtiene una imagen aleatoria de una raza de perro específica desde la API Dog CEO.
    Almacena la información de la solicitud en una base de datos.

    Parámetros:
    - breed_name (str): Nombre de la raza de perro que el usuario solicita.
    
    Salida:
    - Solicitud exitosa:
      * Retorna un JSON con la raza, la URL de la imagen, la marca de tiempo, y el estado 'success'.
      * Código de estado HTTP 200.
    - Raza no es válida:
      * Retorna un JSON con un error, indicando que la raza es inválida.
      * Código de estado HTTP 404.
    - Error de conexión o un tiempo de espera:
      * Retorna un JSON con un mensaje de error.
      *Código de estado HTTP 500.
    """

    # Construir la URL de la API Dog CEO
    api_url = f'https://dog.ceo/api/breed/{breed_name.lower()}/images/random'

    try:
        # Hacer la solicitud GET a la API externa
        response = requests.get(api_url)
        data = response.json() # Convertir la respuesta en JSON

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200 and data['status'] == 'success':
            image_url = data['message']
            timestamp = datetime.datetime.now()

            # Llamar a la función para insertar los datos en la base de datos
            insert_request_data(breed_name, image_url, timestamp,response.status_code)

            # Devolver la respuesta con la información solicitada
            return jsonify({
                'image_url': image_url,
                'status': 'success'
            }), 200
        else:
            # Manejar el caso donde la raza no es válida
            logging.warning(f"Breed '{breed_name}' not found (404)")
            return jsonify({
                'error': 'Invalid breed or breed not found',
                'status': 'failure'
            }), 404
        
    # Manejar el caso de que la solicitud a la API exceda el tiempo de espera
    except requests.exceptions.Timeout as timeout_err:
        # Registrar el error
        logging.error(f"Timeout error occurred: {timeout_err}")
        return jsonify({
            'error': 'Request timed out',
            'message': str(timeout_err),
            'status': 'failure'
        }), 500
    
    # Manejar cualquier otro tipo de error de conexión o fallo de la API externa
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to Dog CEO API: {e}")
        return jsonify({
            'error': 'Error connecting to the Dog CEO API',
            'message': str(e),
            'status': 'failure'
        }), 500

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    app.run(debug=True)
