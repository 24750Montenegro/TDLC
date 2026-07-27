


def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                expresion = line.strip()

                if not expresion:
                    continue
                print (f"Expresión: {expresion}")

    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")


if __name__ == "__main__":
    opcion = 0
    while opcion != 2:
        print("Menú:")
        print("1. Leer archivo")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            filename = input("Ingrese el nombre del archivo: ")
            read_file(filename)

            ## si no se agrega extension al nombre del archivo, se agrega .txt por defecto
            if not filename.endswith('.txt'):
                filename += '.txt'
            
        elif opcion == '2':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione 1 o 2.")
        