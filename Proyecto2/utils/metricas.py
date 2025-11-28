from utils.helper import count_operators, count_parentheses_depth

def compute_metrics(cases):
    total = len(cases)
    valid = sum(1 for c in cases if c["tipo"] == "valida")
    invalid = sum(1 for c in cases if c["tipo"] == "invalida")
    extreme = sum(1 for c in cases if c["tipo"] == "extrema")

    return {
        "total_cadenas": total,
        "porcentajes": {
            "validas": valid / total * 100,
            "invalidas": invalid / total * 100,
            "extremas": extreme / total * 100
        },
        "longitudes": [len(c["cadena"]) for c in cases],
        "operadores": [count_operators(c["cadena"]) for c in cases],
        "profundidades": [count_parentheses_depth(c["cadena"]) for c in cases]
    }
