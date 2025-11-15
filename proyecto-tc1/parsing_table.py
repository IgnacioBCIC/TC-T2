# ============================================
#      FIRST, FOLLOW y TABLA LL(1)
# ============================================

from grammar import GRAMATICA, es_no_terminal


# -------------------------------------------
#              FIRST
# -------------------------------------------

def calcular_first(gramatica):
    first = {nt: set() for nt in gramatica}

    cambio = True
    while cambio:
        cambio = False

        for A in gramatica:
            for produccion in gramatica[A]:

                # Si la producción es E directamente
                if produccion == ["ε"]:
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        cambio = True
                    continue

                # Producción
                for X in produccion:

                    # Caso 1: X es no terminal
                    if es_no_terminal(X):
                        antes = len(first[A])
                        first[A].update(first[X] - {"ε"})
                        despues = len(first[A])
                        if despues > antes:
                            cambio = True

                        if "ε" in first[X]:
                            continue
                        break

                    # Caso 2: X es terminal
                    else:
                        if X not in first[A] and X != "ε":
                            first[A].add(X)
                            cambio = True
                        break
                else:
                    # Si todos derivan ε
                    if "ε" not in first[A]:
                        first[A].add("ε")
                        cambio = True

    return first


# -------------------------------------------
#           FIRST Beta
# -------------------------------------------

def first_beta(beta, first):
    """
    Calcula FIRST(β) donde β es una secuencia
    sin ensuciar FOLLOW.
    """
    resultado = set()

    for X in beta:

        # Si es no terminal
        if es_no_terminal(X):
            resultado.update(first[X] - {"ε"})
            if "ε" in first[X]:
                continue
            break

        # Si es terminal
        resultado.add(X)
        break

    else:
        # Todos derivaron ε
        resultado.add("ε")

    return resultado


# -------------------------------------------
#              FOLLOW
# -------------------------------------------

def calcular_follow(gramatica, first):
    follow = {nt: set() for nt in gramatica}
    follow["S"].add("$")  

    cambio = True
    while cambio:
        cambio = False

        for A in gramatica:
            for produccion in gramatica[A]:

                for i, B in enumerate(produccion):
                    if not es_no_terminal(B):
                        continue

                    beta = produccion[i+1:]

                    # Caso 1: B seguido de beta
                    if beta:
                        fb = first_beta(beta, first)

                        # FIRST(beta) - {ε}
                        antes = len(follow[B])
                        follow[B].update(fb - {"ε"})
                        despues = len(follow[B])
                        if despues > antes:
                            cambio = True

                        # Si ε ∈ FIRST(β) → FOLLOW(A) se propaga a FOLLOW(B)
                        if "ε" in fb:
                            antes = len(follow[B])
                            follow[B].update(follow[A])
                            despues = len(follow[B])
                            if despues > antes:
                                cambio = True

                    # Caso 2: B es último símbolo
                    else:
                        antes = len(follow[B])
                        follow[B].update(follow[A])
                        despues = len(follow[B])
                        if despues > antes:
                            cambio = True

    return follow


# -------------------------------------------
#              TABLA LL(1)
# -------------------------------------------

def generar_tabla_LL1(gramatica, first, follow):
    tabla = {A: {} for A in gramatica}

    for A in gramatica:
        for produccion in gramatica[A]:

            # Caso A → ε
            if produccion == ["ε"]:
                for b in follow[A]:
                    if b in tabla[A]:
                        raise Exception(f"Conflicto LL(1): {A}, {b}")
                    tabla[A][b] = produccion
                continue

            # FIRST( produccion )
            fb = first_beta(produccion, first)

            for t in fb - {"ε"}:
                if t in tabla[A]:
                    raise Exception(f"Conflicto LL(1): {A}, {t}")
                tabla[A][t] = produccion

            # Si FIRST contiene ε → usar FOLLOW(A)
            if "ε" in fb:
                for t in follow[A]:
                    if t in tabla[A]:
                        raise Exception(f"Conflicto LL(1): {A}, {t}")
                    tabla[A][t] = produccion

    return tabla


# -------------------------------------------
#            Guardar tabla en CSV
# -------------------------------------------

import csv
import os

def guardar_tabla(tabla, ruta):
    terminales = set()
    for fila in tabla.values():
        terminales.update(fila.keys())

    terminales = sorted(list(terminales))

    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["NT"] + terminales)

        for nt in tabla:
            fila = []
            for t in terminales:
                prod = tabla[nt].get(t, "")
                p = " ".join(prod) if prod else ""
                fila.append(p)
            w.writerow([nt] + fila)
