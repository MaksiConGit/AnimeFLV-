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


# Obtener la infomación de los nuevos capítulos

URLNEWANIME = 'https://www3.animeflv.net/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/58.0.3029.110 Safari/537.3'
}

pedido = requests.get(URLNEWANIME, headers=HEADERS, timeout=5)

if pedido.status_code != 200:
    print(Fore.RED + "La página de AnimeFLV está caída, inténtelo más tarde")

html = pedido.text

soup = BeautifulSoup(html, "html.parser")

nombres = soup.find_all('strong', class_='Title')
capitulos = soup.find_all('span', class_='Capi')


SUSCRIBED_ANIMES_DIR = os.getcwd() + "\\config\\SUSCRIBEDANIMES.txt"
SEEN_ANIMES_DIR = os.getcwd() + "\\config\\SEENANIMES.txt"


# Obtiene los atributos del anime
class Anime():

    """
    Descripción de la clase

    Tiene las características de un anime
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
            pedido = requests.get(urlnewanime, headers=HEADERS, timeout=5)

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

        else:

            # Le damos el valor a todas los atributos
            self.nombre = nombre.text
            self.episodio = episodio[0].replace("var episodes = [[", "")
            self.estado = estado.text
            self.link = urlnewanime + "-"

            with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
                animessuscritostxt = animessuscritos.readlines()
                suscripciones = len(animessuscritostxt) // 3

            for indice in range(suscripciones):  # Comprueba si ya estás suscrito
                # Índice * 3 es igual al nombre
                if nombre.text == animessuscritostxt[indice * 3].strip():
                    self.animecheck = "Ya estabas suscrito a este anime"

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


def lista_animes_suscritos():
    """
    Descripción de la función:

    Abre el bloc de notas, toma la información
    de los animes SUSCRITOS y los enumera en una lista
    """

    with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
        animessuscritostxt = animessuscritos.readlines()
        suscripciones = len(animessuscritostxt) // 3

    print("\n\n" + Back.LIGHTWHITE_EX + Fore.LIGHTGREEN_EX +
          "Lista de animes suscritos:" + Fore.RESET + Back.RESET + "\n")

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN,
                   Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for indice in range(suscripciones):
        color = next(colors)
        print(Style.BRIGHT + color + str(indice + 1) + ". " +  # Enumera
              Fore.WHITE + animessuscritostxt[indice * 3].strip() +  # Nombre
              Style.NORMAL + Fore.YELLOW + " | " + Style.BRIGHT + Fore.BLUE +  # Separador
              animessuscritostxt[(indice * 3) + 1].strip())  # Episodio

    if suscripciones < 1:  # Confirma si estás suscrito a algún anime
        print(Fore.LIGHTBLACK_EX +
              "No estás suscrito a ningún anime.\n"
              "¡Suscríbete a uno para empezar a recibir notificaciones!")


def lista_animes_vistos():
    """
    Descripción de la función:

    Abre el bloc de notas, toma la información
    de los animes VISTOS y los enumera en una lista
    """

    with open(SEEN_ANIMES_DIR, "r", encoding="utf-8") as seenanimes:
        animesvistostxt = seenanimes.readlines()
        numanimesvistos = len(animesvistostxt) // 3

    print("\n\n" + Style.RESET_ALL + Back.LIGHTWHITE_EX + Fore.LIGHTRED_EX +
          "Lista de animes vistos:" + Fore.RESET + Back.RESET + Style.RESET_ALL + "\n")

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN,
                   Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for indice in range(numanimesvistos):
        color = next(colors)
        print(Style.BRIGHT + color + str(indice + 1) + ". "  # Enumera
              + Fore.WHITE + animesvistostxt[indice * 3].strip()  # Nombre
              + Style.NORMAL + Fore.YELLOW + " | " + Fore.LIGHTBLUE_EX +  # Separador
              animesvistostxt[(i * 3) + 1].strip())  # Episodio

    if numanimesvistos < 1:  # Confirma si viste algún anime
        print(Fore.LIGHTBLACK_EX + "No viste ningún anime.\n"
              "¡Cuando finalice un anime suscrito, vendrá aquí!"
              "\nTIP: Puedes suscribirte a animes finalizados")


def borrar_anime_finalizado():
    """
    Descripción de la función:

    Abre el bloc de notas y actualiza
    la lista de animes suscritos cuando
    finaliza un anime, al final muestra
    la misma lista actualizada
    """

    with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
        animessuscritostxt = animessuscritos.readlines()

    # Borra la información del anime
    animessuscritostxt[(int(desus) - 1) * 3] = ""
    animessuscritostxt[(int(desus) - 1) * 3 + 1] = ""
    animessuscritostxt[(int(desus) - 1) * 3 + 2] = ""

    # Actualiza el bloc de notas
    with open(SUSCRIBED_ANIMES_DIR, "wb") as animessuscritos:
        animessuscritos.writelines(line.encode('utf-8')
                                   for line in animessuscritostxt)

    # Muestra la lista de animes
    lista_animes_suscritos()


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


def on_key_press(event):  # Cancelar la búsqueda de capítulos
    """
    Descripción de la función:

    Cancela la búsqueda de capítulos mediante
    la captura de la tecla "enter".
    """

    if event.name == 'enter':
        keyboard.unhook_all()  # Desactiva la captura de teclas
        print("\n" + Fore.LIGHTBLACK_EX + "Espere...")
        global confirm
        confirm = False


colorama.init(autoreset=True)


print("\n\n¡Bienvenido a " + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT +
      "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL + "!")

# Declarar directorios globales
global imagedir
global sounddir

checkbienvenido = False  # Control del "Bienvenido a", se muestra por defecto
mostraropciones = True  # Control de aparación de las opciones en la primera búsqueda


# Comprueba si el usurio ya configuró el script y lo ordena para evitar errores
try:

    with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
        animessuscritostxt = animessuscritos.readlines()
        suscripciones = len(animessuscritostxt) // 3

    for filename in os.listdir(os.getcwd() + "\\config\\"):

        name, extension = os.path.splitext(
            os.getcwd() + "\\config\\" + filename)

        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            imagedir = os.getcwd() + "\\config\\" + "Image" + extension
            os.rename(os.getcwd() + "\\config\\" + filename, imagedir)

        if extension in [".mp3", ".wav"]:
            sounddir = os.getcwd() + "\\config\\" + "Sound" + extension
            os.rename(os.getcwd() + "\\config\\" + filename, sounddir)

    if suscripciones >= 1:  # Si estamos suscritos a al menos un anime, busca directamente

        lista_animes_suscritos()
        barra_de_carga()

        mostraropciones = False  # No se muestran las opciones
        opciones = "1"  # Selecciona la opción "Buscar nuevos episodios"

# El usuario configura las notificaciones
except OSError:

    print("\n\n¡¡Muchas gracias por apoyar mis proyectos!!")

    input("\n\nPrimero que nada, vamos a personalizar el programa"
          "para que tengas una experiencia única."
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
    try:
        os.makedirs("config")
    except OSError:
        None

    # Mueve los archivos nuevos a la nueva carpeta "config"
    for filename in os.listdir(os.getcwd()):

        name, extension = os.path.splitext(os.getcwd() + filename)

        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            imagedir = os.getcwd() + "\\config\\" + "Image" + extension
            os.rename(os.getcwd() + "\\" + filename, imagedir)

        elif extension in [".mp3", ".wav"]:
            sounddir = os.getcwd() + "\\config\\" + "Sound" + extension
            os.rename(os.getcwd() + "\\" + filename, sounddir)

    # Crea el .txt de los animes suscritos
    with open(SUSCRIBED_ANIMES_DIR, "wb") as animessuscritos:
        None

    checkbienvenido = True  # Confirma que ya se mostró el "Bienvenido a"


class IconThread(threading.Thread):  # Creación del ícono oculto

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


def cerrar():  # Terminamos el hilo secundario antes de cerrar el principal
    """
    Descripción de la función:

    Terminamos el hilo secundario antes de
    cerrar el hilo principal.
    """

    icon.stop()
    icon.update_menu()
    icon_thread.join()
    sys.exit()


# Antes de cerrar el programa, se ejecuta esta línea
atexit.register(cerrar)


# Obtener información del anime suscrito

while True:

    if checkbienvenido is True:  # Comprobar si ya se mostró el "Bienvenido a"

        print("\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT +
              "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL)

    checkbienvenido = True  # Confirma que ya se mostró el "Bienvenido a"

    if mostraropciones is True:

        opciones = input("\nSeleccione una opción | " + Fore.YELLOW + "Ejemplo: " + Fore.LIGHTBLACK_EX + "2" + Fore.RESET + "\n\n" +
                         Style.BRIGHT + Fore.RED + "1. " + Fore.RESET + "Buscar nuevos episodios\n" +
                         Fore.YELLOW + "2. " + Fore.RESET + "Animes suscritos\n" +
                         Fore.GREEN + "3. " + Fore.RESET + "Animes finalizados\n" +
                         Fore.BLUE + "4. " + Fore.RESET + "Abrir AnimeFLV en navegador\n" +
                         Fore.MAGENTA + "5. " + Fore.RESET + "Salir\n\n")

    mostraropciones = True

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

                ingresaranime = "y"

                while ingresaranime == "y":

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

                            ingresaranime = ""

                            while ingresaranime not in ('y', 'n'):
                                ingresaranime = input(
                                    "\n\n¿Desea ingresar un link? (y/n) ")

                        elif newanime.animecheck == "Este link no pertenece a AnimeFLV":

                            print("\n\n" + Fore.RED +
                                  "Este link no pertenece a AnimeFLV.\n")

                            ingresaranime = ""

                            while ingresaranime not in ('y', 'n'):
                                ingresaranime = input(
                                    "\n¿Desea ingresar otro link? (y/n) ")

                        elif newanime.animecheck == "Ya estabas suscrito a este anime":

                            print(
                                "\n\n" + Fore.RED + "¡Ya estabas suscrito a " +
                                newanime.nombre + "!")

                            lista_animes_suscritos()

                    else:

                        # Comprobar si el anime finalizó
                        if newanime.estado == "Finalizado":

                            with open(SEEN_ANIMES_DIR, 'ab') as seenanimes:
                                seenanimes.write(newanime.nombre.encode(
                                    'utf-8') + b"\nEpisodio " + newanime.episodio.encode('utf-8') +
                                    b"\n" + urlnewanime.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " +
                                  newanime.nombre + "!\n" +
                                  Fore.YELLOW + "\nEl anime fue enviado a "
                                  "la lista de animes finalizados.")

                            lista_animes_vistos()

                        else:

                            # Escribir la información en un archivo
                            with open(SUSCRIBED_ANIMES_DIR, 'ab') as animessuscritos:
                                animessuscritos.write(newanime.nombre.encode(
                                    'utf-8') + b"\nEpisodio " + newanime.episodio.encode('utf-8') +
                                    b"\n" + newanime.link.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN +
                                  "¡Te suscribiste a " + newanime.nombre + "!")

                            lista_animes_suscritos()

                        ingresaranime = ""

                        while ingresaranime not in ('y', 'n'):
                            ingresaranime = input(
                                "\n\n¿Desea suscribirse a otro anime? (y/n) ")

                print()  # Genera un espacio por estética

            elif opciones == "2":  # Desuscribirse

                ingresaranime = "y"

                while ingresaranime == "y":

                    with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
                        animessuscritostxt = animessuscritos.readlines()
                        suscripciones = len(animessuscritostxt) // 3

                    print("\n\n" + Style.RESET_ALL + "Selecciona el anime a " +
                          Back.RED + Fore.WHITE + "desuscribirse" + Back.RESET + Fore.RESET + ": | "
                          + Fore.YELLOW + "Ejemplos: " + Fore.LIGHTBLACK_EX + "1")

                    if suscripciones < 1:  # Confirma si estás suscrito a algún anime
                        lista_animes_suscritos()
                        input("\n\nPresione ENTER para continuar.\n")
                        break

                    lista_animes_suscritos()

                    print("\n" + Fore.LIGHTBLACK_EX +
                          "PARA CANCELAR: Presione ENTER sin ingresar nada")

                    desus = input("\n")

                    if desus == "":
                        break

                    confirmdesus = False

                    # Confirma si lo ingresado es un índice de su lista
                    for i in range(suscripciones):

                        if desus == str(i + 1):

                            confirmdesus = True

                    if confirmdesus == False:
                        continue

                    print("\n\n" + Style.BRIGHT + Fore.RED + "¡Te desuscribiste de " +
                          animessuscritostxt[(int(desus) - 1) * 3].strip() + "!")

                    # Borra la información del anime
                    animessuscritostxt[(int(desus) - 1) * 3] = ""
                    animessuscritostxt[(int(desus) - 1) * 3 + 1] = ""
                    animessuscritostxt[(int(desus) - 1) * 3 + 2] = ""

                    with open(SUSCRIBED_ANIMES_DIR, "wb") as animessuscritos:
                        animessuscritos.writelines(line.encode(
                            'utf-8') for line in animessuscritostxt)

                    # Muestra la lista de animes
                    lista_animes_suscritos()

                    if suscripciones < 1:  # Confirma si estás suscrito a algún anime
                        input("\n\nPresione ENTER para continuar.\n")
                        break

                    ingresaranime = ""

                    while ingresaranime not in ('y', 'n'):

                        ingresaranime = input(
                            "\n\n¿Desea desuscribirse a otro anime? (y/n) ")

                print()

            elif opciones == "3":  # Lista de animes suscritos

                lista_animes_suscritos()

                input("\n\nPresione ENTER para continuar.\n")

            elif opciones == "4":
                print()
                break

    elif opciones == "1":  # Buscar nuevos episodios

        lista_animes_suscritos()

        if suscripciones < 1:  # Confirma si estás suscrito a algún anime
            input("\n\nPresione ENTER para continuar.\n")
            continue

        print("\n\n" + Fore.LIGHTBLACK_EX +
              "Presione ENTER para continuar.")  # Cancela la búsqueda

        # Comparar información de los animes suscritos con la información de los nuevos capítulos

        confirm = True

        while True:

            with open(SUSCRIBED_ANIMES_DIR, "r", encoding="utf-8") as animessuscritos:
                animessuscritostxt = animessuscritos.readlines()
                suscripciones = len(animessuscritostxt) // 3

            for y in range(suscripciones):  # Cantidad de animes suscritos

                # Cantidad de animes con nuevos capítulos a la inversa
                for x in range(len(nombres) - 1, -1, -1):

                    if animessuscritostxt[y * 3].strip() == nombres[x].text:

                        if animessuscritostxt[y * 3 + 1].strip() < capitulos[x].text:

                            # Se marca el capítulo como visto
                            animessuscritostxt[y * 3 +
                                               1] = capitulos[x].text + "\n"

                            with open(SUSCRIBED_ANIMES_DIR, "wb",) as animessuscritos:
                                # Se reemplaza el último capítulo visto
                                animessuscritos.writelines(line.encode(
                                    'utf-8') for line in animessuscritostxt)

                            # Obtenemos el número del último episodio
                            numulticap = capitulos[x].text.replace(
                                "Episodio ", "")

                            # Comprobar si el anime finalizó
                            urlnewanime = animessuscritostxt[y * 3 + 2]
                            urlnewanime = urlnewanime.replace(
                                "/ver/", "/anime/")
                            checklink = urlnewanime.rfind('-')
                            urlnewanime = urlnewanime[:checklink]

                            # Toma la información de la página
                            newpedido = requests.get(
                                urlnewanime, headers=HEADERS, timeout=5)
                            newhtml = newpedido.text
                            newsoup = BeautifulSoup(newhtml, "html.parser")
                            finalizado = newsoup.find('span', class_='fa-tv')

                            msgfinalizado = ""

                            # Actualiza las listas
                            if finalizado.text == "Finalizado":

                                msgfinalizado = " | Finalizado"  # Se agrega en la notificación la finalización

                                # Se actualiza la lista de animes vistos
                                with open(SEEN_ANIMES_DIR, 'ab') as seenanimes:
                                    seenanimes.write(nombres[x].text.encode(
                                        'utf-8') + b"\n" + capitulos[x].text.encode('utf-8') + b"\n" + urlnewanime.encode('utf-8') + b"\n")

                                # Borra la información de la lista de animes suscritos
                                animessuscritostxt[y * 3] = ""
                                animessuscritostxt[y * 3 + 1] = ""
                                animessuscritostxt[y * 3 + 2] = ""

                                # Se actualiza la lista de animes suscritos
                                with open(SUSCRIBED_ANIMES_DIR, "wb") as animessuscritos:
                                    animessuscritos.writelines(line.encode(
                                        'utf-8') for line in animessuscritostxt)

                                print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " +
                                      nombres[x].text + "!\n" + Fore.YELLOW + "\nEl anime fue enviado a la lista de animes finalizados")

                                lista_animes_vistos()

                            print("\n\n" + Fore.LIGHTBLACK_EX +
                                  "Presione ENTER para continuar.")

                            toast = Notification(app_id="AnimeFLV+",
                                                 title=nombres[x].text + "!!",
                                                 msg=capitulos[x].text +
                                                 msgfinalizado,
                                                 icon=imagedir,
                                                 duration="short",
                                                 # Agregamos el último episodio al link
                                                 launch=animessuscritostxt[y * \
                                                                           3 + 2] + numulticap
                                                 )

                            if sounddir == "":
                                toast.set_audio(audio.Default, loop=False)
                                toast.show()
                            else:
                                toast.show()
                                playsound(sounddir)

            keyboard.on_press(on_key_press)

            for i in range(60):
                if confirm == False:
                    break  # si se presiona una tecla, interrumpe el bucle
                time.sleep(1)

            if confirm == False:
                input()
                break

    elif opciones == "3":  # Animes finalizados

        lista_animes_vistos()  # Muestra la lista

        ingresaranime = "y"

        while ingresaranime == "y":  # Bucle para quitar los animes que quieras

            print("\n\n" + Fore.LIGHTBLACK_EX + "PARA QUITAR UN ANIME: Seleccione uno y presione ENTER." +
                  "\n" + Fore.LIGHTBLACK_EX + "PARA CANCELAR: Presione ENTER sin ingresar nada.")

            # Obtiene la información de la lista
            with open(SEEN_ANIMES_DIR, "r", encoding="utf-8") as seenanimes:
                animesvistostxt = seenanimes.readlines()
                numanimesvistos = len(animesvistostxt) // 3

            quitaranime = input("\n")

            if quitaranime == "":
                break

            confirmquitar = False

            # Confirma si lo ingresado es un índice de su lista
            for i in range(numanimesvistos):

                if quitaranime == str(i + 1):

                    confirmdesus = True

            if confirmdesus == False:  # Si no es un índice de la lista, se vuele a mostrar las opciones
                continue

            print("\n\n" + Style.BRIGHT + Fore.RED + "¡Quitaste a " + animesvistostxt[(
                int(quitaranime) - 1) * 3].strip() + " de la lista de animes vistos!")

            # Borra la información del anime de la lista
            animesvistostxt[(int(quitaranime) - 1) * 3] = ""
            animesvistostxt[(int(quitaranime) - 1) * 3 + 1] = ""
            animesvistostxt[(int(quitaranime) - 1) * 3 + 2] = ""

            # Guarda los cambios
            with open(SEEN_ANIMES_DIR, "wb") as seenanimes:
                seenanimes.writelines(line.encode('utf-8')
                                      for line in animesvistostxt)

            # Muestra la lista de animes
            lista_animes_vistos()

            if suscripciones < 1:  # Confirma si estás suscrito a algún anime
                input("\n\n")
                break

            ingresaranime = ""

            while ingresaranime != "y" and ingresaranime != "n":

                ingresaranime = input(
                    "\n\n¿Desea desuscribirse a otro anime? (y/n) ")

        print()

    elif opciones == "4":  # Abrir AnimeFLV en navegador
        webbrowser.open(url=urlaniflv, new=0, autoraise=True)

    elif opciones == "5":  # Salir
        cerrar()
