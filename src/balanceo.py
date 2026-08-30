
from .tokens import APERTURA, CIERRE, ESCAPE, PARES_CIERRE


def verificar_balanceo(expresion):
    #recorre la expresion con una pila y devuelve (balanceada, motivo, pasos);
    #cada paso es (posicion, token, accion, pila como texto)
    pila = []
    pasos = []
    balanceada = True
    motivo = ""

    i = 0
    n = len(expresion)
    while i < n:
        c = expresion[i]

        #los caracteres escapados no cuentan como simbolos que interesan
        if c == ESCAPE:
            if i + 1 >= n:
                pasos.append((i, c, "'\\' al final sin caracter que escapar (lit se ignora)",
                              ''.join(pila)))
                i += 1
                continue
            pasos.append((i, expresion[i:i + 2],
                          "caracter escapado, se ignora para el balanceo", ''.join(pila)))
            i += 2
            continue

        if c in APERTURA:
            pila.append(c)
            pasos.append((i, c, f"PUSH  '{c}'", ''.join(pila)))

        elif c in CIERRE:
            if not pila:
                balanceada = False
                motivo = f"'{c}' en la posicion {i} no tiene apertura correspondiente"
                pasos.append((i, c, f"error: pila vacia, no hay que cerrar con '{c}'",
                              ''.join(pila)))
                break

            tope = pila[-1]
            if tope == PARES_CIERRE[c]:
                pila.pop()
                pasos.append((i, c, f"POP   '{tope}' (cierra con '{c}')", ''.join(pila)))
            else:
                balanceada = False
                motivo = (f"'{c}' en la posicion {i} no coincide con el simbolo "
                          f"en el tope de la pila ('{tope}')")
                pasos.append((i, c, f"error: se esperaba cierre de '{tope}', llego '{c}'",
                              ''.join(pila)))
                break
        else:
            pasos.append((i, c, "no es simbolo de interes", ''.join(pila)))

        i += 1

    if balanceada and pila:
        balanceada = False
        motivo = f"quedaron simbolos sin cerrar en la pila: {''.join(pila)}"

    return balanceada, motivo, pasos


def balanceada(expresion):
    #el veredicto solo, para quien no necesita la traza
    return verificar_balanceo(expresion)[0]
