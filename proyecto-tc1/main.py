from lexer import analizar_lexico
from grammar import *
from parsing_table import *
from utils import *

def main():
    contenido = None
    tokens = None
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Cargar archivo")
        print("2. Ejecutar análisis léxico")
        print("3. Guardar tokens")
        print("4. Guardar gramática")
        print("5. Guardar gramática sin recursión")
        print("6. Guardar FIRST")
        print("7. Guardar FOLLOW")
        print("8. Guardar tabla LL(1)")
        print("9. Ejecutar TODO el proceso")
        print("0. Salir")

        op = input("> ")

        if op == "1":
            ruta = input("Ruta del archivo: ")
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                print("[OK] Archivo cargado.")
            except:
                print("[ERROR] Archivo no válido.")

        elif op == "2":
            if not contenido:
                print("Debe cargar un archivo primero.")
                continue
            tokens = analizar_lexico(contenido)
            for t in tokens:
                print(t)

        elif op == "3":
            guardar_tokens(tokens, "output/tokens.txt")
            print("[OK] Tokens guardados.")

        elif op == "4":
            guardar_gramatica(GRAMATICA, "output/gramatica.txt")
            print("[OK] Gramática guardada.")

        elif op == "5":
            guardar_gramatica(GRAMATICA, "output/gramatica_sin_recursion.txt")
            print("[OK] Gramática sin recursión guardada.")

        elif op == "6":
            F = calcular_first(GRAMATICA)
            guardar_first(F, "output/first.txt")
            print("[OK] FIRST guardado.")

        elif op == "7":
            F = calcular_first(GRAMATICA)
            W = calcular_follow(GRAMATICA, F)
            guardar_follow(W, "output/follow.txt")
            print("[OK] FOLLOW guardado.")

        elif op == "8":
            F = calcular_first(GRAMATICA)
            W = calcular_follow(GRAMATICA, F)
            T = generar_tabla_LL1(GRAMATICA, F, W)
            guardar_tabla(T, "output/tabla_LL1.csv")
            print("[OK] Tabla LL(1) guardada.")

        elif op == "9":
            if not contenido:
                print("Debe cargar un archivo primero.")
                continue

            tokens = analizar_lexico(contenido)
            guardar_tokens(tokens, "output/tokens.txt")

            guardar_gramatica(GRAMATICA, "output/gramatica.txt")
            guardar_gramatica(GRAMATICA, "output/gramatica_sin_recursion.txt")

            F = calcular_first(GRAMATICA)
            guardar_first(F, "output/first.txt")

            W = calcular_follow(GRAMATICA, F)
            guardar_follow(W, "output/follow.txt")

            T = generar_tabla_LL1(GRAMATICA, F, W)
            guardar_tabla(T, "output/tabla_LL1.csv")

            print("[OK] Proceso completo finalizado.")

        elif op == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
