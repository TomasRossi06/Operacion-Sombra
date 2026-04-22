import re
import random

FILAS = 5
COLUMNAS = 6

estacionamiento = [[None] * COLUMNAS for _ in range(FILAS)]
vehiculos = {}
patente_objetivo = None


def validar_patente(patente):
    p = patente.strip().upper()
    if re.match(r"^[A-Z]{2}\d{4}$", p) or re.match(r"^[A-Z]{4}\d{2}$", p):
        return True, p
    return False, None


def generar_patente():
    letras = "ABCDEFGHJKLMNPRSTUVWXYZ"
    if random.randint(0, 1):
        return random.choice(letras) + random.choice(letras) + str(random.randint(1000, 9999))
    else:
        return (
            random.choice(letras)
            + random.choice(letras)
            + random.choice(letras)
            + random.choice(letras)
            + str(random.randint(10, 99))
        )


def inicializar():
    global patente_objetivo, estacionamiento, vehiculos

    estacionamiento = [[None] * COLUMNAS for _ in range(FILAS)]
    vehiculos = {}

    posiciones = [[f, c] for f in range(FILAS) for c in range(COLUMNAS)]
    random.shuffle(posiciones)

    cantidad = random.randint(10, 20)
    patentes_usadas = []

    for f, c in posiciones[:cantidad]:
        p = generar_patente()
        while p in patentes_usadas:
            p = generar_patente()
        patentes_usadas.append(p)
        estacionamiento[f][c] = p
        vehiculos[p] = [f, c]

    patente_objetivo = random.choice(list(vehiculos.keys()))

    print("\n  [CENTRAL] Misión iniciada.")
    print(f"  [CENTRAL] Vehículo objetivo: {patente_objetivo}")


def mostrar_estacionamiento():
    print()
    print("     ", end="")
    for c in range(COLUMNAS):
        print(f"  C{c} ", end="")
    print()

    separador = "     " + "+-----" * COLUMNAS + "+"

    for f in range(FILAS):
        print(separador)
        print(f"  F{f} ", end="")
        for c in range(COLUMNAS):
            valor = estacionamiento[f][c]
            celda = f" {valor} " if valor else "  .  "
            print(f"|{celda}", end="")
        print("|")
    print(separador)
    print()


def buscar():
    fila_str = input("  Ingrese fila: ").strip()
    col_str = input("  Ingrese columna: ").strip()

    if not fila_str.isdigit() or not col_str.isdigit():
        print("  [!] Ingrese números válidos.")
        return False

    fila = int(fila_str)
    col = int(col_str)

    if fila < 0 or fila >= FILAS or col < 0 or col >= COLUMNAS:
        print("  [!] Posición fuera de rango.")
        return False

    patente_en_celda = estacionamiento[fila][col]

    if patente_en_celda is None:
        print("  [!] No hay vehículo en esa posición.")
        return False

    print(f"  [INFO] Encontraste: {patente_en_celda}")

    if patente_en_celda == patente_objetivo:
        print()
        print("  ╔══════════════════════════════════════════╗")
        print("  ║  RED ENEMIGA VULNERADA                   ║")
        print("  ╚══════════════════════════════════════════╝")
        return True

    print("  [X] No es el objetivo.")
    return False


def Nivel2():
    inicializar()
    errores = 0

    while True:
        print("\n  ── NIVEL 2 ──")
        print("  1. Ver estacionamiento")
        print("  2. Buscar vehículo")
        print("  0. Salir")

        opcion = input("  Opción: ").strip()

        if opcion == "1":
            mostrar_estacionamiento()

        elif opcion == "2":
            if buscar():
                break
            else:
                errores += 1
                print(f"  [!] Intentos fallidos: {errores}/3")

                if errores >= 3:
                    print()
                    print("  ╔══════════════════════════════════════════╗")
                    print("  ║  MISIÓN FALLIDA                          ║")
                    print("  ║  El agente ha escapado.                  ║")
                    print("  ╚══════════════════════════════════════════╝")
                    break

        elif opcion == "0":
            break

        else:
            print("  [!] Opción inválida.")


Nivel2()