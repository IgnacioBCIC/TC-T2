
GRAMATICA = {
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
    ],
}


# AUXILIARES


def es_no_terminal(x):
    return x in GRAMATICA

def obtener_producciones(nt):
    return GRAMATICA[nt]
