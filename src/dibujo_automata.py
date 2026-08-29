
import os
import shutil

from graphviz import Digraph

from .automata import texto

#Consolas no existe fuera de Windows; en el contenedor se cambia con AFN_FUENTE
FUENTE_GRAFO = os.environ.get("AFN_FUENTE", "Consolas")

FLECHA_INICIAL = "__inicio__"

COLOR_ESTADO = "#334155"
COLOR_LINEA = "#0d59c4"
COLOR_INICIAL = COLOR_LINEA
COLOR_EPSILON = "#15803d"
COLOR_ACEPTACION = COLOR_EPSILON
COLOR_SIMBOLO = "#8f9e05"
COLOR_TITULO = "#d81d1d"


def _asegurar_dot():
    #el instalador de Graphviz en Windows no siempre deja dot en el PATH
    if shutil.which('dot'):
        return
    for carpeta in (r"C:\Program Files\Graphviz\bin",
                    r"C:\Program Files (x86)\Graphviz\bin"):
        if os.path.isfile(os.path.join(carpeta, 'dot.exe')):
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + carpeta
            return


def dibujar(automata, titulo=None, etiquetas=None):
    #graphviz solo necesita los nodos y las aristas, el acomodo lo resuelve dot;
    #sirve igual para el AFN y para el AFD
    grafo = Digraph(type(automata).__name__, format='svg')
    grafo.attr(rankdir='LR', bgcolor='white', fontname=FUENTE_GRAFO,
               labelloc='t', fontsize='16', fontcolor=COLOR_TITULO)
    if titulo:
        grafo.attr(label=titulo)

    grafo.attr('node', fontname=FUENTE_GRAFO, fontsize='14', shape='circle',
               color=COLOR_ESTADO, fontcolor=COLOR_ESTADO, penwidth='1.4')
    grafo.attr('edge', fontname=FUENTE_GRAFO, fontsize='13', color=COLOR_LINEA,
               arrowsize='0.7')

    grafo.node(FLECHA_INICIAL, shape='none', label='')
    for estado in automata.estados:
        nombre = (etiquetas or {}).get(estado, str(estado))
        if automata.es_aceptacion(estado):
            grafo.node(str(estado), label=nombre, shape='doublecircle',
                       color=COLOR_ACEPTACION, fontcolor=COLOR_ACEPTACION)
        elif estado == automata.inicio:
            grafo.node(str(estado), label=nombre,
                       color=COLOR_INICIAL, fontcolor=COLOR_INICIAL)
        else:
            grafo.node(str(estado), label=nombre)

    grafo.edge(FLECHA_INICIAL, str(automata.inicio), color=COLOR_INICIAL)

    #las aristas paralelas se juntan en una sola con las etiquetas separadas por coma
    simbolos_de = {}
    for origen, simbolo, destino in automata.pares():
        simbolos_de.setdefault((origen, destino), set()).add(simbolo)

    for (origen, destino), simbolos in sorted(simbolos_de.items()):
        vacia = simbolos == {None}
        etiqueta = ','.join(texto(s) for s in
                            sorted(simbolos, key=lambda s: (s is None, s or '')))
        grafo.edge(str(origen), str(destino), label=f" {etiqueta} ",
                   fontcolor=COLOR_EPSILON if vacia else COLOR_SIMBOLO,
                   color=COLOR_EPSILON if vacia else COLOR_LINEA,
                   style='dashed' if vacia else 'solid')

    return grafo


def guardar(automata, ruta_base, titulo=None, abrir=False, etiquetas=None):
    _asegurar_dot()
    return dibujar(automata, titulo, etiquetas).render(ruta_base, cleanup=True,
                                                       view=abrir)
