
import os

import svgling
from svgling.core import EdgeStyle

from shuntingyard import (operadoresUnarios, operadoresBinarios, desproteger,
                          format, procesar_protegido)

EPSILON = 'ε'
CONCATENACION = '·'

FUENTE = "font-family: Consolas, monospace;"

COLOR_OPERADOR = "#d81d1d"
COLOR_OPERANDO = "#8f9e05"
COLOR_EPSILON = "#15803d"

COLOR_LINEA = "#0d59c4"
GROSOR_LINEA = 1.5


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


#Dibujo del AST

def color_de(nodo):
    if nodo.simbolo == EPSILON:
        return COLOR_EPSILON
    if not nodo.es_hoja:
        return COLOR_OPERADOR
    return COLOR_OPERANDO


def simbolo_de(nodo):
    #el '.' de la concatenacion se pinta como '·': un punto en la linea base se
    #pierde entre las aristas. el '\.' literal no cambia
    return CONCATENACION if nodo.simbolo == '.' else nodo.simbolo


def a_tupla(nodo):
    #svgling recibe el arbol como tuplas anidadas: (simbolo, hijo, hijo)
    if nodo.es_hoja:
        return simbolo_de(nodo)
    return tuple([simbolo_de(nodo)] + [a_tupla(hijo) for hijo in nodo.hijos])


def dibujar(raiz):
    dibujo = svgling.draw_tree(a_tupla(raiz), font_size=26)

    def pintar_nodos(nodo, ruta):
        #la ruta de un nodo son los indices que hay que seguir desde la raiz.
        #el estilo se fija completo en cada nodo: set_node_style() reemplaza el
        #del nodo, no lo mezcla, y los hijos heredarian la negrita del padre
        peso = "normal" if nodo.es_hoja else "bold"
        dibujo.set_node_style(ruta, text_color=color_de(nodo),
                              font_style=f"{FUENTE} font-weight: {peso};")
        for i, hijo in enumerate(nodo.hijos):
            pintar_nodos(hijo, ruta + (i,))

    def pintar_aristas(nodo, ruta):
        #cada arista se identifica por la ruta del hijo al que baja
        for i, hijo in enumerate(nodo.hijos):
            dibujo.set_edge_style(ruta + (i,),
                                  EdgeStyle(stroke=COLOR_LINEA,
                                            stroke_width=GROSOR_LINEA))
            pintar_aristas(hijo, ruta + (i,))

    #las aristas van al final: set_node_style() rehace el layout y las descolora
    pintar_nodos(raiz, ())
    pintar_aristas(raiz, ())
    return dibujo


#---entrada del programa

def graficar_archivo(filename, expandir=True, carpeta_salida="ast"):
    #lee el archivo, arma un AST por linea y guarda un svg por expresion
    arboles = []

    try:
        with open(filename, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                expresion = linea.strip()
                if not expresion:
                    continue
                try:
                    postfix, raiz = arbol_de(expresion, expandir)
                    arboles.append((expresion, raiz))
                    print(f"Expresión: {expresion:<20} - Formateada(infix): "
                          f"{format(expresion):<20} - Postfix: {postfix}")
                except ValueError as error:
                    print(f"Expresión inválida '{expresion}': {error}")
    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")
        return

    if not arboles:
        return

    os.makedirs(carpeta_salida, exist_ok=True)

    for n, (expresion, raiz) in enumerate(arboles, 1):
        ruta = os.path.join(carpeta_salida, f"ast_{n}.svg")
        dibujar(raiz).saveas(ruta)
        print(f"  {n}. {expresion}  ->  {ruta}")

    print(f"\n{len(arboles)} árboles guardados en: {os.path.abspath(carpeta_salida)}")
