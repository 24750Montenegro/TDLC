
import svgling
from svgling.core import EdgeStyle

from .tokens import EPSILON

#el '.' de la concatenacion se pinta como '·', un punto se pierde entre las aristas
CONCATENACION = '·'

FUENTE = "font-family: Consolas, monospace;"

COLOR_OPERADOR = "#d81d1d"
COLOR_OPERANDO = "#8f9e05"
COLOR_EPSILON = "#15803d"
COLOR_LINEA = "#0d59c4"
GROSOR_LINEA = 1.5


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

