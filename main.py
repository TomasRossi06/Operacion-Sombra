import random
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

desplazamiento = generardesplazamiento()
palabra_cifrada = cifrado_cesar(palabra.lower(), desplazamiento)

print(f"Palabra cifrada: {palabra_cifrada}")

def ingresar_palabra():
    print("El desplazamiento es de: ", desplazamiento)
    return input("Ingresa la palabra: ")


palabra_usuario = ingresar_palabra()

if palabra_usuario.lower() == palabra.lower():
    print("Correcto! Adivinaste la palabra.")
else:
    print("Incorrecto. Intenta de nuevo.")

    

