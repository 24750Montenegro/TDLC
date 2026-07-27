

operadoresUnarios = ['?', '*', '+']
operadoresBinarios = ['|', '.', '^']
operadores = operadoresUnarios + operadoresBinarios


def format(expresion):
    formatted = ""

    for i in range(len(expresion)):
        p1 = expresion[i]
        formatted += p1 #escribir el caracter actual

        #insertar . solo si p1 cierra una subexpresion y p2 abre otra
        if i + 1 < len(expresion):
            p2 = expresion[i + 1]

            #cierran: operando, ')' y los unarios postfijos
            cierra = p1 == ')' or p1 in operadoresUnarios or (p1 != '(' and p1 not in operadoresBinarios)
            #abren: operando y '('
            abre = p2 == '(' or (p2 != ')' and p2 not in operadores)

            if cierra and abre:
                formatted += '.'

    return formatted


def precedence(p):
    #jerarquia de precedencia de los operadores
    precedences = {
        '(': 1,
        '|': 2,
        '.': 3,
        '^': 4,   #binario: debe quedar por debajo de los unarios postfijos
        '?': 5,
        '*': 5,
        '+': 5,
    }

    #los operandos ya no pasan por aqui, cualquier otra cosa es precedencia minima
    return precedences.get(p, 0)

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
            if not stack:
                raise ValueError("paréntesis ')' sin '(' que lo abra")
            stack.pop()  # quitar el '('
        elif char in operadores:
            while stack and stack[-1] != '(' and precedence(stack[-1]) >= precedence(char):
                postfix += stack.pop()

            stack.append(char)
        else:
            postfix += char  #los operandos van directo a la salida

    while stack:
        op = stack.pop()
        if op == '(':
            raise ValueError("paréntesis '(' sin cerrar")
        postfix += op

    return postfix

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                expresion = line.strip() #limpiar espacios en blanco al inicio y al final de la línea

                if not expresion:
                    continue
                try:
                    print (f"Expresión: {expresion:<20} - Formateada(infix): {format(expresion):<20} - Postfix: {infix_to_postfix(expresion)}")
                    
                except ValueError as e:
                    print(f"Expresión inválida '{expresion}': {e}")

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
        