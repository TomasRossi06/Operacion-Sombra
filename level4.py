import os

# =============================================================================
# NIVEL 4 : INFORME DE RESOLUCION
# La central le envia al jugador una orden: debe crear, en la carpeta donde
# se encuentra main.py, un archivo de texto llamado "Resolucion.txt" que
# contenga unicamente un codigo especifico.
# Tiene un maximo de 3 intentos fallidos antes de perder.
# =============================================================================

FileName         = "Resolucion.txt"
KeyWord  = "Programacion1-UADE-operacion_sombra"
MaxErrors      = 3


def GetBasePath():
    """
    | Descripcion: Obtiene la ruta absoluta de la carpeta base del proyecto, es decir,
    |              la carpeta donde se encuentra este archivo (y por lo tanto main.py).
    |              Se usa para que la busqueda del archivo funcione sin importar desde
    |              donde se ejecute el programa.
    | Entrada: No recibe parametros.
    | Salida: string con la ruta absoluta de la carpeta base.
    """
    return os.path.dirname(os.path.abspath(__file__))


def CheckResolutionFile():
    """
    | Descripcion: Verifica si el archivo Resolucion.txt existe en la carpeta base
    |              y si su contenido coincide exactamente con el esperado.
    | Entrada: No recibe parametros.
    | Salida: True  si el archivo existe y su contenido es correcto.
    |         False si no existe, no se pudo leer, o el contenido no coincide.
    """
    path = os.path.join(GetBasePath(), FileName)

    if not os.path.isfile(path):
        print(f"  [!] No se encontro el archivo {FileName} en la carpeta base.")
        return False

    try:
        with open(path, "r") as f:
            content = f.read().strip()
    except Exception as e:
        print("Error", e)
        return False

    if content.lower() == KeyWord.lower():
        return True

    print("  [X] El archivo existe, pero el contenido no es correcto.")
    return False


def Level4():
    """
    | Descripcion: Ejecuta el Nivel 4 del juego. Le indica al jugador la orden de la
    |              central: crear el archivo Resolucion.txt en la carpeta de main.py
    |              con un contenido especifico. El jugador verifica desde un menu
    |              cuando considera que ya lo creo. Tiene un maximo de 3 intentos
    |              fallidos antes de perder.
    | Entrada: No recibe parametros.
    | Salida: True  si el archivo fue creado correctamente dentro del limite de intentos.
    |         False si se agotaron los intentos o el jugador abandono la mision.
    """
    print("\n######################################")
    print("    NIVEL 4: INFORME DE RESOLUCION")
    print("######################################")
    print("  [CENTRAL] Orden recibida:")
    print(f"  Crea en la carpeta donde esta main.py un archivo")
    print(f"  llamado {FileName} que contenga unicamente:\n")
    print(f"      {KeyWord}\n")
    print("  Cuando lo termines, verificalo desde el menu.\n")

    attempts = 0

    while True:
        print(f"######################################")
        print(f"  NIVEL 4  (Intentos fallidos: {attempts}/{MaxErrors})")
        print("######################################")
        print("  1. Verificar archivo")
        print("  0. Abandonar mision")

        option = input("  option: ").strip()

        if option == "1":
            if CheckResolutionFile():
                print()
                print("  +==========================================+")
                print("  |  INFORME RECIBIDO POR LA CENTRAL         |")
                print("  +==========================================+")
                return True

            attempts += 1
            print(f"  [!] Intentos fallidos: {attempts}/{MaxErrors}\n")

            if attempts >= MaxErrors:
                print("  +==========================================+")
                print("  |  MISION FALLIDA                          |")
                print("  |  La central perdio la conexion.          |")
                print("  +==========================================+")
                return False

        elif option == "0":
            print("  [!] Mision abandonada.")
            return False
        else:
            print("  [!] option invalida.")