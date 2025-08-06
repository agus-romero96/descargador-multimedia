# Dockerfile

# Usa una imagen base de Python 3.10 que es ligera
FROM python:3.10-slim

# Actualiza la lista de paquetes e instala FFmpeg, que es necesario para yt-dlp
RUN apt-get update && apt-get install -y ffmpeg

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos de tu proyecto al contenedor
COPY . .

# Instala todas las dependencias de Python listadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Este es el comando que ejecutará la aplicación de Flask con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]