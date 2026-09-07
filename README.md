# Shunting Yard — Infix a Postfix

**Integrantes:** Alejandra Avilés · Joel Nerio · Juan Montenegro

---

## Video de demostración del proyecto

<div align="center">



### **[https://youtu.be/_EtjkIjiTiU](https://youtu.be/_EtjkIjiTiU)**


</div>

---

Un solo programa, **`main.py`**: el menú que pide la opción, el archivo y la cadena `w`.

No tiene algoritmo adentro; solo arma su menú sobre el paquete **`src/`**, donde vive
todo. Cada módulo hace una sola cosa, así que se puede usar suelto desde Python sin pasar
por el menú:

| Módulo | Qué hace |
|---|---|
| `src/tokens.py` | la definición de los símbolos: operadores, precedencias, pares que se balancean, `ε` y el escape |
| `src/parseo.py` | escapes, concatenación explícita, validación y formateo de la expresión |
| `src/shuntingyard.py` | el algoritmo Shunting Yard de Dijkstra: infix → postfix y su traza |
| `src/balanceo.py` | verificación de balanceo de `()`, `[]` y `{}` con una pila |
| `src/arbol.py` | el AST a partir del postfix |
| `src/automata.py` | clase base `Automata`, común al AFN y al AFD |
| `src/afn.py` | AFN por Thompson y su simulación por conjuntos de estados |
| `src/afd.py` | AFD por subconjuntos, su simulación y su minimización |
| `src/dibujo_arbol.py` | dibujo del AST con `svgling` |
| `src/dibujo_automata.py` | dibujo del AFN y del AFD con `graphviz` |
| `src/reportes.py` | los textos que se imprimen: tablas, transiciones y trazas |
| `src/archivos.py` | lectura de los `.txt` y creación de las carpetas de salida |
| `src/aplicacion.py` | une todo lo anterior: es lo que llama cada opción del menú |

Los `.txt` de ejemplo están en **`datos/`**, y las imágenes se generan en `ast/`, `afn/`,
`afd/` y `afd_min/`.

## Video de ejecución
Demostración de  programas corriendo:

#### Proyecto - Demostración final
**https://youtu.be/_EtjkIjiTiU**

#### Lab 2 - Balanceo y ShuntingYard

 **https://youtu.be/dZ4LygP9FF8**

#### Lab 3 - Generación de AST's
**https://youtu.be/ZuII4VVMHmY**

#### Lab 4 - Construcción y simulación del AFN
**https://youtu.be/OUuJWsCNV_8**

## Requisitos

- Python 3
- `svgling` — lo usa `src/dibujo_arbol.py`, es decir la opción 3 del menú, la que dibuja
  el AST.
- `graphviz` — lo usa `src/dibujo_automata.py`, es decir las opciones 4 a 7, las que
  dibujan el AFN y el AFD.

```
pip install -r requirements.txt
```

El paquete `graphviz` de Python solo arma el grafo; quien lo dibuja es el programa `dot`,
que se instala aparte:

```
winget install Graphviz.Graphviz
```

En Linux es `sudo apt install graphviz` y en Mac `brew install graphviz`.

Si el instalador no deja `dot` en el `PATH`, `src/dibujo_automata.py` lo busca solo en
`C:\Program Files\Graphviz\bin`. Si aun asi no lo encuentra, lo avisa y continúa: la
simulación se imprime igual, lo único que falta es la imagen.

**Si prefiere no instalar nada**, el repositorio trae un `Dockerfile` con todo adentro:
vea [Correr con Docker](#correr-con-docker).

## Cómo ejecutar el Shunting Yard

El repositorio ya incluye `datos/expresiones.txt` con expresiones de prueba

```
python main.py
```

Aparece un menú:

```
=============Menú=============
1. Leer archivo
2. Leer archivo paso a paso
3. Leer archivo y graficar el AST
4. Leer archivo, generar el AFN y simular una cadena
5. Leer archivo, convertir el AFN a AFD y simular una cadena
6. Leer archivo, minimizar el AFD y simular una cadena
7. Leer archivo y generar AFN, AFD y AFD mínimo
8. Salir
==============================
```

- **Opción 1** — imprime, por cada línea del archivo: la expresión original, la
  expresión formateada (con las concatenaciones `.` explícitas) y el postfix.
- **Opción 2** — lo mismo, pero además muestra la traza paso a paso del algoritmo
  (token leído, contenido de la pila y salida parcial en cada iteración).
- **Opción 3** — lo mismo que la opción 1 y además guarda un `.svg` por expresión en la
  carpeta `ast/` (`ast_1.svg`, `ast_2.svg`, …) con su árbol sintáctico. Los `a+` y `a?`
  se dibujan ya expandidos como `a.a*` y `a|ε`.
- **Opción 4** — construye el AFN de cada expresión con el algoritmo de Thompson, guarda
  un `.svg` por AFN en la carpeta `afn/` y simula sobre cada uno la cadena `w` que se pida,
  respondiendo **sí** o **no** según `w` pertenezca o no a `L(r)`.
- **Opción 5** — convierte ese AFN a AFD por construcción de subconjuntos, guarda el
  `.svg` en `afd/` y simula `w` sobre el AFD.
- **Opción 6** — minimiza el AFD y guarda el `.svg` en `afd_min/`.
- **Opción 7** — hace las tres cosas para cada expresión: AFN, AFD y AFD mínimo, cada uno
  con su imagen y su simulación de `w`. Los tres deben dar el mismo veredicto.
- **Opción 8** — salir.

Después de elegir una opción pide el nombre del archivo. Escriba:

```
expresiones
```

No hace falta la extensión ni la carpeta: el archivo se busca tal cual y, si no está, se
busca dentro de `datos/`. `expresiones`, `expresiones.txt` y `datos/expresiones.txt` son
la misma cosa. Las opciones 4 a 7 piden además la cadena `w` y si quiere abrir las
imágenes al terminar.

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

- edite `datos/afn.txt` o cree su propio `.txt` en su máquina, con el editor que quiera;
- corra `docker compose run --rm afn`, elija la opción que quiera y escriba el nombre del
  archivo;
- los `.svg` aparecen en las carpetas `ast/`, `afn/`, `afd/` y `afd_min/` de su máquina, no
  dentro del contenedor.

Lo mismo aplica al código: si modifica un `.py`, el cambio se toma en la siguiente corrida.
Solo hay que reconstruir (`docker compose build`) si cambia `requirements.txt`.

### Diferencias con la ejecución nativa

- La respuesta a *"¿Abrir las imágenes al terminar?"* debe ser **n**: el contenedor no
  tiene escritorio, así que los `.svg` se abren desde su máquina.
- El grafo usa DejaVu Sans Mono en vez de Consolas, que no existe en Linux. La fuente se
  cambia con la variable `AFN_FUENTE`.

## Agregar sus propias expresiones

Puede agregar más líneas a `datos/expresiones.txt` o crear otro archivo `.txt` (una
expresión por línea; las líneas vacías se ignoran) y pasar su nombre en el menú.

### Prefiera caracteres ASCII

**Se recomienda escribir las expresiones solo con ASCII**, por portabilidad.

El archivo se lee siempre como UTF-8, así que caracteres como el `ε` (épsilon) de la
línea 4 de `datos/expresiones.txt` se procesan sin problema. Lo que puede fallar es
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
| `.` | punto literal, un símbolo más del alfabeto (`\.` es lo mismo) |
| `^` | operador binario de menor precedencia que los unarios |
| `?` | cero o una repetición |
| `*` | cero o más repeticiones (Kleene) |
| `+` | una o más repeticiones |
| `( )` | agrupación |
| `[ ]` | clase de caracteres: `[ae03]` equivale a `(a\|e\|0\|3)` |
| `\` | escape: `\(` es un paréntesis literal, `\*` un asterisco literal |

### La concatenación no se escribe

**La concatenación es implícita**: se escribe `ab`, no `a.b`, y el programa la inserta sola
como el operador `.` antes de convertir a postfix. Por eso el `.` que usted escriba es
siempre un **punto literal**, igual que `\.`: es el símbolo `.` del alfabeto, no un
operador. En `[ae03]+@[ae03]+.(com|net|org)` ese `.` es el punto del dominio, y por eso la
expresión formateada lo muestra como `\.`:

```
Expresión: [ae03]+@[ae03]+.(com|net|org)
Formateada(infix): [a|e|0|3]+.@.[a|e|0|3]+.\..(c.o.m|n.e.t|o.r.g)
```

Los `.` sueltos de esa línea son las concatenaciones que insertó el programa; el `\.` es el
punto que usted escribió.

Precedencia (de menor a mayor): `(` `[` < `|` < `.` < `^` < `?` `*` `+`, donde ese `.` es
la concatenación ya insertada.

Dentro de una clase `[ ]` todo es literal salvo el `]` que la cierra y el `\` que escapa.

Todo esto está en un solo lugar, `src/tokens.py`, y de ahí lo toman el parseo, el shunting
yard y el verificador de balanceo.

## Validación

Las expresiones inválidas no detienen el programa: se reporta el error y se continúa con
la siguiente línea. Se detectan, entre otros:

- expresión vacía
- operador sin operando a la izquierda o a la derecha
- paréntesis o corchetes sin cerrar / sin abrir
- cierre que no corresponde con su apertura (`(a]`)
- subexpresión vacía `()` o clase vacía `[]`
- `\` al final de la expresión

## Cómo se construye el AST (`src/arbol.py`)

La opción 3 pasa por `src/arbol.py`. El módulo no reimplementa el algoritmo: toma el
postfix que ya produjo `src/shuntingyard.py` y lo recorre con una pila, un caracter a la
vez.

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
  Así se distingue del punto literal, que se dibuja como `\.` igual que los demás
  caracteres escapados.
- Los operadores van en rojo y negrita, los operandos en verde oliva, el `ε` en verde y las
  aristas en azul.
- Se guarda un `.svg` por expresión en `ast/`, numerados en el orden del archivo
  (`ast_1.svg`, `ast_2.svg`, …). La carpeta se crea sola y los archivos se sobrescriben en
  cada corrida; las expresiones inválidas no generan archivo, así que la numeración
  corresponde solo a las expresiones válidas.

### Usarlo desde Python

```python
from src.arbol import arbol_de
from src.dibujo_arbol import dibujar
from src.aplicacion import graficar_archivo

postfix, raiz = arbol_de("(a|b)+")   # postfix legible + raíz del AST
raiz.postorden()                     # 'ab|ab|*.'  (ya expandido)
dibujar(raiz).saveas("mi_arbol.svg")

graficar_archivo("datos/expresiones.txt")   # exactamente lo que hace la opción 3
```

`arbol_de(expresion, expandir=True)` y
`graficar_archivo(filename, expandir=True, carpeta_salida="ast")` aceptan `expandir=False`
para dejar los `+` y `?` sin expandir, y `carpeta_salida` para cambiar el destino
de los `.svg`.

## Cómo se construye el AFN (`src/afn.py`)

La opción 4 pasa por `src/afn.py`, que no vuelve a parsear nada: recibe el AST que armó
`src/arbol.py` y le aplica el **algoritmo de Thompson**.

El repositorio incluye `datos/afn.txt` con las cuatro expresiones del enunciado:

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

Como `src/arbol.py` ya expande `a+` como `a·a*` y `a?` como `a|ε`, en la práctica al AFN
solo le llegan `·`, `|` y `*`; las construcciones de `+` y `?` están de todos modos, por si
se usa `expandir=False`. El operador `^` no tiene semántica de autómata, así que se reporta
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

## Cómo se construye el AFD (`src/afd.py`)

Las opciones 5, 6 y 7 pasan por `src/afd.py`, que reutiliza el AFN del paso anterior: no
hay una segunda construcción desde la expresión.

### Construcción por subconjuntos

Cada estado del AFD es un conjunto de estados del AFN:

1. el estado inicial es la cerradura `ε` del inicial del AFN;
2. desde un conjunto `S` y un símbolo `a`, el destino es la cerradura `ε` de todos los
   estados a los que `S` llega leyendo `a`;
3. los conjuntos nuevos entran a una cola y se repite hasta que no aparezcan más;
4. acepta todo conjunto que contenga el estado de aceptación del AFN.

Los destinos vacíos no se guardan: el AFD queda **parcial**, y una transición que no existe
significa que la cadena ya no puede pertenecer al lenguaje. Como los conjuntos se generan
con un BFS desde el inicial, solo aparecen los estados alcanzables y el inicial siempre
queda numerado como `0`.

Debajo de la tabla se imprime a qué conjunto de estados del AFN corresponde cada estado del
AFD, que es lo que hace legible la construcción.

### Minimización

Se minimiza por **particiones (Moore)**, sobre el AFD ya construido:

1. se quitan los estados inalcanzables;
2. se completa el autómata: las transiciones que faltan van a un estado sumidero, para que
   toda firma exista;
3. se parte en dos bloques, aceptación y no aceptación;
4. se refina: dos estados siguen en el mismo bloque mientras cada símbolo los mande al
   mismo bloque. Cuando ningún bloque se puede partir, cada bloque es un estado;
5. se eliminan los estados muertos (los que ya no pueden llegar a una aceptación, el
   sumidero entre ellos) y se renumera con un BFS desde el inicial.

Igual que con los subconjuntos, se imprime qué bloque de estados del AFD quedó en cada
estado del AFD mínimo. Por ejemplo, el AFD de `(a|b)*abb(a|b)*` tiene 9 estados y su
mínimo tiene 4:

```
     Estado  a     b
  -> 0       1     0
     1       1     2
     2       1     3
    *3       3     3
  Bloques de estados del AFD:
    0 = {0, 2}
    1 = {1}
    2 = {3}
    3 = {4, 5, 6, 7, 8}
```

### La simulación del AFD

Es directa, sin conjuntos: se arranca en el estado inicial y cada símbolo de `w` mueve a un
único estado. Si el símbolo no tiene transición la cadena se rechaza ahí mismo y la traza lo
marca como `— (no hay transición)`. `w ∈ L(r)` si el estado donde se termina es de
aceptación.

### El dibujo

`graphviz` recibe solo los nodos y las aristas; el acomodo lo resuelve `dot`. El mismo
módulo dibuja el AFN y el AFD, porque los dos son un `Automata`:

- el estado inicial va en azul y con una flecha de entrada que no sale de ningún estado;
- los estados de aceptación van en doble círculo verde;
- las transiciones `ε` (solo las hay en el AFN) van punteadas en verde y las que consumen
  un símbolo en línea continua azul;
- las aristas paralelas entre el mismo par de estados se juntan en una sola con las
  etiquetas separadas por coma;
- el título del grafo lleva el tipo de autómata, la expresión `r`, la cadena `w` y el
  veredicto.

Se guarda un `.svg` por expresión en `afn/`, `afd/` y `afd_min/` según la opción,
numerados en el orden del archivo (`afn_1.svg`, `afd_1.svg`, `afd_min_1.svg`, …).

### Usarlo desde Python

```python
from src.afn import afn_de, simular, acepta
from src.afd import afd_de, afd_de_expresion, minimizar, minimo_de_expresion
from src.afd import simular as simular_afd
from src.dibujo_automata import guardar
from src.aplicacion import procesar_archivo

postfix, automata = afn_de("(a|b)*abb(a|b)*")
automata                      # AFN(estados=22, inicio=0, aceptacion=21)
automata.alfabeto             # {'a', 'b'}
automata.salidas(0)           # [(None, 1), (None, 2)]  -> None es ε

acepta("(a|b)*abb(a|b)*", "babba")     # True
simular(automata, "abb")               # (True, [('', [...]), ('a', [...]), ...])

afd = afd_de(automata)                 # AFD(estados=9, inicio=0, aceptacion=[4, 5, 6, 7, 8])
afd.subconjuntos[0]                    # los estados del AFN que forman el estado 0
afd.destino(0, 'a')                    # 1  (None si no hay transición)
simular_afd(afd, "abb")                # (True, [('', 0), ('a', 1), ('b', 3), ('b', 4)])

minimo = minimizar(afd)                # AFD(estados=4, inicio=0, aceptacion=[3])
minimo_de_expresion("(a|b)*abb(a|b)*") # el postfix y el AFD mínimo, en un paso

guardar(minimo, "afd_min/mi_afd", titulo="(a|b)*abb(a|b)*")
procesar_archivo("datos/afn.txt", "abb")    # exactamente lo que hace la opción 4
```

`procesar_archivo(filename, w, tipos=('afn',), carpeta_salida=None, abrir=False,
expandir=True, detalle=True)` es la única entrada que usan las opciones 4 a 7: `tipos`
elige qué autómatas construir (`'afn'`, `'afd'`, `'min'`), `abrir=True` abre cada `.svg` al
generarlo y `detalle=False` imprime solo el resumen y el veredicto, sin las transiciones ni
la traza.

## El verificador de balanceo (`src/balanceo.py`)

El verificador de balanceo de `()`, `[]` y `{}` — el ejercicio 2 del Lab 2 — ya no es un
programa aparte: es un módulo más de `src/`, sin menú propio. La verificación está en
`src/balanceo.py`, la traza en `src/reportes.py` y el recorrido de un archivo entero en
`verificar_archivo()` de `src/aplicacion.py`. El repositorio incluye
`datos/ejercicio2.txt` con las expresiones de prueba de ese inciso (varias están
deliberadamente desbalanceadas).

```python
from src.aplicacion import verificar_archivo

verificar_archivo("datos/ejercicio2.txt")
```

Por cada línea imprime la traza completa de la pila y el veredicto.

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

### Usarlo desde Python

```python
from src.balanceo import verificar_balanceo, balanceada
from src.reportes import tabla_balanceo

balanceada("(a{b})")                 # True
verificar_balanceo("(a|b]")          # (False, "']' en la posicion 4 ...", [pasos])
print(tabla_balanceo("(a{b})")[1])   # la traza completa, ya formateada
```

### Detalles

- Se verifican los tres pares: `()`, `[]` y `{}`, que salen de `PARES` en `src/tokens.py`.
  Cualquier otro caracter no toca la pila.
- Los caracteres escapados con `\` se ignoran: en `\(a\)` no hay nada que balancear.
- La traza se corta en el primer error. Un símbolo de apertura que nunca se cierra se
  reporta al final: *"quedaron simbolos sin cerrar en la pila"*.

> **Nota.** A diferencia del Shunting Yard, este verificador no interpreta clases de
> caracteres: `[({]` se reporta como no balanceada, aunque el shunting yard la aceptaría
> como una clase que contiene `(` y `{`. Es intencional — el ejercicio 2 es un verificador
> de balanceo genérico, no un parser de expresiones regulares. Por eso `src/parseo.py` no
> llama a `src/balanceo.py`: comparten los símbolos, no las reglas.

Las llaves `{}` solo son significativas aquí. Para el Shunting Yard son símbolos literales
del alfabeto (no agrupan y no son cuantificador `{n,m}`), así que `a{2,3}` se convierte sin
error a `a{.2.,.3.}.`; por eso el balanceo de llaves se comprueba en este módulo y no allá.

## Estructura

- `main.py` — el único menú: la opción, el archivo y la cadena `w`. Nada más.
- `src/` — el paquete con todo el algoritmo (vea la tabla del inicio).
- `datos/expresiones.txt` — expresiones de ejemplo para el ejercicio 3 Lab 2.
- `datos/afn.txt` — las cuatro expresiones del Lab 4, que sirven igual para el AFD.
- `datos/ejercicio2.txt` — expresiones de ejemplo para el verificador de balanceo.
- `ast/`, `afn/`, `afd/`, `afd_min/` — carpetas donde se guardan los `.svg` de cada opción.
- `requirements.txt` — dependencias (`svgling`, `graphviz`).
- `Dockerfile` y `compose.yaml` — imagen con `dot` ya instalado, para correr el proyecto
  sin instalar Graphviz en la máquina.
- `doc/` — PDFs de los ejercicios escritos.
