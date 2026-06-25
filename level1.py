import random
# =============================================================================
# NIVEL 1 : CIFRADO CESAR
# El jugador recibe una palabra cifrada con el metodo Cesar y debe descifrarla.
# El cifrado Cesar desplaza cada letra del abecedario N posiciones hacia adelante.
# Ejemplo con desplazamiento 3: a->d, b->e, c->f ...
# =============================================================================


abcedary = list("abcdefghijklmnopqrstuvwxyz")
word = "agente"


def GenerateDisplacement():
    """
    | Descripcion: Genera un numero de desplazamiento aleatorio para el cifrado Cesar.
    | Entrada: No recibe parametros.
    | Salida: Un numero entero entre 1 y 10 (incluidos).
    """

    return random.randint(1, 10)


def CodeCesar(text, displacement):
    """
    | Descripcion: Cifra un texto usando el metodo Cesar.
    |              Cada letra se reemplaza por la que esta N posiciones mas adelante
    |              en el abecedario. Si se llega al final, vuelve al principio (es circular).
    | Entrada: texto          -> string con la palabra a cifrar (ej: "agente")
    |          desplazamiento -> entero con cuantas posiciones mover cada letra (ej: 3)
    | Salida: string con la palabra cifrada (ej: "djhqwh")
    """
    result = ""
    for letter in text.lower():
        if letter in abcedary:
            index = (abcedary.index(letter) + displacement) % len(abcedary)
            result += abcedary[index]
        else:
            result += letter
    return result


def DecodeCesar(text, displacement):
    """
    | Descripcion: Descifra un texto cifrado con el metodo Cesar. Hace el proceso inverso al cifrado: resta el desplazamiento
    |              en lugar de sumarlo para recuperar la letra original.
    | Entrada: texto          -> string con la palabra cifrada (ej: "djhqwh")
    |          desplazamiento -> entero con cuantas posiciones se habia desplazado (ej: 3)
    | Salida: string con la palabra descifrada (ej: "agente")
    """
    result = ""
    for letter in text.lower():
        if letter in abcedary:
            index = (abcedary.index(letter) - displacement) % len(abcedary)
            result += abcedary[index]
        else:
            result += letter
    return result


def Level1():
    """
    | Descripcion: Ejecuta el Nivel 1 del juego. Muestra una palabra cifrada con
    |              Cesar y pide al jugador que la descifre manualmente.
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador descifro correctamente la palabra.
    |         False si la respuesta fue incorrecta.
    """

    displacement  = GenerateDisplacement()
    encryptedword = CodeCesar(word, displacement)

    print("\n######################################")
    print("       NIVEL 1: CIFRADO CESAR")
    print("######################################")
    print(f"  Palabra cifrada:    {encryptedword}")
    print(f"  Desplazamiento:     {displacement}")
    print("  Descifra la palabra y escribila abajo.\n")

    
    try:
        UserWord = input("  Ingresa la palabra: ").strip()

    except Exception as e:
        print("Error", e)
        return False

    if UserWord.lower() == word.lower():
        print("  [OK] Correcto! Acceso concedido.")
        return True
    else:
        print(f"  [X] Incorrecto. La palabra era: {word}")
        return False


