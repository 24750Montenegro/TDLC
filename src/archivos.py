
import os


def normalizar(nombre):
    #el menu acepta 'expresiones' igual que 'expresiones.txt'
    return nombre if nombre.lower().endswith('.txt') else nombre + '.txt'


def leer_expresiones(filename):
    #una expresion por linea, las vacias se ignoran
    with open(filename, 'r', encoding='utf-8') as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def preparar_carpeta(carpeta):
    os.makedirs(carpeta, exist_ok=True)
    return os.path.abspath(carpeta)
