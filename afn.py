
import os
import shutil
import textwrap
from collections import deque

from graphviz import Digraph, ExecutableNotFound

from arbol import (EPSILON, arbol_de, COLOR_EPSILON, COLOR_OPERANDO,
                   COLOR_OPERADOR, COLOR_LINEA)

#Consolas no existe fuera de Windows; en el contenedor se cambia con AFN_FUENTE
FUENTE_GRAFO = os.environ.get("AFN_FUENTE", "Consolas")
FLECHA_INICIAL = "__inicio__"

COLOR_ESTADO = "#334155"
COLOR_INICIAL = COLOR_LINEA
COLOR_ACEPTACION = COLOR_EPSILON
COLOR_SIMBOLO = COLOR_OPERANDO
COLOR_TITULO = COLOR_OPERADOR


class AFN:
    #transiciones: {(estado, simbolo): {estados}}, con simbolo None para epsilon
    def __init__(self, inicio, aceptacion, transiciones, alfabeto):
        self.inicio = inicio
        self.aceptacion = aceptacion
        self.transiciones = transiciones
        self.alfabeto = alfabeto

    @property
    def estados(self):
        estados = {self.inicio, self.aceptacion}
        for (origen, _), destinos in self.transiciones.items():
            estados.add(origen)
            estados.update(destinos)
        return sorted(estados)

    def destinos(self, estado, simbolo):
        return self.transiciones.get((estado, simbolo), frozenset())

    def salidas(self, estado):
        #(simbolo, destino) ordenadas, con las epsilon al final
        pares = []
        for (origen, simbolo), destinos in self.transiciones.items():
            if origen == estado:
                pares += [(simbolo, destino) for destino in destinos]
        return sorted(pares, key=lambda par: (par[0] is None, par[0] or '', par[1]))

    def __repr__(self):
        return (f"AFN(estados={len(self.estados)}, inicio={self.inicio}, "
                f"aceptacion={self.aceptacion})")


class _Fabrica:
    #numera los estados y acumula las transiciones mientras se sube por el AST
    def __init__(self):
        self.contador = 0
        self.transiciones = {}
        self.alfabeto = set()

    def estado(self):
        self.contador += 1
        return self.contador - 1

    def par(self):
        return self.estado(), self.estado()

    def conectar(self, origen, simbolo, destino):
        self.transiciones.setdefault((origen, simbolo), set()).add(destino)


def literal_de(etiqueta):
    #las hojas escapadas llegan como '\x'; el simbolo que consume el AFN es 'x'
    return etiqueta[1] if len(etiqueta) == 2 and etiqueta[0] == '\\' else etiqueta


def _fragmento(nodo, fabrica):
    #cada fragmento devuelve (inicio, aceptacion) y nunca reusa esos dos estados
    if nodo.es_hoja:
        inicio, aceptacion = fabrica.par()
        simbolo = None if nodo.simbolo == EPSILON else literal_de(nodo.simbolo)
        if simbolo is not None:
            fabrica.alfabeto.add(simbolo)
        fabrica.conectar(inicio, simbolo, aceptacion)
        return inicio, aceptacion

    operador = nodo.simbolo

    if operador == '.':
        inicio, medio = _fragmento(nodo.izquierda, fabrica)
        entrada, aceptacion = _fragmento(nodo.derecha, fabrica)
        fabrica.conectar(medio, None, entrada)
        return inicio, aceptacion

    if operador == '|':
        arriba, fin_arriba = _fragmento(nodo.izquierda, fabrica)
        abajo, fin_abajo = _fragmento(nodo.derecha, fabrica)
        inicio, aceptacion = fabrica.par()
        fabrica.conectar(inicio, None, arriba)
        fabrica.conectar(inicio, None, abajo)
        fabrica.conectar(fin_arriba, None, aceptacion)
        fabrica.conectar(fin_abajo, None, aceptacion)
        return inicio, aceptacion

    if operador in ('*', '+', '?'):
        entrada, salida = _fragmento(nodo.izquierda, fabrica)
        inicio, aceptacion = fabrica.par()
        fabrica.conectar(inicio, None, entrada)
        fabrica.conectar(salida, None, aceptacion)
        if operador in ('*', '+'):
            fabrica.conectar(salida, None, entrada)
        if operador in ('*', '?'):
            fabrica.conectar(inicio, None, aceptacion)
        return inicio, aceptacion

    raise ValueError(f"el operador '{operador}' no tiene construcción de Thompson")


def _renumerar(afn):
    #Thompson numera de abajo hacia arriba, asi que el inicial no queda en 0;
    #un BFS desde el inicial reordena, y la aceptacion se manda al final para que
    #el AFN quede numerado de 0 (inicial) a n-1 (aceptacion)
    adyacentes = {}
    for (origen, _), destinos in afn.transiciones.items():
        adyacentes.setdefault(origen, set()).update(destinos)

    orden = [afn.inicio]
    cola = deque(orden)
    while cola:
        for destino in sorted(adyacentes.get(cola.popleft(), ())):
            if destino not in orden:
                orden.append(destino)
                cola.append(destino)

    orden += [estado for estado in afn.estados if estado not in orden]
    orden.append(orden.pop(orden.index(afn.aceptacion)))
    nuevo = {estado: i for i, estado in enumerate(orden)}

    transiciones = {(nuevo[origen], simbolo): {nuevo[d] for d in destinos}
                    for (origen, simbolo), destinos in afn.transiciones.items()}

    return AFN(nuevo[afn.inicio], nuevo[afn.aceptacion], transiciones, afn.alfabeto)


def afn_de(expresion, expandir=True):
    #expresion infix -> postfix -> AST -> AFN de Thompson
    postfix, raiz = arbol_de(expresion, expandir)
    fabrica = _Fabrica()
    inicio, aceptacion = _fragmento(raiz, fabrica)
    return postfix, _renumerar(AFN(inicio, aceptacion,
                                   fabrica.transiciones, fabrica.alfabeto))


#---Simulación del AFN

def cerradura_epsilon(afn, estados):
    #todos los estados alcanzables sin consumir nada
    cerrada = set(estados)
    pila = list(estados)
    while pila:
        for destino in afn.destinos(pila.pop(), None):
            if destino not in cerrada:
                cerrada.add(destino)
                pila.append(destino)
    return cerrada


def mover(afn, estados, simbolo):
    destinos = set()
    for estado in estados:
        destinos |= afn.destinos(estado, simbolo)
    return destinos


def simular(afn, w):
    #devuelve (acepta, pasos); cada paso es (simbolo consumido, estados actuales)
    actuales = cerradura_epsilon(afn, {afn.inicio})
    pasos = [('', sorted(actuales))]

    for simbolo in w:
        actuales = cerradura_epsilon(afn, mover(afn, actuales, simbolo))
        pasos.append((simbolo, sorted(actuales)))
        if not actuales:
            break

    return afn.aceptacion in actuales, pasos


def acepta(expresion, w, expandir=True):
    return simular(afn_de(expresion, expandir)[1], w)[0]


#---Dibujo del AFN

def _asegurar_dot():
    #el instalador de Graphviz en Windows no siempre deja dot en el PATH
    if shutil.which('dot'):
        return
    for carpeta in (r"C:\Program Files\Graphviz\bin",
                    r"C:\Program Files (x86)\Graphviz\bin"):
        if os.path.isfile(os.path.join(carpeta, 'dot.exe')):
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + carpeta
            return


def _texto(simbolo):
    return EPSILON if simbolo is None else simbolo


def dibujar(afn, titulo=None):
    #graphviz solo necesita los nodos y las aristas, el acomodo lo resuelve dot
    grafo = Digraph('AFN', format='svg')
    grafo.attr(rankdir='LR', bgcolor='white', fontname=FUENTE_GRAFO,
               labelloc='t', fontsize='16', fontcolor=COLOR_TITULO)
    if titulo:
        grafo.attr(label=titulo)

    grafo.attr('node', fontname=FUENTE_GRAFO, fontsize='14', shape='circle',
               color=COLOR_ESTADO, fontcolor=COLOR_ESTADO, penwidth='1.4')
    grafo.attr('edge', fontname=FUENTE_GRAFO, fontsize='13', color=COLOR_LINEA,
               arrowsize='0.7')

    grafo.node(FLECHA_INICIAL, shape='none', label='')
    for estado in afn.estados:
        if estado == afn.aceptacion:
            grafo.node(str(estado), shape='doublecircle',
                       color=COLOR_ACEPTACION, fontcolor=COLOR_ACEPTACION)
        elif estado == afn.inicio:
            grafo.node(str(estado), color=COLOR_INICIAL, fontcolor=COLOR_INICIAL)
        else:
            grafo.node(str(estado))

    grafo.edge(FLECHA_INICIAL, str(afn.inicio), color=COLOR_INICIAL)

    #las aristas paralelas se juntan en una sola con las etiquetas separadas por coma
    etiquetas = {}
    for (origen, simbolo), destinos in afn.transiciones.items():
        for destino in destinos:
            etiquetas.setdefault((origen, destino), set()).add(simbolo)

    for (origen, destino), simbolos in sorted(etiquetas.items()):
        vacia = simbolos == {None}
        texto = ','.join(_texto(s) for s in
                         sorted(simbolos, key=lambda s: (s is None, s or '')))
        grafo.edge(str(origen), str(destino), label=f" {texto} ",
                   fontcolor=COLOR_EPSILON if vacia else COLOR_SIMBOLO,
                   color=COLOR_EPSILON if vacia else COLOR_LINEA,
                   style='dashed' if vacia else 'solid')

    return grafo


def guardar(afn, ruta_base, titulo=None, abrir=False):
    _asegurar_dot()
    return dibujar(afn, titulo).render(ruta_base, cleanup=True, view=abrir)


#---entrada del programa

def _resumen(afn):
    estados = afn.estados
    return (f"  Estados: {len(estados)} (0..{estados[-1]})   "
            f"Inicial: {afn.inicio}   Aceptación: {afn.aceptacion}   "
            f"Alfabeto: {{{', '.join(sorted(afn.alfabeto))}}}")


def _transiciones_texto(afn):
    partes = [f"{origen}-{_texto(simbolo)}->{destino}"
              for origen in afn.estados
              for simbolo, destino in afn.salidas(origen)]
    return textwrap.fill(' '.join(partes), width=100,
                         initial_indent="  Transiciones: ",
                         subsequent_indent=" " * 16)


def _traza_texto(pasos):
    lineas = []
    for simbolo, estados in pasos:
        etiqueta = "inicio" if not simbolo else f"lee '{simbolo}'"
        conjunto = '{' + ', '.join(str(estado) for estado in estados) + '}'
        lineas.append(textwrap.fill(f"    {etiqueta:<9} -> {conjunto}", width=100,
                                    subsequent_indent=" " * 17))
    return '\n'.join(lineas)


def procesar_archivo(filename, w, carpeta_salida="afn", abrir=False,
                     expandir=True, detalle=True):
    #una linea del archivo es una r: se construye su AFN, se dibuja y se simula con w
    try:
        with open(filename, 'r', encoding='utf-8') as archivo:
            expresiones = [linea.strip() for linea in archivo]
    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")
        return

    os.makedirs(carpeta_salida, exist_ok=True)
    generados = 0

    for expresion in expresiones:
        if not expresion:
            continue

        try:
            postfix, automata = afn_de(expresion, expandir)
        except ValueError as error:
            print(f"Expresión inválida '{expresion}': {error}\n")
            continue

        generados += 1
        aceptada, pasos = simular(automata, w)
        veredicto = "sí" if aceptada else "no"

        print(f"r = {expresion:<24} Postfix: {postfix}")
        print(_resumen(automata))
        if detalle:
            print(_transiciones_texto(automata))
            print(f"  Simulación con w = \"{w}\":")
            print(_traza_texto(pasos))

        titulo = f"r = {expresion}    w = \"{w}\"    w pertenece a L(r): {veredicto}"
        ruta = os.path.join(carpeta_salida, f"afn_{generados}")

        try:
            archivo_svg = guardar(automata, ruta, titulo=titulo, abrir=abrir)
            print(f"  Imagen: {archivo_svg}")
        except ExecutableNotFound:
            print("  Imagen: no se generó, falta el binario de Graphviz "
                  "(instálelo con: winget install Graphviz.Graphviz)")

        print(f"  ¿w = \"{w}\" pertenece a L(r)?  ->  {veredicto.upper()}\n")

    if generados:
        print(f"{generados} AFN generados en: {os.path.abspath(carpeta_salida)}")
