# app.py
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, after_this_request
from modules.downloader import DownloadManager
import os
import shutil
# Esto solo funcionará localmente, en Render no se ejecutará
load_dotenv() 
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

        file_path = None

        try:
            file_path, filename = manager.download(plataforma, tipo, url, formato, calidad, noplaylist)

            if not os.path.exists(file_path):
                raise Exception("El archivo no se generó correctamente.")

            # Limpieza posterior al envío del archivo
            @after_this_request
            def cleanup(response):
                try:
                    temp_dir = os.path.dirname(file_path)
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception as cleanup_error:
                    print(f"Error al limpiar archivos temporales: {cleanup_error}")
                return response

            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )

        except Exception as e:
            # Limpieza si hubo error
            if file_path and os.path.exists(file_path):
                temp_dir = os.path.dirname(file_path)
                shutil.rmtree(temp_dir, ignore_errors=True)
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('index'))

    # Mostrar formulario vacío
    opciones = manager.get_options()
    return render_template('index.html', opciones=opciones)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
