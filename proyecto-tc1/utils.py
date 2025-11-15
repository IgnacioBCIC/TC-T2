# ============================================
#                 UTILIDADES GENERALES
# ============================================

import os

# --------------------------------------------
# Crear carpeta si no existe
# --------------------------------------------
def asegurar_carpeta(ruta):
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)

# --------------------------------------------
# Normalizar tokens del lexer:
#   ("RESERVADA", "print") → ("PRINT", "print")
#   ("RESERVADA", "read") → ("READ", "read")
# --------------------------------------------

def normalizar_tokens(tokens):
    """
    Convierte tokens RESERVADA a PRINT / READ para que
    coincidan con los terminales de la gramática.
    """
    normalizados = []
    for tipo, lexema, linea in tokens:
        if tipo == "RESERVADA":
            if lexema == "print":
                normalizados.append(("PRINT", lexema, linea))
            elif lexema == "read":
                normalizados.append(("READ", lexema, linea))
            else:
                # Por si se agregan más palabras reservadas
                normalizados.append((lexema.upper(), lexema, linea))
        else:
            normalizados.append((tipo, lexema, linea))
    return normalizados

# --------------------------------------------
# Guardar tokens en archivo
# --------------------------------------------

def guardar_tokens(tokens, ruta):
    if not tokens:
        print("[ADVERTENCIA] No hay tokens para guardar.")
        return

    asegurar_carpeta(ruta)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("TIPO\tLEXEMA\tLINEA\n")
        f.write("----------------------------------------\n")
        for t in tokens:
            tipo, lexema, linea = t
            f.write(f"{tipo}\t{lexema}\t{linea}\n")

# --------------------------------------------
# Guardar la gramática en archivo
# --------------------------------------------

def guardar_gramatica(gramatica, ruta):
    asegurar_carpeta(ruta)

    with open(ruta, "w", encoding="utf-8") as f:
        for nt in gramatica:
            for prod in gramatica[nt]:
                p = " ".join(prod)
                f.write(f"{nt} -> {p}\n")

# --------------------------------------------
# Guardar FIRST en archivo
# --------------------------------------------

def guardar_first(first, ruta):
    asegurar_carpeta(ruta)

    with open(ruta, "w", encoding="utf-8") as f:
        for nt, valores in first.items():
            vals = ", ".join(sorted(list(valores)))
            f.write(f"FIRST({nt}) = {{ {vals} }}\n")

# --------------------------------------------
# Guardar FOLLOW en archivo
# --------------------------------------------

def guardar_follow(follow, ruta):
    asegurar_carpeta(ruta)

    with open(ruta, "w", encoding="utf-8") as f:
        for nt, valores in follow.items():
            vals = ", ".join(sorted(list(valores)))
            f.write(f"FOLLOW({nt}) = {{ {vals} }}\n")
