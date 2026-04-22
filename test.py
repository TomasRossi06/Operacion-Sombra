import re
import random
import os

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
                return True
            else:
                errores += 1
                print(f"  [!] Intentos fallidos: {errores}/3")

                if errores >= 3:
                    print()
                    print("  ╔══════════════════════════════════════════╗")
                    print("  ║  MISIÓN FALLIDA                          ║")
                    print("  ║  El agente ha escapado.                  ║")
                    print("  ╚══════════════════════════════════════════╝")
                    return False

        elif opcion == "0":
            return False

        else:
            print("  [!] Opción inválida.")


abcedario = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

palabra = "agente"

def generardesplazamiento():
    return random.randint(1, 10)


def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for letra in texto:
        if letra in abcedario:
            indice = (abcedario.index(letra) + desplazamiento) % len(abcedario)
            resultado += abcedario[indice]
        else:
            resultado += letra
    return resultado


def descifrado_cesar(texto, desplazamiento):
    resultado = ""
    for letra in texto:
        if letra in abcedario:
            indice = (abcedario.index(letra) - desplazamiento) % len(abcedario)
            resultado += abcedario[indice]
        else:
            resultado += letra
    return resultado


def ingresar_palabra(desplazamiento):
    print("El desplazamiento es de:", desplazamiento)
    return input("Ingresa la palabra: ")


def Nivel1():
    desplazamiento = generardesplazamiento()
    palabra_cifrada = cifrado_cesar(palabra.lower(), desplazamiento)

    print("\n── NIVEL 1: CIFRADO CÉSAR ──")
    print(f"Palabra cifrada: {palabra_cifrada}")

    palabra_usuario = ingresar_palabra(desplazamiento)

    if palabra_usuario.lower() == palabra.lower():
        print("Correcto! Adivinaste la palabra.")
        return True
    else:
        print("Incorrecto. Intenta de nuevo.")

    



perfiles = {}
ranking  = {}

CODIGO_SECRETO = "NIVEL99"

BANNER = """
+====================================================+
||                                                  ||
||    O P E R A C I O N     S O M B R A             ||
||    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           ||
||                                                  ||
||              6 NIVELES DE MISION                 ||
||                                                  ||
+====================================================+
"""

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\n  Presiona ENTER para continuar...")

def crear_perfil():
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CREAR PERFIL          |")
    print("  +-----------------------------+\n")

    nombre = input("  Nombre de usuario: ").strip()

    if nombre == "":
        print("  [!] El nombre no puede estar vacio.")
        pausar()
        return

    if nombre in perfiles:
        print(f"  [!] El usuario '{nombre}' ya existe.")
        pausar()
        return

    perfiles[nombre] = {
        "nivel_max":       1,
        "partidas":        0,
        "acceso_especial": False
    }

    print(f"  [OK] Perfil '{nombre}' creado con exito.")
    pausar()

def seleccionar_usuario():
    if not perfiles:
        print("\n  [!] No hay perfiles registrados. Crea uno primero.")
        pausar()
        return False 

    print("  Perfiles disponibles:\n")
    lista = list(perfiles.keys())
    for i, nombre in enumerate(lista, 1):
        nivel = perfiles[nombre]["nivel_max"]
        print(f"    {i}. {nombre}  (nivel max: {nivel})")

    print()
    entrada = input("  Elige un perfil (0 para cancelar): ").strip()

    if not entrada.isdigit():
        print("  [!] Entrada invalida. Usa numeros.")
        pausar()
        return False

    eleccion = int(entrada)

    if eleccion <= 0 or eleccion > len(lista):
        return False

    return lista[eleccion - 1]

def iniciar_partida():
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       INICIAR PARTIDA       |")
    print("  +-----------------------------+\n")

    nombre = seleccionar_usuario() 
    
    # Validamos si nombre es False (el usuario cancelo o no hay perfiles)
    if nombre == False:
        return

    datos = perfiles[nombre]
    nivel_max = datos["nivel_max"]

    print(f"\n  Agente: {nombre}")
    if datos["acceso_especial"]:
        print("  [*] Acceso especial activo - todos los niveles desbloqueados.")

    print()
    for i in range(1, 3):
        estado = "[+]" if i <= nivel_max else "[ ]"
        print(f"    {estado}  Nivel {i}")

    print()
    entrada_nivel = input("  Elige un nivel (0 para cancelar): ").strip()

    if not entrada_nivel.isdigit():
        print("  [!] Por favor, ingresa un numero.")
        pausar()
        return

    nivel = int(entrada_nivel)

    if nivel == 0:
        return



    if nivel < 1 or nivel > 6:
        print("  [!] Nivel invalido.")
        pausar()
        return

    if nivel > nivel_max and not datos["acceso_especial"]:
        print("  [ ] Nivel bloqueado. Completa los anteriores.")
        pausar()
        return

    print(f"\n  >> Iniciando Nivel {nivel}...")
    #print("  (Logica del nivel por implementar)\n")

    if nivel == 1:
        if Nivel1() == True:
            completado = True

    if nivel == 2:
        resultado = Nivel2()
        if resultado == True:
            completado = True
        


    if completado:
        if nivel == nivel_max and nivel_max < 6:
            perfiles[nombre]["nivel_max"] += 1
            print(f"  [OK] Nivel {nivel + 1} desbloqueado.")
        actualizar_ranking(nombre, nivel)

    perfiles[nombre]["partidas"] += 1
    pausar()

def acceso_codigo_secreto():
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CODIGO SECRETO        |")
    print("  +-----------------------------+\n")

    nombre = seleccionar_usuario()
    if nombre == False:
        return

    codigo = input("\n  Ingresa el codigo secreto: ").strip().upper()

    if codigo == CODIGO_SECRETO:
        perfiles[nombre]["acceso_especial"] = True
        perfiles[nombre]["nivel_max"]       = 6
        print("  [OK] Codigo correcto. Niveles desbloqueados.")
    else:
        print("  [!] Codigo incorrecto.")

    pausar()

def actualizar_ranking(nombre, nivel):
    if nombre not in ranking:
        ranking[nombre] = {"puntaje": 0, "niveles_completados": 0}
    ranking[nombre]["puntaje"]             += nivel * 100
    ranking[nombre]["niveles_completados"] += 1

def ver_ranking():
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |           RANKING           |")
    print("  +-----------------------------+\n")

    if not ranking:
        print("  (Sin registros aun)\n")
        pausar()
        return

    tabla = sorted(ranking.items(), key=lambda x: x[1]["puntaje"], reverse=True)

    print(f"  {'#':<4} {'Agente':<20} {'Puntaje':>8}  {'Niveles':>7}")
    print("  " + "-" * 44)
    for i, (jugador, datos) in enumerate(tabla, 1):
        pos = f"{i}."
        print(f"  {pos:<4} {jugador:<20} {datos['puntaje']:>8}  {datos['niveles_completados']:>5} niv.")

    pausar()

""" Main """
def menu_principal():
    ejecutando = True
    while ejecutando:
        limpiar()
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

        opcion = input("\n  Opcion: ").strip()

        if   opcion == "1": crear_perfil()
        elif opcion == "2": iniciar_partida()
        elif opcion == "3": acceso_codigo_secreto()
        elif opcion == "4": ver_ranking()
        elif opcion == "0":
            limpiar()
            print("\n  Hasta la proxima, agente.\n")
            ejecutando = False
        else:
            print("  [!] Opcion invalida.")
            pausar()

menu_principal()