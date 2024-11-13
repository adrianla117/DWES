from operaciones import suma, resta, multiplicacion, division

def calculadora():
    while True:
        try:
            a = float(input("Introduce el primer número: "))
            b = float(input("Introduce el segundo número: "))

            print("\nElige una operación: ")
            print("1. Suma")
            print("2. Resta")
            print("3. Multiplicación")
            print("4. División")
            opcion = input("Introduce el número de la operación (1, 2, 3, 4): ")

            if opcion == "1":
                resultado = suma(a, b)
                print(f"Resultado de la suma: {resultado}")
            elif opcion == "2":
                resultado = resta(a, b)
                print(f"Resultado de la resta: {resultado}")
            elif opcion == "3":
                resultado = multiplicacion(a, b)
                print(f"Resultado de la multiplicación: {resultado}")
            elif opcion == "4":
                resultado = division(a, b)
                print(f"Resultado de la división: {resultado}")
            else:
                print("Opción no válida.")
                continue

            pregunta = input("Otra operación? (s/n)")
            if pregunta != "s":
                print("Cálculo finalizado")
                break

        except ValueError:
            print("Error: Por favor, introduce un número válido.")
        except Exception as e:
            print(f"Un error ha aparecido: {e}")

if __name__ == "__main__":
    calculadora()