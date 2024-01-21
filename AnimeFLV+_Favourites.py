import os
import re

FAVOURITES_ANIMES_DIR = os.getcwd() + "//config//FAVOURITESANIMES.txt"

with open(FAVOURITES_ANIMES_DIR, "r", encoding="utf-8") as favourites_animes:
    favourites_animes_txt = favourites_animes.readlines()
    cantidad_favoritos = len(favourites_animes_txt) // 3

animes = []

if cantidad_favoritos > 0:  # Comprueba si existe al menos un anime

    for indice in range(cantidad_favoritos):
        animes += [{"id": str(indice + 1),
                    "nombre": favourites_animes_txt[indice * 3].strip(),
                    "episodio": favourites_animes_txt[(indice * 3) + 1].strip()}]
        
    animes1 = []
        
    for anime in animes:

        nombre_archivo = anime["nombre"].replace(" ", "_").upper() + "_LOG.txt"
        ANIME_LOG_DIR = os.getcwd() + f"//config//logs1//{nombre_archivo}"
    
        with open(ANIME_LOG_DIR, "r", encoding="utf-8") as anime_log:
            anime_log_txt = anime_log.readlines()
            cantidad_logs = len(anime_log_txt) // 2

        print(anime["nombre"])

        for indice in range(cantidad_logs):
            print(anime_log_txt[indice * 2].strip())