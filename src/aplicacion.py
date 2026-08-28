
import os

from .arbol import arbol_de
from .archivos import leer_expresiones, preparar_carpeta
from .dibujo_arbol import dibujar
from .parseo import format


def _expresiones(filename):
    #None avisa que el archivo no existe; el menu solo vuelve a preguntar
    try:
        return leer_expresiones(filename)
    except FileNotFoundError:
        print(f"Error 404: El archivo '{filename}' no existe.")
        return None


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
            print(f"Expresión: {expresion:<20} - Formateada(infix): "
                  f"{format(expresion):<20} - Postfix: {postfix}")
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
