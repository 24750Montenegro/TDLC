
from .parseo import desproteger
from .shuntingyard import procesar_protegido
from .tokens import EPSILON, operadoresBinarios, operadoresUnarios


class Nodo:
    #las hojas son operandos (sin hijos), los unarios tienen solo izquierda y
    #los binarios tienen los dos
    def __init__(self, simbolo, izquierda=None, derecha=None):
        self.simbolo = simbolo
        self.izquierda = izquierda
        self.derecha = derecha

    @property
    def hijos(self):
        return [h for h in (self.izquierda, self.derecha) if h is not None]

    @property
    def es_hoja(self):
        return not self.hijos

    def clonar(self):
        #copia profunda, la necesita la expansion de a+ como a.a*
        return Nodo(self.simbolo,
                    self.izquierda.clonar() if self.izquierda else None,
                    self.derecha.clonar() if self.derecha else None)

    def postorden(self):
        #el postfix del arbol, sirve para comprobar la construccion
        return ''.join(h.postorden() for h in self.hijos) + self.simbolo

    def __repr__(self):
        return f"Nodo({self.simbolo!r})"


def etiqueta(caracter, literales):
    #los caracteres escapados viajan protegidos, se muestran como '\x'
    return '\\' + literales[caracter] if caracter in literales else caracter


def construir(postfix, literales=None, expandir=True):
    #recorre el postfix con una pila
    literales = literales or {}
    pila = []

    for caracter in postfix:
        if caracter in operadoresBinarios:
            if len(pila) < 2:
                raise ValueError(f"el operador '{caracter}' no tiene dos operandos")
            derecha = pila.pop()
            izquierda = pila.pop()
            pila.append(Nodo(caracter, izquierda, derecha))

        elif caracter in operadoresUnarios:
            if not pila:
                raise ValueError(f"el operador '{caracter}' no tiene operando")
            hijo = pila.pop()

            if expandir and caracter == '+':
                pila.append(Nodo('.', hijo, Nodo('*', hijo.clonar())))
            elif expandir and caracter == '?':
                pila.append(Nodo('|', hijo, Nodo(EPSILON)))
            else:
                pila.append(Nodo(caracter, hijo))

        else:
            pila.append(Nodo(etiqueta(caracter, literales)))

    if len(pila) != 1:
        raise ValueError("postfix mal formado: quedaron operandos sin unir")

    return pila[0]


def arbol_de(expresion, expandir=True):
    #expresion infix -> postfix -> AST
    postfix, literales, _ = procesar_protegido(expresion)
    return desproteger(postfix, literales), construir(postfix, literales, expandir)

