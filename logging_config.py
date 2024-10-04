## Capa de Registro

# Librerías
import logging # Módulo para registrar eventos y mensajes
from logging.handlers import TimedRotatingFileHandler  # Manejador de logs con rotación programada

# Función para configurar el sistema de logging
def setup_logging():
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
    info_handler = TimedRotatingFileHandler('info.log', when='D', interval=1, backupCount=4)
    info_handler.setLevel(logging.INFO) # Establecer el nivel de log a INFO
    # Definir el formato de los mensajes de log (incluyendo tiempo, nivel y mensaje)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    error_handler = TimedRotatingFileHandler('error.log', when='D', interval=1, backupCount=4)
    error_handler.setLevel(logging.ERROR) # Establecer el nivel de log a ERROR
    # Definir el formato de los mensajes de log (incluyendo tiempo, nivel y mensaje)   
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configurar el logger
    logging.basicConfig(level=logging.INFO, handlers=[info_handler, error_handler])
