import random
import re
# =============================================================================
# NIVEL 2 : parking_lot
# El jugador debe encontrar un vehiculo objetivo dentro de una grilla (matriz).
# La grilla representa un parking_lot con ROWS y COLUMNS.
# Tiene un maximo de 3 intentos fallidos antes de perder.
# =============================================================================

# Dimensiones del parking_lot
ROWS    = 5
COLUMNS = 6

'''
parking_lot: matriz (lista de listas) que representa las cocheras.
vehicles: diccionario que relaciona cada patent con su posicion [row, columna]. Ejemplo: {"AB1234": [2, 3], "XY9900": [0, 5]}
target_patent: string con la patent que el jugador debe encontrar.Cada cell contiene una patent (string) o None si esta vacia.'''


parking_lot = [[None] * COLUMNS for _ in range(ROWS)]
vehicles       = {}
target_patent = None


def validate_patent(patent):
    """
    | Descripcion: Verifica que una patent tenga un formato valido. Acepta dos formatos:
    |                - Formato viejo: 2 letters + 4 numeros  (ej: AB1234)
    |                - Formato nuevo: 4 letters + 2 numeros  (ej: ABCD12)
    | Entrada: patent -> string con la patent a validar (ej: "ab1234" o "AB1234")
    | Salida: string con la patent en mayusculas si es valida (ej: "AB1234") None si el formato no es correcto.
    """
    p = patent.strip().upper()
    if re.match(r"^[A-Z]{2}\d{4}$", p) or re.match(r"^[A-Z]{4}\d{2}$", p):
        return p
    return None


def generate_patent():
    """
    | Descripcion: Genera una patent aleatoria valida. Con probabilidad 50/50 elige entre el formato viejo (2L+4N)
    |              o el formato nuevo (4L+2N).
    | Entrada: No recibe parametros.
    | Salida: string con una patent generada aleatoriamente (ej: "KR5821" o "MNTP34")
    """
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"

    if random.randint(0, 1):
        return (random.choice(letters)
                + random.choice(letters)
                + str(random.randint(1000, 9999)))
    else:
        return (random.choice(letters)
                + random.choice(letters)
                + random.choice(letters)
                + random.choice(letters)
                + str(random.randint(10, 99)))


def initialize():
    """
    | Descripcion: Prepara el parking_lot para una nueva partida. Limpia la grilla, genera entre 10 y 20 vehicles con patents
    |              unicas en positions aleatorias, y elige uno como objetivo.
    | Entrada: No recibe parametros. Modifica las variables globales: parking_lot, vehicles, target_patent.
    | Salida: No retorna nada. Imprime el vehiculo objetivo en pantalla.
    """
    global target_patent, parking_lot, vehicles

    parking_lot = [[None] * COLUMNS for _ in range(ROWS)]
    vehicles       = {}

    positions = [[f, c] for f in range(ROWS) for c in range(COLUMNS)]

    random.shuffle(positions)

    amount = random.randint(10, 20)
    used_patents = []

    for f, c in positions[:amount]:
        p = generate_patent()
        while p in used_patents:
            p = generate_patent()
        used_patents.append(p)
        parking_lot[f][c] = p
        vehicles[p] = [f, c]
    target_patent = random.choice(list(vehicles.keys()))

    print("\n  [CENTRAL] Mision iniciada.")
    print(f"  [CENTRAL] Vehiculo objetivo: {target_patent}")


def show_parking_lot():
    """
    | Descripcion: Imprime en consola la grilla del parking_lot. Las cells vacias muestran ".".
    | Entrada: No recibe parametros.
    | Salida: No retorna nada. Solo imprime la grilla en pantalla.
    """
    print()
    print("     ", end="")
    for c in range(COLUMNS):
        print(f"  C{c} ", end="")
    print()

    separator = "     " + "+------" * COLUMNS + "+"

    for f in range(ROWS):
        print(separator)
        print(f"  F{f} ", end="")
        for c in range(COLUMNS):
            value = parking_lot[f][c]
            cell = (value if value else ".").center(4)
            print(f"| {cell} ", end="")
        print("|")
    print(separator)
    print()


def search(errors_actuales):
    """
    | Descripcion: Pide al jugador que ingrese una posicion (row y columna) y verifica si hay un vehiculo ahi, y si ese vehiculo es el objetivo.
    | Entrada: errors_actuales -> entero con la amount de errors acumulados
    | (se recibe pero no se usa directamente aqui. Sirve como contexto para llamadas futuras).
    | Salida: True  -> encontro el vehiculo objetivo. El jugador gana.
    |         False -> habia un vehiculo pero no era el objetivo. Cuenta como error.
    |         None  -> entrada invalida o cell vacia. NO cuenta como error.
    """
    row_str = input("  Ingrese row (0-4): ").strip()
    col_str  = input("  Ingrese columna (0-5): ").strip()


    if not row_str.isdigit() or not col_str.isdigit():
        print("  [!] Ingrese numeros validos.")
        return None


    row = int(row_str)
    col  = int(col_str)

    if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS:
        print(f"  [!] Posicion fuera de rango. rows: 0-{ROWS-1}, Columnas: 0-{COLUMNS-1}.")
        return None

    patent_in_cell = parking_lot[row][col]

    if patent_in_cell is None:
        print("  [!] No hay vehiculo en esa posicion. Intente otra cell.")
        return None

    print(f"  [INFO] Encontraste: {patent_in_cell}")

    if patent_in_cell == target_patent:
        print()
        print("  +==========================================+")
        print("  |  RED ENEMIGA VULNERADA                   |")
        print("  +==========================================+")
        return True

    print("  [X] No es el objetivo. Sigue buscando...")
    return False


def Level2():
    """
    | Descripcion: Ejecuta el Nivel 2 del juego. Muestra un menu con optiones para ver el parking_lot o search el vehiculo objetivo.
    |              El jugador tiene hasta 3 intentos fallidos antes de perder.
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador encontro el vehiculo objetivo.
    |         False si supero el limite de errors o abandono la mision.
    """
    initialize()
    errors    = 0
    MAX_errors = 3

    while True:
        print(f"\n######################################")
        print(f"  NIVEL 2  (Intentos fallidos: {errors}/{MAX_errors})")
        print("######################################")
        print("  1. Ver parking_lot")
        print("  2. search vehiculo")
        print("  0. Abandonar mision")

        option = input("  option: ").strip()

        if option == "1":
            show_parking_lot()

        elif option == "2":
            result = search(errors)

            if result is True:
                return True

            elif result is False:
                errors += 1
                print(f"  [!] Intentos fallidos: {errors}/{MAX_errors}")

                if errors >= MAX_errors:
                    print()
                    print("  +==========================================+")
                    print("  |  MISION FALLIDA                          |")
                    print("  |  El agente ha escapado.                  |")
                    print("  +==========================================+")
                    return False
        elif option == "0":
            print("  [!] Mision abandonada.")
            return False
        else:
            print("  [!] option invalida.")