
import textwrap

from .automata import texto

ANCHO = 100


def resumen(automata):
    estados = automata.estados
    aceptacion = ', '.join(str(estado) for estado in sorted(automata.aceptaciones))
    return (f"  Estados: {len(estados)} (0..{estados[-1]})   "
            f"Inicial: {automata.inicio}   Aceptación: {{{aceptacion}}}   "
            f"Alfabeto: {{{', '.join(sorted(automata.alfabeto))}}}")


def transiciones_texto(automata):
    partes = [f"{origen}-{texto(simbolo)}->{destino}"
              for origen in automata.estados
              for simbolo, destino in automata.salidas(origen)]
    return textwrap.fill(' '.join(partes), width=ANCHO,
                         initial_indent="  Transiciones: ",
                         subsequent_indent=" " * 16)


def conjunto(estados):
    return '{' + ', '.join(str(estado) for estado in estados) + '}'


def traza_texto(pasos):
    #cada paso es (simbolo consumido, conjunto de estados actuales)
    lineas = []
    for simbolo, estados in pasos:
        etiqueta = "inicio" if not simbolo else f"lee '{simbolo}'"
        lineas.append(textwrap.fill(f"    {etiqueta:<9} -> {conjunto(estados)}",
                                    width=ANCHO, subsequent_indent=" " * 17))
    return '\n'.join(lineas)
