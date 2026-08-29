
from collections import deque

from .arbol import arbol_de
from .automata import Automata
from .tokens import EPSILON


class AFN(Automata):
    #transiciones: {(estado, simbolo): {estados}}, con simbolo None para epsilon
    def __init__(self, inicio, aceptacion, transiciones, alfabeto):
        super().__init__(inicio, {aceptacion}, transiciones, alfabeto)

    @property
    def aceptacion(self):
        #Thompson deja siempre un unico estado de aceptacion
        return next(iter(self.aceptaciones))

    def pares(self):
        return [(origen, simbolo, destino)
                for (origen, simbolo), destinos in self.transiciones.items()
                for destino in destinos]

    def destinos(self, estado, simbolo):
        return self.transiciones.get((estado, simbolo), frozenset())

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

