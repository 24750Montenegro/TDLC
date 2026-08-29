
from .tokens import EPSILON


class Automata:
    #base de AFN y AFD: transiciones {(estado, simbolo): destino(s)}, simbolo None
    #para epsilon. Las subclases dicen como se leen esas transiciones
    def __init__(self, inicio, aceptaciones, transiciones, alfabeto):
        self.inicio = inicio
        self.aceptaciones = frozenset(aceptaciones)
        self.transiciones = transiciones
        self.alfabeto = set(alfabeto)

    def pares(self):
        #(origen, simbolo, destino) de cada transicion
        raise NotImplementedError

    def destinos(self, estado, simbolo):
        raise NotImplementedError

    @property
    def estados(self):
        estados = set(self.aceptaciones) | {self.inicio}
        for origen, _, destino in self.pares():
            estados.add(origen)
            estados.add(destino)
        return sorted(estados)

    @property
    def simbolos(self):
        return sorted(self.alfabeto)

    def es_aceptacion(self, estado):
        return estado in self.aceptaciones

    def salidas(self, estado):
        #(simbolo, destino) ordenadas, con las epsilon al final
        pares = [(simbolo, destino) for origen, simbolo, destino in self.pares()
                 if origen == estado]
        return sorted(pares, key=lambda par: (par[0] is None, par[0] or '', par[1]))

    def __repr__(self):
        return (f"{type(self).__name__}(estados={len(self.estados)}, "
                f"inicio={self.inicio}, "
                f"aceptacion={sorted(self.aceptaciones)})")


def texto(simbolo):
    #el None de las transiciones vacias se muestra como epsilon
    return EPSILON if simbolo is None else simbolo
