import random
import re

# Importamos el parser LL(1)
from parser.parser import (
    calcular_first,
    calcular_follow,
    crear_tabla_LL1,
    validar_LL1
)

# Importamos la gramatica desde archivo
from gramatica.loader import cargar_gramatica_desde_txt


class Mutator:

    def __init__(self):

        # Cargamos gramatica TXT
        self.gramatica = cargar_gramatica_desde_txt("gramatica.txt")

        # Construimos FIRST, FOLLOW y la TABLA LL(1)
        self.first = calcular_first(self.gramatica)
        self.follow = calcular_follow(self.gramatica, self.first)
        self.tabla = crear_tabla_LL1(self.gramatica, self.first, self.follow)

        if self.tabla is None:
            raise Exception("La gramática NO es LL(1). No se puede construir el validador.")

    # Validador LL(1)
    def is_valid(self, expr):
        """
        Usa un parser predictivo LL(1) para determinar si la expresión
        es válida según la gramática cargada desde el archivo.
        """
        try:
            return validar_LL1(expr, self.gramatica, self.tabla)
        except:
            return False

    # MUTACIÓN

    def mutate(self, s):
        """
        Aplica mutaciones sucesivas hasta que la cadena se vuelva invalida.
        """
        for _ in range(30):  # intentos seguros
            mutated = self._mutate_once(s)

            # si NO pasa el parser LL(1) inválida
            if not self.is_valid(mutated):
                return mutated

        # Si despues de varios intentos sigue siendo valida forzamos error
        return s + "$"


    # MUTACION (solo una mutación)
    def _mutate_once(self, s):

        ops = [
            self.remove_random_char,
            self.insert_invalid_char,
            self.double_operator,
            self.random_cut,
            self.swap_operator,
        ]

        return random.choice(ops)(s)

    # OPERACIONES DE MUTACION

    def remove_random_char(self, s):
        if len(s) <= 1:
            return s + "$"
        i = random.randint(0, len(s)-1)
        return s[:i] + s[i+1:]

    def insert_invalid_char(self, s):
        i = random.randint(0, len(s)-1)
        return s[:i] + "$" + s[i:]

    def double_operator(self, s):
        i = random.randint(0, len(s)-1)
        return s[:i] + "++" + s[i:]

    def random_cut(self, s):
        if len(s) <= 2:
            return s + "$"
        i = random.randint(1, len(s)-1)
        return s[:i]

    def swap_operator(self, s):
        ops = "+-*/%"
        i = random.randint(0, len(s)-1)
        return s[:i] + random.choice(ops) + s[i+1:]
