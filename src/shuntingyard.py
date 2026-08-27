
from .parseo import desproteger, insertar_concatenacion, preparar
from .tokens import abren, cierran, operadores, precedence


def procesar_protegido(expresion):
    #devuelve (postfix con los literales aun protegidos, literales, pasos);
    #cada paso es (token, pila, salida). El postfix protegido tiene un caracter
    #por token, que es lo que necesita el constructor del AST
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

    return postfix, literales, pasos


def procesar(expresion):
    #devuelve (postfix legible, pasos)
    postfix, literales, pasos = procesar_protegido(expresion)
    return desproteger(postfix, literales), pasos


def infix_to_postfix(expresion):
    return procesar(expresion)[0]
