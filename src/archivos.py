
import os

#los .txt de ejemplo viven aparte del codigo
CARPETA_DATOS = "datos"


def normalizar(nombre):
    #el menu acepta 'expresiones' igual que 'expresiones.txt'
    return nombre if nombre.lower().endswith('.txt') else nombre + '.txt'


def resolver(nombre):
    #se puede escribir 'expresiones', 'expresiones.txt' o 'datos/expresiones.txt':
    #primero se busca tal cual y despues dentro de datos/
    ruta = normalizar(nombre)
    if not os.path.isfile(ruta):
        en_datos = os.path.join(CARPETA_DATOS, ruta)
        if os.path.isfile(en_datos):
            return en_datos
    return ruta


def leer_expresiones(filename):
    #una expresion por linea, las vacias se ignoran
    with open(filename, 'r', encoding='utf-8') as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def preparar_carpeta(carpeta):
    os.makedirs(carpeta, exist_ok=True)
    return os.path.abspath(carpeta)
