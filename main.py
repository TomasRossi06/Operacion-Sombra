import os

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
    for i in range(1, 7):
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
    print("  (Logica del nivel por implementar)\n")

    completado = input("  Completaste el nivel? (s/n): ").strip().lower() == "s"

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