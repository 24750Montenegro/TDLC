
import sys

from src.aplicacion import graficar_archivo, procesar_archivo, read_file
from src.archivos import resolver

OPCIONES = [
    "1. Leer archivo",
    "2. Leer archivo paso a paso",
    "3. Leer archivo y graficar el AST",
    "4. Leer archivo, generar el AFN y simular una cadena",
    "5. Leer archivo, convertir el AFN a AFD y simular una cadena",
    "6. Leer archivo, minimizar el AFD y simular una cadena",
    "7. Leer archivo y generar AFN, AFD y AFD mínimo",
    "8. Salir",
]

#que automatas construye cada opcion del menu
TIPOS = {
    '4': ('afn',),
    '5': ('afd',),
    '6': ('min',),
    '7': ('afn', 'afd', 'min'),
}


def pedir_archivo():
    return resolver(input("Ingrese el nombre del archivo: "))


def pedir_simulacion():
    #la cadena w y si se abren los .svg al terminar
    w = input("Ingrese la cadena w a evaluar: ")
    respuesta = input("¿Abrir las imágenes al terminar? (s/n): ")
    return w, respuesta.strip().lower().startswith('s')


def mostrar_menu():
    print()
    print("=============Menú=============")
    for opcion in OPCIONES:
        print(opcion)
    print("==============================")
    print()


def ejecutar(opcion):
    #devuelve False cuando la opcion elegida es salir
    if opcion == '8':
        print("Saliendo del programa.")
        return False

    if opcion not in ('1', '2', '3', '4', '5', '6', '7'):
        print("Opción inválida. Por favor, seleccione un número del 1 al 8.")
        return True

    filename = pedir_archivo()

    if opcion == '3':
        graficar_archivo(filename)
    elif opcion in TIPOS:
        w, abrir = pedir_simulacion()
        procesar_archivo(filename, w, tipos=TIPOS[opcion], abrir=abrir)
    else:
        read_file(filename, pasos=(opcion == '2'))

    return True


def main():
    #el menu imprime epsilon y acentos: sin esto falla si la consola no es UTF-8
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass

    while True:
        mostrar_menu()
        if not ejecutar(input("Seleccione una opción: ")):
            break


if __name__ == "__main__":
    main()
