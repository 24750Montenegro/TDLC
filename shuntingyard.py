operadoresUnarios = ['?', '*', '+']
operadoresBinarios = ['|', '.', '^']
operadores = operadoresUnarios + operadoresBinarios

abren = ['(', '[']
cierran = [')', ']']

#dentro de una clase todo es literal salvo el ']' que la cierra y el '\' que escapa
literalesEnClase = operadores + abren + [')']


def proteger_escapes(expresion):
    #los \x, los . y los operadores dentro de [ ] se guardan como caracteres del area
    #de uso privado de unicode, asi el resto del algoritmo los trata como operandos y
    #el unico '.' operador es el que inserta insertar_concatenacion()
    protegida = ""
    literales = {}
    dentro_clase = False
    i = 0

    while i < len(expresion):
        c = expresion[i]

        if c == '\\':
            if i + 1 >= len(expresion):
                raise ValueError("'\\' al final de la expresión, no escapa ningún caracter")
            literal = expresion[i + 1]
            salto = 2
        elif c == '.' or (dentro_clase and c in literalesEnClase):
            literal = c
            salto = 1
        else:
            if c == '[':
                dentro_clase = True
            elif c == ']':
                dentro_clase = False
            protegida += c
            i += 1
            continue

        marca = chr(0xE000 + len(literales))
        literales[marca] = literal
        protegida += marca
        i += salto

    return protegida, literales


def desproteger(cadena, literales):
    return ''.join('\\' + literales[c] if c in literales else c for c in cadena)


def preparar(expresion):
    protegida, literales = proteger_escapes(expresion)
    return ''.join(protegida.split()), literales


def insertar_concatenacion(expresion):
    formatted = ""
    dentro_clase = False

    for i in range(len(expresion)):
        p1 = expresion[i]
        formatted += p1

        if p1 == '[':
            dentro_clase = True
        elif p1 == ']':
            dentro_clase = False

        if i + 1 >= len(expresion):
            continue

        p2 = expresion[i + 1]

        #dentro de [ ] los simbolos se unen con | : [ae03] es (a|e|0|3)
        if dentro_clase:
            if p1 != '[' and p2 != ']':
                formatted += '|'
            continue

        #p1 cierra una subexpresion (operando, ')', ']' o unario) y p2 abre otra
        cierra = p1 in cierran or p1 in operadoresUnarios or (p1 not in abren and p1 not in operadoresBinarios)
        abre = p2 in abren or (p2 not in cierran and p2 not in operadores)

        if cierra and abre:
            formatted += '.'

    return validar(formatted)


def validar(formatted):
    #con con concatenaciones explicitas, se valida por pares
    if not formatted:
        raise ValueError("expresión vacía")

    if formatted[0] in operadores:
        raise ValueError(f"el operador '{formatted[0]}' no tiene operando a la izquierda")

    if formatted[-1] in operadoresBinarios:
        raise ValueError(f"el operador '{formatted[-1]}' no tiene operando a la derecha")

    for i in range(len(formatted) - 1):
        p1 = formatted[i]
        p2 = formatted[i + 1]

        if p1 in operadoresBinarios or p1 in abren:
            if p2 in operadores:
                raise ValueError(f"el operador '{p2}' no tiene operando a la izquierda")
            if p2 in cierran:
                if p1 not in abren:
                    raise ValueError(f"el operador '{p1}' no tiene operando a la derecha")
                if cierran[abren.index(p1)] != p2:
                    raise ValueError(f"'{p1}' no cierra con '{p2}'")
                if p1 == '(':
                    raise ValueError("subexpresión vacía '()'")
                raise ValueError("clase de caracteres vacía '[]'")

    return formatted


def format(expresion):
    protegida, literales = preparar(expresion)
    return desproteger(insertar_concatenacion(protegida), literales)


def precedence(p):
    precedences = {
        '(': 1,
        '[': 1,
        '|': 2,
        '.': 3,
        '^': 4,   #binario, va debajo de los unarios postfijos
        '?': 5,
        '*': 5,
        '+': 5,
    }

    return precedences.get(p, 0)


def procesar(expresion):
    #devuelve (postfix, pasos); cada paso es (token, pila, salida)
    postfix = ""
    stack = []
    pasos = []
    protegida, literales = preparar(expresion)
    formatted = insertar_concatenacion(protegida)

    def anotar(token):
        pasos.append((desproteger(token, literales), ''.join(stack),
                      desproteger(postfix, literales)))

    for char in formatted:
        if char in abren:
            stack.append(char)
        elif char in cierran:
            apertura = abren[cierran.index(char)]
            while stack and stack[-1] != apertura:
                if stack[-1] in abren:
                    raise ValueError(f"'{stack[-1]}' sin cerrar antes de '{char}'")
                postfix += stack.pop()
            if not stack:
                raise ValueError(f"'{char}' sin '{apertura}' que lo abra")
            stack.pop()
        elif char in operadores:
            while stack and stack[-1] not in abren and precedence(stack[-1]) >= precedence(char):
                postfix += stack.pop()
            stack.append(char)
        else:
            postfix += char

        anotar(char)

    while stack:
        op = stack.pop()
        if op in abren:
            raise ValueError(f"'{op}' sin cerrar")
        postfix += op
        anotar(op)

    return desproteger(postfix, literales), pasos


def infix_to_postfix(expresion):
    return procesar(expresion)[0]


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
    while True:
        print("Menú:")
        print("1. Leer archivo")
        print("2. Leer archivo paso a paso")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion in ('1', '2'):
            filename = input("Ingrese el nombre del archivo: ")
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            read_file(filename, pasos=(opcion == '2'))

        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione 1, 2 o 3.")
