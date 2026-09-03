
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


#---Minimización

def _alcanzables(afd):
    #estados a los que se llega desde el inicial
    vistos = {afd.inicio}
    cola = deque(vistos)

    while cola:
        actual = cola.popleft()
        for simbolo in afd.simbolos:
            destino = afd.destino(actual, simbolo)
            if destino is not None and destino not in vistos:
                vistos.add(destino)
                cola.append(destino)

    return vistos


def _productivos(afd):
    #estados desde los que todavia se puede llegar a una aceptacion
    entrantes = {}
    for origen, _, destino in afd.pares():
        entrantes.setdefault(destino, set()).add(origen)

    vistos = set(afd.aceptaciones)
    cola = deque(vistos)

    while cola:
        for origen in entrantes.get(cola.popleft(), ()):
            if origen not in vistos:
                vistos.add(origen)
                cola.append(origen)

    return vistos


def _restringir(afd, conservados):
    transiciones = {(origen, simbolo): destino
                    for (origen, simbolo), destino in afd.transiciones.items()
                    if origen in conservados and destino in conservados}
    subconjuntos = {estado: origenes
                    for estado, origenes in afd.subconjuntos.items()
                    if estado in conservados}
    return AFD(afd.inicio, afd.aceptaciones & set(conservados), transiciones,
               afd.alfabeto, subconjuntos)


def _renumerar(afd):
    #deja los estados en 0..n-1 siguiendo un BFS desde el inicial
    orden = [afd.inicio]
    cola = deque(orden)

    while cola:
        actual = cola.popleft()
        for simbolo in afd.simbolos:
            destino = afd.destino(actual, simbolo)
            if destino is not None and destino not in orden:
                orden.append(destino)
                cola.append(destino)

    nuevo = {estado: i for i, estado in enumerate(orden)}
    transiciones = {(nuevo[origen], simbolo): nuevo[destino]
                    for (origen, simbolo), destino in afd.transiciones.items()
                    if origen in nuevo and destino in nuevo}
    subconjuntos = {nuevo[estado]: origenes
                    for estado, origenes in afd.subconjuntos.items()
                    if estado in nuevo}

    return AFD(0, {nuevo[estado] for estado in afd.aceptaciones if estado in nuevo},
               transiciones, afd.alfabeto, subconjuntos)


def completar(afd):
    #para particionar hace falta que exista toda transicion: las que faltan van a
    #un sumidero que no acepta nada
    if afd.completo:
        return afd

    estados = afd.estados
    sumidero = max(estados) + 1
    transiciones = dict(afd.transiciones)

    for estado in estados + [sumidero]:
        for simbolo in afd.simbolos:
            transiciones.setdefault((estado, simbolo), sumidero)

    return AFD(afd.inicio, afd.aceptaciones, transiciones, afd.alfabeto,
               afd.subconjuntos)


def _particiones(afd):
    #Moore: se parte en aceptacion / no aceptacion y se refina mientras algun
    #bloque tenga estados que con el mismo simbolo caen en bloques distintos
    aceptan = frozenset(estado for estado in afd.estados if afd.es_aceptacion(estado))
    resto = frozenset(estado for estado in afd.estados if estado not in aceptan)
    particion = [bloque for bloque in (aceptan, resto) if bloque]

    while True:
        bloque_de = {estado: i for i, bloque in enumerate(particion)
                     for estado in bloque}
        nueva = []

        for bloque in particion:
            grupos = {}
            for estado in sorted(bloque):
                firma = tuple(bloque_de[afd.destino(estado, simbolo)]
                              for simbolo in afd.simbolos)
                grupos.setdefault(firma, []).append(estado)
            nueva += [frozenset(grupo) for grupo in grupos.values()]

        if len(nueva) == len(particion):
            return nueva
        particion = nueva


def minimizar(afd):
    #cada bloque de estados equivalentes queda como un solo estado; al final se
    #quitan los estados muertos (el sumidero entre ellos) y se renumera
    total = completar(_restringir(afd, _alcanzables(afd)))
    particion = _particiones(total)

    bloque_de = {estado: i for i, bloque in enumerate(particion) for estado in bloque}
    transiciones = {}
    aceptaciones = set()
    bloques = {}

    for i, bloque in enumerate(particion):
        representante = min(bloque)
        for simbolo in total.simbolos:
            transiciones[(i, simbolo)] = bloque_de[total.destino(representante, simbolo)]
        if total.es_aceptacion(representante):
            aceptaciones.add(i)
        bloques[i] = frozenset(bloque)

    minimo = AFD(bloque_de[total.inicio], aceptaciones, transiciones,
                 total.alfabeto, bloques)

    vivos = _productivos(minimo)
    if minimo.inicio not in vivos:
        #el lenguaje es vacio: queda solo el estado inicial, sin transiciones
        return AFD(0, set(), {}, minimo.alfabeto,
                   {0: minimo.subconjuntos[minimo.inicio]})

    return _renumerar(_restringir(minimo, vivos))


def minimo_de_expresion(expresion, expandir=True):
    #expresion -> AFN -> AFD -> AFD minimo
    postfix, automata = afd_de_expresion(expresion, expandir)
    return postfix, minimizar(automata)
