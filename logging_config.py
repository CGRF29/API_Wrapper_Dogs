## Capa de Registro

# Librerías
import os
import logging # Módulo para registrar eventos y mensajes
from logging.handlers import TimedRotatingFileHandler  # Manejador de logs con rotación programada

# Crear el directorio de logs si no existe
os.makedirs('logs', exist_ok=True)

# Función para configurar el sistema de logging
def setup_logging(testing=False):
    """
    Descripción:
    Configura el sistema de logging de la aplicación.
    - Nivel INFO --> INFO, WARNING, ERROR, CRITICAL.
    Estos logs se guardarán en 'info.log', rotando cada día
    - Nivel ERROR --> ERROR and CRITICAL.
    Estos logs se guardarán en 'error.log', también con rotación diaria

    Parametros:
    - 'when': Establece cuándo se debe rotar el archivo de log. 'D' significa que la rotación se hará diariamente.
    - 'interval': Especifica el intervalo en que ocurrirá la rotación. Aquí está configurado para cada 1 día.
    - 'backupCount': Define cuántos archivos antiguos de log se guardarán. Aquí se mantendrán 4 archivos antiguos antes de sobrescribir.
    """

        # Definir la ruta para los logs
    info_log_path = os.path.join('logs', 'info.log')
    error_log_path = os.path.join('logs', 'error.log')

    info_handler = TimedRotatingFileHandler(info_log_path, when='D', interval=1, backupCount=4)
    info_handler.setLevel(logging.INFO) # Establecer el nivel de log a INFO
    # Definir el formato de los mensajes de log (incluyendo tiempo, nivel y mensaje)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    error_handler = TimedRotatingFileHandler(error_log_path, when='D', interval=1, backupCount=4)
    error_handler.setLevel(logging.ERROR) # Establecer el nivel de log a ERROR
    # Definir el formato de los mensajes de log (incluyendo tiempo, nivel y mensaje)   
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configurar el logger
    logging.basicConfig(level=logging.INFO, handlers=[info_handler, error_handler])

    # Si estamos en modo de prueba, agrega un handler para info_test.log
    if testing:
        test_info_handler = TimedRotatingFileHandler(os.path.join('logs', 'info_test.log'), when='D', interval=1, backupCount=4)
        test_info_handler.setLevel(logging.INFO)
        test_info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(test_info_handler)  