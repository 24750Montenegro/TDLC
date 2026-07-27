# Shunting Yard — Infix a Postfix

Convierte expresiones regulares de notación infija a postfija usando el algoritmo Shunting Yard de Dijkstra.

## Requisitos

- Python 3 (sin dependencias externas)

## Cómo ejecutarlo

El repositorio ya incluye `expresiones.txt` con expresiones de prueba listas para usar (las listadas en el inciso 1).

```
python shuntingyard.py
```

Aparece un menú:

```
Menú:
1. Leer archivo
2. Leer archivo paso a paso
3. Salir
Seleccione una opción:
```

- **Opción 1** — imprime, por cada línea del archivo: la expresión original, la
  expresión formateada (con las concatenaciones `.` explícitas) y el postfix.
- **Opción 2** — lo mismo, pero además muestra la traza paso a paso del algoritmo
  (token leído, contenido de la pila y salida parcial en cada iteración).
- **Opción 3** — salir.

Después de elegir 1 o 2 pide el nombre del archivo. Escriba:

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

## Estructura

- `shuntingyard.py` — implementación completa y menú interactivo.
- `expresiones.txt` — expresiones de ejemplo.
