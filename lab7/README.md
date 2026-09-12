# Laboratorio No. 7

Implementación del Ejercicio No. 2 del Laboratorio No. 7 del curso de Teoría de la Computación.

El programa permite leer gramáticas libres de contexto desde archivos de texto, validar su formato, encontrar símbolos anulables y eliminar las producciones-ε.

## Integrantes

- Alejandra Avilés - 24722
- Joel Nerio - 24253
- Juan Montenegro - 24750

## Descripción del proyecto

El programa implementa una parte del proceso de simplificación de gramáticas libres de contexto.

Las operaciones implementadas son:

1. Lectura de gramáticas desde archivos de texto.
2. Validación de la sintaxis de cada producción mediante expresiones regulares.
3. Interpretación de las producciones.
4. Identificación de símbolos anulables.
5. Generación de nuevas producciones eliminando símbolos anulables.
6. Eliminación de producciones-ε.
7. Impresión de los pasos del algoritmo y de la gramática resultante.

## Requisitos

- Python 3.10 o superior.
- Git, si se desea clonar o contribuir al repositorio.

El programa utiliza únicamente módulos incluidos en la biblioteca estándar de Python. No requiere paquetes externos.

## Estructura del repositorio

```text
lab7/
├── README.md
├── src/
│   ├── __init__.py
│   └── main.py
├── grammars/
│   ├── grammar1.txt
│   └── grammar2.txt
│   └── grammar_invalid.txt
├── docs/
│   └── procedimiento_ejercicio_1.pdf
└── video/
│   └── enlace.txt

### Archivo de prueba inválido

El archivo 'grammars/grammar_invalid' tiene el propósito de mostrar qué hace el programa al encontrar una producción en formato erróneo, por ejemplo:

'''text
S=A
'''

## Vídeo de demostración
[Ver vídeo de demostración](https://www.youtube.com/watch?v=XXXXXXXXXXXXX)