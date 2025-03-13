import os
import time
import pyautogui
import sys
import threading
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
import pygame

# Ruta de Google Chrome
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Crear objetos para controlar teclado y mouse
keyboard_control = Controller()
mouse_control = MouseController()

# Variable para detectar movimiento del mouse
mouse_moving = False
stop_program = False  # Variable para detener el programa

#Función para reproducir audio

def reproducir_audio(audio, canal_id):
    """ Reproduce un audio en un canal específico """
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio)
    channel = pygame.mixer.Channel(canal_id)
    channel.play(sound)

def reproducir_audio2(audio, canal_id):
    """ Reproduce un audio en un canal específico """
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio)
    channel = pygame.mixer.Channel(canal_id)
    channel.play(sound, loops=-1)

# Función para detectar movimiento del mouse
def detectar_movimiento():
    global mouse_moving, stop_program
    posicion_anterior = mouse_control.position
    tiempo_inicio = time.time()

    while not stop_program:
        time.sleep(0.1)  # Revisar cada 100 ms
        posicion_actual = mouse_control.position

        if posicion_actual != posicion_anterior:
            if not mouse_moving:
                mouse_moving = True
                tiempo_inicio = time.time()  # Reiniciar el tiempo
            elif time.time() - tiempo_inicio >= 1:
                print("El usuario ha movido el mouse. Deteniendo el programa...")
                stop_program = True
                reproducir_audio("stop.mp3",4)
                sys.exit()  # Detener ejecución

        else:
            mouse_moving = False  # Resetear si el mouse no se mueve
        posicion_anterior = posicion_actual

# Iniciar el monitoreo del mouse en un hilo
threading.Thread(target=detectar_movimiento, daemon=True).start()

# Imagen de elementos a buscar
imagenes = {
    "buscador": "buscador.png",
    "uji": "uji.png",
    "herramientas": "herramientas.png",
    "aula_virtual": "aula_virtual.png",
    "cursos": "cursos.png",
    "inicio_sesion": "inicio_sesion.png",
    "cuenta": "cuenta.png",
    "continuar": "continuar.png",
    "nueva_pestana": "nueva_pestana.png",
    "menu_derecho": "menu_derecho.png",
    "gmail": "gmail.png",
    "codigo": "codigo.png",
    "pestana_numeros": "pestana_numeros.png",
    "confirmacion": "confirmacion.png",
    "retroceder": "retroceder.png"
}

# Función para buscar una imagen en pantalla y hacer clic en ella
def buscar_y_click(imagen, descripcion, confianza=0.8, pausa=0.5, intentos=10):
    global stop_program
    for _ in range(intentos):
        if stop_program:
            return False  # Detener si el programa debe terminar

        try:
            elemento = pyautogui.locateOnScreen(imagen, confidence=confianza, grayscale=True)
            if elemento:
                print(f"{descripcion} encontrado en: {elemento.left}, {elemento.top}")

                # Calcular la posición central del elemento
                x_centro = elemento.left + elemento.width // 2
                y_centro = elemento.top + elemento.height // 2

                # Mover el cursor y hacer clic
                pyautogui.moveTo(x_centro, y_centro, duration=0.5)
                pyautogui.click(x_centro, y_centro)
                print(f"¡Click en {descripcion}!")
                time.sleep(pausa)  # Esperar un poco antes de continuar
                return True
            else:
                print(f"{descripcion} no encontrado, reintentando...")
                time.sleep(1)  # Espera antes de reintentar
        except pyautogui.ImageNotFoundException:
            print(f"No se encontró la imagen de {descripcion}, reintentando...")
            time.sleep(1)  # Espera antes de reintentar
        except Exception as e:
            print(f"Error inesperado al buscar {descripcion}: {e}")
            time.sleep(1)  # Espera antes de reintentar
    return False  # Si no lo encontró en los intentos permitidos, retorna False

#lineas
threading.Thread(target=reproducir_audio("iniciando_protocolo.mp3",0), daemon=True).start()
time.sleep(1.5)
threading.Thread(target=reproducir_audio("protocolo_activado.mp3", 2), daemon=True).start()
# Abrir Chrome con la URL
os.system(f'start "" "{chrome_path}" "https://www.google.com"')
# Buscar y hacer clic en el buscador
if buscar_y_click(imagenes["buscador"], "buscador", confianza=0.6):
    time.sleep(1)
    threading.Thread(target=reproducir_audio2("procesando.mp3", 1), daemon=True).start()
    keyboard_control.type("UJI")
    time.sleep(0.5)
    keyboard_control.press(Key.enter)
    keyboard_control.release(Key.enter)
    print("Buscando 'UJI' en Google...")

# Buscar y hacer clic en la página de UJI
if not buscar_y_click(imagenes["uji"], "UJI", intentos=5):
    buscar_y_click(imagenes["retroceder"], "Retroceso", intentos=5)
    buscar_y_click(imagenes["uji"], "UJI")

time.sleep(2)
# Acceder al menú de herramientas
if not buscar_y_click(imagenes["herramientas"], "Menú de herramientas", intentos=5):
    buscar_y_click(imagenes["uji"], "UJI", intentos=5)
    buscar_y_click(imagenes["herramientas"], "Menú de herramientas")

# Acceder al aula virtual
if not buscar_y_click(imagenes["aula_virtual"], "Aula Virtual", intentos=3):
    buscar_y_click(imagenes["herramientas"], "Menú de herramientas", intentos=3)
    buscar_y_click(imagenes["aula_virtual"], "Aula Virtual")

# Intentar encontrar los cursos
print("Buscando confirmación...")

if not buscar_y_click(imagenes["confirmacion"], "Confirmacion", confianza=0.6, intentos=3):
    print("No se encontró la confirmación. Intentando iniciar sesión...")
else:
    threading.Thread(target=reproducir_audio("fin.mp3", 3), daemon=True).start()
    time.sleep(2.5)
    sys.exit()

# Si no encontró los cursos, intentar iniciar sesión
buscar_y_click(imagenes["inicio_sesion"], "Inicio de sesión")

# Intentar acceder a la cuenta
if not buscar_y_click(imagenes["cuenta"], "Cuenta", intentos=5):
    buscar_y_click(imagenes["inicio_sesion"], "Inicio de sesión", intentos=5)
    buscar_y_click(imagenes["cuenta"], "Cuenta")

# Pulsar el botón de continuar
buscar_y_click(imagenes["continuar"], "Continuar", intentos=5)

# Acceder a una nueva pestaña
buscar_y_click(imagenes["nueva_pestana"], "Pestaña")

# Acceder al menú derecho
buscar_y_click(imagenes["menu_derecho"], "Menú derecho", confianza=0.6)

# Acceder al Gmail
buscar_y_click(imagenes["gmail"], "Gmail", confianza=0.6)

# Mover el cursor a la posición especificada y hacer clic en el correo
time.sleep(1)
pyautogui.moveTo(730, 340, duration=0.5)
pyautogui.click(730, 340)
print("¡Click en el correo!")

# Hacer click izquierdo en la posicion (182, 8) relativa a la imagen que esta mas baja en la pantalla en el caso de haber repetición, mantener, arrastrar un poco hacia la derecha, hacer ctrl + c
#imagen: codigo.png

time.sleep(2)

# Configuración
confianza = 0.8  # Nivel de confianza para la detección de la imagen
desplazamiento_x = 182  # Posición relativa en X dentro de la imagen
desplazamiento_y = 8    # Posición relativa en Y dentro de la imagen

# Buscar todas las coincidencias de la imagen en la pantalla
coincidencias = list(pyautogui.locateAllOnScreen(imagenes["codigo"], confidence=confianza, grayscale=True))

if coincidencias:
    # Seleccionar la imagen que esté más abajo (mayor coordenada Y)
    codigo_mas_bajo = max(coincidencias, key=lambda elem: elem.top)

    print(f"Imagen 'codigo' encontrada en {codigo_mas_bajo.left}, {codigo_mas_bajo.top}")

    # Calcular la posición donde hacer clic dentro de la imagen
    x_click = codigo_mas_bajo.left + desplazamiento_x
    y_click = codigo_mas_bajo.top + desplazamiento_y

    # Hacer clic y mantener
    pyautogui.moveTo(x_click, y_click, duration=0.5)
    pyautogui.mouseDown()  # Mantener clic izquierdo

    # Arrastrar hacia la derecha (100 píxeles)
    pyautogui.moveRel(100, 0, duration=0.5)
    pyautogui.mouseUp()  # Soltar clic

    # Hacer Ctrl + C para copiar
    time.sleep(0.5)  # Esperar un poco antes de copiar
    keyboard_control.press(Key.ctrl)
    keyboard_control.press('c')
    keyboard_control.release('c')
    keyboard_control.release(Key.ctrl)

    print("Texto copiado con Ctrl + C.")

else:
    print("No se encontró la imagen 'codigo'.")

# Accede a la pestaña anterior y pega el código
buscar_y_click(imagenes["pestana_numeros"], "Gmail", confianza=0.6)
time.sleep(0.5)
keyboard_control.press(Key.ctrl)
keyboard_control.press('v')
keyboard_control.release('v')
keyboard_control.release(Key.ctrl)

time.sleep(0.5)
keyboard_control.press(Key.enter)
keyboard_control.release(Key.enter)

threading.Thread(target=reproducir_audio("fin.mp3", 3), daemon=True).start()
time.sleep(2.5)

sys.exit()