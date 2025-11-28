from gramatica.loader import cargar_gramatica_desde_txt

# ============================
# FIRST
# ============================
def calcular_first(gramatica):
    first = {nt: set() for nt in gramatica}

    cambio = True
    while cambio:
        cambio = False

        for A in gramatica:
            for prod in gramatica[A]:

                # Produccion epsilon
                if prod == ["ε"]:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        cambio = True
                    continue

                for X in prod:

                    # X no terminal
                    if X in gramatica:
                        antes = len(first[A])
                        first[A].update(first[X] - {"ε"})
                        despues = len(first[A])

                        if despues > antes:
                            cambio = True

                        if "ε" in first[X]:
                            continue
                        break

                    # X terminal
                    else:
                        if X not in first[A]:
                            first[A].add(X)
                            cambio = True
                        break

                else:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        cambio = True

    return first

# FIRST de una cadena (epsilon)
def first_beta(beta, first, gramatica):
    res = set()

    for X in beta:
        if X in gramatica:
            res.update(first[X] - {"ε"})
            if "ε" in first[X]:
                continue
            break
        else:
            res.add(X)
            break
    else:
        res.add("ε")

    return res

# FOLLOW
def calcular_follow(gramatica, first):
    follow = {nt: set() for nt in gramatica}

    S = next(iter(gramatica))
    follow[S].add("$")

    cambio = True

    while cambio:
        cambio = False

        for A in gramatica:
            for prod in gramatica[A]:
                for i, B in enumerate(prod):

                    if B not in gramatica:
                        continue

                    beta = prod[i + 1:]

                    if beta:
                        fb = first_beta(beta, first, gramatica)

                        antes = len(follow[B])
                        follow[B].update(fb - {"ε"})
                        despues = len(follow[B])

                        if despues > antes:
                            cambio = True

                        if "ε" in fb:
                            antes = len(follow[B])
                            follow[B].update(follow[A])
                            despues = len(follow[B])
                            if despues > antes:
                                cambio = True
                    else:
                        antes = len(follow[B])
                        follow[B].update(follow[A])
                        despues = len(follow[B])
                        if despues > antes:
                            cambio = True

    return follow

# TABLA LL(1)

def crear_tabla_LL1(gramatica, first, follow):
    tabla = {A: {} for A in gramatica}

    for A in gramatica:
        for prod in gramatica[A]:

            fb = first_beta(prod, first, gramatica)

            for t in fb - {"ε"}:
                if t in tabla[A]:
                    return None
                tabla[A][t] = prod

            if "ε" in fb:
                for t in follow[A]:
                    if t in tabla[A]:
                        return None
                    tabla[A][t] = prod

    return tabla


# CONVERTIR CADENA TOKENS LL(1)
def convertir_lexemas(expr):
    tokens = []

    for c in expr:
        if c.isdigit():
            tokens.append("NUM")
        elif c in ["x", "y", "z"]:
            tokens.append("ID")
        elif c == "v":
            # detectar "var"
            tokens.append("ID")  # simplificado, ID = var
        elif c == "+":
            tokens.append("PLUS")
        elif c == "-":
            tokens.append("MINUS")
        elif c == "*":
            tokens.append("MULT")
        elif c == "/":
            tokens.append("DIV")
        elif c == "%":
            tokens.append("MOD")
        elif c == "(":
            tokens.append("PAR_A")
        elif c == ")":
            tokens.append("PAR_C")
        else:
            return ["ERR"]  # simbolo invalido

    return tokens

# PARSER LL(1) CON PILA

def validar_LL1(cadena, gramatica, tabla):
    tokens = convertir_lexemas(cadena)

    if "ERR" in tokens:
        return False

    tokens.append("$")

    S = next(iter(gramatica))
    pila = ["$", S]
    i = 0

    while pila:
        tope = pila.pop()

        if tope == tokens[i]:
            i += 1
            continue

        if tope not in tabla:
            return False

        if tokens[i] not in tabla[tope]:
            return False

        produccion = tabla[tope][tokens[i]]

        if produccion != ["ε"]:
            for s in reversed(produccion):
                pila.append(s)

    return tokens[i] == "$"
