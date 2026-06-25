import random
import operator

# =============================================================================
# NIVEL 3 : CAPTCHA
# El jugador debe superar dos etapas:
#   1. Escribir correctamente una palabra dada.
#   2. Resolver una operacion aritmetica.
# Tiene un maximo de 3 errores en total antes de perder.
# =============================================================================

words     = ["Agente", "Mision", "Operacion", "Sombra"]
operation = [operator.add, operator.sub, operator.mul]

MaxErrors = 3


def OperatorName(sign):
    """
    | Descripcion: Devuelve el nombre en texto de un operador.
    | Entrada: sign -> funcion operador (ej: operator.add)
    | Salida: string con el nombre (ej: "Suma")
    """
    names = {
        operator.add:      "+",
        operator.sub:      "-",
        operator.mul:      "x",
        operator.truediv:  "/",
        operator.pow:      "^",
        operator.mod:      "%",
        operator.floordiv: "//",
    }
    return names.get(sign, "?")


def ValidateWord(RandomWord, errors):
    """
    | Descripcion: Etapa 1 del captcha. Pide al jugador que escriba la palabra mostrada.
    | Entrada: RandomWord -> string con la palabra que debe escribir el jugador.
    |          errors      -> entero con los errores acumulados hasta ahora.
    | Salida: (passed, errors) -> bool indicando si supero la etapa, y errores actualizados.
    """
    print("\n  -- ETAPA 1: Escribe la siguiente palabra --")
    while errors < MaxErrors:
        word = input(f"  Palabra: {RandomWord} -> ").strip()

        if not word.isalpha():
            print("  [!] Solo letras, sin numeros ni simbolos.")
            errors += 1
        elif word != RandomWord:
            print("  [X] Palabra incorrecta. Intenta de nuevo.")
            errors += 1
        else:
            print("  [OK] Etapa 1 superada.")
            return True, errors

        if errors >= MaxErrors:
            break

    return False, errors


def SolveOperation(sign, errors):
    """
    | Descripcion: Etapa 2 del captcha. Genera dos numeros aleatorios y pide al jugador
    |              que resuelva la operacion indicada.
    | Entrada: sign   -> funcion operador a usar.
    |          errors -> entero con los errores acumulados hasta ahora.
    | Salida: (passed, errors) -> bool indicando si supero la etapa, y errores actualizados.
    """
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    expected = sign(num1, num2)

    print("\n  -- ETAPA 2: Resuelve la operacion --")
    while errors < MaxErrors:
        try:
            answer = int(input(f"  {num1} {OperatorName(sign)} {num2} = ").strip())
        except ValueError:
            print("  [!] Debes ingresar un numero entero valido.")
            errors += 1
            continue

        if answer == int(expected):
            print("  [OK] Etapa 2 superada.")
            return True, errors
        else:
            print("  [X] Resultado incorrecto. Intenta de nuevo.")
            errors += 1

        if errors >= MaxErrors:
            break

    return False, errors


def Level3():
    """
    | Descripcion: Ejecuta el Nivel 3 del juego (sistema de captcha en dos etapas).
    | Entrada: No recibe parametros.
    | Salida: True  si el jugador supero ambas etapas dentro del limite de errores.
    |         False si acumulo 3 errores o fallo alguna etapa.
    """
    print("\n######################################")
    print("       NIVEL 3: CAPTCHA")
    print("######################################")
    print(f"  Tienes un maximo de {MaxErrors} errores en total.\n")

    RandomWord = random.choice(words)
    sign        = random.choice(operation)
    errors      = 0

    PassedWord, errors = ValidateWord(RandomWord, errors)
    if not PassedWord:
        print(f"\n  [!] Demasiados errores. Sistema de alertas activado.")
        return False

    PassedOp, errors = SolveOperation(sign, errors)
    if not PassedOp:
        print(f"\n  [!] Demasiados errores. Sistema de alertas activado.")
        return False

    print("\n  [OK] Captcha superado. Acceso concedido.")
    return True
