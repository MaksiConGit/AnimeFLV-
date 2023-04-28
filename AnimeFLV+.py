from bs4 import BeautifulSoup
from winotify import Notification, audio
from playsound import playsound
import requests
import re
import time
import colorama
from colorama import Back, Fore, Style
import keyboard
import os
import webbrowser
import win32gui
import win32console
import win32con
import pystray
from PIL import Image
import threading
import atexit
from tqdm import tqdm
from itertools import cycle
import sys


def comprobar_suscripciones():
    """
    Comprueba si estás suscrito a al menos
    un anime para empezar a buscar episodios
    automáticamente. Retorna valores que
    pueden mostrar o no las opciones.
    """

    animes_suscritos, mostrar_lista, _ = lista_animes_suscritos()

    if animes_suscritos >= 1:  # Si estamos suscritos a al menos un anime, busca directamente
        print(mostrar_lista)
        barra_de_carga()

        return False, "1"

    return True, None


def configurar_notificaciones():
    """
    El usuario configura el script. Se crea
    una carpeta y se mueven el sonido y la
    imagen a la misma, también se crean los
    .txt en esta carpeta para ordenar todo.
    Retorna True para no volver a mostrar el
    "Bienvenido a".
    """

    print("\n\n¡¡Muchas gracias por apoyar mis proyectos!!")

    input("\n\nPrimero que nada, vamos a personalizar el programa"
          " para que tengas una experiencia única."
          "\n\nPresione ENTER para continuar.")

    print("\n\n\nPaso 1: Elije una imagen para las notificaciones.")
    print("\n\nEsta imagen se mostrará junto con"
          "el nombre del anime y el número del nuevo capítulo.")

    input("\n\n1. Copia una imagen (jpg, jpeg, png, gif) de tus archivos locales."
          "\n\n2. Pega esa imagen en la carpeta del programa."
          "\n\n3. Presione ENTER cuando esté listo.")

    print("\n\n\nPaso 2: Elije un sonido para las notificaciones.")
    print("\n\nEste sonido debe ser corto, puede ser una parte de "
          "una canción o un simple sonido de notificación.")
    print("\n\n1. Copia un sonido (.mp3, .wav) de tus archivos locales." +
          "\n\n2. Pega ese sonido en la carpeta del programa."
          "\n\n3. Presione ENTER cuando esté listo.")
    print("\n\nIMPORTANTE:\n\n"
          "Si desea el sonido de notificación predeterminado de Windows, "
          "no haga ningún cambio, únicamente presione ENTER.\n")

    input()

    # Se crea la carpeta
    if not os.path.exists(os.getcwd() + "\\config\\"):
        os.makedirs("config")

    # Mueve la imagen y el sonido a la nueva carpeta
    for filename in os.listdir(os.getcwd()):

        name, extension = os.path.splitext(os.getcwd() + filename)

        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            image_dir = os.getcwd() + "\\config\\" + "Image" + extension
            os.rename(os.getcwd() + "\\" + filename, image_dir)

        elif extension in [".mp3", ".wav"]:
            sound_dir = os.getcwd() + "\\config\\" + "Sound" + extension
            os.rename(os.getcwd() + "\\" + filename, sound_dir)

    # Crea el .txt de los animes suscritos
    with open(SUSCRIBED_ANIMES_DIR, "wb") as suscribed_animes:
        pass

    with open(SEEN_ANIMES_DIR, "wb") as seen_animes:
        pass

    return True  # Confirma que ya se mostró el "Bienvenido a"


def nuevos_capitulos():
    """
    Descripción de la función:

    Obtiene la información de los nuevos capítulos
    de la página AnimeFLV
    """

    url_anime_flv = 'https://www3.animeflv.net/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/58.0.3029.110 Safari/537.3'
    }

    pedido = requests.get(url_anime_flv, headers=headers, timeout=5)

    if pedido.status_code != 200:
        print(Fore.RED + "La página de AnimeFLV está caída, inténtelo más tarde")

    html = pedido.text

    soup = BeautifulSoup(html, "html.parser")

    nombres = soup.find_all('strong', class_='Title')
    capitulos = soup.find_all('span', class_='Capi')

    return nombres, capitulos


def barra_de_carga():
    """
    Descripción de la función:

    Antes de empezar a buscar nuevos capítulos
    de los animes suscritos, se informará al
    usuario que se le notificará cuando esto pase,
    además de darle instrucciones para volver 
    a abrir la consola si se desea.
    Paralelamente, se muestra una barra de carga
    que indica cuánto falta para ocultar la consola.
    """

    print(Fore.YELLOW + "\n\n¡Te notificaremos cuando se estrene un nuevo episodio!\n\n"
          "La consola se esconderá en unos segundos...\n\n"
          "Consulta el ícono oculto para mostrar la consola.\n\n")

    def progress_bar(progress, total):

        percent = 100 * (progress/float(total))

        if percent > 75.0:
            barra_cargando = Fore.MAGENTA + "█" * \
                int(percent) + "-" * (100 - int(percent))

        elif percent > 50.0:
            barra_cargando = Fore.BLUE + "█" * \
                int(percent) + "-" * (100 - int(percent))

        elif percent > 25:
            barra_cargando = Fore.GREEN + "█" * \
                int(percent) + "-" * (100 - int(percent))

        elif percent >= 0:
            barra_cargando = Fore.YELLOW + "█" * \
                int(percent) + "-" * (100 - int(percent))

        print(f"\r|{barra_cargando}| {percent:.2f}%", end="\r")

    progress_bar(0, 100)
    for porcentaje_de_barra in range(100):
        time.sleep(0.07)
        progress_bar(porcentaje_de_barra + 1, 100)

    win32gui.ShowWindow(win32console.GetConsoleWindow(),
                        win32con.SW_HIDE)  # Esconder la consola

    os.system("cls")  # Limpiar la terminal

    print("\n\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT +
          "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL)


def on_key_press(event):
    """
    Descripción de la función:

    Cancela la búsqueda de capítulos mediante
    la captura de la tecla "enter".
    """

    if event.name == 'enter':
        keyboard.unhook_all()  # Desactiva la captura de teclas
        print("\n" + Fore.LIGHTBLACK_EX + "Espere...")
        global CONFIRM
        CONFIRM = False


def lista_animes_suscritos():
    """
    Descripción de la función:

    Abre el bloc de notas, toma la información
    de los animes SUSCRITOS y los enumera en una lista.
    Retorna la cantidad de animes suscritos.
    """

    with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as suscribed_animes:
        suscribed_animes_txt = suscribed_animes.readlines()
        suscripciones = len(suscribed_animes_txt) // 3

    mostrar_lista_suscritos = "\n\n" + Back.LIGHTWHITE_EX + Fore.LIGHTGREEN_EX + \
        "Lista de animes suscritos:" + Fore.RESET + Back.RESET + "\n\n"

    animes = []

    if suscripciones < 1:  # Comprueba si existe al menos un anime
        mostrar_lista_suscritos += Fore.LIGHTBLACK_EX + "No estás suscrito a ningún anime.\n" + \
            "¡Suscríbete a uno para empezar a recibir notificaciones!"

        return suscripciones, mostrar_lista_suscritos, animes

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN,
                   Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for indice in range(suscripciones):
        animes += [{"id": str(indice + 1),
                    "nombre": suscribed_animes_txt[indice * 3].strip(),
                    "episodio": suscribed_animes_txt[(indice * 3) + 1].strip(),
                    "link": suscribed_animes_txt[(indice * 3) + 2].strip()}]

    for anime in animes:
        color = next(colors)
        mostrar_lista_suscritos += ("\n" + Style.BRIGHT + color + anime["id"] + ". "
                                    + Fore.WHITE + anime["nombre"]
                                    + Style.NORMAL + Fore.YELLOW + " | "
                                    + Style.BRIGHT + Fore.BLUE + anime["episodio"])

    return suscripciones, mostrar_lista_suscritos, animes


def lista_animes_vistos():
    """
    Descripción de la función:

    Abre el bloc de notas, toma la información
    de los animes VISTOS y los enumera en una lista.
    Retorna la cantidad de animes vistos.
    """

    with open(SEEN_ANIMES_DIR, "r", encoding="utf-8") as seen_animes:
        seen_animes_txt = seen_animes.readlines()
        num_animes_vistos = len(seen_animes_txt) // 3

    mostrar_lista_vistos = ("\n\n" + Style.RESET_ALL + Back.LIGHTWHITE_EX + Fore.LIGHTRED_EX +
                            "Lista de animes vistos:" + Fore.RESET + Back.RESET + Style.RESET_ALL + "\n")

    animes_vistos = []

    if num_animes_vistos < 1:  # Comprueba si existe al menos un anime

        mostrar_lista_vistos += (Fore.LIGHTBLACK_EX + "No viste ningún anime.\n"
                                 "¡Cuando finalice un anime suscrito, vendrá aquí!"
                                 "\nTIP: Puedes suscribirte a animes finalizados")

        return num_animes_vistos, mostrar_lista_vistos, animes_vistos

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN,
                   Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for indice in range(num_animes_vistos):
        animes_vistos += [{"id": str(indice + 1),
                           "nombre": seen_animes_txt[indice * 3].strip(),
                           "episodio": seen_animes_txt[(indice * 3) + 1].strip(),
                           "link": seen_animes_txt[(indice * 3) + 2].strip()}]

    for anime in animes_vistos:

        color = next(colors)

        mostrar_lista_vistos += ("\n" + Style.BRIGHT + color + anime["id"] + ". "  # Enumera
                                 + Fore.WHITE + anime["nombre"]  # Nombre
                                 + Style.NORMAL + Fore.YELLOW + " | "  # Separador
                                 + Fore.LIGHTBLUE_EX + anime["episodio"])  # Episodio

    return num_animes_vistos, mostrar_lista_vistos, animes_vistos


def borrar_anime_finalizado(anime_id_borrar):
    """
    Descripción de la función:

    Comprueba si el anime finalizó,
    si lo hizo, abre el bloc de notas y
    actualiza la lista de animes suscritos,
    al final muestra la misma lista actualizada.
    Devuelve el mensaje de "Finalizado" si el
    anime finalizó.
    """

    _, _, animes = lista_animes_suscritos()

    new_suscribed_animes = []

    for anime in animes:

        if anime["id"] == anime_id_borrar:

            # Limpiamos el link para transformarlo al de la página del anime
            url_anime_subs = anime["link"]
            url_anime_subs = url_anime_subs.replace("/ver/", "/anime/")
            clean_url = url_anime_subs.rfind('-')
            url_anime_subs = url_anime_subs[:clean_url]

            # Toma la información de la página
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                'AppleWebKit/537.36 (KHTML, like Gecko)'
                'Chrome/58.0.3029.110 Safari/537.3'
            }
            anime_subs_pedido = requests.get(
                url_anime_subs, headers=headers, timeout=5)
            anime_subs_html = anime_subs_pedido.text
            anime_subs_soup = BeautifulSoup(anime_subs_html, "html.parser")
            anime_susbs_estado = anime_subs_soup.find('span', class_='fa-tv')

            msg_finalizado = ""

            # Comprueba si finalizó
            if anime_susbs_estado.text == "Finalizado":

                msg_finalizado = " | Finalizado"  # Se agrega la esta información a la notificación

                # Se actualiza la lista de animes vistos
                with open(SEEN_ANIMES_DIR, 'ab') as seen_animes:
                    seen_animes.write(anime["nombre"].encode('utf-8') +
                                      b"\n" + anime["episodio"].encode('utf-8') +
                                      b"\n" + url_anime_subs.encode('utf-8') + b"\n")

                print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " + anime["nombre"] + "!\n" +
                      Fore.YELLOW + "\nEl anime fue enviado a la lista de animes finalizados")

                sumar_anime_suscrito = False

                _, mostrar_lista, _ = lista_animes_vistos()

                print(mostrar_lista)

            else:

                sumar_anime_suscrito = True

        else:

            sumar_anime_suscrito = True

        if sumar_anime_suscrito is True:

            new_suscribed_animes += anime["nombre"], "\n", anime["episodio"], "\n", anime["link"], "\n"

    # Actualiza la información del bloc de notas
    with open(SUSCRIBED_ANIMES_DIR, "wb") as suscribed_animes:
        suscribed_animes.writelines(line.encode(
            'utf-8') for line in new_suscribed_animes)

    return msg_finalizado


def cerrar_script():
    """
    Descripción de la función:

    Terminamos el hilo secundario antes de
    cerrar el hilo principal.
    """

    icon.stop()
    icon.update_menu()
    icon_thread.join()
    sys.exit()


class Anime():

    """
    Descripción de la clase:

    Tiene las características de un anime:
    nombre, episodio, estado y link.
    """

    def get_info(self, urlnewanime):  # Obtener información a partir del link
        """
        Extrae la información del anime
        """

        if urlnewanime == "":
            self.animecheck = "No ingresó nada"
            return

        # Comprobar si es un link de un capítulo, si lo es, lo tranforma al
        # link de la página del anime
        if "https://www3.animeflv.net/ver/" in urlnewanime:
            urlnewanime = urlnewanime.replace("/ver/", "/anime/")
            checklink = urlnewanime.rfind('-')
            urlnewanime = urlnewanime[:checklink]

        # Toma la información de la página
        try:

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                'AppleWebKit/537.36 (KHTML, like Gecko)'
                'Chrome/58.0.3029.110 Safari/537.3'
            }

            pedido = requests.get(urlnewanime, headers=headers, timeout=5)

        except requests.exceptions.InvalidURL:
            self.animecheck = "Link inválido"
            return

        html = pedido.text
        newsoup = BeautifulSoup(html, "html.parser")

        # Buscar nombre del anime
        nombre = newsoup.find('h1', class_='Title')

        # Buscar el número del último episodio
        episodio = re.findall("var episodes = \[\[[\w-]*", html)

        # Buscar el estado del anime
        estado = newsoup.find('span', class_='fa-tv')

        # Buscar el link del anime
        urlnewanime = urlnewanime.replace("/anime/", "/ver/")

        # Comprobar si el link es de un anime de AnimeFLV
        if nombre is None or len(episodio) == 0:
            self.animecheck = "Este link no pertenece a AnimeFLV"
            return

        # Le damos el valor a todas los atributos
        self.nombre = nombre.text
        self.episodio = episodio[0].replace("var episodes = [[", "")
        self.estado = estado.text
        self.link = urlnewanime + "-"

        _, _, animes_vistos = lista_animes_vistos()

        _, _, animes_suscritos = lista_animes_suscritos()

        for anime_suscrito in animes_suscritos:

            if anime_suscrito["nombre"] == self.nombre:
                self.animecheck = "Ya estabas suscrito a este anime"

        for anime_visto in animes_vistos:

            if anime_visto["nombre"] == self.nombre:
                self.animecheck = "Ya viste este anime"

    def __init__(self):  # Inicializa la clase con sus atributos
        """
        Descripción del método

        Se inicializa la clase y se declaran los atributos
        del anime.
        """

        self.animecheck = None
        self.nombre = None
        self.episodio = None
        self.link = None
        self.estado = None


class IconThread(threading.Thread):

    """
    Descripción de la clase:

    Se crea un hilo secundario mediante el cual
    se mostrará un ícono en los íconos
    ocultos.
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        image = Image.open(os.getcwd() + "\\Icons\\icon4.jpg")

        # Creamos el menú para el ícono
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar",
                             lambda: win32gui.ShowWindow(win32console.GetConsoleWindow(),
                                                         win32con.SW_SHOW)))
        global icon
        icon = pystray.Icon("Nombre del ícono", image, menu=menu)
        icon.run()


# Iniciamos el ícono en un hilo secundario
icon_thread = IconThread()
icon_thread.start()


# Declararciones
SUSCRIBED_ANIMES_DIR = os.getcwd() + "\\config\\SUSCRIBEDANIMES.txt"
SEEN_ANIMES_DIR = os.getcwd() + "\\config\\SEENANIMES.txt"

CHECK_BIENVENIDO = False  # Control del "Bienvenido a", se muestra por defecto
MOSTRAR_OPCIONES = True  # Control de aparación de las opciones en la primera búsqueda


# Antes de cerrar el script
# atexit.register(cerrar_script)


colorama.init(autoreset=True)


print("\n\n¡Bienvenido a " + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT +
      "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL + "!")


# Comprueba si ya se configuró el script
if os.path.exists(os.getcwd() + "\\config\\SUSCRIBEDANIMES.txt"):

    MOSTRAR_OPCIONES, opciones = comprobar_suscripciones()

else:

    CHECK_BIENVENIDO = configurar_notificaciones()

# Comprueba el directorio de la imagen y el sonido
for filename in os.listdir(os.getcwd() + "\\config\\"):

    name, extension = os.path.splitext(os.getcwd() + "\\config\\" + filename)

    if extension in [".jpg", ".jpeg", ".png", ".gif"]:
        image_dir = os.getcwd() + "\\config\\" + "Image" + extension

    elif extension in [".mp3", ".wav"]:
        sound_dir = os.getcwd() + "\\config\\" + "Sound" + extension


# Obtener información del anime suscrito

while True:

    # Mostrar las opciones

    if CHECK_BIENVENIDO is True:  # Comprobar si ya se mostró el "Bienvenido a"

        print("\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT +
              "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL)

    CHECK_BIENVENIDO = True  # Confirma que ya se mostró el "Bienvenido a"

    if MOSTRAR_OPCIONES is True:

        opciones = input("\nSeleccione una opción | " + Fore.YELLOW + "Ejemplo: " + Fore.LIGHTBLACK_EX + "2" + Fore.RESET + "\n\n" +
                         Style.BRIGHT + Fore.RED + "1. " + Fore.RESET + "Buscar nuevos episodios\n" +
                         Fore.YELLOW + "2. " + Fore.RESET + "Animes suscritos\n" +
                         Fore.GREEN + "3. " + Fore.RESET + "Animes finalizados\n" +
                         Fore.BLUE + "4. " + Fore.RESET + "Abrir AnimeFLV en navegador\n" +
                         Fore.MAGENTA + "5. " + Fore.RESET + "Salir\n\n")

    MOSTRAR_OPCIONES = True

    if opciones == "2":  # Animes suscritos

        while True:

            print("\n" + Fore.WHITE + Back.LIGHTBLACK_EX +
                  Style.BRIGHT + "Animes " + Fore.CYAN + "suscritos")

            opciones = input("\nSeleccione una opción | " + Fore.YELLOW +
                             "Ejemplo: " + Fore.LIGHTBLACK_EX + "2" + Fore.RESET + "\n\n" +
                             Style.BRIGHT + Fore.BLUE + "1. " + Fore.RESET + "Suscribirse\n" +
                             Fore.GREEN + "2. " + Fore.RESET + "Desuscribirse\n" +
                             Fore.YELLOW + "3. " + Fore.RESET + "Lista de animes suscritos\n" +
                             Fore.RED + "4. " + Fore.RESET + "Volver\n\n")

            if opciones == "1":  # Suscribirse

                INGRESAR_ANIME = "y"

                while INGRESAR_ANIME == "y":

                    print("\n\n" + Style.RESET_ALL + "Ingresar link del anime a " +
                          Back.GREEN + "suscribirse" + Back.RESET + ": | " +
                          Fore.YELLOW + "Ejemplos: " + Fore.LIGHTBLACK_EX +
                          "https://www3.animeflv.net/anime/one-piece-tv\n" +
                          " "*51 + "https://www3.animeflv.net/ver/one-piece-tv-1056\n" + Fore.RESET)

                    urlnewanime = input(
                        Fore.LIGHTBLACK_EX + "PARA CANCELAR: Presione ENTER sin ingresar nada\n\n" + Fore.RESET)

                    # Código nuevo
                    newanime = Anime()
                    newanime.get_info(urlnewanime)

                    if newanime.animecheck is not None:  # Verifica si hubo un error con el link

                        if newanime.animecheck == "No ingresó nada":

                            break

                        if newanime.animecheck == "Link inválido":

                            print("\n\n" + Fore.RED + "Link inválido")

                            INGRESAR_ANIME = ""

                            while INGRESAR_ANIME not in ('y', 'n'):
                                INGRESAR_ANIME = input(
                                    "\n\n¿Desea ingresar un link? (y/n) ")

                        elif newanime.animecheck == "Este link no pertenece a AnimeFLV":

                            print("\n\n" + Fore.RED +
                                  "Este link no pertenece a AnimeFLV.\n")

                            INGRESAR_ANIME = ""

                            while INGRESAR_ANIME not in ('y', 'n'):
                                INGRESAR_ANIME = input(
                                    "\n¿Desea ingresar otro link? (y/n) ")

                        elif newanime.animecheck == "Ya estabas suscrito a este anime":

                            print(
                                "\n\n" + Fore.RED + "¡Ya estabas suscrito a " +
                                newanime.nombre + "!")

                            _, mostrar_lista, _ = lista_animes_suscritos()

                            print(mostrar_lista)

                            input("\n\nPresione ENTER para continuar.\n")

                        elif newanime.animecheck == "Ya viste este anime":

                            print(
                                "\n\n" + Fore.RED + "¡Ya viste " +
                                newanime.nombre + "!")

                            _, mostrar_lista, _ = lista_animes_vistos()

                            print(mostrar_lista)

                            input("\n\nPresione ENTER para continuar.\n")

                    else:

                        # Comprobar si el anime finalizó
                        if newanime.estado == "Finalizado":

                            with open(SEEN_ANIMES_DIR, 'ab') as seen_animes:
                                seen_animes.write(newanime.nombre.encode(
                                    'utf-8') + b"\nEpisodio " + newanime.episodio.encode('utf-8') +
                                    b"\n" + urlnewanime.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " +
                                  newanime.nombre + "!\n" +
                                  Fore.YELLOW + "\nEl anime fue enviado a "
                                  "la lista de animes finalizados.")

                            _, mostrar_lista, _ = lista_animes_vistos()

                            print(mostrar_lista)

                        else:

                            # Escribir la información en un archivo
                            with open(SUSCRIBED_ANIMES_DIR, 'ab') as suscribed_animes:
                                suscribed_animes.write(newanime.nombre.encode(
                                    'utf-8') + b"\nEpisodio " + newanime.episodio.encode('utf-8') +
                                    b"\n" + newanime.link.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN +
                                  "¡Te suscribiste a " + newanime.nombre + "!")

                            _, mostrar_lista, _ = lista_animes_suscritos()

                            print(mostrar_lista)

                        INGRESAR_ANIME = ""

                        while INGRESAR_ANIME not in ('y', 'n'):
                            INGRESAR_ANIME = input(
                                "\n\n¿Desea suscribirse a otro anime? (y/n) ")

                print()  # Genera un espacio por estética

            elif opciones == "2":  # Desuscribirse

                INGRESAR_ANIME = "y"

                while INGRESAR_ANIME == "y":

                    print("\n\n" + Style.RESET_ALL + "Selecciona el anime a " +
                          Back.RED + Fore.WHITE + "desuscribirse" + Back.RESET + Fore.RESET + ": | "
                          + Fore.YELLOW + "Ejemplos: " + Fore.LIGHTBLACK_EX + "1")

                    animes_suscritos, mostrar_lista, _ = lista_animes_suscritos()

                    print(mostrar_lista)

                    if animes_suscritos < 1:  # Confirma si estás suscrito a algún anime
                        input("\n\nPresione ENTER para continuar.\n")
                        break

                    print("\n" + Fore.LIGHTBLACK_EX +
                          "PARA CANCELAR: Presione ENTER sin ingresar nada")

                    desuscripcion = input("\n")

                    if desuscripcion == "":
                        break

                    CONFIRMAR_DESUSCRIPCION = False

                    # Confirma si lo ingresado es un índice de su lista
                    for indice in range(animes_suscritos):

                        if desuscripcion == str(indice + 1):

                            CONFIRMAR_DESUSCRIPCION = True

                    if CONFIRMAR_DESUSCRIPCION is False:
                        continue

                    _, _, animes = lista_animes_suscritos()

                    new_suscribed_animes = []

                    # Realiza una lista nueva para actualizar la anterior
                    for anime in animes:
                        # Te muestra el anime al cual te desuscribiste
                        if anime["id"] == desuscripcion:
                            print("\n\n" + Style.BRIGHT + Fore.RED +
                                  "¡Te desuscribiste de " + anime["nombre"] + "!")

                        else:  # Va desempaquetando las bibliotecas en una lista para actualizar el bloc de notas

                            new_suscribed_animes += anime["nombre"], "\n", anime["episodio"], "\n", anime["link"], "\n"

                    # Actualiza la información del bloc de notas
                    with open(SUSCRIBED_ANIMES_DIR, "wb") as suscribed_animes:
                        suscribed_animes.writelines(line.encode('utf-8') for line in new_suscribed_animes)

                    animes_suscritos, mostrar_lista, _ = lista_animes_suscritos()

                    # Muestra la lista actualizada
                    print(mostrar_lista)

                    if animes_suscritos < 1:  # Confirma si estás suscrito a algún anime
                        input("\n\nPresione ENTER para continuar.\n")
                        break

                    INGRESAR_ANIME = ""

                    while INGRESAR_ANIME not in ('y', 'n'):

                        INGRESAR_ANIME = input(
                            "\n\n¿Desea desuscribirse a otro anime? (y/n) ")

                print()

            elif opciones == "3":  # Lista de animes suscritos

                _, mostrar_lista, _ = lista_animes_suscritos()

                print(mostrar_lista)

                input("\n\nPresione ENTER para continuar.\n")

            elif opciones == "4":
                print()
                break

    elif opciones == "1":  # Buscar nuevos episodios

        animes_suscritos, mostrar_lista, animes = lista_animes_suscritos()

        print(mostrar_lista)

        if animes_suscritos < 1:  # Confirma si estás suscrito a algún anime
            input("\n\nPresione ENTER para continuar.\n")
            continue

        print("\n\n" + Fore.LIGHTBLACK_EX +
              "Presione ENTER para continuar.")  # Cancela la búsqueda

        # Comparar información de los animes suscritos con la información de los nuevos capítulos

        CONFIRM = True

        while True:

            animes_suscritos, mostrar_lista, animes = lista_animes_suscritos()
            nombres, episodios = nuevos_capitulos()

            new_suscribed_animes = []
            ACTUALIZAR_BLOCK = False

            for anime in animes:

                for anime_nuevo_episodio in range(len(nombres) - 1, -1, -1):

                    if anime["nombre"] == nombres[anime_nuevo_episodio].text:

                        if anime["episodio"] < episodios[anime_nuevo_episodio].text:

                            anime["episodio"] = episodios[anime_nuevo_episodio].text

                            ACTUALIZAR_BLOCK = True

                            # Obtenemos el número del último episodio
                            num_ulti_cap = anime["episodio"].replace(
                                "Episodio ", "")

                            # Creamos el link del último capítulo
                            ulti_cap_link = anime["link"] + num_ulti_cap

                            MSG_ESTADO = borrar_anime_finalizado(anime["id"])

                            toast = Notification(app_id="AnimeFLV+",
                                                 title=anime["nombre"] + "!!",
                                                 msg=anime["episodio"] +
                                                 MSG_ESTADO,
                                                 icon=image_dir,
                                                 duration="short",
                                                 launch=ulti_cap_link
                                                 )

                            if sound_dir == "":
                                toast.set_audio(audio.Default, loop=False)
                                toast.show()
                            else:
                                toast.show()
                                playsound(sound_dir)

                new_suscribed_animes += anime["nombre"], "\n", anime["episodio"], "\n", anime["link"], "\n"

            if ACTUALIZAR_BLOCK is True:
                with open(SUSCRIBED_ANIMES_DIR, "wb") as suscribed_animes:
                    suscribed_animes.writelines(line.encode(
                        'utf-8') for line in new_suscribed_animes)

            keyboard.on_press(on_key_press)

            for i in range(60):
                if CONFIRM is False:
                    break  # Si se presiona ENTER, se interrumpe el bucle
                time.sleep(1)

            if CONFIRM is False:
                input()
                break

    elif opciones == "3":  # Animes finalizados

        INGRESAR_ANIME = "y"

        while INGRESAR_ANIME == "y":

            print("\n\n" + Fore.LIGHTBLACK_EX + "PARA QUITAR UN ANIME: "
                  "Seleccione uno y presione ENTER." +
                  "\n" + Fore.LIGHTBLACK_EX + "PARA CANCELAR: "
                  "Presione ENTER sin ingresar nada.")

            num_animes_vistos, mostrar_lista, animes_vistos = lista_animes_vistos()

            print(mostrar_lista)

            if num_animes_vistos < 1:  # Confirma si estás suscrito a algún anime
                input("\n\nPresione ENTER para continuar.\n")
                break

            print("\n" + Fore.LIGHTBLACK_EX +
                  "PARA CANCELAR: Presione ENTER sin ingresar nada")

            desuscripcion = input("\n")

            if desuscripcion == "":
                break

            CONFIRMAR_DESUSCRIPCION = False

            # Confirma si lo ingresado es un índice de su lista
            for indice in range(num_animes_vistos):

                if desuscripcion == str(indice + 1):

                    CONFIRMAR_DESUSCRIPCION = True

            if CONFIRMAR_DESUSCRIPCION is False:
                continue

            seen_animes_update = []

            # Realiza una lista nueva para actualizar la anterior
            for anime in animes_vistos:
                # Te muestra el anime al cual te desuscribiste
                if anime["id"] == desuscripcion:
                    print("\n\n" + Style.BRIGHT + Fore.RED +
                          "¡Quitaste a " + anime["nombre"] + " de la lista de animes vistos!")

                else:  # Va desempaquetando las bibliotecas en una lista para actualizar el bloc de notas

                    seen_animes_update += anime["nombre"], "\n", anime["episodio"], "\n", anime["link"], "\n"

            # Actualiza la información del bloc de notas
            with open(SEEN_ANIMES_DIR, "wb") as seen_animes:
                seen_animes.writelines(line.encode(
                    'utf-8') for line in seen_animes_update)

            num_animes_vistos, mostrar_lista, _ = lista_animes_vistos()

            # Muestra la lista actualizada
            print(mostrar_lista)

            if num_animes_vistos < 1:  # Confirma si estás suscrito a algún anime
                input("\n\nPresione ENTER para continuar.\n")
                break

            INGRESAR_ANIME = ""

            while INGRESAR_ANIME not in ('y', 'n'):

                INGRESAR_ANIME = input(
                    "\n\n¿Desea quitar otro anime finalizado? (y/n) ")

        print()

    elif opciones == "4":  # Abrir AnimeFLV en navegador
        webbrowser.open(url="https://www3.animeflv.net/",
                        new=0, autoraise=True)

    elif opciones == "5":  # Salir
        cerrar_script()
