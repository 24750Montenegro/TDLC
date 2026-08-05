# Shunting Yard — Infix a Postfix

Dos programas independientes, cada uno con su propio menú y su propio archivo de pruebas:

- **`shuntingyard.py`** (ejercicio 3) — convierte expresiones regulares de notación infija
  a postfija usando el algoritmo Shunting Yard de Dijkstra.
- **`Balanceo.py`** (ejercicio 2) — verifica el balanceo de `()`, `[]` y `{}` con una pila,
  mostrando la traza paso a paso.

## Video de ejecución

Demostración de ambos programas corriendo: **https://youtu.be/dZ4LygP9FF8**

## Requisitos

- Python 3
- `svgling` (Python puro, no necesita ningún binario aparte). Solo lo usa la opción 3
  del menú, la que dibuja el AST:

```
pip install -r requirements.txt
```

## Cómo ejecutar el Shunting Yard

El repositorio ya incluye `expresiones.txt` con expresiones de prueba listas para usar (las listadas en el inciso 1).

```
python shuntingyard.py
```

Aparece un menú:

```
Menú:
1. Leer archivo
2. Leer archivo paso a paso
3. Leer archivo y graficar el AST
4. Salir
Seleccione una opción:
```

- **Opción 1** — imprime, por cada línea del archivo: la expresión original, la
  expresión formateada (con las concatenaciones `.` explícitas) y el postfix.
- **Opción 2** — lo mismo, pero además muestra la traza paso a paso del algoritmo
  (token leído, contenido de la pila y salida parcial en cada iteración).
- **Opción 3** — lo mismo que la opción 1 y además guarda un `.svg` por expresión en la
  carpeta `ast/` (`ast_1.svg`, `ast_2.svg`, …) con su árbol sintáctico. Los `a+` y `a?`
  se dibujan ya expandidos como `a.a*` y `a|ε`.
- **Opción 4** — salir.

Después de elegir 1, 2 o 3 pide el nombre del archivo. Escriba:

```
expresiones.txt
```

La extensión `.txt` se puede agregar sola, así que basta con escribir `expresiones`.

### Salida esperada (opción 1)

```
Expresión: (a|t)c               - Formateada(infix): (a|t).c              - Postfix: at|c.
Expresión: (a|b)*               - Formateada(infix): (a|b)*               - Postfix: ab|*
Expresión: (a*|b*)*             - Formateada(infix): (a*|b*)*             - Postfix: a*b*|*
...
```

## Agregar sus propias expresiones

Puede agregar más líneas a `expresiones.txt` o crear otro archivo `.txt` (una expresión
por línea; las líneas vacías se ignoran) y pasar su nombre en el menú.

### Prefiera caracteres ASCII

**Se recomienda escribir las expresiones solo con ASCII**, por portabilidad.

El archivo se lee siempre como UTF-8, así que caracteres como el `ε` (épsilon) de la
línea 4 de `expresiones.txt` se procesan sin problema. Lo que puede fallar es
*imprimirlos*: eso depende de la codificación de salida del entorno. Si la consola está
en UTF-8 ( que es lo normal en Windows 11 y en la terminal de VS Code)
todo se ve bien. Pero si la salida se redirige a un archivo o a un pipe, Python usa la
codificación regional y puede fallar con:

```
UnicodeEncodeError: 'charmap' codec can't encode character 'ε'
```

## Sintaxis soportada

| Símbolo | Significado |
|---|---|
| `\|` | alternancia (or) |
| `.` | concatenación (se inserta automáticamente; escríbala como `\.` si quiere un punto literal) |
| `^` | operador binario de menor precedencia que los unarios |
| `?` | cero o una repetición |
| `*` | cero o más repeticiones (Kleene) |
| `+` | una o más repeticiones |
| `( )` | agrupación |
| `[ ]` | clase de caracteres: `[ae03]` equivale a `(a\|e\|0\|3)` |
| `\` | escape: `\(` es un paréntesis literal, `\.` un punto literal |

Precedencia (de menor a mayor): `(` `[` < `|` < `.` < `^` < `?` `*` `+`

Dentro de una clase `[ ]` todo es literal salvo el `]` que la cierra y el `\` que escapa.

## Validación

Las expresiones inválidas no detienen el programa: se reporta el error y se continúa con
la siguiente línea. Se detectan, entre otros:

- expresión vacía
- operador sin operando a la izquierda o a la derecha
- paréntesis o corchetes sin cerrar / sin abrir
- cierre que no corresponde con su apertura (`(a]`)
- subexpresión vacía `()` o clase vacía `[]`
- `\` al final de la expresión

## Cómo ejecutar el verificador de balanceo

`Balanceo.py` resuelve el ejercicio 2. El repositorio incluye `ejercicio2.txt` con las
expresiones de prueba de ese inciso (varias están deliberadamente desbalanceadas).

```
python Balanceo.py
```

Aparece un menú:

```
========== Ejercicio 2: Verificador de balanceo ==========
1. Leer el  archivo y verificar balanceo
2. Salir
```

Después de elegir 1 pide el nombre del archivo. Escriba `ejercicio2.txt`, o basta con
`ejercicio2`: la extensión `.txt` se agrega sola. Por cada línea imprime la traza completa
de la pila y el veredicto.

### Salida esperada

```
Expresion: (a{b})
    #  Pos  Token  Accion                                        Pila
    1    0   (      PUSH  '('                                     (
    2    1   a      no es simbolo de interes                      (
    3    2   {      PUSH  '{'                                     ({
    4    3   b      no es simbolo de interes                      ({
    5    4   }      POP   '{' (cierra con '}')                    (
    6    5   )      POP   '(' (cierra con ')')
>> Resultado: BIEN BALANCEADA

Expresion: (a|b]
    #  Pos  Token  Accion                                        Pila
    1    0   (      PUSH  '('                                     (
    2    1   a      no es simbolo de interes                      (
    3    2   |      no es simbolo de interes                      (
    4    3   b      no es simbolo de interes                      (
    5    4   ]      error: se esperaba cierre de '(', llego ']'   (
>> Resultado: NO BALANCEADA -> ']' en la posicion 4 no coincide con el simbolo en el tope de la pila ('(')
```

### Detalles

- Se verifican los tres pares: `()`, `[]` y `{}`. Cualquier otro caracter no toca la pila.
- Los caracteres escapados con `\` se ignoran: en `\(a\)` no hay nada que balancear.
- La traza se corta en el primer error. Un símbolo de apertura que nunca se cierra se
  reporta al final: *"quedaron simbolos sin cerrar en la pila"*.

> **Nota.** A diferencia de `shuntingyard.py`, este verificador no interpreta clases de
> caracteres: `[({]` se reporta como no balanceada, aunque el shunting yard la aceptaría
> como una clase que contiene `(` y `{`. Es intencional — el ejercicio 2 es un verificador
> de balanceo genérico, no un parser de expresiones regulares.

Las llaves `{}` solo son significativas aquí. En `shuntingyard.py` son símbolos literales
del alfabeto (no agrupan y no son cuantificador `{n,m}`), así que `a{2,3}` se convierte sin
error a `a{.2.,.3.}.`; por eso el balanceo de llaves se comprueba en este programa y no allá.

## Estructura

- `shuntingyard.py` — ejercicio 3: implementación completa y menú interactivo.
- `expresiones.txt` — expresiones de ejemplo para el ejercicio 3.
- `Balanceo.py` — ejercicio 2: verificador de balanceo con traza de la pila.
- `ejercicio2.txt` — expresiones de ejemplo para el ejercicio 2.
