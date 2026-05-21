import random
import operator
words = ["Agente", "Mision", "Operacion", "Sombra"]
# operation = [operator.add, operator.sub, operator.mul, operator.truediv, operator.pow, operator.mod, operator.floordiv, operator.lt, operator.gt]
operation = [operator.add, operator.sub, operator.mul]



def main():
    errors = 0
    random_word = random.choice(words)
    sign = random.choice(operation)
    errors = ValidateWord(random_word, errors)
    errors = Operation(sign, errors)


def GenerateRandomNumber():
    return random.randint(0,100)


def ValidateWord(randomword, errors):
    while True:
        word = input(f"Ingrese la word  {randomword}:  \n")
        # Validar que sea solo letras
        if not word.isalpha():
            print("Debes ingresar solo letras, sin números ni símbolos.")
            errors += 1
        elif word != randomword:
            print("Cuidado, ingresaste mal la word")
            errors += 1
        else:
            print("Correcto, pasaste la primera etapa del sistema de Captcha")
            break
        if errors >= 3:
            print("Demasiados errors, se activo el sistema de alertas, corre")
            break
    return errors


def StringToOperator(sign):
    if sign == operator.add:
        return "Suma"
    elif sign == operator.sub:
        return "Resta"
    elif sign == operator.mul:
        return "Multiplicacion"
    elif sign == operator.truediv:
        return "Division"
    elif sign == operator.pow:
        return "Potencia"
    elif sign == operator.mod:
        return "Modulo"
    elif sign == operator.floordiv:
        return "Division entera"
    elif sign == operator.lt:
        return "Menor que"
    elif sign == operator.gt:
        return "Mayor que"
    else:
        return "Operador desconocido"



def Operation(sign, errors):
    num1 = GenerateRandomNumber()
    num2 = GenerateRandomNumber()
    print("Realiza la siguiente operation: ")

    while True:
        try:
            USinput = int(input(f"{num1} {StringToOperator(sign)} {num2} = ? \n"))
        except ValueError:
            print("Debes ingresar un número entero válido.")
            errors += 1
            if errors >= 3:
                print("Demasiados errors, se activo el sistema de alertas, corre")
                return errors
            continue

        result = sign(num1, num2)

        print("DEBUG Resultado: ", result)
        print("DEBUG TYPE: ", type(result))
        print("DEBUG Entrada: ", USinput)
        print("DEBUG TYPE: ", type(USinput))

        if USinput == result:
            print("Correcto, pasaste la segunda etapa del sistema de Captcha")
            break
        else:
            print("Cuidado, ingresaste mal la respuesta")
            errors += 1
            if errors >= 3:
                print("Demasiados errors, se activo el sistema de alertas, corre")
                break
    return errors

main()