
from .tokens import (ESCAPE, abren, cierran, literalesEnClase, operadores,
                     operadoresBinarios, operadoresUnarios)


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

        if c == ESCAPE:
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
    return ''.join(ESCAPE + literales[c] if c in literales else c for c in cadena)


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
    #con concatenaciones explicitas, se valida por pares
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
