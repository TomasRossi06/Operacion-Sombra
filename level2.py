import random
import re
# =============================================================================
# NIVEL 2 : parking_lot
# El jugador debe encontrar un vehiculo objetivo dentro de una grilla (matriz).
# La grilla representa un parking_lot con ROWS y COLUMNS.
# Tiene un maximo de 3 intentos fallidos antes de perder.
# =============================================================================

ROWS    = 5
COLUMNS = 6


def validate_patent(patent):
    """
    | Descripcion: Verifica que una patent tenga un formato valido. Acepta dos formatos:
    |                - Formato viejo: 2 letras + 4 numeros  (ej: AB1234)
    |                - Formato nuevo: 4 letras + 2 numeros  (ej: ABCD12)
    | Entrada: patent -> string con la patent a validar (ej: "ab1234" o "AB1234")
    | Salida: string con la patent en mayusculas si es valida (ej: "AB1234")
    |         None si el formato no es correcto.
    """
    p = patent.strip().upper()
    if re.match(r"^[A-Z]{2}\d{4}$", p) or re.match(r"^[A-Z]{4}\d{2}$", p):
        return p
    return None


def generate_patent():
    """
    | Descripcion: Genera una patente aleatoria valida. Con probabilidad 50/50 elige
    |              entre el formato viejo (2L+4N) o el formato nuevo (4L+2N).
    | Entrada: No recibe parametros.
    | Salida: string con una patente generada aleatoriamente (ej: "KR5821" o "MNTP34")
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
    | Descripcion: Prepara el estacionamiento para una nueva partida. Genera una grilla limpia,
    |              coloca entre 10 y 20 vehiculos con patentes unicas en posiciones aleatorias,
    |              y elige uno como objetivo.
    | Entrada: No recibe parametros.
    | Salida: Una tupla (parking_lot, vehicles, target_patent) con el estado inicial de la partida.
    |           parking_lot   -> matriz (lista de listas) con las patentes ubicadas.
    |           vehicles      -> diccionario {patent: [fila, columna]}.
    |           target_patent -> string con la patente que el jugador debe encontrar.
    """
    parking_lot = [[None] * COLUMNS for _ in range(ROWS)]
    vehicles = {}

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

    return parking_lot, vehicles, target_patent


def show_parking_lot(parking_lot):
    """
    | Descripcion: Imprime en consola la grilla del estacionamiento. Las celdas vacias muestran ".".
    | Entrada: parking_lot -> matriz (lista de listas) con el estado actual del estacionamiento.
    | Salida: No retorna nada. Solo imprime la grilla en pantalla.
    """
    print()
    print("     ", end="")
    for c in range(COLUMNS):
        print(f"    C{c} ", end="  ")
    print()

    separator = "     " + "+--------" * COLUMNS + "+"

    for f in range(ROWS):
        print(separator)
        print(f"  F{f} ", end="")
        for c in range(COLUMNS):
            value = parking_lot[f][c]
            cell = (value if value else "  .").center(4)
            print(f"| {cell:<6} ", end="")
        print("|")
    print(separator)
    print()


def search(parking_lot, vehicles, target_patent, errors_actuales):
    """
    | Descripcion: Pide al jugador una posicion (fila y columna) y verifica si hay un
    |              vehiculo ahi y si es el objetivo.
    | Entrada: parking_lot    -> matriz con el estado actual del estacionamiento.
    |          vehicles       -> diccionario {patent: [fila, columna]}.
    |          target_patent  -> string con la patente objetivo.
    |          errors_actuales -> entero con los errores acumulados (contexto para el llamador).
    | Salida: True  -> encontro el vehiculo objetivo.
    |         False -> habia un vehiculo pero no era el objetivo. Cuenta como error.
    |         None  -> entrada invalida o celda vacia. NO cuenta como error.
    """
    row_str = input("  Ingrese fila (0-4): ").strip()
    col_str = input("  Ingrese columna (0-5): ").strip()

    if not row_str.isdigit() or not col_str.isdigit():
        print("  [!] Ingrese numeros validos.")
        return None

    row = int(row_str)
    col = int(col_str)

    if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS:
        print(f"  [!] Posicion fuera de rango. Filas: 0-{ROWS-1}, Columnas: 0-{COLUMNS-1}.")
        return None

    patent_in_cell = parking_lot[row][col]

    if patent_in_cell is None:
        print("  [!] No hay vehiculo en esa posicion. Intente otra celda.")
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
    | Descripcion: Ejecuta el Nivel 2 del juego. Inicializa el estacionamiento y muestra
    |              un menu para verlo o buscar el vehiculo objetivo.
    |              El jugador tiene hasta 3 intentos fallidos antes de perder.
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador encontro el vehiculo objetivo.
    |         False si supero el limite de errores o abandono la mision.
    """
    parking_lot, vehicles, target_patent = initialize()

    errors     = 0
    MAX_ERRORS = 3

    while True:
        print(f"\n######################################")
        print(f"  NIVEL 2  (Intentos fallidos: {errors}/{MAX_ERRORS})")
        print("######################################")
        print("  1. Ver parking_lot")
        print("  2. Buscar vehiculo")
        print("  0. Abandonar mision")

        option = input("  option: ").strip()

        if option == "1":
            show_parking_lot(parking_lot)

        elif option == "2":
            result = search(parking_lot, vehicles, target_patent, errors)

            if result is True:
                return True

            elif result is False:
                errors += 1
                print(f"  [!] Intentos fallidos: {errors}/{MAX_ERRORS}")

                if errors >= MAX_ERRORS:
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