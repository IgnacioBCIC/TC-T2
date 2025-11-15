# ============================================
#                 ANALIZADOR LÉXICO
# ============================================

import string

# Palabras reservadas del lenguaje academico reducido
RESERVADAS = {
    "print",
    "read"
}

# Simbolos simples 
SIMBOLOS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "%": "MOD",
    "=": "ASSIGN",
    "(": "PAR_A",
    ")": "PAR_C",
    ";": "PUNTO_COMA"
}

def es_letra(c):
    return c.isalpha() or c == "_"

def es_digito(c):
    return c.isdigit()

def analizar_lexico(texto):
    """
    Devuelve lista de tokens con la forma:
    (TIPO, LEXEMA, LINEA)
    """
    tokens = []
    i = 0
    linea = 1
    n = len(texto)

    while i < n:
        c = texto[i]

        # Saltos de línea
        if c == "\n":
            linea += 1
            i += 1
            continue

        # Espacios y tabulaciones
        if c in [" ", "\t", "\r"]:
            i += 1
            continue

        # Comentario de línea //
        if c == "/" and i + 1 < n and texto[i+1] == "/":
            i += 2
            while i < n and texto[i] != "\n":
                i += 1
            continue

        # Comentario multi-línea /* ... */
        if c == "/" and i + 1 < n and texto[i+1] == "*":
            i += 2
            while i + 1 < n and not (texto[i] == "*" and texto[i+1] == "/"):
                if texto[i] == "\n":
                    linea += 1
                i += 1
            i += 2
            continue

        # Símbolos simples
        if c in SIMBOLOS:
            tokens.append((SIMBOLOS[c], c, linea))
            i += 1
            continue

        # Identificadores y palabras reservadas
        if es_letra(c):
            lexema = c
            i += 1
            while i < n and (es_letra(texto[i]) or es_digito(texto[i])):
                lexema += texto[i]
                i += 1

            # Palabras reservadas print y read
            if lexema == "print":
                tokens.append(("PRINT", lexema, linea))
                continue

            if lexema == "read":
                tokens.append(("READ", lexema, linea))
                continue
            # IDENTIFICADOR NORMAL
            tokens.append(("ID", lexema, linea))
            continue

        # Números
        if es_digito(c):
            lexema = c
            i += 1
            while i < n and es_digito(texto[i]):
                lexema += texto[i]
                i += 1
            tokens.append(("NUM", lexema, linea))
            continue

        # Si no coincide nada, es desconocido
        tokens.append(("DESCONOCIDO", c, linea))
        i += 1

    return tokens
