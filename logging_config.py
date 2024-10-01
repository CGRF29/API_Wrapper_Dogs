## Register layer
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    # Configurar el logger para los logs --> INFO, WARNING, ERROR, CRITICAL.
    info_handler = TimedRotatingFileHandler('info.log', when='D', interval=1, backupCount=4)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configurar el logger para los logs --> ERROR and CRITICAL.
    error_handler = TimedRotatingFileHandler('error.log', when='D', interval=1, backupCount=4)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configurar el logger
    logging.basicConfig(level=logging.INFO, handlers=[info_handler, error_handler])
"""
when='days': Especifica que la rotación se basa en días.
interval=7: Esto significa que la rotación de los logs ocurrirá cada 7 días.
backupCount=4: Mantendrá 4 archivos antiguos. Puedes ajustar este número según tus necesidades.
"""
