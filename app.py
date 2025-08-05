# --- app.py ---
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, after_this_request
from modules.downloader import DownloadManager
import os

app = Flask(__name__)
app.secret_key = 'cambia_por_una_clave_segura'
manager = DownloadManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        plataforma = request.form.get('plataforma')
        tipo = request.form.get('tipo')
        url = request.form.get('url')
        formato = request.form.get('formato')
        calidad = request.form.get('calidad')
        noplaylist = request.form.get('noplaylist') == 'on'
        try:
            # Descargar y obtener ruta de archivo temporal
            file_path, filename = manager.download(plataforma, tipo, url, formato, calidad, noplaylist)
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('index'))

        @after_this_request
        def cleanup(response):
            try:
                os.remove(file_path)
            except Exception:
                pass
            return response

        # Enviar el archivo al cliente para descarga
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )

    opciones = manager.get_options()
    return render_template('index.html', opciones=opciones)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
