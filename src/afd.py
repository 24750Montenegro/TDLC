
from collections import deque

from .afn import afn_de, cerradura_epsilon, mover
from .automata import Automata


class AFD(Automata):
    #transiciones: {(estado, simbolo): estado}; sin epsilon y con un solo destino
    def __init__(self, inicio, aceptaciones, transiciones, alfabeto,
                 subconjuntos=None):
        super().__init__(inicio, aceptaciones, transiciones, alfabeto)
        #de que estados del automata anterior salio cada estado, para el reporte
        self.subconjuntos = subconjuntos or {}

    def pares(self):
        return [(origen, simbolo, destino)
                for (origen, simbolo), destino in self.transiciones.items()]

    def destino(self, estado, simbolo):
        return self.transiciones.get((estado, simbolo))

    def destinos(self, estado, simbolo):
        destino = self.destino(estado, simbolo)
        return frozenset() if destino is None else frozenset({destino})

    @property
    def completo(self):
        return all(self.destino(estado, simbolo) is not None
                   for estado in self.estados for simbolo in self.simbolos)

    def __repr__(self):
        return (f"AFD(estados={len(self.estados)}, inicio={self.inicio}, "
                f"aceptacion={sorted(self.aceptaciones)})")


#---Construcción por subconjuntos

def afd_de(afn):
    #cada estado del AFD es una cerradura epsilon del AFN; el BFS deja el
    #inicial en 0 y solo genera los subconjuntos alcanzables
    inicial = frozenset(cerradura_epsilon(afn, {afn.inicio}))
    subconjuntos = [inicial]
    indices = {inicial: 0}
    transiciones = {}
    cola = deque([inicial])

    while cola:
        actual = cola.popleft()
        for simbolo in sorted(afn.alfabeto):
            destino = frozenset(cerradura_epsilon(afn, mover(afn, actual, simbolo)))
            if not destino:
                continue
            if destino not in indices:
                indices[destino] = len(subconjuntos)
                subconjuntos.append(destino)
                cola.append(destino)
            transiciones[(indices[actual], simbolo)] = indices[destino]

    aceptaciones = {i for i, conjunto in enumerate(subconjuntos)
                    if afn.aceptacion in conjunto}

    return AFD(0, aceptaciones, transiciones, set(afn.alfabeto),
               dict(enumerate(subconjuntos)))


def afd_de_expresion(expresion, expandir=True):
    #expresion -> AFN de Thompson -> AFD por subconjuntos
    postfix, automata = afn_de(expresion, expandir)
    return postfix, afd_de(automata)


#---Simulación del AFD

def simular(afd, w):
    #devuelve (acepta, pasos); cada paso es (simbolo consumido, estado actual)
    actual = afd.inicio
    pasos = [('', actual)]

    for simbolo in w:
        actual = afd.destino(actual, simbolo)
        pasos.append((simbolo, actual))
        if actual is None:
            break

    return actual is not None and afd.es_aceptacion(actual), pasos


def acepta(expresion, w, expandir=True):
    return simular(afd_de_expresion(expresion, expandir)[1], w)[0]

