# API_Wrapper_Dogs 🐶

![API](https://github.com/user-attachments/assets/09bdf1fd-8ee5-45bb-82e0-7d1a48914641)

## 📌 Description

This project is an API wrapper that acts as an intermediary between users and the Dog CEO API. Its purpose is to provide additional control, such as logging and storing requests in a MySQL database. Users can request random images of dog breeds, and the information is stored in the database for future analysis.

> [!NOTE]
> This project includes error handling and unit testing using pytest, and is designed to run locally, without docker-compose.


## 📌  Project Files

`requirements.txt`

The file contains a list of Python dependencies that the application needs to function properly.

`init.sql`

Contains the SQL script that is executed when the MySQL container is initialized when using docker-compose. This script is used to configure the application database, for example, creating required tables, users, or initial configurations.

`Dockerfile`

It contains instructions for building a Docker image, defining how to build and configure the environment to run the Flask application. This file allows the application to be replicated in any environment in a consistent manner.

`docker-compose.yml`

Defines the services required to run the application in separate containers and how they interact with each other. Allows multiple Docker services, such as the Flask application and MySQL database, to run together with a single command.

`app.py`

It contains the main logic of the Flask API. The endpoint /dog/breed/<breed_name>  is defined here, which connects to the Dog CEO API to get images of dog breeds. The file handles responses, logs errors and stores the results in the MySQL database.

`controllers.py`

Defines database-related functions, such as connection setup and data insertion. It contains the logic for inserting into the requests table, where the requested dog breed, the image URL, the timestamp and the API response code are stored.

`logging_config.py`

Configures the application logging system. Errors and request information are logged in info.log, error.log and info_test.log files, respectively. The logging system is configured by levels (INFO, ERROR) to separate general information from errors, and is automatically rotated according to time. This is achieved by defined time intervals (when and backupCount parameters), which ensures that log files are saved and archived efficiently.

📁 tests

`test_app.py`

It includes unit tests for the app.py file. Mocks are used to simulate Dog CEO API responses, validating different scenarios such as successes, connection errors, invalid races and timeouts.

`test_controllers.py`

This file contains the tests for the controllers.py functions, especially the database handling. It validates that data is correctly stored in the database and that connection errors are handled.

## 📌 Installation without docker-compose

Configure the MySQL database:
- Ensure That you have Docker installed
- Run the following command to create and run the MySQL container:
```
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=dog_api -p 3306:3306 -d mysql:latest
```
- Ensure that the connection details in controllers.py are correct.

Installation of the dependencies:
```
pip install -r requirements.txt
```

## 📌 Use

1. To run the application, use the following command:
```
python app.py
```

2. Test the endpoint using:
HTML
- Enter the URL: 
```
http://localhost:5000/dog/breed/<type_breed>
```

Postman
- Create a new GET request
- Enter the URL: 
```
http://localhost:5000/dog/breed/<type_breed>
```
- Click on “Send” and watch the response

3. Visualize the correct request in MySQL Container
```
docker exec -it mysql-container mysql -u root -p
```
```
#MySQL
USE dog_api;
SELECT * FROM requests;
```

## 📌 Use with Docker-Compose

> [!NOTE]
> Make sure you have Docker installed

Steps to execute the application:

1.	Clone the project repository:
```
git clone https://github.com/CGRF29/API_Wrapper_Dogs.git
cd API_Wrapper_Dogs
```

2.	(Optional) Modify the configuration:
-	Modify MySQL credentials: You can change the credentials and the database name in the .env file in the environment variables.
-	Logs: You can customize the configuration in the logging_config.py file to adjust the automatic rotation of logs according to time by modifying parameters such as when (time interval) and backupCount (number of backup files).

3.	Build and lift containers
Navigate to the directory where your docker-compose.yml file is located and run:
```
docker-compose up –build -d
docker-compose up
```
The containers will be ready for use when you see something similar to:
```
flask_app   |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

4.	Access the application:
Once the containers are running, you can access the Flask API in your browser or by using tools such as Postman 
- HTML
Enter the URL 
```
http://localhost:5000/dog/breed/<type_breed>
```
- Postman
1. Create a new GET request
2. Enter the URL: 
```
http://localhost:5000/dog/breed/<type_breed>
```
3. Click on “Send” and watch the response

5. Visualize the correct request in MySQL Container
```
docker exec -it mysql_db mysql -u root -p
```
```
#MySQL
USE dog_api;
SELECT * FROM requests;
```

6.	Stop the application:
If you want to stop the containers, simply press CTRL + C in the terminal where you ran docker-compose up. To stop and remove all containers and associated networks, run:
```
docker-compose down
```

## 📌 Tests
This project includes several unit tests designed to ensure the functionality and robustness of the API. Tools such as pytest and pytest-cov are used to run the tests and measure code coverage.

1. Key points considered:   

    `Key Functionality Coverage:` Make sure to test all critical API functionality, including endpoints and database interaction.

    ` Error Handling:` Check the implementation to handle error situations, such as invalid API requests and database connection failures. This includes verifying that error messages are correctly recorded in the logs.
    
    `Exception Testing:` Mocking techniques use to simulate errors in external dependencies, such as the external API and database, ensuring that they are handled properly
    
    ` Response Validation:` The tests validate not only the status code of the response, but also the content of the JSON response to ensure that the data returned is correct.
    
    `Logging:` Verify that errors are properly recorded in the log files, which helps in debugging and monitoring the system.
    
    `Use of Testing Tools:` Use pytest to facilitate the execution and organization of tests, as well as pytest-cov to measure code coverage.

2. Use
To run automated tests:
- Ensure MySQL container is running
- Create the database 'dog_api_test' in MySQL:
```
    CREATE DATABASE dog_api_test;
    USE dog_api_test;
```
To run all tests, use:
```
coverage run -m pytest tests/ -v -s
```
To view the coverage report:
```
coverage report -m
```
The project has 97% test coverage, indicating that the majority of the code has been evaluated through unit testing.

## 📌 Future improvements

This project can be further enhanced and scaled with different additional functionalities. An example of improvement would be the implementation of rate limiting in the Flask API to prevent abuse and server overloads, which would help ensure controlled and efficient access to the API, protecting it from excessive or malicious use.
Any suggestion to improve or modify the project is welcome.

## 📌 Bibliography

What are API Wrappers? [Page](https://apidog.com/blog/what-are-api-wrappers/).

How to Set Up and Configure MySQL in Docker [Page](https://www.datacamp.com/tutorial/set-up-and-configure-mysql-in-docker).

Python and MySQL Database: A Practical Introduction [Page](https://realpython.com/python-mysql/).

Logging in Python [Page](https://realpython.com/python-logging/).

Create Tests for the Flask Framework Using Pytest-Flask[Page](https://openclassrooms.com/en/courses/7747411-test-your-python-project/7894396-create-tests-for-the-flask-framework-using-pytest-flask).

Testing Flask Applications with Pytest [Page](https://testdriven.io/blog/flask-pytest/).

Mastering Python Mock and Patch: Mocking For Unit Testing [Page](https://codefather.tech/blog/python-mock-and-patch/).

Dockerizing a Flask-MySQL app with docker-compose[Page](https://stavshamir.github.io/python/dockerizing-a-flask-mysql-app-with-docker-compose/).

Dockerizing Flask+MySQL Application Using Compose[Page](https://blog.abbasmj.com/dockerizing-flaskmysql-application-using-compose).
