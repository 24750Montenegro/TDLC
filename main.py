import sys

from src.parseo import format
from src.shuntingyard import infix_to_postfix, procesar


def imprimir_pasos(expresion):
    postfix, pasos = procesar(expresion)

    print(f"Expresión:        {expresion}")
    print(f"Infix formateado: {format(expresion)}")
    print(f"  {'#':>3}  {'Token':<6} {'Pila':<12} Salida")
    for n, (token, stack, salida) in enumerate(pasos, 1):
        print(f"  {n:>3}  {token:<6} {stack:<12} {salida}")
    print(f"Postfix: {postfix}\n")


def read_file(filename, pasos=False):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                expresion = line.strip()

                if not expresion:
                    continue
                try:
                    if pasos:
                        imprimir_pasos(expresion)
                    else:
                        print(f"Expresión: {expresion:<20} - Formateada(infix): {format(expresion):<20} - Postfix: {infix_to_postfix(expresion)}")
                except ValueError as e:
                    print(f"Expresión inválida '{expresion}': {e}")

    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")


if __name__ == "__main__":
    #el menu imprime epsilon y acentos: sin esto falla si la consola no es UTF-8
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass

    while True:
        print()
        print("=============Menú=============")
        print("1. Leer archivo")
        print("2. Leer archivo paso a paso")
        print("3. Leer archivo y graficar el AST")
        print("4. Leer archivo, generar el AFN y simular una cadena")
        print("5. Salir")
        print("==============================")
        print()
        opcion = input("Seleccione una opción: ")

        if opcion in ('1', '2', '3', '4'):
            filename = input("Ingrese el nombre del archivo: ")
            if not filename.lower().endswith('.txt'):
                filename += '.txt'

            if opcion == '3':
                from src.aplicacion import graficar_archivo
                graficar_archivo(filename)
            elif opcion == '4':
                from src.aplicacion import procesar_archivo
                w = input("Ingrese la cadena w a evaluar: ")
                respuesta = input("¿Abrir las imágenes al terminar? (s/n): ")
                procesar_archivo(filename, w,
                                 abrir=respuesta.strip().lower().startswith('s'))
            else:
                read_file(filename, pasos=(opcion == '2'))

        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione 1, 2, 3, 4 o 5.")
