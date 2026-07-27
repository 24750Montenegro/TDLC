"""
Ejercicio 2  que es verificador de balanceo de simbolos () [] {}
usando una pila del ejercicio 3, para expresiones regulares en formato infix.

el uso se va a determinar por:
    correr en terminal -> python balanceo.py
    (que va a pedir el nombre del archivo de texto a procesar en este caso ejercicio2.txt, una expresion por linea)
"""

PARES_CIERRE = {')': '(', ']': '[', '}': '{'}
APERTURA = set(PARES_CIERRE.values())
CIERRE = set(PARES_CIERRE.keys())


def verificar_balanceo(expresion):
    """
    Verifica el balanceo de (), [], {} en 'expresion' usando una pila.

    Devuelve:
        balanceada (bool)
        motivo (str)          -> vacio si esta balanceada, explicacion si no esta balanceada
        pasos (list of tupla) -> (posicion, token, accion, pila_como_texto)
    """
    pila = []
    pasos = []
    balanceada = True
    motivo = ""

    i = 0
    n = len(expresion)
    while i < n:
        c = expresion[i]

        # los caracteres con \ no cuentan como simbolos que interesan
        if c == '\\':
            if i + 1 >= n:
                pasos.append((i, c, "'\\' al final sin caracter que escapar (lit se ignora)", ''.join(pila)))
                i += 1
                continue
            token = expresion[i:i + 2]
            pasos.append((i, token, "caracter escapado, se ignora para el balanceo", ''.join(pila)))
            i += 2
            continue

        if c in APERTURA:
            pila.append(c)
            pasos.append((i, c, f"PUSH  '{c}'", ''.join(pila)))

        elif c in CIERRE:
            if not pila:
                balanceada = False
                motivo = f"'{c}' en la posicion {i} no tiene apertura correspondiente"
                pasos.append((i, c, f"error: pila vacia, no hay que cerrar con '{c}'", ''.join(pila)))
                break

            tope = pila[-1]
            if tope == PARES_CIERRE[c]:
                pila.pop()
                pasos.append((i, c, f"POP   '{tope}' (cierra con '{c}')", ''.join(pila)))
            else:
                balanceada = False
                motivo = (f"'{c}' en la posicion {i} no coincide con el simbolo "
                          f"en el tope de la pila ('{tope}')")
                pasos.append((i, c, f"error: se esperaba cierre de '{tope}', llego '{c}'", ''.join(pila)))
                break
        else:
            # caracter que no es simbolo de interes, no se toca la pila
            pasos.append((i, c, "no es simbolo de interes", ''.join(pila)))

        i += 1

    if balanceada and pila:
        balanceada = False
        motivo = f"quedaron simbolos sin cerrar en la pila: {''.join(pila)}"

    return balanceada, motivo, pasos


def imprimir_resultado(expresion):
    balanceada, motivo, pasos = verificar_balanceo(expresion)

    print(f"Expresion: {expresion}")
    print(f"  {'#':>3}  {'Pos':>3}  {'Token':<6} {'Accion':<45} {'Pila'}")
    for n, (pos, token, accion, pila) in enumerate(pasos, 1):
        print(f"  {n:>3}  {pos:>3}   {token:<6} {accion:<45} {pila}")

    if balanceada:
        print(">> Resultado: BIEN BALANCEADA\n")
    else:
        print(f">> Resultado: NO BALANCEADA -> {motivo}\n")

    return balanceada


def procesar_archivo(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for linea in f:
                expresion = linea.strip()
                if not expresion:
                    continue
                imprimir_resultado(expresion)
    except FileNotFoundError:
        print(f"Error 404: el archivo '{filename}' no existe.")


if __name__ == "__main__":
    while True:
        print("\n========== Ejercicio 2: Verificador de balanceo ==========")
        print("1. Leer el  archivo y verificar balanceo")
        print("2. Salir")
        print("============================================================")
        opcion = input("Seleccione una opcion: ")

        if opcion == '1':
            filename = input("Ingrear el nombre del archivo: ")
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            procesar_archivo(filename)
        elif opcion == '2':
            print("Saliendo del programa.")
            break
        else:
            print("Opcion invalida. Por favor, seleccione 1 o 2.")