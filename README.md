# Shunting Yard — Infix a Postfix

Dos programas independientes, cada uno con su propio menú y su propio archivo de pruebas:

- **`shuntingyard.py`**  — convierte expresiones regulares de notación infija
  a postfija usando el algoritmo Shunting Yard de Dijkstra.
- **`Balanceo.py`**  — verifica el balanceo de `()`, `[]` y `{}` con una pila,
  mostrando la traza paso a paso.

- **`arbol.py`**  — construye el AST (árbol sintáctico) a partir del postfix y lo dibuja
  en SVG. No tiene menú propio: lo llama la opción 3 de `shuntingyard.py`.

- **`afn.py`**  — aplica el algoritmo de Thompson al AST para construir el AFN, lo dibuja
  con Graphviz y simula una cadena `w` sobre él. Tampoco tiene menú propio: lo llama la
  opción 4 de `shuntingyard.py`.

## Video de ejecución
Demostración de  programas corriendo:

#### Lab 2 - Balanceo y ShuntingYard

 **https://youtu.be/dZ4LygP9FF8**

#### Lab 3 - Generación de AST's
**https://youtu.be/ZuII4VVMHmY**

#### Lab 4 - Construcción y simulación del AFN
**https://youtu.be/OUuJWsCNV_8**

## Requisitos

- Python 3
- `svgling` — lo usa `arbol.py`, es decir la opción 3 del menú, la que dibuja el AST.
- `graphviz` — lo usa `afn.py`, es decir la opción 4, la que dibuja el AFN.

```
pip install -r requirements.txt
```

El paquete `graphviz` de Python solo arma el grafo; quien lo dibuja es el programa `dot`,
que se instala aparte:

```
winget install Graphviz.Graphviz
```

En Linux es `sudo apt install graphviz` y en Mac `brew install graphviz`.

Si el instalador no deja `dot` en el `PATH`, `afn.py` lo busca solo en
`C:\Program Files\Graphviz\bin`. Si aun asi no lo encuentra, lo avisa y continúa: la
simulación se imprime igual, lo único que falta es la imagen.

**Si prefiere no instalar nada**, el repositorio trae un `Dockerfile` con todo adentro:
vea [Correr con Docker](#correr-con-docker).

## Cómo ejecutar el Shunting Yard

El repositorio ya incluye `expresiones.txt` con expresiones de prueba

```
python shuntingyard.py
```

Aparece un menú:

```
Menú:
1. Leer archivo
2. Leer archivo paso a paso
3. Leer archivo y graficar el AST
4. Leer archivo, generar el AFN y simular una cadena
5. Salir
Seleccione una opción:
```

- **Opción 1** — imprime, por cada línea del archivo: la expresión original, la
  expresión formateada (con las concatenaciones `.` explícitas) y el postfix.
- **Opción 2** — lo mismo, pero además muestra la traza paso a paso del algoritmo
  (token leído, contenido de la pila y salida parcial en cada iteración).
- **Opción 3** — lo mismo que la opción 1 y además guarda un `.svg` por expresión en la
  carpeta `ast/` (`ast_1.svg`, `ast_2.svg`, …) con su árbol sintáctico. Los `a+` y `a?`
  se dibujan ya expandidos como `a.a*` y `a|ε`. De esto se encarga `arbol.py`.
- **Opción 4** — construye el AFN de cada expresión con el algoritmo de Thompson, guarda
  un `.svg` por AFN en la carpeta `afn/` y simula sobre cada uno la cadena `w` que se pida,
  respondiendo **sí** o **no** según `w` pertenezca o no a `L(r)`. De esto se encarga
  `afn.py`. Además del archivo pide la cadena `w` y si quiere abrir las imágenes al
  terminar.
- **Opción 5** — salir.

Después de elegir 1, 2, 3 o 4 pide el nombre del archivo. Escriba:

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

## Correr con Docker

`dot` es un programa en C, así que no se puede instalar con `pip`. Para no tener que
instalarlo en cada máquina, la imagen de Docker ya lo trae, junto con Python y las dos
dependencias:

```
docker compose run --rm afn
```

Eso abre el mismo menú de siempre. La primera vez construye la imagen (un par de minutos);
después arranca de inmediato.

### Probar sus propias expresiones

El `compose.yaml` monta la carpeta del proyecto dentro del contenedor, así que **no hay que
reconstruir la imagen para probar cosas nuevas**:

- edite `afn.txt` o cree su propio `.txt` en su máquina, con el editor que quiera;
- corra `docker compose run --rm afn`, elija la opción 4 y escriba el nombre del archivo;
- los `.svg` aparecen en las carpetas `afn/` y `ast/` de su máquina, no dentro del
  contenedor.

Lo mismo aplica al código: si modifica un `.py`, el cambio se toma en la siguiente corrida.
Solo hay que reconstruir (`docker compose build`) si cambia `requirements.txt`.

### Diferencias con la ejecución nativa

- La respuesta a *"¿Abrir las imágenes al terminar?"* debe ser **n**: el contenedor no
  tiene escritorio, así que los `.svg` se abren desde su máquina.
- El grafo usa DejaVu Sans Mono en vez de Consolas, que no existe en Linux. La fuente se
  cambia con la variable `AFN_FUENTE`.

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

## Cómo se construye el AST (`arbol.py`)

La opción 3 pasa por `arbol.py`. El módulo no reimplementa el algoritmo: toma el postfix
que ya produjo `shuntingyard.py` y lo recorre con una pila, un caracter a la vez.

- un operando apila una hoja;
- un operador unario (`*`, `+`, `?`) desapila un nodo y lo cuelga como su único hijo;
- un operador binario (`|`, `.`, `^`) desapila dos y los cuelga como hijo izquierdo y
  derecho (el primero en salir es el derecho).

Al terminar debe quedar exactamente un nodo en la pila: la raíz. Si queda más de uno, o si
a un operador le faltan operandos, se reporta la expresión como inválida y se sigue con la
siguiente línea, igual que en las otras opciones.

### Expansión de `+` y `?`

Por defecto los dos azúcares sintácticos se dibujan con los operadores básicos:

| Escrito | Dibujado |
|---|---|
| `a+` | `a·a*` |
| `a?` | `a\|ε` |

Por eso el árbol de `(a|b)+` tiene dos copias del subárbol `a|b`, y su recorrido en
postorden da `ab|ab|*.` aunque el postfix impreso sea `ab|+`. Con `expandir=False` se
dibuja el nodo `+` o `?` tal cual, sin expandir.

### El dibujo

- La concatenación se pinta como `·`: un punto en la línea base se pierde entre las aristas.
  El `\.` literal no cambia, y los demás caracteres escapados también conservan su `\`.
- Los operadores van en rojo y negrita, los operandos en verde oliva, el `ε` en verde y las
  aristas en azul.
- Se guarda un `.svg` por expresión en `ast/`, numerados en el orden del archivo
  (`ast_1.svg`, `ast_2.svg`, …). La carpeta se crea sola y los archivos se sobrescriben en
  cada corrida; las expresiones inválidas no generan archivo, así que la numeración
  corresponde solo a las expresiones válidas.

### Usarlo desde Python

Las tres funciones útiles si quiere llamarlo directamente:

```python
from arbol import arbol_de, dibujar, graficar_archivo

postfix, raiz = arbol_de("(a|b)+")   # postfix legible + raíz del AST
raiz.postorden()                     # 'ab|ab|*.'  (ya expandido)
dibujar(raiz).saveas("mi_arbol.svg")

graficar_archivo("expresiones.txt")  # exactamente lo que hace la opción 3
```

`arbol_de(expresion, expandir=True)` y
`graficar_archivo(filename, expandir=True, carpeta_salida="ast")` aceptan `expandir=False`
para dejar los `+` y `?` sin expandir, y `carpeta_salida` para cambiar el destino
de los `.svg`.

## Cómo se construye el AFN (`afn.py`)

La opción 4 pasa por `afn.py`, que resuelve el Lab 4 reutilizando lo del Lab 3: no vuelve a
parsear nada, recibe el AST que armó `arbol.py` y le aplica el **algoritmo de Thompson**.

El repositorio incluye `afn.txt` con las cuatro expresiones del enunciado:

```
(a*|b*)+
((ε|a)|b*)*
(a|b)*abb(a|b)*
0?(1?)?0*
```

### Thompson

Cada nodo del AST produce un fragmento con exactamente un estado inicial y uno de
aceptación, y los fragmentos se van encadenando al subir por el árbol:

| Nodo | Construcción |
|---|---|
| símbolo `a` | `i --a--> f` |
| `ε` | `i --ε--> f` |
| `r·s` | se une la aceptación de `r` con el inicio de `s` por `ε` |
| `r\|s` | un `i` nuevo entra por `ε` a los dos, y los dos salen por `ε` a un `f` nuevo |
| `r*` | `i --ε--> r --ε--> f`, más el regreso `ε` de la salida de `r` a su entrada y el atajo `i --ε--> f` |
| `r+` | igual que `r*` pero sin el atajo `i --ε--> f` |
| `r?` | igual que `r*` pero sin el regreso |

Como `arbol.py` ya expande `a+` como `a·a*` y `a?` como `a|ε`, en la práctica al AFN solo
le llegan `·`, `|` y `*`; las construcciones de `+` y `?` están de todos modos, por si se
usa `expandir=False`. El operador `^` no tiene semántica de autómata, así que se reporta
como expresión inválida y se sigue con la siguiente línea.

Los estados se numeran al final con un BFS desde el inicial, y la aceptación se manda al
último número: así todo AFN queda numerado de `0` (inicial) a `n-1` (aceptación).

### La simulación

Es la simulación clásica por conjuntos de estados, sin convertir a AFD:

1. se parte de la cerradura `ε` del estado inicial;
2. por cada símbolo de `w` se toman las transiciones con ese símbolo y se vuelve a cerrar
   con `ε`;
3. `w ∈ L(r)` si al terminar el estado de aceptación quedó dentro del conjunto.

Si el conjunto queda vacío a media cadena se corta y la respuesta es **no**. La traza
imprime el conjunto de estados después de cada símbolo leído.

### El dibujo

`graphviz` recibe solo los nodos y las aristas; el acomodo lo resuelve `dot`:

- el estado inicial va en azul y con una flecha de entrada que no sale de ningún estado;
- el de aceptación va en doble círculo verde;
- las transiciones `ε` van punteadas en verde y las que consumen un símbolo en línea
  continua azul;
- las aristas paralelas entre el mismo par de estados se juntan en una sola con las
  etiquetas separadas por coma;
- el título del grafo lleva la expresión `r`, la cadena `w` y el veredicto.

Se guarda un `.svg` por expresión en `afn/`, numerados en el orden del archivo
(`afn_1.svg`, `afn_2.svg`, …), igual que los del AST.

### Usarlo desde Python

```python
from afn import afn_de, simular, acepta, guardar, procesar_archivo

postfix, automata = afn_de("(a|b)*abb(a|b)*")
automata                      # AFN(estados=22, inicio=0, aceptacion=21)
automata.alfabeto             # {'a', 'b'}
automata.salidas(0)           # [(None, 1), (None, 2)]  -> None es ε

acepta("(a|b)*abb(a|b)*", "babba")     # True
simular(automata, "abb")               # (True, [('', [...]), ('a', [...]), ...])

guardar(automata, "afn/mi_afn", titulo="(a|b)*abb(a|b)*")
procesar_archivo("afn.txt", "abb")     # exactamente lo que hace la opción 4
```

`procesar_archivo(filename, w, carpeta_salida="afn", abrir=False, expandir=True,
detalle=True)` acepta `abrir=True` para abrir cada `.svg` al generarlo y `detalle=False`
para imprimir solo el resumen y el veredicto, sin las transiciones ni la traza.

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

- `shuntingyard.py` — ejercicio 3 Lab 2: implementación completa y menú interactivo.
- `expresiones.txt` — expresiones de ejemplo para el ejercicio 3 Lab 2.
- `arbol.py` — construcción y dibujo del AST a partir del postfix Lab 3.
- `ast/` — carpeta donde la opción 3 guarda los `.svg`.
- `afn.py` — Lab 4: AFN por Thompson a partir del AST, su dibujo y su simulación.
- `afn.txt` — las cuatro expresiones del Lab 4.
- `afn/` — carpeta donde la opción 4 guarda los `.svg`.
- `Balanceo.py` — ejercicio 2 Lab 2: verificador de balanceo con traza de la pila.
- `ejercicio2.txt` — expresiones de ejemplo para el ejercicio 2 Lab 2.
- `requirements.txt` — dependencias (`svgling`, `graphviz`).
- `Dockerfile` y `compose.yaml` — imagen con `dot` ya instalado, para correr el proyecto
  sin instalar Graphviz en la máquina.
- `doc/` — PDFs de los ejercicios escritos.
