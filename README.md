# API_Wrapper_Dogs

## 📌 Descripción

Este proyecto es una API wrapper que actúa como intermediario entre los usuarios y la API Dog CEO. Su propósito es proporcionar un control adicional, como el registro de logs y almacenamiento de solicitudes en una base de datos MySQL. Los usuarios pueden solicitar imágenes aleatorias de razas de perros, y la información se guarda en la base de datos para su análisis futuro.
Este proyecto incluye manejo de errores y pruebas unitarias usando pytest, y está diseñado para ejecutarse localmente.

## 📌 Archivos del Proyecto

`app.py`

Este archivo contiene la lógica principal de la API Flask. Aquí se define el endpoint /dog/breed/<breed_name>, que se conecta a la API de Dog CEO para obtener imágenes de razas de perros. El archivo maneja las respuestas, registra errores y almacena los resultados en la base de datos MySQL.

`controllers.py`

Define las funciones relacionadas con la base de datos, como la configuración de la conexión y la inserción de datos. Contiene la lógica para insertar en la tabla requests, en donde se almacena la raza de perro solicitada, la URL de la imagen, la marca de tiempo y el código de respuesta de la API.

`logging_config.py`

Configura el sistema de registro de la aplicación. Establece los manejadores de logs para almacenar información de nivel INFO y errores en archivos separados (info.log, error.log y info_test.log), permitiendo la rotación de logs diarios.

📁 tests

`test_app.py`

Incluye las pruebas unitarias para el archivo app.py. Se usan mocks para simular respuestas de la API Dog CEO, validando diferentes escenarios como éxitos, errores de conexión, razas no válidas y tiempos de espera.

`test_controllers.py`

Este archivo contiene las pruebas para las funciones de controllers.py, especialmente el manejo de la base de datos. Valida que los datos se guarden correctamente en la base de datos y que se manejen los errores de conexión.

## 📌 Instalación

Configurar la base de datos MySQL:
- Asegurarse de tener Docker instalado
- Ejecuta el siguiente comando para crear y ejecutar el contenedor MySQL:
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=dog_api -p 3306:3306 -d mysql:latest
- Asegurarse que los detalles de conexión en controllers.py estén correctos.

Instalación de las dependencias:
pip install -r requirements.txt

## 📌 Uso

Para ejecutar la aplicación, usa el siguiente comando:
python app.py

Puedes probar el endpoint utilizando:
HTML
- Ingresa la URL: http://localhost:5000/dog/breed/<type_breed>

Postman
- Crea una nueva solicitud GET
- Ingresa la URL: http://localhost:5000/dog/breed/<type_breed>
- Haz clic en "Enviar" y observa la respuesta

## 📌 Pruebas
Este proyecto incluye varias pruebas unitarias diseñadas para asegurar la funcionalidad y robustez de la API. Se utilizan herramientas como pytest y pytest-cov para ejecutar las pruebas y medir la cobertura del código.

1. Puntos Clave Considerados para las Pruebas Unitarias
    `Cobertura de Funcionalidades Clave:` Se aseguraron de probar todas las funcionalidades críticas de la API, incluyendo los endpoints y la interacción con la base de datos.
    `Manejo de Errores:` Se implementaron pruebas para manejar situaciones de error, como solicitudes inválidas a la API y fallos de conexión a la base de datos. Esto incluye verificar que los mensajes de error se registren correctamente en los logs.
    `Pruebas de Excepciones:` Se usaron técnicas de simulación (mocking) para simular errores en las dependencias externas, como la API externa y la base de datos, asegurando que se manejen adecuadamente.
    `Validación de Respuestas:` Las pruebas validan no solo el código de estado de la respuesta, sino también el contenido de la respuesta JSON para asegurarse de que los datos devueltos sean correctos.
    `Registro de Logs:` Se verificó que los errores se registraran adecuadamente en los archivos de log, lo que ayuda en la depuración y monitoreo del sistema.
    `Uso de Herramientas de Prueba:` Se utilizó pytest para facilitar la ejecución y organización de las pruebas, así como pytest-cov para medir la cobertura del código. 

2. Uso
Para ejecutar las pruebas automatizadas:
- Asegurarse que el contenedor de MySQL esté en ejecución
- Crear la base de datos 'dog_api_test' en MySQL:
    CREATE DATABASE dog_api_test;
    USE dog_api_test;

Para ejecutar todas las pruebas, utiliza:
coverage run -m pytest tests/ -v -s

Para ver el reporte de cobertura:
coverage report -m

El proyecto cuenta con un 97% de cobertura de pruebas, lo que indica que la mayoría del código ha sido evaluado a través de pruebas unitarias. 

## 📌 Registro de Errores

Los errores y la información de las solicitudes se registran en los archivos info.log, error.log y info_test.log, respectivamente.





