
import os

from graphviz import ExecutableNotFound

from .afn import afn_de, simular
from .arbol import arbol_de
from .archivos import leer_expresiones, preparar_carpeta
from .dibujo_arbol import dibujar
from .dibujo_automata import guardar
from .reportes import (linea_expresion, resumen, tabla_balanceo, tabla_pasos,
                       transiciones_texto, traza_texto)


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


def _guardar_imagen(automata, ruta, titulo, abrir):
    try:
        print(f"  Imagen: {guardar(automata, ruta, titulo=titulo, abrir=abrir)}")
    except ExecutableNotFound:
        print("  Imagen: no se generó, falta el binario de Graphviz "
              "(instálelo con: winget install Graphviz.Graphviz)")


def procesar_archivo(filename, w, carpeta_salida="afn", abrir=False,
                     expandir=True, detalle=True):
    #una linea del archivo es una r: se construye su AFN, se dibuja y se simula con w
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    preparar_carpeta(carpeta_salida)
    generados = 0

    for expresion in expresiones:
        try:
            postfix, automata = afn_de(expresion, expandir)
        except ValueError as error:
            print(f"Expresión inválida '{expresion}': {error}\n")
            continue

        generados += 1
        aceptada, pasos = simular(automata, w)
        veredicto = "sí" if aceptada else "no"

        print(f"r = {expresion:<24} Postfix: {postfix}")
        print(resumen(automata))
        if detalle:
            print(transiciones_texto(automata))
            print(f"  Simulación con w = \"{w}\":")
            print(traza_texto(pasos))

        titulo = f"r = {expresion}    w = \"{w}\"    w pertenece a L(r): {veredicto}"
        _guardar_imagen(automata, os.path.join(carpeta_salida, f"afn_{generados}"),
                        titulo, abrir)

        print(f"  ¿w = \"{w}\" pertenece a L(r)?  ->  {veredicto.upper()}\n")

    if generados:
        print(f"{generados} AFN generados en: {os.path.abspath(carpeta_salida)}")


def verificar_archivo(filename):
    #el ejercicio 2: por cada linea, la traza de la pila y el veredicto
    expresiones = _expresiones(filename)
    if expresiones is None:
        return

    for expresion in expresiones:
        print(tabla_balanceo(expresion)[1])
