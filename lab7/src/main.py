import re
import sys
from pathlib import Path
from itertools import product

class Grammar:
    def __init__(self, productions):
        self.productions = productions

    @property
    def non_terminals(self):
        # Obtiene los no terminales de la gramática (letras mayúsculas).
        return set(self.productions.keys())

    def all_symbols(self):
        # Obtiene los símbolos usados en las producciones.
        symbols = set(self.non_terminals)

        for bodies in self.productions.values():
            for body in bodies:
                symbols.update(body)

        return symbols

    def print_grammar(self, title = None):
        # Imprime la gramática en un formato legible.
        if title:
            print(f"\n{title}")

        for left_side, bodies in self.productions.items():
            formatted_bodies = []

            for body in bodies:
                if body == "":
                    formatted_bodies.append("ε")
                else:
                    formatted_bodies.append("".join(body))

            print(f"{left_side} -> {' | '.join(formatted_bodies)}")

def validate_line(line, line_number):
    """ Validación de una línea en producción. 
        Formato permitido: S -> 0A0 | 1B1 | BB
        El lado izquierdo debe ser una letra mayúscula. Los cuerpos pueden contener:
            - Letras mayúsculas: no terminales
            - Letras minúsculas: terminales
            - Dígitos: terminales
            - ε: cadena vacía """

    pattern = r"^[A-Z]\s*->\s*(?:ε|[A-Za-z0-9]+)(?:\s*\|\s*(?:ε|[A-Za-z0-9]+))*$"

    if not re.fullmatch(pattern, line):
        raise ValueError(
            f"Error de sintaxis en la línea {line_number}: {line}\n"
            "Formato esperado: S -> 0A0 | 1B1 | BB"
        )

def parse_grammar(file_path):
    """ Lee y transforma un archivo de texto en un objeto Grammar """
    productions = {}

    try:
        with open(file_path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        # Ignorando líneas vacías
        if not line:
            continue

        validate_line(line, line_number)

        left_side, right_side = re.split(r"\s*\->\s*", line, maxsplit = 1)

        alternatives = re.split(r"\s*\|\s*", right_side)

        if left_side not in productions:
            productions[left_side] = []

        for alternative in alternatives:
            if alternative == "ε":
                # La cadena vacía se representa internamente como ""
                productions[left_side].append("")
            else:
                # Cada símbolo se almacena individualmente
                productions[left_side].append(list(alternative))
        
    if not productions:
        raise ValueError("El archivo no contiene producciones.")

    return Grammar(productions)

def find_nullable_symbols(grammar):
    """ Encuetra todos los no terminales anulables.
        Un símbolo es anulable si puede producir ε directa o indirectamente.
            
        Ejemplo:
            C -> ε
            A -> C
                
        Entonces C y A son anulables. """

    nullable = set()

    print("\nEncontrando símbolos anulables...")

    # Producciones directamente anulables
    for left_side, bodies in grammar.productions.items():
        if "" in bodies:
            nullable.add(left_side)
            print(f"- {left_side} es anulable porque {left_side} -> ε")
        
    # producciones cuyos símbolos ya son anulables
    changed = True

    while changed:
        changed = False

        for left_side, bodies in grammar.productions.items():
            if left_side in nullable:
                continue

            for body in bodies:
                if body and all( symbol in nullable for symbol in body):
                    nullable.add(left_side)
                    print(
                        f"- {left_side} es anulable porque "
                        f"{left_side} -> {''.join(body)}"
                    )
                    changed = True
                    break

    print("Símbolos anulables encontrados: " + (", ".join(sorted(nullable)) if nullable else "ninguno"))

    return nullable

def generate_variants(body, nullable):
    """ Genera todas las variantes de un cuerpo eliminando/conservando los síbolos anulables.
    
        Ejemplo:
            cuerpo = A B C
            anulables = {A, C}
                
        Variantes generadas:
            ABC
            BC
            AB
            B """
    positions = [
        index
        for index, symbol in enumerate(body)
        if symbol in nullable
    ]

    variants = set()

    # Cada posición anulable puede conservarse o eliminarse
    for options in product([False, True], repeat=len(positions)):
        positions_to_remove = {
            position
            for position, remove in zip(positions, options)
            if remove
        }

        variant= tuple(
            symbol
            for index, symbol in enumerate(body)
            if index not in positions_to_remove
        )

        variants.add(variant)

    return variants

def remove_epsilon_productions(grammar):
    # Eliminar producciones ε con símbolos anulables
    nullable = find_nullable_symbols(grammar)

    print("\nGenerando nuevas producciones...")

    new_productions = {
        left_side: set()
        for left_side in grammar.productions
    }

    for left_side, bodies in grammar.productions.items():
        for body in bodies:
            # La producción ε original se elimina
            if body == "":
                continue

            variants= generate_variants(body, nullable)

            for variant in variants:
                # No agregar producciones vacías.
                if not variant:
                    continue

                # Se omite ε de la gramática resultante
                new_productions[left_side].add(variant)

                original = "".join(body)
                generated = "".join(variant)

                if original != generated:
                    print(
                        f"- {left_side} -> {original}"
                        f" genera {left_side} -> {generated}"
                    )

    # Se convierten los conjuntos a listas ordenadas para imprimir resultados deterministas
    ordered_productions = {}

    for left_side, bodies in new_productions.items():
        ordered_productions[left_side] = sorted(bodies, key=lambda body: "".join(body))

    result = Grammar(ordered_productions)

    print("\nResultado sin producciones ε")
    result.print_grammar()

    return result

def main():
    if len(sys.argv) != 2:
        print("Uso:")
        print("python src/main.py grammars/grammar1.txt")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    try:
        grammar = parse_grammar(file_path)

        print("Gramática original")
        grammar.print_grammar()

        remove_epsilon_productions(grammar)

    except (ValueError, FileNotFoundError) as error:
        print(f"\n{error}")
        sys.exit(1)

if __name__ == "__main__":
    main()