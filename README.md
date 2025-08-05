# 📥 Descargador Multimedia Accesible

Este proyecto es una aplicación web sencilla y accesible, construida con el framework Flask de Python, que permite descargar contenido multimedia (audio y video) desde plataformas como YouTube y Spotify.

La aplicación está diseñada para ser fácil de usar, con una interfaz web que puede ser controlada tanto visualmente como a través de un lector de pantalla.

## 🚀 Características

* **Interfaz Web Accesible:** Un formulario simple para seleccionar las opciones de descarga.
* **Soporte Multi-Plataforma:** Descarga desde **YouTube** y **Spotify**.
* **Opciones de Formato y Calidad:** Elige entre diferentes formatos (`mp3`, `mp4`, `wav`, etc.) y calidades para tus descargas.
* **Manejo de Playlists:** Opción para descargar pistas individuales o listas de reproducción completas.
* **Descarga en el Cliente:** Los archivos descargados se envían directamente al navegador del usuario para su almacenamiento local.

## ⚙️ Instalación

Asegúrate de tener Python 3.8 o superior instalado.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
    cd tu_repositorio
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # En Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # En macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    Crea un archivo llamado `requirements.txt` en la carpeta principal con el siguiente contenido:
    ```
    Flask
    yt-dlp
    spotipy
    mutagen
    requests
    gTTS
    ```
    Luego, ejecuta el siguiente comando para instalar todo:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Uso

1.  Asegúrate de que tu entorno virtual esté activo.
2.  Ejecuta el servidor de la aplicación desde la terminal:
    ```bash
    python app.py
    ```
3.  Abre tu navegador web y visita la siguiente dirección:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```

## 📂 Estructura del Proyecto

* `app.py`: Archivo principal de la aplicación Flask.
* `modules/downloader.py`: Contiene toda la lógica de descarga.
* `templates/index.html`: La interfaz de usuario del formulario.
* `requirements.txt`: Lista de dependencias del proyecto.
* `.gitignore`: Archivo para ignorar directorios y archivos que no deben subirse a Git.
