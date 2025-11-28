import random
from gramatica.grammar import GRAMATICA, es_no_terminal

class Derivator:

    def __init__(self, max_depth=6):
        self.max_depth = max_depth

    def generate(self, symbol="EXPR"):
        return self._expand(symbol, 0)

    def _expand(self, symbol, depth):

        # Caso terminal
        if not es_no_terminal(symbol):
            return self._terminal_value(symbol)

        producciones = GRAMATICA[symbol]

        # si es muy profundo evita recursion
        if depth >= self.max_depth:

            # FACTOR → elegir NUM o ID
            if symbol == "FACTOR":
                return random.choice([self._terminal_value("NUM"),
                                      self._terminal_value("ID")])

            # EXPR_P o TERM_P → epsilon
            if symbol in ("EXPR_P", "TERM_P"):
                return ""

            # EXPR y TERM deben seguir estructura minima
            if symbol == "EXPR":
                return self._expand("TERM", depth)
            if symbol == "TERM":
                return self._expand("FACTOR", depth)

        #  Producción normal
  
        prod = random.choice(producciones)

        # Producción epsilon
        if prod == ["ε"]:
            # Solo permitido en EXPR_P y TERM_P
            if symbol in ("EXPR_P", "TERM_P"):
                return ""
            # NO permitido en EXPR, TERM, FACTOR
            # elegir otra producción
            prod = random.choice(
                [p for p in producciones if p != ["ε"]]
            )

        # 3) Expandir produccion
        result = ""
        for s in prod:
            result += self._expand(s, depth + 1)

        return result

    # VALORES TERMINALES
 
    def _terminal_value(self, symbol):
        if symbol == "NUM":
            return str(random.randint(0, 9))
        if symbol == "ID":
            return random.choice(["x", "y", "z", "var"])
        return {
            "PLUS": "+",
            "MINUS": "-",
            "MULT": "*",
            "DIV": "/",
            "MOD": "%",
            "PAR_A": "(",
            "PAR_C": ")"
        }.get(symbol, symbol)
