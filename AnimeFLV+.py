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


# Oculta la ventana de la consola

hidebool = False

#Obtener la infomación de los nuevos capítulos

urlaniflv = 'https://www3.animeflv.net/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

pedido = requests.get(urlaniflv, headers=headers)

if pedido.status_code != 200:
    print(Fore.RED + "La página de AnimeFLV está caída, inténtelo más tarde")

html = pedido.text

soup = BeautifulSoup(html, "html.parser")

nombres = soup.find_all('strong', class_='Title')
capitulos = soup.find_all('span', class_='Capi')


#Creación de una lista con los nombres y el número del capítulo

#lista_concatenada = []

#for i in range(len(nombres)):
 #   nombre = nombres[i].text
  #  capitulo = capitulos[i].text
   # texto_concatenado = nombre + ' ' + capitulo
    #lista_concatenada.append(texto_concatenado)


def listaanimes(): #Mostrar la lista de animes suscritos

    with open(txtdir, "r", encoding="utf-8") as animesemision:
        animesemisiontxt = animesemision.readlines()
        suscripciones = len(animesemisiontxt) // 3

    print("\n\n" + Back.LIGHTWHITE_EX + Fore.LIGHTGREEN_EX + "Lista de animes suscritos:" + Fore.RESET + Back.RESET + "\n")

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for i in range(suscripciones):
        color = next(colors)
        print(Style.BRIGHT + color + str(i + 1) + ". " + Fore.WHITE + animesemisiontxt[i * 3].strip() + Style.NORMAL + Fore.YELLOW + " | " + Style.BRIGHT + Fore.BLUE + animesemisiontxt[(i * 3) + 1].strip())

    if suscripciones < 1: #Confirma si estás suscrito a algún anime
        print(Fore.LIGHTBLACK_EX + "No estás suscrito a ningún anime.\n¡Suscríbete a uno para empezar a recibir notificaciones!")


def listavistos():

    with open(os.getcwd() + "\\config\\AnimesVistos.txt", "r", encoding="utf-8") as animesvistos:
        animesvistostxt = animesvistos.readlines()
        numanimesvistos = len(animesvistostxt) // 3

    print("\n\n" + Style.RESET_ALL + Back.LIGHTWHITE_EX + Fore.LIGHTRED_EX + "Lista de animes vistos:" + Fore.RESET + Back.RESET + Style.RESET_ALL + "\n")

    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

    for i in range(numanimesvistos):
        color = next(colors)
        print(Style.BRIGHT + color + str(i + 1) + ". " + Fore.WHITE + animesvistostxt[i * 3].strip() + Style.NORMAL + Fore.YELLOW + " | " + Fore.LIGHTBLUE_EX + animesvistostxt[(i * 3) + 1].strip())

    if numanimesvistos < 1: #Confirma si viste algún anime
        print(Fore.LIGHTBLACK_EX + "No viste ningún anime.\n¡Cuando finalice un anime suscrito, vendrá aquí!\nTIP: Puedes suscribirte a animes finalizados")


def finalizar():

    with open(txtdir, "r", encoding="utf-8") as animesemision:
        animesemisiontxt = animesemision.readlines()
        suscripciones = len(animesemisiontxt) // 3

    #Borra la información del anime
    animesemisiontxt[(int(desus) - 1) * 3] = ""
    animesemisiontxt[(int(desus) - 1) * 3 + 1] = ""
    animesemisiontxt[(int(desus) - 1) * 3 + 2] = ""

    with open(txtdir, "wb") as animesemision:
        animesemision.writelines(line.encode('utf-8') for line in animesemisiontxt) 
    
    #Muestra la lista de animes
    listaanimes()



def buscaranimes():
        
        print(Fore.YELLOW + "\n\n¡Te notificaremos cuando se estrene un nuevo episodio!")

        print("\n\nLa consola se esconderá en unos segundos...\n\nConsulta el ícono oculto para mostrar la consola.\n\n")

        def progress_bar(progress, total):

            percent = 100 * (progress/float(total))

            bar = Fore.RED + "█" * int(percent) + "-" * (100 - int(percent))

            if percent > 25:
                bar = Fore.YELLOW + "█" * int(percent) + "-" * (100 - int(percent))

                if percent > 50.0:
                    bar = Fore.GREEN + "█" * int(percent) + "-" * (100 - int(percent))

                if percent > 75.0:
                    bar = Fore.BLUE + "█" * int(percent) + "-" * (100 - int(percent))

                if percent >= 99.0:
                    bar = Fore.MAGENTA + "█" * int(percent) + "-" * (100 - int(percent))

            print(f"\r|{bar}| {percent:.2f}%", end="\r")

        progress_bar(0, 100)
        for i in range(100):
            time.sleep(0.07)
            progress_bar(i + 1, 100)

        win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
        
        os.system("cls")

        print("\n\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT + "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL)




def on_key_press(event):
    
    if event.name == 'enter':
        keyboard.unhook_all()  # Desactiva la captura de teclas
        print("\n" + Fore.LIGHTBLACK_EX + "Espere...")
        global confirm
        confirm = False


colorama.init(autoreset=True)


print("\n\n¡Bienvenido a " + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT + "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL + "!")

checklogo = False

global txtdir
txtdir = os.getcwd() + "\\config\\DONTMODIFY.txt"
global imagedir
global sounddir

boolbuscar = False


#Crear el entorno para una correcta ejecución

try:
    with open(txtdir, "r", encoding="utf-8") as animesemision:
        animesemisiontxt = animesemision.readlines()
        suscripciones = len(animesemisiontxt) // 3

    imagedir = ""
    sounddir = ""

    for filename in os.listdir(os.getcwd() + "\\config\\"):

        name, extension = os.path.splitext(os.getcwd() + "\\config\\" + filename)
        
        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            imagedir = os.getcwd() + "\\config\\" + "Image" + extension
            os.rename(os.getcwd() + "\\config\\" + filename, imagedir)

        if extension in [".mp3", ".wav"]:
            sounddir = os.getcwd() + "\\config\\" + "Sound" + extension
            os.rename(os.getcwd() + "\\config\\" + filename, sounddir)

    if suscripciones >= 1:

        listaanimes()
        buscaranimes()

        boolbuscar = True
        hidebool = False
        opciones = "1"
    
        
except:

    print("\n\n¡¡Muchas gracias por apoyar mis proyectos!!")

    input("\n\nPrimero que nada, vamos a personalizar el programa para que tengas una experiencia única.\n\nPresione ENTER para continuar.")

    print("\n\n\nPaso 1: Elije una imagen para las notificaciones.")
    print("\n\nEsta imagen se mostrará junto con el nombre del anime y el número del nuevo capítulo.")
    input("\n\n1. Copia una imagen (jpg, jpeg, png, gif) de tus archivos locales." + "\n\n2. Pega esa imagen en la carpeta del programa.\n\n3. Presione ENTER cuando esté listo.")

    print("\n\n\nPaso 2: Elije un sonido para las notificaciones.")
    print("\n\nEste sonido debe ser corto, puede ser una parte de una canción o un simple sonido de notificación.")
    print("\n\n1. Copia un sonido (.mp3, .wav) de tus archivos locales." + "\n\n2. Pega ese sonido en la carpeta del programa.\n\n3. Presione ENTER cuando esté listo.")
    print("\n\nIMPORTANTE:\n\nSi desea el sonido de notificación predeterminado de Windows, no haga ningún cambio, únicamente presione ENTER.\n")
    input()

    try:
        os.makedirs("config")
    except:
        None

    imagedir = ""
    sounddir = ""

    for filename in os.listdir(os.getcwd()):

        name, extension = os.path.splitext(os.getcwd() + filename)

        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            imagedir = os.getcwd() + "\\config\\" + "Image" + extension
            os.rename(os.getcwd() + "\\" + filename, imagedir)


        elif extension in [".mp3", ".wav"]:
            sounddir = os.getcwd() + "\\config\\" + "Sound" + extension
            os.rename(os.getcwd() + "\\" + filename, sounddir)
            
    with open(txtdir, "wb") as animesemision:
        None

    checklogo = True


class IconThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        # Creamos la imagen para el ícono

        image = Image.open(os.getcwd() + "\\Icons\\icon4.jpg")

        # Creamos el menú para el ícono
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar", lambda: win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_SHOW)))
        global icon
        icon = pystray.Icon("Nombre del ícono", image, menu=menu)
        icon.run()

# Creamos el objeto de subproceso para el ícono
icon_thread = IconThread()

# Iniciamos el subproceso del ícono
icon_thread.start()


def cerrar():
    icon.stop()
    icon.update_menu()
    icon_thread.join()
    icon.update_menu()
    exit()

atexit.register(cerrar)

#Obtener información del anime suscrito

while True:

    if checklogo == True: #Mostrar el logo después de que se nos haya dado la bienvenida por primera vez

        print("\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT + "Anime" + Fore.CYAN + "FLV+" + Fore.WHITE + Back.BLACK + Style.NORMAL)

    checklogo = True

    if boolbuscar == False:

        opciones = input("\nSeleccione una opción | " + Fore.YELLOW + "Ejemplo: "+ Fore.LIGHTBLACK_EX + "2" + Fore.RESET + "\n\n" + 
                        Style.BRIGHT + Fore.RED + "1. " + Fore.RESET + "Buscar nuevos episodios\n" + 
                        Fore.YELLOW + "2. " + Fore.RESET + "Animes suscritos\n" + 
                        Fore.GREEN + "3. " + Fore.RESET + "Animes finalizados\n" + 
                        Fore.BLUE + "4. " + Fore.RESET + "Abrir AnimeFLV en navegador\n" +
                        Fore.MAGENTA + "5. " + Fore.RESET + "Salir\n\n")
        
    boolbuscar = False

    if opciones == "2":
            
        while True:

            print("\n" + Fore.WHITE + Back.LIGHTBLACK_EX + Style.BRIGHT + "Animes " + Fore.CYAN + "suscritos")

            opciones = input("\nSeleccione una opción | " + Fore.YELLOW + "Ejemplo: "+ Fore.LIGHTBLACK_EX + "2" + Fore.RESET + "\n\n" + 
                    Style.BRIGHT + Fore.BLUE + "1. " + Fore.RESET + "Suscribirse\n" + 
                    Fore.GREEN + "2. " + Fore.RESET + "Desuscribirse\n" + 
                    Fore.YELLOW + "3. " + Fore.RESET + "Lista de animes suscritos\n" + 
                    Fore.RED + "4. " + Fore.RESET + "Volver\n\n")

            if opciones == "1": #Suscribirse

                inganim = "y"

                while inganim == "y":

                    susbool = False

                    print("\n\n" + Style.RESET_ALL + "Ingresar link del anime a " + Back.GREEN + "suscribirse" + Back.RESET + ": | " 
                        + Fore.YELLOW + "Ejemplos: " + Fore.LIGHTBLACK_EX + "https://www3.animeflv.net/anime/one-piece-tv\n" 
                        + " "*51 + "https://www3.animeflv.net/ver/one-piece-tv-1056\n" + Fore.RESET)
                    
                    urlnewanime = input(Fore.LIGHTBLACK_EX + "PARA CANCELAR: Presione ENTER sin ingresar nada\n\n" + Fore.RESET)

                    if urlnewanime == "":
                        break
                    

                    #Comprobar si es un link de un capítulo
                    try:
                        checklink = re.findall("https://www3.animeflv.net/ver/", urlnewanime)
                        if checklink[0] == "https://www3.animeflv.net/ver/": #Tranformar el link del capítulo a link del anime
                            urlnewanime = urlnewanime.replace("/ver/", "/anime/")
                            checklink = urlnewanime.rfind('-')
                            urlnewanime = urlnewanime[:checklink]
                    except:
                        None
                        
                    #Toma la información de la página
                    try:
                        newpedido = requests.get(urlnewanime, headers=headers)

                    except:

                        inganim = ""

                        print("\n\n" + Fore.RED + "Link inválido\n")

                        while inganim != "y" and inganim != "n":
                            inganim = input("\n¿Desea ingresar un link? (y/n) ")

                        continue

                    newhtml = newpedido.text
                    newsoup = BeautifulSoup(newhtml, "html.parser")

                    #Buscar nombre del anime
                    seminewnombre = newsoup.find('h1', class_='Title')

                    #Buscar el número del último episodio
                    seminewcapitulo = re.findall("var episodes = \[\[[\w-]*", newhtml)

                    #Buscar el estado del anime
                    finalizado = newsoup.find('span', class_='fa-tv')


                    if seminewnombre == None or len(seminewcapitulo) == 0: #Comprobar si el link es de un anime de AnimeFLV

                        print("\n\n" + Fore.RED + "Este link no pertenece a AnimeFLV.\n")

                        inganim = ""

                        while inganim != "y" and inganim != "n":
                            inganim = input("\n¿Desea ingresar otro link? (y/n) ")
                
                    else:

                        newcapitulo = seminewcapitulo[0]
                        newcapitulo = newcapitulo.replace("var episodes = [[", "")

                        newnombre = seminewnombre.text

                        with open(txtdir, "r", encoding="utf-8") as animesemision:
                            animesemisiontxt = animesemision.readlines()
                            suscripciones = len(animesemisiontxt) // 3

                        for i in range(suscripciones): #Comprueba si ya estás suscrito

                            if newnombre == animesemisiontxt[i * 3].strip():
                                
                                susbool = True
                                print("\n\n" + Fore.RED + "¡Ya estabas suscrito a " + newnombre + "!")
                            
                        if susbool == False:

                            newlink = urlnewanime.replace("/anime/", "/ver/")
                            newlink = newlink + "-"

                        #Comprobar si el anime finalizó
                        if finalizado.text == "Finalizado":

                            with open(os.getcwd() + "\\config\\AnimesVistos.txt", 'ab') as animesvistos:
                                animesvistos.write(newnombre.encode('utf-8') + b"\nEpisodio " + newcapitulo.encode('utf-8') + b"\n" + urlnewanime.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " + newnombre + "!\n" + Fore.YELLOW + "\nEl anime fue enviado a la lista de animes finalizados.")
                        
                            listavistos()

                        else:

                            #Escribir la información en un archivo
                            with open(txtdir, 'ab') as animesemision:
                                animesemision.write(newnombre.encode('utf-8') + b"\nEpisodio " + newcapitulo.encode('utf-8') + b"\n" + newlink.encode('utf-8') + b"\n")

                            print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Te suscribiste a " + newnombre + "!")

                            hidebool = True #Aparece la pantalla de carga al buscar animes
                        
                            listaanimes()

                        inganim = ""
                        
                        while inganim != "y" and inganim != "n":
                            inganim = input("\n\n¿Desea suscribirse a otro anime? (y/n) ")
                
                print()


            elif opciones == "2": #Desuscribirse
                
                inganim = "y"

                while inganim == "y":

                    with open(txtdir, "r", encoding="utf-8") as animesemision:
                        animesemisiontxt = animesemision.readlines()
                        suscripciones = len(animesemisiontxt) // 3

                    print("\n\n" + Style.RESET_ALL + "Selecciona el anime a " + Back.RED + Fore.WHITE + "desuscribirse" + Back.RESET + Fore.RESET + ": | " 
                        + Fore.YELLOW + "Ejemplos: " + Fore.LIGHTBLACK_EX + "1")
                    
                    if suscripciones < 1: #Confirma si estás suscrito a algún anime
                        listaanimes()
                        input("\n\nPresione ENTER para continuar.\n")
                        break
                    
                    listaanimes()

                    print("\n" + Fore.LIGHTBLACK_EX + "PARA CANCELAR: Presione ENTER sin ingresar nada")
                    
                    desus = input("\n")

                    if desus == "":
                        break

                    confirmdesus = False
                    
                    for i in range(suscripciones): #Confirma si lo ingresado es un índice de su lista

                        if desus == str(i + 1):

                            confirmdesus = True

                    if confirmdesus == False:
                        continue

                    print("\n\n" + Style.BRIGHT + Fore.RED + "¡Te desuscribiste de " + animesemisiontxt[(int(desus) - 1) * 3].strip() + "!")


                    #Borra la información del anime
                    animesemisiontxt[(int(desus) - 1) * 3] = ""
                    animesemisiontxt[(int(desus) - 1) * 3 + 1] = ""
                    animesemisiontxt[(int(desus) - 1) * 3 + 2] = ""

                    with open(txtdir, "wb") as animesemision:
                        animesemision.writelines(line.encode('utf-8') for line in animesemisiontxt) 
                    
                    #Muestra la lista de animes
                    listaanimes()

                    if suscripciones < 1: #Confirma si estás suscrito a algún anime
                        input("\n\nPresione ENTER para continuar.\n")
                        break
                    
                    inganim = ""
                        
                    while inganim != "y" and inganim != "n":

                        inganim = input("\n\n¿Desea desuscribirse a otro anime? (y/n) ")
                
                print()


            elif opciones == "3": #Lista de animes suscritos

                listaanimes()

                input("\n\nPresione ENTER para continuar.\n")

            elif opciones == "4":
                print()
                break


    elif opciones == "1": #Buscar nuevos episodios

        #Confirma si estás suscrito a al menos un anime

        listaanimes()

        if suscripciones < 1: #Confirma si estás suscrito a algún anime
            input("\n\nPresione ENTER para continuar.\n")
            continue

        if hidebool == True: #No mostrar la primera vez
            buscaranimes()
            listaanimes()

        hidebool = True
        
        print("\n\n" + Fore.LIGHTBLACK_EX + "Presione ENTER para continuar.")
        
        #Comparar información de los animes suscritos con la información de los nuevos capítulos
        
        confirm = True

        while True: 

            with open(txtdir, "r", encoding="utf-8") as animesemision:
                animesemisiontxt = animesemision.readlines()
                suscripciones = len(animesemisiontxt) // 3

            for y in range(suscripciones): #Cantidad de animes suscritos

                for x in range(len(nombres) - 1, -1, -1): #Cantidad de animes con nuevos capítulos a la inversa

                    if animesemisiontxt[y * 3].strip() == nombres[x].text:

                        if animesemisiontxt[y * 3 + 1].strip() < capitulos[x].text:

                            animesemisiontxt[y * 3 + 1] = capitulos[x].text + "\n" #Se marca el capítulo como visto

                            with open(txtdir, "wb",) as animesemision:
                                animesemision.writelines(line.encode('utf-8') for line in animesemisiontxt) #Se reemplaza el último capítulo visto

                            numulticap = capitulos[x].text.replace("Episodio ", "") #Obtenemos el número del último episodio


                            #Comprobar si el anime finalizó
                            urlnewanime = animesemisiontxt[y * 3 + 2]
                            urlnewanime = urlnewanime.replace("/ver/", "/anime/")
                            checklink = urlnewanime.rfind('-')
                            urlnewanime = urlnewanime[:checklink]
                                
                            #Toma la información de la página
                            newpedido = requests.get(urlnewanime, headers=headers)
                            newhtml = newpedido.text
                            newsoup = BeautifulSoup(newhtml, "html.parser")
                            finalizado = newsoup.find('span', class_='fa-tv')
                            
                            msgfinalizado = ""

                            #Actualiza las listas
                            if finalizado.text == "Finalizado":

                                msgfinalizado = " | Finalizado" #Se agrega en la notificación la finalización

                                #Se actualiza la lista de animes vistos
                                with open(os.getcwd() + "\\config\\AnimesVistos.txt", 'ab') as animesvistos:
                                    animesvistos.write(nombres[x].text.encode('utf-8') + b"\n" + capitulos[x].text.encode('utf-8') + b"\n" + urlnewanime.encode('utf-8') + b"\n")

                                #Borra la información de la lista de animes suscritos
                                animesemisiontxt[y * 3] = ""
                                animesemisiontxt[y * 3 + 1] = ""
                                animesemisiontxt[y * 3 + 2] = ""

                                #Se actualiza la lista de animes suscritos
                                with open(txtdir, "wb") as animesemision:
                                    animesemision.writelines(line.encode('utf-8') for line in animesemisiontxt) 

                                print("\n\n" + Style.BRIGHT + Fore.GREEN + "¡Viste " + nombres[x].text + "!\n" + Fore.YELLOW + "\nEl anime fue enviado a la lista de animes finalizados")

                                listavistos()

                            print("\n\n" + Fore.LIGHTBLACK_EX + "Presione ENTER para continuar.")

                            toast = Notification(app_id="AnimeFLV+",
                                        title=nombres[x].text+ "!!", 
                                        msg=capitulos[x].text + msgfinalizado, 
                                        icon=imagedir,
                                        duration="short", 
                                        launch=animesemisiontxt[y * 3 + 2] + numulticap #Agregamos el último episodio al link
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
                    break # si se presiona una tecla, interrumpe el bucle
                time.sleep(1)

            if confirm == False:
                input()
                break
    
    elif opciones == "3": #Animes finalizados

        listavistos() #Muestra la lista

        inganim = "y"

        while inganim == "y": #Bucle para quitar los animes que quieras

            print("\n\n" + Fore.LIGHTBLACK_EX + "PARA QUITAR UN ANIME: Seleccione uno y presione ENTER." +
                   "\n" + Fore.LIGHTBLACK_EX + "PARA CANCELAR: Presione ENTER sin ingresar nada.")

            #Obtiene la información de la lista
            with open(os.getcwd() + "\\config\\AnimesVistos.txt", "r", encoding="utf-8") as animesvistos:
                animesvistostxt = animesvistos.readlines()
                numanimesvistos = len(animesvistostxt) // 3
            
            quitaranime = input("\n")

            if quitaranime == "":
                break

            confirmquitar = False
            
            for i in range(numanimesvistos): #Confirma si lo ingresado es un índice de su lista

                if quitaranime == str(i + 1):

                    confirmdesus = True

            if confirmdesus == False: #Si no es un índice de la lista, se vuele a mostrar las opciones
                continue

            print("\n\n" + Style.BRIGHT + Fore.RED + "¡Quitaste a " + animesvistostxt[(int(quitaranime) - 1) * 3].strip() + " de la lista de animes vistos!")


            #Borra la información del anime de la lista
            animesvistostxt[(int(quitaranime) - 1) * 3] = ""
            animesvistostxt[(int(quitaranime) - 1) * 3 + 1] = ""
            animesvistostxt[(int(quitaranime) - 1) * 3 + 2] = ""

            #Guarda los cambios
            with open(os.getcwd() + "\\config\\AnimesVistos.txt", "wb") as animesvistos:
                animesvistos.writelines(line.encode('utf-8') for line in animesvistostxt) 
            
            #Muestra la lista de animes
            listavistos()

            if suscripciones < 1: #Confirma si estás suscrito a algún anime
                input("\n\n")
                break
            
            inganim = ""
                
            while inganim != "y" and inganim != "n":

                inganim = input("\n\n¿Desea desuscribirse a otro anime? (y/n) ")
        
        print()


    elif opciones == "4": #Abrir AnimeFLV en navegador
        webbrowser.open(url=urlaniflv, new=0, autoraise=True)

    elif opciones == "5": #Salir
        cerrar()