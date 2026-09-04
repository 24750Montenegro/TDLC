
import os

from graphviz import ExecutableNotFound

from .afd import afd_de, minimizar
from .afd import simular as simular_afd
from .afn import afn_de
from .afn import simular as simular_afn
from .arbol import arbol_de
from .archivos import leer_expresiones, preparar_carpeta
from .dibujo_arbol import dibujar
from .dibujo_automata import guardar
from .reportes import (linea_expresion, resumen, subconjuntos_texto,
                       tabla_balanceo, tabla_pasos, tabla_transiciones,
                       traza_determinista, traza_texto, transiciones_texto)

#cada tipo de automata trae su nombre, su carpeta y el prefijo de sus imagenes
AUTOMATAS = {
    'afn': ("AFN (Thompson)", "afn", "afn"),
    'afd': ("AFD (subconjuntos)", "afd", "afd"),
    'min': ("AFD mínimo", "afd_min", "afd_min"),
}

ORIGEN = {'afd': "  Subconjuntos de estados del AFN:",
          'min': "  Bloques de estados del AFD:"}


def _expresiones(filename):
    #None avisa que el archivo no existe; el menu solo vuelve a preguntar
    try:
        return leer_expresiones(filename)
    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")
        return None


def read_file(filename, pasos=False):
    #imprime cada expresion del archivo: postfix, o la traza completa del algoritmo
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    for expresion in expresiones:
        try:
            print(tabla_pasos(expresion) if pasos else linea_expresion(expresion))
        except ValueError as error:
            print(f"Expresión inválida '{expresion}': {error}")


def graficar_archivo(filename, expandir=True, carpeta_salida="ast"):
    #lee el archivo, arma un AST por linea y guarda un svg por expresion
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    arboles = []

    for expresion in expresiones:
        try:
            postfix, raiz = arbol_de(expresion, expandir)
            arboles.append((expresion, raiz))
            print(linea_expresion(expresion, postfix))
        except ValueError as error:
            print(f"Expresión inválida '{expresion}': {error}")

    if not arboles:
        return

    destino = preparar_carpeta(carpeta_salida)

    for n, (expresion, raiz) in enumerate(arboles, 1):
        ruta = os.path.join(carpeta_salida, f"ast_{n}.svg")
        dibujar(raiz).saveas(ruta)
        print(f"  {n}. {expresion}  ->  {ruta}")

    print(f"\n{len(arboles)} árboles guardados en: {destino}")


def construir_automatas(expresion, tipos=('afn',), expandir=True):
    #devuelve (postfix, {tipo: automata}); el AFD sale del AFN y el minimo del AFD
    postfix, automata = afn_de(expresion, expandir)
    construidos = {'afn': automata}

    if 'afd' in tipos or 'min' in tipos:
        construidos['afd'] = afd_de(automata)
    if 'min' in tipos:
        construidos['min'] = minimizar(construidos['afd'])

    return postfix, {tipo: construidos[tipo] for tipo in tipos}


def simular(tipo, automata, w):
    return (simular_afn if tipo == 'afn' else simular_afd)(automata, w)


def _guardar_imagen(automata, ruta, titulo, abrir):
    try:
        print(f"  Imagen: {guardar(automata, ruta, titulo=titulo, abrir=abrir)}")
    except ExecutableNotFound:
        print("  Imagen: no se generó, falta el binario de Graphviz "
              "(instálelo con: winget install Graphviz.Graphviz)")


def _detallar(tipo, automata, w, pasos):
    if tipo == 'afn':
        print(transiciones_texto(automata))
    else:
        print(tabla_transiciones(automata))
        print(subconjuntos_texto(automata, ORIGEN[tipo]))

    print(f"  Simulación con w = \"{w}\":")
    print(traza_texto(pasos) if tipo == 'afn' else traza_determinista(pasos))


def procesar_archivo(filename, w, tipos=('afn',), carpeta_salida=None,
                     abrir=False, expandir=True, detalle=True):
    #una linea del archivo es una r: se construyen sus automatas, se dibujan y
    #se simula w sobre cada uno
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    carpetas = {tipo: carpeta_salida or AUTOMATAS[tipo][1] for tipo in tipos}
    for carpeta in set(carpetas.values()):
        preparar_carpeta(carpeta)

    generados = 0

    for expresion in expresiones:
        try:
            postfix, automatas = construir_automatas(expresion, tipos, expandir)
        except ValueError as error:
            print(f"Expresión inválida '{expresion}': {error}\n")
            continue

        generados += 1
        print(f"r = {expresion:<24} Postfix: {postfix}")
        veredicto = "no"

        for tipo, automata in automatas.items():
            nombre, _, prefijo = AUTOMATAS[tipo]
            aceptada, pasos = simular(tipo, automata, w)
            veredicto = "sí" if aceptada else "no"

            print(f"  {nombre}")
            print(resumen(automata))
            if detalle:
                _detallar(tipo, automata, w, pasos)

            titulo = (f"{nombre}    r = {expresion}    w = \"{w}\"    "
                      f"w pertenece a L(r): {veredicto}")
            ruta = os.path.join(carpetas[tipo], f"{prefijo}_{generados}")
            _guardar_imagen(automata, ruta, titulo, abrir)

        print(f"  ¿w = \"{w}\" pertenece a L(r)?  ->  {veredicto.upper()}\n")

    if generados:
        for carpeta in sorted(set(carpetas.values())):
            print(f"{generados} autómatas generados en: {os.path.abspath(carpeta)}")


def verificar_archivo(filename):
    #el ejercicio 2: por cada linea, la traza de la pila y el veredicto
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    for expresion in expresiones:
        print(tabla_balanceo(expresion)[1])
