
import textwrap

from .automata import texto
from .balanceo import verificar_balanceo
from .parseo import format
from .shuntingyard import infix_to_postfix, procesar

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


def tabla_balanceo(expresion):
    #la traza de la pila del ejercicio 2: devuelve (balanceada, texto)
    esta_balanceada, motivo, pasos = verificar_balanceo(expresion)
    lineas = [f"Expresion: {expresion}",
              f"  {'#':>3}  {'Pos':>3}  {'Token':<6} {'Accion':<45} {'Pila'}"]

    for n, (pos, token, accion, pila) in enumerate(pasos, 1):
        lineas.append(f"  {n:>3}  {pos:>3}   {token:<6} {accion:<45} {pila}")

    lineas.append(">> Resultado: BIEN BALANCEADA\n" if esta_balanceada
                  else f">> Resultado: NO BALANCEADA -> {motivo}\n")

    return esta_balanceada, '\n'.join(lineas)


def linea_expresion(expresion, postfix=None):
    #la linea de una sola expresion: original, infix formateado y postfix
    postfix = postfix if postfix is not None else infix_to_postfix(expresion)
    return (f"Expresión: {expresion:<20} - Formateada(infix): "
            f"{format(expresion):<20} - Postfix: {postfix}")


def tabla_pasos(expresion):
    #la traza del shunting yard: token leido, pila y salida parcial
    postfix, pasos = procesar(expresion)
    lineas = [f"Expresión:        {expresion}",
              f"Infix formateado: {format(expresion)}",
              f"  {'#':>3}  {'Token':<6} {'Pila':<12} Salida"]
    for n, (token, stack, salida) in enumerate(pasos, 1):
        lineas.append(f"  {n:>3}  {token:<6} {stack:<12} {salida}")
    lineas.append(f"Postfix: {postfix}\n")
    return '\n'.join(lineas)


def tabla_transiciones(afd):
    #la tabla del AFD: una fila por estado y una columna por simbolo
    simbolos = afd.simbolos
    ancho = max(6, max((len(str(estado)) for estado in afd.estados), default=1) + 2)
    filas = ["     " + "Estado".ljust(ancho)
             + ''.join(simbolo.center(ancho) for simbolo in simbolos)]

    for estado in afd.estados:
        marca = ('->' if estado == afd.inicio else '  ')
        marca += ('*' if afd.es_aceptacion(estado) else ' ')
        celdas = ''
        for simbolo in simbolos:
            destino = afd.destino(estado, simbolo)
            celdas += ('-' if destino is None else str(destino)).center(ancho)
        filas.append(f"  {marca}" + str(estado).ljust(ancho) + celdas)

    return '\n'.join(filas)


def subconjuntos_texto(afd, titulo="  Subconjuntos:"):
    #de que estados del automata anterior salio cada estado del AFD
    lineas = [titulo]
    for estado, origenes in sorted(afd.subconjuntos.items()):
        lineas.append(textwrap.fill(f"    {estado} = {conjunto(sorted(origenes))}",
                                    width=ANCHO, subsequent_indent=" " * 8))
    return '\n'.join(lineas)


def traza_determinista(pasos):
    #cada paso es (simbolo consumido, estado actual); None es cadena rechazada
    lineas = []
    for simbolo, estado in pasos:
        etiqueta = "inicio" if not simbolo else f"lee '{simbolo}'"
        destino = "— (no hay transición)" if estado is None else str(estado)
        lineas.append(f"    {etiqueta:<9} -> {destino}")
    return '\n'.join(lineas)
