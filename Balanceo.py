"""
Ejercicio 2: verificador de balanceo de simbolos () [] {} usando una pila,
para expresiones regulares en formato infix.

el uso se va a determinar por:
    correr en terminal -> python Balanceo.py
    (que va a pedir el nombre del archivo de texto a procesar, en este caso
    ejercicio2.txt, una expresion por linea)

la verificacion vive en src/balanceo.py y la traza en src/reportes.py, asi que
tambien se pueden reutilizar desde otro programa.
"""

import sys

from src.aplicacion import verificar_archivo
from src.archivos import resolver


def mostrar_menu():
    print()
    print("========== Ejercicio 2: Verificador de balanceo ==========")
    print("1. Leer el  archivo y verificar balanceo")
    print("2. Salir")
    print("============================================================")


def ejecutar(opcion):
    #devuelve False cuando la opcion elegida es salir
    if opcion == '2':
        print("Saliendo del programa.")
        return False

    if opcion != '1':
        print("Opcion invalida. Por favor, seleccione 1 o 2.")
        return True

    verificar_archivo(resolver(input("Ingrear el nombre del archivo: ")))
    return True


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass

    while True:
        mostrar_menu()
        if not ejecutar(input("Seleccione una opcion: ")):
            break


if __name__ == "__main__":
    main()
