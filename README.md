# API_Wrapper_Dogs

## 📌 Descripción

Este proyecto es una API wrapper que actúa como intermediario entre los usuarios y la API Dog CEO. Su propósito es proporcionar un control adicional, como el registro de logs y almacenamiento de solicitudes en una base de datos MySQL. Los usuarios pueden solicitar imágenes aleatorias de razas de perros, y la información se guarda en la base de datos para su análisis futuro.
Este proyecto incluye manejo de errores y pruebas unitarias usando pytest, y está diseñado para ejecutarse localmente.

## 📌 Archivos del Proyecto

`app.py`

Este archivo contiene la lógica principal de la API Flask. Aquí se define el endpoint /dog/breed/<breed_name>, que se conecta a la API de Dog CEO para obtener imágenes de razas de perros. El archivo maneja las respuestas, registra errores y almacena los resultados en la base de datos MySQL.

`controllers.py`

Define las funciones relacionadas con la base de datos, como la configuración de la conexión y la inserción de datos. Contiene la lógica para insertar en la tabla requests, que almacena la raza solicitada, la URL de la imagen, la marca de tiempo y el código de respuesta de la API.

`logging_config.py`

Configura el sistema de registro de la aplicación. Establece los manejadores de logs para almacenar información de nivel INFO y errores en archivos separados (info.log y error.log), permitiendo la rotación de logs diarios.

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

Puedes probar el endpoint utilizando Postman:
- Crea una nueva solicitud GET
- Ingresa la URL: http://localhost:5000/dog/breed/hound
- Haz clic en "Enviar" y observa la respuesta

## 📌 Pruebas

Para ejecutar las pruebas automatizadas:
- Asegurarse que el contenedor de MySQL esté en ejecución
- Ejecuta las pruebas utilizando pytest:
coverage run -m pytest tests/
- Para ver el reporte de cobertura:
coverage report -m

El proyecto tiene una cobertura de pruebas del 96%, con todas las áreas clave cubiertas. Las áreas faltantes se encuentran principalmente en el manejo de errores dentro de controllers.py, donde algunas rutas de error podrían requerir pruebas adicionales para alcanzar una cobertura del 100%.

## 📌 Registro de Errores

Los errores y la información de las solicitudes se registran en los archivos info.log y error.log, respectivamente.





