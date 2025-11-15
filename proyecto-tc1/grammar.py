# ============================================
#                DEFINICIÓN DE LA GRAMÁTICA
# ============================================

"""
Gramática formal del lenguaje reducido LL(1):

S           → STMT_LIST

STMT_LIST   → STMT STMT_LIST
            → ε

STMT        → ASSIGN_STMT PUNTO_COMA
            → PRINT_STMT  PUNTO_COMA
            → READ_STMT   PUNTO_COMA

ASSIGN_STMT → ID ASSIGN EXPR      (ID = EXPR)

PRINT_STMT  → PRINT PAR_A EXPR PAR_C
READ_STMT   → READ_PAR
READ_PAR    → READ PAR_A ID PAR_C     (read(id))

EXPR        → TERM EXPR_P
EXPR_P      → PLUS TERM EXPR_P
            → MINUS TERM EXPR_P
            → ε

TERM        → FACTOR TERM_P
TERM_P      → MULT FACTOR TERM_P
            → DIV FACTOR TERM_P
            → MOD FACTOR TERM_P
            → ε

FACTOR      → NUM
            → ID
            → PAR_A EXPR PAR_C
"""

# TERMINALES
TERMINALES = {
    "ID",
    "NUM",
    "PUNTO_COMA",
    "ASSIGN",       # token '=' del lexer
    "PLUS",         # +
    "MINUS",        # -
    "MULT",         # *
    "DIV",          # /
    "MOD",          # %
    "PAR_A",        # (
    "PAR_C",        # )
    "PRINT",        # palabra reservada print
    "READ"          # palabra reservada read
}

# ------------------------------------------------------
# GRAMÁTICA COMO DICCIONARIO:
# ------------------------------------------------------

GRAMATICA = {
    "S": [["STMT_LIST"]],

    "STMT_LIST": [
        ["STMT", "STMT_LIST"],
        ["ε"]
    ],

    "STMT": [
        ["ASSIGN_STMT", "PUNTO_COMA"],
        ["PRINT_STMT", "PUNTO_COMA"],
        ["READ_STMT", "PUNTO_COMA"]
    ],

    "ASSIGN_STMT": [
        ["ID", "ASSIGN", "EXPR"]
    ],

    "PRINT_STMT": [
        ["PRINT", "PAR_A", "EXPR", "PAR_C"]
    ],

    "READ_STMT": [
        ["READ_PAR"]
    ],

    "READ_PAR": [
        ["READ", "PAR_A", "ID", "PAR_C"]
    ],

    "EXPR": [
        ["TERM", "EXPR_P"]
    ],

    "EXPR_P": [
        ["PLUS", "TERM", "EXPR_P"],
        ["MINUS", "TERM", "EXPR_P"],
        ["ε"]
    ],

    "TERM": [
        ["FACTOR", "TERM_P"]
    ],

    "TERM_P": [
        ["MULT", "FACTOR", "TERM_P"],
        ["DIV", "FACTOR", "TERM_P"],
        ["MOD", "FACTOR", "TERM_P"],
        ["ε"]
    ],

    "FACTOR": [
        ["NUM"],
        ["ID"],
        ["PAR_A", "EXPR", "PAR_C"]
    ]
}

# ------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------

def obtener_no_terminales():
    return list(GRAMATICA.keys())

def obtener_terminales():
    # Descubrir símbolos terminales automáticamente
    ts = set()
    for prods in GRAMATICA.values():
        for prod in prods:
            for simbolo in prod:
                if simbolo not in GRAMATICA and simbolo != "ε":
                    ts.add(simbolo)
    return ts

def obtener_producciones(nt):
    return GRAMATICA[nt]

def es_no_terminal(x):
    return x in GRAMATICA
