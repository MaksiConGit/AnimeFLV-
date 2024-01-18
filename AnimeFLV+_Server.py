from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import re

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

        # Se crea la carpeta
        if not os.path.exists(os.getcwd() + "\\config\\logs\\"):
            os.makedirs("config\\logs")

        EXTENSION_LOG_DIR = os.getcwd() + "\\config\\EXTENSIONLOG.txt"

        # Obtener el nombre y el número del capítulo desde los datos
        anime_name = data.get('animeName', '')
        chapter_number = data.get('chapterNumber', '')
        
        with open(EXTENSION_LOG_DIR, "a", encoding="utf-8") as extension_log:

            # Construir la cadena con la hora, el nombre y el número del capítulo
            log_entry = f"{anime_name}\nEpisodio {chapter_number}\n{current_time}\n"

            # Escribir la cadena en el archivo de registro
            extension_log.write(log_entry + "\n")

        nombre_anime_log = anime_name.replace(' ', '_').upper() + "_LOG"

        ANIME_LOG_DIR = os.getcwd() + f"\\config\\logs\\{nombre_anime_log}.txt"

        with open(ANIME_LOG_DIR, "a", encoding="utf-8") as anime_log:
            anime_log_entry = f"Episodio {chapter_number}\n{current_time}\n"
            anime_log.write(anime_log_entry + "\n")

        response = "Datos recibidos y guardados correctamente"

    return response

if __name__ == '__main__':
    app.run(debug=True)
