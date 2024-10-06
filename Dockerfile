# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt a la imagen
COPY requirements.txt .

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
