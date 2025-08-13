suma = 0
while True:
    try:
        numero = int(input("Ingrese un número entero (Ctrl-C para salir): "))
        suma += numero
    except ValueError:
        print("Error: Debe ingresar un número entero.")
    except KeyboardInterrupt:
        print("\nSaliendo...")
        break  # rompe el bucle while True
    else:
        print(f"Suma parcial: {suma}")
print(f"Total acumulado: {suma}")