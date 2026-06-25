# LIBRERIAS
import re
import random
import os
import json

from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4



# NOTAS CLASE 8 EXCEPCIONES, CLASE 9 PRUEBAS DE DESARROLLO, CLASE 10 ARCHIVOS TXT CSV, CLASE 11 ARCHIVOS JSON, CLASE 12 RECURSIVIDAD

ActPath  = os.path.dirname(__file__)
FilePath = os.path.join(ActPath, "operacion_sombra.json")


def SaveData(profiles, ranking):
    """
    | Descripcion: Guarda el estado actual de profiles y ranking en un archivo JSON.
    |              El archivo se crea o sobreescribe en la misma carpeta del script.
    | Entrada: profiles -> diccionario con los perfiles de los jugadores.
    |          ranking  -> diccionario con los puntajes acumulados.
    | Salida: No retorna nada.
    """
    try:
        data = {
            "profiles": profiles,
            "ranking":  ranking
        }
        with open(FilePath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error", e)


def LoadData():
    """
    | Descripcion: Carga profiles y ranking desde el archivo JSON si existe.
    |              Si el archivo no existe o esta corrupto, retorna diccionarios vacios.
    | Entrada: No recibe parametros.
    | Salida: Una tupla (profiles, ranking) con los datos cargados.
    """
    if not os.path.exists(FilePath):
        return {}, {}
    try:
        with open(FilePath) as f:
            data = json.load(f)
        return data.get("profiles", {}), data.get("ranking", {})
    except Exception as e:
        print(" Error.", e)
        return {}, {}


# =============================================================================
#  CONSTANTES
# =============================================================================

Secret_code  = "NIVEL99"
Total_levels = 4

BANNER = """
+====================================================+
||                                                  ||
||    O P E R A C I O N     S O M B R A             ||
||    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           ||
||                                                  ||
+====================================================+
"""


# =============================================================================
#  UTILIDADES
# =============================================================================

def clean():
    """
    | Descripcion: Limpia la pantalla de la consola.
    | Entrada: No recibe parametros.
    | Salida: No retorna nada.
    """
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """
    | Descripcion: Detiene la ejecucion hasta que el jugador presione ENTER.
    | Entrada: No recibe parametros.
    | Salida: No retorna nada.
    """
    input("\n  Presiona ENTER para continuar...")


# =============================================================================
#  GESTION DE PERFILES
# =============================================================================

def CreateProfile(profiles, ranking):
    """
    | Descripcion: Menu para crear un nuevo perfil de jugador.
    |              Valida que el nombre no este vacio ni repetido.
    |              Guarda automaticamente al crear el perfil.
    | Entrada: profiles -> diccionario con los perfiles existentes.
    |          ranking  -> diccionario con los puntajes (necesario para guardar).
    | Salida: No retorna nada. Modifica profiles en el lugar.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CREAR PERFIL          |")
    print("  +-----------------------------+\n")

    name = input("  Nombre de usuario: ").strip()

    if name == "":
        print("  [!] El nombre no puede estar vacio.")
        pause()
        return

    if name in profiles:
        print(f"  [!] El usuario {name} ya existe.")
        pause()
        return

    profiles[name] = {
        "max_level":      1,
        "games":          0,
        "special_access": False
    }

    SaveData(profiles, ranking)
    print(f"  [OK] Perfil {name} creado con exito.")
    pause()


def SelectUser(profiles):
    """
    | Descripcion: Muestra la lista de profiles y pide elegir uno por numero.
    | Entrada: profiles -> diccionario con los perfiles existentes.
    | Salida: string con el nombre del perfil elegido, o False si cancela.
    """
    if not profiles:
        print("\n  [!] No hay perfiles registrados. Crea uno primero.")
        pause()
        return False

    print("  Perfiles disponibles:\n")
    lista = list(profiles.keys())

    for i, name in enumerate(lista, 1):
        level = profiles[name]["max_level"]
        print(f"    {i}. {name}  (nivel max: {level})")

    print()
    usinput = input("  Elige un perfil (0 para cancelar): ").strip()

    if not usinput.isdigit():
        print("  [!] Entrada invalida. Usa numeros.")
        pause()
        return False

    choice = int(usinput)

    if choice == 0:
        return False

    if choice < 1 or choice > len(lista):
        print("  [!] Numero fuera de rango.")
        pause()
        return False

    return lista[choice - 1]


# =============================================================================
#  PARTIDA
# =============================================================================

def StartGame(profiles, ranking):
    """
    | Descripcion: Permite al jugador elegir un nivel e iniciarlo.
    |              Guarda automaticamente al completar o fallar un nivel.
    | Entrada: profiles -> diccionario con los perfiles de los jugadores.
    |          ranking  -> diccionario con los puntajes acumulados.
    | Salida: No retorna nada.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       INICIAR PARTIDA       |")
    print("  +-----------------------------+\n")

    name = SelectUser(profiles)
    if name is False:
        return

    data      = profiles[name]
    max_level = data["max_level"]

    print(f"\n  Agente: {name}")
    if data["special_access"]:
        print("  [*] Acceso especial activo - todos los niveles desbloqueados.")

    print()
    for i in range(1, Total_levels + 1):
        state = "[+]" if i <= max_level else "[ ]"
        print(f"    {state}  Nivel {i}")

    print()
    input_level = input("  Elige un nivel (0 para cancelar): ").strip()

    if not input_level.isdigit():
        print("  [!] Por favor, ingresa un numero.")
        pause()
        return

    level = int(input_level)

    if level == 0:
        return

    if level < 1 or level > 6:
        print("  [!] Nivel invalido.")
        pause()
        return

    if level > max_level and not data["special_access"]:
        print("  [ ] Nivel bloqueado. Completa los anteriores primero.")
        pause()
        return

    if level > Total_levels and not data["special_access"]:
        print("  [ ] Ese nivel aun no esta implementado.")
        pause()
        return

    print(f"\n  >> Iniciando Nivel {level}...\n")

    completed = False

    if level == 1:
        completed = Level1() == True
    elif level == 2:
        completed = Level2() == True
    elif level == 3:
        completed = Level3() == True
    elif level == 4:
        completed = Level4() == True

    if completed:
        print(f"\n  [OK] Nivel {level} superado.")
        if level == max_level and max_level < Total_levels:
            profiles[name]["max_level"] += 1
            print(f"  [OK] Nivel {level + 1} desbloqueado.")
        UpdateRanking(ranking, name, level)
    else:
        print(f"\n  [!] Nivel {level} no superado. Vuelve a intentarlo.")

    profiles[name]["games"] += 1
    SaveData(profiles, ranking)
    pause()


# =============================================================================
#  CODIGO SECRETO
# =============================================================================

def AccessSecretCode(profiles, ranking):
    """
    | Descripcion: Permite ingresar un codigo secreto para desbloquear todos los niveles.
    |              Guarda automaticamente si el codigo es correcto.
    | Entrada: profiles -> diccionario con los perfiles de los jugadores.
    |          ranking  -> diccionario con los puntajes (necesario para guardar).
    | Salida: No retorna nada. Modifica el perfil del jugador si el codigo es correcto.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CODIGO SECRETO        |")
    print("  +-----------------------------+\n")

    name = SelectUser(profiles)
    if name is False:
        return

    code = input("\n  Ingresa el codigo secreto: ").strip().upper()

    if code == Secret_code:
        profiles[name]["special_access"] = True
        profiles[name]["max_level"]       = 6
        SaveData(profiles, ranking)
        print("  [OK] Codigo correcto. Todos los niveles desbloqueados.")
    else:
        print("  [!] Codigo incorrecto.")

    pause()


# =============================================================================
#  RANKING
# =============================================================================

def UpdateRanking(ranking, name, level):
    """
    | Descripcion: Registra el puntaje obtenido al completar un nivel. Score = nivel x 100.
    | Entrada: ranking -> diccionario con los puntajes acumulados.
    |          name    -> string con el nombre del jugador.
    |          level   -> entero con el numero de nivel completado.
    | Salida: No retorna nada. Modifica ranking en el lugar.
    """
    if name not in ranking:
        ranking[name] = {"score": 0, "completed_levels": 0}
    ranking[name]["score"]            += level * 100
    ranking[name]["completed_levels"] += 1


def ShowRanking(ranking):
    """
    | Descripcion: Muestra la tabla de puntajes ordenada de mayor a menor.
    | Entrada: ranking -> diccionario con los puntajes acumulados.
    | Salida: No retorna nada. Solo imprime el ranking en pantalla.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |           RANKING           |")
    print("  +-----------------------------+\n")

    if not ranking:
        print("  (Sin registros aun)\n")
        pause()
        return

    table = sorted(ranking.items(), key=lambda x: x[1]["score"], reverse=True)

    print(f"  {"#":<4} {"Agente":<20} {"Score":>8}  {"Niveles":>7}")
    print("  " + "-" * 44)
    for i, (player, data) in enumerate(table, 1):
        pos = f"{i}."
        print(f"  {pos:<4} {player:<20} {data["score"]:>8}  {data["completed_levels"]:>5} niv.")

    pause()


# =============================================================================
#  MENU PRINCIPAL
# =============================================================================

def MainMenu():
    """
    | Descripcion: Muestra el menu principal y redirige al jugador segun su eleccion.
    |              Carga los datos guardados al iniciar.
    | Entrada: Opcion numerica ingresada por teclado.
    | Salida: No retorna nada.
    """
    profiles, ranking = LoadData()

    executing = True
    while executing:
        clean()
        print(BANNER)
        print("  +-----------------------------+")
        print("  |        MENU PRINCIPAL       |")
        print("  +-----------------------------+")
        print("  |  1. Crear perfil            |")
        print("  |  2. Iniciar partida         |")
        print("  |  3. Codigo secreto          |")
        print("  |  4. Ver ranking             |")
        print("  |  0. Salir                   |")
        print("  +-----------------------------+")

        option = input("\n  Opcion: ").strip()

        if   option == "1": 
            CreateProfile(profiles, ranking)
        elif option == "2": 
            StartGame(profiles, ranking)
        elif option == "3": 
            AccessSecretCode(profiles, ranking)
        elif option == "4": 
            ShowRanking(ranking)
        elif option == "0":
            clean()
            print("\n  Hasta la proxima, agente.\n")
            executing = False
        else:
            print("  [!] Opcion invalida.")
            pause()


MainMenu()
