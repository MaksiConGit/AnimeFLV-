from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/save-data', methods=['POST', 'OPTIONS'])
def save_data():
    if request.method == 'OPTIONS':
        # Responder a la solicitud OPTIONS
        response = jsonify({})
    else:
        data = request.get_json()

        # Obtener la hora actual
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        EXTENSION_LOG_DIR = os.getcwd() + "\\config\\EXTENSIONLOG.txt"
        with open(EXTENSION_LOG_DIR, "a", encoding="utf-8") as extension_log:
            # Obtener el nombre y el número del capítulo desde los datos
            anime_name = data.get('animeName', '')
            chapter_number = data.get('chapterNumber', '')

            # Construir la cadena con la hora, el nombre y el número del capítulo
            log_entry = f"{anime_name}\nEpisodio {chapter_number}\n{current_time}"

            # Escribir la cadena en el archivo de registro
            extension_log.write(log_entry + "\n")

        response = "Datos recibidos y guardados correctamente"

    return response

if __name__ == '__main__':
    app.run(debug=True)
