#LIBRERIAS
import re
import random
import os 

from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4

profiles = {}

ranking  = {}
Secret_code = "NIVEL99"


Total_levels = 4

BANNER = """
+====================================================+
||                                                  ||
||    O P E R A C I O N     S O M B R A             ||
||    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           ||
||                                                  ||
+====================================================+
"""


def clean():
    """
    | Descripcion: Limpia la pantalla de la consola
    | Entrada: No recibe parametros
    | Salida: No retorna nada. Solo limpia la consola
    """

    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """
    | Descripcion: Detiene la ejecucion hasta que el jugador presione ENTER. Sirve para que el jugador pueda leer los mensajes en pantalla
    |              antes de que se limpie la consola.
    | Entrada: No recibe parametros.
    | Salida: No retorna nada.
    """
    input("\n  Presiona ENTER para continuar...")


def create_profile():
    """
    | Descripcion: Menu para crear un nuevo perfil de jugador. Valida que el name no este vacio ni repetido.
    | Entrada: Nombre de usuario ingresado por teclado.
    | Salida: Nuevo perfil agregado al diccionario profiles. No retorna ningun valor.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CREAR PERFIL          |")
    print("  +-----------------------------+\n")

    name = input("  Nombre de usuario: ").strip()

    if name == "":
        print("  [!] El Nombre no puede estar vacio.")
        pause()
        return

    if name in profiles:
        print(f"  [!] El usuario '{name}' ya existe.")
        pause()
        return
    
    profiles[name] = {
        "max_level":       1,     
        "games":        0,
        "special_access": False
    }

    print(f"  [OK] Perfil '{name}' creado con exito.")
    pause()


def select_user():
    """
    | Descripcion: Muestra la lista de profiles existentes y pide al jugador que elija uno por numero
    | Entrada: Seleccion numerica ingresada por teclado
    | Salida: string con el nombre del perfil elegido si la seleccion es valida.
    |         False si el jugador cancela (elige 0) o ingresa algo invalido
    """
    if not profiles:
        print("\n  [!] No hay perfiles registrados. Crea uno primero.")
        pause()
        return False

    print("  Perfiles disponibles:\n")

    lista = list(profiles.keys())

    for i, name in enumerate(lista, 1):
        level = profiles[name]["max_level"]
        print(f"    {i}. {name}  (level max: {level})")

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


def start_game():
    """
    | Descripcion: Permite al jugador elegir un level e iniciarlo. Solo muestra los niveles disponibles segun el progreso del jugador.
    |              Un level se desbloquea al completar el anterior.
    | Entrada: Seleccion de usuario y level ingresada por teclado.
    | Salida: No retorna nada. Llama a la funcion del level elegido y actualiza el progreso del jugador segun el resultado.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       INICIAR PARTIDA       |")
    print("  +-----------------------------+\n")

    name = select_user()

    if name is False:
        return

    data     = profiles[name]
    max_level = data["max_level"]

    print(f"\n  Agente: {name}")
    if data["special_access"]:
        print("  [*] Acceso especial activo - todos los niveles desbloqueados.")

    print()
    for i in range(1, Total_levels + 1):
        state = "[+]" if i <= max_level else "[ ]"
        print(f"    {state}  Nivel {i}")

    print()
    input_level = input("  Elige un level (0 para cancelar): ").strip()

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
        print("  [ ] Ese level aun no esta implementado.")
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
        if level == max_level and max_level < 6:
            profiles[name]["max_level"] += 1
            print(f"  [OK] Nivel {level + 1} desbloqueado.")
        update_ranking(name, level)
    else:
        print(f"\n  [!] Nivel {level} no superado. Vuelve a intentarlo.")

    profiles[name]["games"] += 1
    pause()


def access_secret_code():
    """
    | Descripcion: Permite ingresar un codigo secreto para desbloquear todos los niveles de un perfil sin tener que completarlos.
    | Entrada: Nombre de usuario (elegido de la lista) y codigo secreto por teclado.
    | Salida: Modifica el perfil del jugador si el codigo es correcto. No retorna ningun valor.
    """
    clean()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CODIGO SECRETO        |")
    print("  +-----------------------------+\n")

    name = select_user()
    if name is False:
        return

    code = input("\n  Ingresa el codigo secreto: ").strip().upper()

    if code == Secret_code:
        profiles[name]["special_access"] = True
        profiles[name]["max_level"]       = 6
        print("  [OK] Codigo correcto. Todos los niveles desbloqueados.")
    else:
        print("  [!] Codigo incorrecto.")

    pause()


def update_ranking(name, level):
    """
    | Descripcion: Registra el score obtenido por un jugador al completar un nivel.
    |              Si el jugador no tiene usinput en el ranking, la crea. El score se calcula como nivelx100.
    | Entrada: name -> string con el name del jugador (ej: "Juan")
    |          nivel  -> entero con el numero de nivel completado (ej: 2)
    | Salida: Modifica el diccionario ranking. No retorna ningun valor.
    """
    if name not in ranking:
        ranking[name] = {"score": 0, "completed_levels": 0}
    ranking[name]["score"]             += level * 100
    ranking[name]["completed_levels"] += 1


def show_ranking():
    """
    | Descripcion: Muestra en pantalla la tabla de puntajes de todos los jugadores, ordenados de mayor a menor score.
    | Entrada: No recibe parametros.
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


    print(f"  {'#':<4} {'Agent':<20} {'Score':>8}  {'Levels':>7}")
    print("  " + "-" * 44)
    for i, (player, data) in enumerate(table, 1):
        pos = f"{i}."
        print(f"  {pos:<4} {player:<20} {data['score']:>8}  {data['completed_levels']:>5} niv.")

    pause()



def main_menu():
    """
    | Descripcion: Muestra el menu principal y redirige al jugador segun su choice.
    | Entrada: option numerica ingresada por teclado.
    | Salida: No retorna nada.
    """

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

        option = input("\n  option: ").strip()

        if   option == "1": create_profile()
        elif option == "2": start_game()
        elif option == "3": access_secret_code()
        elif option == "4": show_ranking()
        elif option == "0":
            clean()
            print("\n  Hasta la proxima, agente.\n")
            executing = False
        else:
            print("  [!] option invalida.")
            pause()
            
main_menu()