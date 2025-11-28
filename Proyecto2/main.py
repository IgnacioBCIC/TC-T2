from gramatica.loader import cargar_gramatica_desde_txt
from generador.derivador import Derivator
from generador.mutador import Mutator
from generador.extremo import ExtremeGenerator
from generador.clasificador import Classifier
from generador.json import Exporter
from utils.metricas import compute_metrics

def main():
    print("\n===== GENERADOR AUTOMATICO DE EXPRESIONES =====")

    #  CARGAR GRAMATICA
    ruta = input("\nIngrese ruta de la gramatica (.txt): ")
    try:
        GRAMATICA = cargar_gramatica_desde_txt(ruta)
        print("[OK] Gramatica cargada correctamente.")
    except:
        print("[ERROR] No se pudo cargar la gramatica.")
        return

    #  CONFIGURACION USUARIO

    n_validas = int(input("\nCantidad de cadenas validas: "))
    n_invalidas = int(input("Cantidad de cadenas invalidas: "))
    n_extremas = int(input("Cantidad de cadenas extremas: "))

    profundidad = int(input("\nProfundidad maxima de derivacion (ej. 6): "))

    max_length_extremos = int(input("Longitud maxima para casos extremos (ej. 200): "))

    # Preparar componentes
    deriv = Derivator(max_depth=profundidad)
    mut = Mutator()
    classify = Classifier()
    export = Exporter()
    extreme = ExtremeGenerator(deriv)

    casos = []

    #  Generar validas
    for _ in range(n_validas):
        v = deriv.generate()
        casos.append({"cadena": v, "tipo": classify.classify(v, "valid")})

    #  Generar invalidas

    for _ in range(n_invalidas):
        base = deriv.generate()
        inv = mut.mutate(base)
        casos.append({"cadena": inv, "tipo": classify.classify(inv, "invalid")})

    # Generar extremas configurables
    for _ in range(n_extremas):
        expr = extreme.long_expression(
            repetitions=20,
            max_length=max_length_extremos
        )
        casos.append({"cadena": expr, "tipo": classify.classify(expr, "extreme")})


    #  Metricas

    metrics = compute_metrics(casos)
    print("\n=== MÉTRICAS ===")
    print(metrics)

    #  Exportar
    export.export(casos)
    print("\n[OK] Casos exportados en output/casos.json")


if __name__ == "__main__":
    main()
