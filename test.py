#LIBRERIAS
import re #Expresiones regulares
import random #Generar numeros aleatorios
import os #Manejar comandos en la terminal

# =============================================================================
#  OPERACION SOMBRA
#  Proyecto grupal - Python
#  Estructura del archivo:
#    1. Nivel 1 : Cifrado Cesar (lineas ~50  en adelante)
#    2. Nivel 2 : Estacionamiento (lineas ~110 en adelante)
#    3. Sistema de perfiles y menu (lineas ~270 en adelante)
#    4. Main(al final)
# =============================================================================


# =============================================================================
# NIVEL 1 : CIFRADO CESAR
# El jugador recibe una palabra cifrada con el metodo Cesar y debe descifrarla.
# El cifrado Cesar desplaza cada letra del abecedario N posiciones hacia adelante.
# Ejemplo con desplazamiento 3: a->d, b->e, c->f ...
# =============================================================================

# La usamos para saber en que posicion esta cada letra y calcular el desplazamiento.
abcedario = list("abcdefghijklmnopqrstuvwxyz")

# Palabra que el jugador debe descifrar
palabra = "agente"


def generar_desplazamiento():
    """
    | Descripcion: Genera un numero de desplazamiento aleatorio para el cifrado Cesar.
    | Entrada: No recibe parametros.
    | Salida: Un numero entero entre 1 y 10 (incluidos).
    """
    # randint(1, 10) devuelve un numero entero al azar entre 1 y 10, ambos incluidos.
    return random.randint(1, 10)


def cifrado_cesar(texto, desplazamiento):
    """
    | Descripcion: Cifra un texto usando el metodo Cesar.
    |              Cada letra se reemplaza por la que esta N posiciones mas adelante
    |              en el abecedario. Si se llega al final, vuelve al principio (es circular).
    | Entrada: texto          -> string con la palabra a cifrar (ej: "agente")
    |          desplazamiento -> entero con cuantas posiciones mover cada letra (ej: 3)
    | Salida: string con la palabra cifrada (ej: "djhqwh")
    """
    resultado = ""
    for letra in texto.lower():
        if letra in abcedario:
            # .index(letra) devuelve la posicion de esa letra en la lista.
            # Sumamos el desplazamiento para avanzar N posiciones.
            # El % len(abcedario) hace que si nos pasamos del final, volvamos al principio.
            indice = (abcedario.index(letra) + desplazamiento) % len(abcedario)
            resultado += abcedario[indice]
            # Ejemplo: letra "x" (posicion 23) + desplazamiento 5 = posicion 28
            #          28 % 26 = 2, que corresponde a la letra "c".
        else:
            # Si el caracter no es una letra (espacio, numero, etc.) lo dejamos igual.
            resultado += letra
    return resultado


def descifrado_cesar(texto, desplazamiento):
    """
    | Descripcion: Descifra un texto cifrado con el metodo Cesar. Hace el proceso inverso al cifrado: resta el desplazamiento
    |              en lugar de sumarlo para recuperar la letra original.
    | Entrada: texto          -> string con la palabra cifrada (ej: "djhqwh")
    |          desplazamiento -> entero con cuantas posiciones se habia desplazado (ej: 3)
    | Salida: string con la palabra descifrada (ej: "agente")
    """
    resultado = ""
    for letra in texto.lower():
        if letra in abcedario:
            # Restamos el desplazamiento para volver a la letra original
            # El % len(abcedario) maneja el caso de llegar a un indice negativo,
            # haciendo que vuelva por el final del abecedario de forma circular
            indice = (abcedario.index(letra) - desplazamiento) % len(abcedario)
            resultado += abcedario[indice]
        else:
            resultado += letra
    return resultado


def Nivel1():
    """
    | Descripcion: Ejecuta el Nivel 1 del juego. Muestra una palabra cifrada con
    |              Cesar y pide al jugador que la descifre manualmente.
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador descifro correctamente la palabra.
    |         False si la respuesta fue incorrecta.
    """

    #Genera un numero de desplazamiento aleatorio para el cifrado Cesar.
    desplazamiento  = generar_desplazamiento()
    #Cifra un texto usando el metodo Cesar.
    palabra_cifrada = cifrado_cesar(palabra, desplazamiento)

    print("\n######################################")
    print("       NIVEL 1: CIFRADO CESAR")
    print("######################################")
    print(f"  Palabra cifrada:    {palabra_cifrada}")
    print(f"  Desplazamiento:     {desplazamiento}")
    print("  Descifra la palabra y escribila abajo.\n")

    # .strip() elimina espacios en blanco al principio y al final del string
    palabra_usuario = input("  Ingresa la palabra: ").strip()


#### como hace para descifrarlo?
    if palabra_usuario.lower() == palabra.lower():
        print("  [OK] Correcto! Acceso concedido.")
        return True
    else:
        print(f"  [X] Incorrecto. La palabra era: {palabra}")
        return False


# =============================================================================
# NIVEL 2 : ESTACIONAMIENTO
# El jugador debe encontrar un vehiculo objetivo dentro de una grilla (matriz).
# La grilla representa un estacionamiento con filas y columnas.
# Tiene un maximo de 3 intentos fallidos antes de perder.
# =============================================================================

# Dimensiones del estacionamiento
FILAS    = 5
COLUMNAS = 6

'''
estacionamiento: matriz (lista de listas) que representa las cocheras.
vehiculos: diccionario que relaciona cada patente con su posicion [fila, columna]. Ejemplo: {"AB1234": [2, 3], "XY9900": [0, 5]}
patente_objetivo: string con la patente que el jugador debe encontrar.Cada celda contiene una patente (string) o None si esta vacia.'''

# Estas tres variables se declaran aqui y se inicializan dentro de inicializar().
estacionamiento = [[None] * COLUMNAS for _ in range(FILAS)]
vehiculos       = {}
patente_objetivo = None


def validar_patente(patente):
    """
    | Descripcion: Verifica que una patente tenga un formato valido. Acepta dos formatos:
    |                - Formato viejo: 2 letras + 4 numeros  (ej: AB1234)
    |                - Formato nuevo: 4 letras + 2 numeros  (ej: ABCD12)
    | Entrada: patente -> string con la patente a validar (ej: "ab1234" o "AB1234")
    | Salida: string con la patente en mayusculas si es valida (ej: "AB1234") None si el formato no es correcto.
    """
    # .upper() convierte todas las letras a mayusculas para comparar de forma uniforme
    p = patente.strip().upper()

    # re.match() verifica si el string cumple con un patron (expresion regular)
    # El patron r"^[A-Z]{2}\d{4}$" significa:
    #   ^       -> inicio del string
    #   [A-Z]{2}-> exactamente 2 letras mayusculas
    #   \d{4}   -> exactamente 4 digitos numericos
    #   $       -> fin del string
    # Si el string coincide con alguno de los dos patrones, la patente es valida.
    if re.match(r"^[A-Z]{2}\d{4}$", p) or re.match(r"^[A-Z]{4}\d{2}$", p):
        return p
    return None


def generar_patente():
    """
    | Descripcion: Genera una patente aleatoria valida. Con probabilidad 50/50 elige entre el formato viejo (2L+4N)
    |              o el formato nuevo (4L+2N).
    | Entrada: No recibe parametros.
    | Salida: string con una patente generada aleatoriamente (ej: "KR5821" o "MNTP34")
    """
    letras = "ABCDEFGHJKLMNPRSTUVWXYZ"

    # random.randint(0, 1) devuelve 0 o 1. Lo usamos para elegir el formato de patente.
    if random.randint(0, 1):
        # Formato viejo: 2 letras + 4 numeros (ej: KR5821)
        # random.choice(letras) elige un caracter al azar del string letras.
        return (random.choice(letras)
                + random.choice(letras)
                + str(random.randint(1000, 9999)))
    else:
        # Formato nuevo: 4 letras + 2 numeros (ej: MNTP34)
        return (random.choice(letras)
                + random.choice(letras)
                + random.choice(letras)
                + random.choice(letras)
                + str(random.randint(10, 99)))


def inicializar():
    """
    | Descripcion: Prepara el estacionamiento para una nueva partida. Limpia la grilla, genera entre 10 y 20 vehiculos con patentes
    |              unicas en posiciones aleatorias, y elige uno como objetivo.
    | Entrada: No recibe parametros. Modifica las variables globales: estacionamiento, vehiculos, patente_objetivo.
    | Salida: No retorna nada. Imprime el vehiculo objetivo en pantalla.
    """
    # Necesitamos declarar estas variables como globales porque vamos a
    # reasignarlas (no solo modificar su contenido).
    global patente_objetivo, estacionamiento, vehiculos

    # Reiniciamos la matriz a todas celdas vacias usando lista por comprension.
    # crea una lista de FILAS listas,cada una con COLUMNAS valores None. None representa una celda sin vehiculo.
    estacionamiento = [[None] * COLUMNAS for _ in range(FILAS)]
    vehiculos       = {}

    # Generamos todas las posiciones posibles como pares [fila, columna].
    # List comprehension equivalente a dos for anidados:
    #   for f in range(FILAS):
    #       for c in range(COLUMNAS):
    #           posiciones.append([f, c])
    posiciones = [[f, c] for f in range(FILAS) for c in range(COLUMNAS)]

    # random.shuffle() mezcla la lista en el lugar de forma aleatoria.
    # Asi, las primeras N posiciones, quedan distribuidas al azar.
    random.shuffle(posiciones)

    cantidad = random.randint(10, 20)
    patentes_usadas = []

    for f, c in posiciones[:cantidad]:
        p = generar_patente()
        # Nos aseguramos de que no haya dos vehiculos con la misma patente.
        while p in patentes_usadas:
            p = generar_patente()
        patentes_usadas.append(p)
        estacionamiento[f][c] = p
        vehiculos[p] = [f, c]

    # vehiculos.keys() devuelve todas las patentes del diccionario.
    # list() la convierte en una lista para poder usarla con random.choice() y rando melige un elemento al azar de esa lista.
    patente_objetivo = random.choice(list(vehiculos.keys()))

    print("\n  [CENTRAL] Mision iniciada.")
    print(f"  [CENTRAL] Vehiculo objetivo: {patente_objetivo}")


def mostrar_estacionamiento():
    """
    | Descripcion: Imprime en consola la grilla del estacionamiento. Las celdas vacias muestran ".".
    | Entrada: No recibe parametros.
    | Salida: No retorna nada. Solo imprime la grilla en pantalla.
    """
    print()
    print("     ", end="")
    for c in range(COLUMNAS):
        print(f"  C{c} ", end="")
        # end="" evita que print salte de linea al terminar, permitiendo imprimir toda la fila de encabezados en una sola linea.
    print()

    separador = "     " + "+------" * COLUMNAS + "+"

    for f in range(FILAS):
        print(separador)
        print(f"  F{f} ", end="")
        for c in range(COLUMNAS):
            valor = estacionamiento[f][c]
            # .center(4) centra el texto dentro de un campo de 4 caracteres, agregando espacios a izquierda y derecha
            celda = (valor if valor else ".").center(4)
            print(f"| {celda} ", end="")
        print("|")
    print(separador)
    print()


def buscar(errores_actuales):
    """
    | Descripcion: Pide al jugador que ingrese una posicion (fila y columna) y verifica si hay un vehiculo ahi, y si ese vehiculo es el objetivo.
    | Entrada: errores_actuales -> entero con la cantidad de errores acumulados
    | (se recibe pero no se usa directamente aqui. Sirve como contexto para llamadas futuras).
    | Salida: True  -> encontro el vehiculo objetivo. El jugador gana.
    |         False -> habia un vehiculo pero no era el objetivo. Cuenta como error.
    |         None  -> entrada invalida o celda vacia. NO cuenta como error.
    """
    fila_str = input("  Ingrese fila (0-4): ").strip()
    col_str  = input("  Ingrese columna (0-5): ").strip()

    # .isdigit() devuelve True si el string contiene solo digitos numericos (0-9).
    # Lo usamos para evitar errores al convertir a int().
    if not fila_str.isdigit() or not col_str.isdigit():
        # Si el usuario escribe "abc" o deja vacio, isdigit() devuelve False.
        print("  [!] Ingrese numeros validos.")
        return None

    #Convertimos a entero, sabiendo que son digitos validos
    # fila_str es el texto ingresado tipo string y fila es ese mismo valor convertido a entero
    fila = int(fila_str)
    col  = int(col_str)

    if fila < 0 or fila >= FILAS or col < 0 or col >= COLUMNAS:
        print(f"  [!] Posicion fuera de rango. Filas: 0-{FILAS-1}, Columnas: 0-{COLUMNAS-1}.")
        return None

    patente_en_celda = estacionamiento[fila][col]

    # Si la celda vale None, significa que esta vacia (no hay vehiculo). En ese caso devolvemos None para no contar el intento.
    if patente_en_celda is None:
        print("  [!] No hay vehiculo en esa posicion. Intente otra celda.")
        return None

    print(f"  [INFO] Encontraste: {patente_en_celda}")

    #Comparamos la patente encontrada con la patente objetivo.
    #True (victoria) y False (error valido: habia vehiculo pero no era el correcto).
    # Usamos booleanos (True/False) para que la funcion que llama a buscar() pueda tomar decisiones claras segun el resultado.
    if patente_en_celda == patente_objetivo:
        print()
        print("  +==========================================+")
        print("  |  RED ENEMIGA VULNERADA                   |")
        print("  +==========================================+")
        return True

    print("  [X] No es el objetivo. Sigue buscando...")
    return False


def Nivel2():
    """
    | Descripcion: Ejecuta el Nivel 2 del juego. Muestra un menu con opciones para ver el estacionamiento o buscar el vehiculo objetivo.
    |              El jugador tiene hasta 3 intentos fallidos antes de perder.
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador encontro el vehiculo objetivo.
    |         False si supero el limite de errores o abandono la mision.
    """
    inicializar()
    errores    = 0
    MAX_ERRORES = 3

    while True:
        print(f"\n######################################")
        print(f"  NIVEL 2  (Intentos fallidos: {errores}/{MAX_ERRORES})")
        print("######################################")
        print("  1. Ver estacionamiento")
        print("  2. Buscar vehiculo")
        print("  0. Abandonar mision")

        opcion = input("  Opcion: ").strip()

        if opcion == "1":
            mostrar_estacionamiento()

        elif opcion == "2":
            resultado = buscar(errores)

            if resultado is True:
                # El jugador encontro el objetivo: salimos del nivel con exito.
                return True

            elif resultado is False:
                # Habia un vehiculo pero no era el objetivo: contamos el error.
                errores += 1
                print(f"  [!] Intentos fallidos: {errores}/{MAX_ERRORES}")

                if errores >= MAX_ERRORES:
                    print()
                    print("  +==========================================+")
                    print("  |  MISION FALLIDA                          |")
                    print("  |  El agente ha escapado.                  |")
                    print("  +==========================================+")
                    return False
            # Si resultado es None (entrada invalida o celda vacia)
        elif opcion == "0":
            print("  [!] Mision abandonada.")
            return False
        else:
            print("  [!] Opcion invalida.")


# =============================================================================
# SISTEMA DE PERFILES Y MENU PRINCIPAL
# Maneja la creacion de jugadores, el acceso a niveles y el ranking global.
# Los perfiles y el ranking se guardan en memoria mientras el programa esta abierto
# =============================================================================

# perfiles: diccionario donde cada clave es el nombre del jugador. Cada jugador tiene: nivel_max (hasta donde llego), 
#partidas (cuantas jugo) y acceso_especial (si uso el codigo secreto para desbloquear todo)
perfiles = {}

# ranking: Guarda el puntaje acumulado y la cantidad de niveles completados
ranking  = {}

# Codigo para desbloquear todos los niveles
CODIGO_SECRETO = "NIVEL99"

""" Actualizar este numero cuando se agreguen nuevos niveles """
NIVELES_TOTALES = 2

BANNER = """
+====================================================+
||                                                  ||
||    O P E R A C I O N     S O M B R A             ||
||    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           ||
||                                                  ||
+====================================================+
"""


def limpiar():
    """
    | Descripcion: Limpia la pantalla de la consola
    | Entrada: No recibe parametros
    | Salida: No retorna nada. Solo limpia la consola
    """
    # os.name devuelve "nt" en Windows y "posix" en Linux/Mac
    # En Windows el comando para limpiar la consola es "cls" y en Linux/Mac es "clear".
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """
    | Descripcion: Detiene la ejecucion hasta que el jugador presione ENTER. Sirve para que el jugador pueda leer los mensajes en pantalla
    |              antes de que se limpie la consola.
    | Entrada: No recibe parametros.
    | Salida: No retorna nada.
    """
    input("\n  Presiona ENTER para continuar...")


def crear_perfil():
    """
    | Descripcion: Menu para crear un nuevo perfil de jugador. Valida que el nombre no este vacio ni repetido.
    | Entrada: Nombre de usuario ingresado por teclado.
    | Salida: Nuevo perfil agregado al diccionario perfiles. No retorna ningun valor.
    """
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

    # Creamos el perfil con sus valores iniciales.
    perfiles[nombre] = {
        "nivel_max":       1,     # nivel_max=1 porque todos empiezan con acceso solo al nivel 1.
        "partidas":        0,
        "acceso_especial": False
    }

    print(f"  [OK] Perfil '{nombre}' creado con exito.")
    pausar()


def seleccionar_usuario():
    """
    | Descripcion: Muestra la lista de perfiles existentes y pide al jugador que elija uno por numero
    | Entrada: Seleccion numerica ingresada por teclado
    | Salida: string con el nombre del perfil elegido si la seleccion es valida.
    |         False si el jugador cancela (elige 0) o ingresa algo invalido
    """
    if not perfiles:
        print("\n  [!] No hay perfiles registrados. Crea uno primero.")
        pausar()
        return False

    print("  Perfiles disponibles:\n")

    # .keys() devuelve una vista con todos los nombres (claves) del diccionario. Convertimos a lista para poder acceder por indice numerico.
    lista = list(perfiles.keys())

    # enumerate(lista, 1) recorre la lista entregando (numero, elemento). Cuenta desde 1 en lugar de 0. Asi mostramos "1. Juan", "2. Ana", etc.
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

    if eleccion == 0:
        return False

    if eleccion < 1 or eleccion > len(lista):
        print("  [!] Numero fuera de rango.")
        pausar()
        return False

    return lista[eleccion - 1]


def iniciar_partida():
    """
    | Descripcion: Permite al jugador elegir un nivel e iniciarlo. Solo muestra los niveles disponibles segun el progreso del jugador.
    |              Un nivel se desbloquea al completar el anterior.
    | Entrada: Seleccion de usuario y nivel ingresada por teclado.
    | Salida: No retorna nada. Llama a la funcion del nivel elegido y actualiza el progreso del jugador segun el resultado.
    """
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       INICIAR PARTIDA       |")
    print("  +-----------------------------+\n")

    # seleccionar_usuario() devuelve False si el jugador cancelo o hubo error.
    nombre = seleccionar_usuario()

    # Verificamos exactamente False porque un nombre como string vacio "" tambien seria falso pero no querriamos ignorarlo. 
    #Esto se llama comparacion "truthy/falsy": en Python, False, None, 0, ""
    # y listas vacias se evaluan como falsos en un if. Usamos "is False" para distinguir el caso de cancelacion del caso de nombre valido.
    if nombre is False:
        return

    datos     = perfiles[nombre]
    nivel_max = datos["nivel_max"]

    print(f"\n  Agente: {nombre}")
    if datos["acceso_especial"]:
        print("  [*] Acceso especial activo - todos los niveles desbloqueados.")

    print()
    for i in range(1, NIVELES_TOTALES + 1):
        # [+] indica nivel desbloqueado y [ ] indica nivel bloqueado.
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
        print("  [ ] Nivel bloqueado. Completa los anteriores primero.")
        pausar()
        return

    if nivel > NIVELES_TOTALES and not datos["acceso_especial"]:
        print("  [ ] Ese nivel aun no esta implementado.")
        pausar()
        return

    print(f"\n  >> Iniciando Nivel {nivel}...\n")

    completado = False

    if nivel == 1:
        # Nivel1() devuelve True o False.
        completado = Nivel1() == True

    elif nivel == 2:
        completado = Nivel2() == True

    # AQUI SE AGREGARAN LOS NIVELES 3, 4 Y 5 CUANDO ESTEN IMPLEMENTADOS

    if completado:
        print(f"\n  [OK] Nivel {nivel} superado.")
        # Solo desbloqueamos el siguiente nivel si el jugador acaba de superar su maximo actual
        if nivel == nivel_max and nivel_max < 6:
            perfiles[nombre]["nivel_max"] += 1
            print(f"  [OK] Nivel {nivel + 1} desbloqueado.")
        actualizar_ranking(nombre, nivel)
    else:
        print(f"\n  [!] Nivel {nivel} no superado. Vuelve a intentarlo.")

    perfiles[nombre]["partidas"] += 1
    pausar()


def acceso_codigo_secreto():
    """
    | Descripcion: Permite ingresar un codigo secreto para desbloquear todos los niveles de un perfil sin tener que completarlos.
    | Entrada: Nombre de usuario (elegido de la lista) y codigo secreto por teclado.
    | Salida: Modifica el perfil del jugador si el codigo es correcto. No retorna ningun valor.
    """
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |       CODIGO SECRETO        |")
    print("  +-----------------------------+\n")

    nombre = seleccionar_usuario()
    if nombre is False:
        return

    codigo = input("\n  Ingresa el codigo secreto: ").strip().upper()

    if codigo == CODIGO_SECRETO:
        perfiles[nombre]["acceso_especial"] = True
        perfiles[nombre]["nivel_max"]       = 6
        print("  [OK] Codigo correcto. Todos los niveles desbloqueados.")
    else:
        print("  [!] Codigo incorrecto.")

    pausar()


def actualizar_ranking(nombre, nivel):
    """
    | Descripcion: Registra el puntaje obtenido por un jugador al completar un nivel.
    |              Si el jugador no tiene entrada en el ranking, la crea. El puntaje se calcula como nivelx100.
    | Entrada: nombre -> string con el nombre del jugador (ej: "Juan")
    |          nivel  -> entero con el numero de nivel completado (ej: 2)
    | Salida: Modifica el diccionario ranking. No retorna ningun valor.
    """
    if nombre not in ranking:
        ranking[nombre] = {"puntaje": 0, "niveles_completados": 0}
    ranking[nombre]["puntaje"]             += nivel * 100
    ranking[nombre]["niveles_completados"] += 1


def ver_ranking():
    """
    | Descripcion: Muestra en pantalla la tabla de puntajes de todos los jugadores, ordenados de mayor a menor puntaje.
    | Entrada: No recibe parametros.
    | Salida: No retorna nada. Solo imprime el ranking en pantalla.
    """
    limpiar()
    print(BANNER)
    print("  +-----------------------------+")
    print("  |           RANKING           |")
    print("  +-----------------------------+\n")

    # Si el diccionario ranking esta vacio (ningun jugador ha completado niveles aun),
    # "not ranking" es True y mostramos el mensaje correspondiente
    if not ranking:
        print("  (Sin registros aun)\n")
        pausar()
        return

    # key=lambda x: x[1]["puntaje"] indica por que campo ordenar:
    #   x es cada par (nombre, datos), x[1] son los datos y x[1]["puntaje"] es el puntaje de ese jugador
    # Una funcion lambda equivale a escribir: def obtener_puntaje(x): return x[1]["puntaje"]
    tabla = sorted(ranking.items(), key=lambda x: x[1]["puntaje"], reverse=True)
    # sorted() devuelve una lista ordenada.
    # ranking.items() entrega pares (nombre, datos) del diccionario.
    # reverse=True ordena de mayor a menor.

    print(f"  {'#':<4} {'Agente':<20} {'Puntaje':>8}  {'Niveles':>7}")
    print("  " + "-" * 44)
    for i, (jugador, datos) in enumerate(tabla, 1):
        pos = f"{i}."
        print(f"  {pos:<4} {jugador:<20} {datos['puntaje']:>8}  {datos['niveles_completados']:>5} niv.")

    pausar()


# =============================================================================
# MAIN - PUNTO DE ENTRADA DEL PROGRAMA

def menu_principal():
    """
    | Descripcion: Muestra el menu principal y redirige al jugador segun su eleccion.
    | Entrada: Opcion numerica ingresada por teclado.
    | Salida: No retorna nada.
    """
    # Usamos una variable booleana para controlar el bucle en lugar de "while True" porque asi podemos salir
    # del bucle de forma clara cambiando ejecutando = False, Es mas legible cuando hay varios puntos de salida.
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
            # Cambiamos la variable a False para que el while termine al final de esta iteracion.
            ejecutando = False
        else:
            print("  [!] Opcion invalida.")
            # pausar() le da tiempo al jugador de leer el mensaje de error
            # antes de que limpiar() borre la pantalla en la siguiente vuelta del bucle.
            pausar()
            
menu_principal()