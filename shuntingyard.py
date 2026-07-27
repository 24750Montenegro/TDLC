

def format(expresion):
    operadores = ['|', '?', '*', '+', '^']
    operadoresBinarios = ['|', '^']
    formatted = ""

    for i in range(len(expresion)):
        p1 = expresion[i]
        formatted += p1 #escribir el caracter actual

        #insertar . si se agrega otro caracter que no sea operador
        if i + 1 < len(expresion):
            p2 = expresion[i + 1]
            if (p1 != '(' and p2 != ')' and p2 not in operadores and p1 not in operadoresBinarios):
                formatted += '.'

    return formatted


def precedence(p):
    #jerarquia de precedencia de los operadores
    precedences = {
        '(': 1,
        '|': 2,   
        '.': 3,   
        '?': 4,   
        '*': 4,
        '+': 4,
        '^': 5,  
    }

    #retornar la precedencia del operador, si no se encuentra en el diccionario, retornar 6 (precedencia más baja)
    return precedences.get(p, 6)

def infix_to_postfix(expresion):
    postfix = ""
    stack = []
    formatted = format(expresion)

    for char in formatted:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            if stack:
                stack.pop()  # quitar el '('
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                postfix += stack.pop()
            
            stack.append(char)

    while stack:
        postfix += stack.pop()

    return postfix

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                expresion = line.strip() #limpiar espacios en blanco al inicio y al final de la línea

                if not expresion:
                    continue
                print (f"Expresión: {expresion} -> Formateada: {format(expresion)}")
                print(f"Expresión en notación posfija: {infix_to_postfix(expresion)}")

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
            ## si no se agrega extension al nombre del archivo, se agrega .txt por defecto
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            read_file(filename)



        elif opcion == '2':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione 1 o 2.")
        