
#los simbolos del lenguaje, en un solo lugar: los usan el parseo, el shunting
#yard, el balanceo y los automatas

EPSILON = 'ε'
ESCAPE = '\\'

operadoresUnarios = ['?', '*', '+']
operadoresBinarios = ['|', '.', '^']
operadores = operadoresUnarios + operadoresBinarios

#los que agrupan en una expresion regular
abren = ['(', '[']
cierran = [')', ']']

#todos los pares que se balancean; las llaves solo son simbolos del alfabeto
#para el shunting yard, pero el verificador del ejercicio 2 si las cuenta
PARES = {'(': ')', '[': ']', '{': '}'}
PARES_CIERRE = {cierre: apertura for apertura, cierre in PARES.items()}
APERTURA = set(PARES)
CIERRE = set(PARES_CIERRE)

#dentro de una clase todo es literal salvo el ']' que la cierra y el '\' que escapa
literalesEnClase = operadores + abren + [')']

PRECEDENCIAS = {
    '(': 1,
    '[': 1,
    '|': 2,
    '.': 3,
    '^': 4,   #binario, va debajo de los unarios postfijos
    '?': 5,
    '*': 5,
    '+': 5,
}


def precedence(p):
    return PRECEDENCIAS.get(p, 0)
