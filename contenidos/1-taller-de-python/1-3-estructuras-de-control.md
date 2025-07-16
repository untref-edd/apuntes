---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Estructuras de Control en Python

## Condicionales

### Sintaxis `if-elif-else`

```{code-cell}
# Sintaxis completa
edad = 25
salario = 45000

if edad < 18:
    categoria = "menor"
elif edad < 65 and salario > 30000:
    categoria = "adulto solvente"
elif edad < 65:
    categoria = "adulto"
else:
    categoria = "jubilado"

print(f"Categoría: {categoria}")
```

### Operadores lógicos y comparación

```{code-cell}
# Python usa palabras en lugar de símbolos
x, y, z = 5, 10, 15 

# Equivalentes a && || ! en otros lenguajes
if x < y and y < z:          # and = && en Java/Go
    print("Orden ascendente")

if x == 5 or y == 5:         # or = || en Java/Go
    print("Alguno es 5")

if not (x > y):              # not = ! en Java/Go
    print("x no es mayor que y")

# Comparaciones encadenadas (única de Python)
if x < y < z:
    print("Orden ascendente (sintaxis pythónica)")
```

### Expresión condicional (operador ternario)

```{code-cell}
# Equivalente al operador ?: de Java/Go
numero = 7
resultado = "par" if numero % 2 == 0 else "impar"
print(f"El número {numero} es {resultado}")
```

El fragmento anterior es una forma concisa de asignar un valor basado en una condición. Es útil para asignaciones simples y mejora la legibilidad del código. Es equivalente a:

```{code-cell}
if numero % 2 == 0:
    resultado = "par"
else:
    resultado = "impar"
print(f"El número {numero} es {resultado}")
```

## Ciclos

### Ciclo `for` - Iteración sobre secuencias

```{code-cell}
# for-in: itera directamente sobre elementos (no índices)
frutas = ["manzana", "banana", "naranja"]

for fruta in frutas:
  print(fruta)
```

```{code-cell}
# Con índices usando enumerate()
frutas = ["manzana", "banana", "naranja"]

for i, fruta in enumerate(frutas):
  print(f"{i}: {fruta}")
```

La función `enumerate()` es útil para obtener tanto el índice como el valor del elemento en una lista.

```{code-cell}
help(enumerate)
```

```{code-cell}
# Equivalente a for(int i=0; i<frutas.length; i++) en Java
frutas = ["manzana", "banana", "naranja"]

for i in range(len(frutas)):
  print(f"{i}: {frutas[i]}")
```

### Función `range()` para ciclos numéricos

La función `range()` genera una secuencia de números, útil para ciclos `for`. Es como si generara una lista de números, pero de forma más eficiente.

La sintaxis de `range()` es:

```python
range(start, stop[, step])
```

```{code-cell}
# range(stop)
for i in range(5):          # 0, 1, 2, 3, 4
  print(i)
```

```{code-cell}
# range(start, stop)
for i in range(1, 5):       # 1, 2, 3, 4
  print(i)
```

```{code-cell}
# range(start, stop, step)
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
  print(i)
```

```{code-cell}
# Decremento
for i in range(10, 0, -1):  # 10, 9, 8, ..., 1
  print(i)
```

### Ciclo `while`

```{code-cell}
# Sintaxis similar a otros lenguajes
contador = 0
while contador < 5:
    print(f"Contador: {contador}")
    contador += 1
```

```python
# Ciclo infinito con break
while True:
    respuesta = input("¿Continuar? (s/n): ")
    if respuesta.lower() != 's':
        break
```

### `break`, `continue` y `else` en ciclos

```{code-cell}
# break y continue funcionan igual que en otros lenguajes
for i in range(10):
    if i == 3:
        continue    # Salta a la siguiente iteración
    if i == 7:
        break       # Sale del ciclo
    print(i)        # Imprime: 0, 1, 2, 4, 5, 6
```

```{code-cell}
# else en ciclos: ÚNICO DE PYTHON
# Se ejecuta si el ciclo termina normalmente (sin break)
for i in range(5):
    if i == 10:  # Nunca se cumple
        break
else:
    print("Ciclo completado sin break")  # Se ejecuta
```

```{code-cell}
# Ejemplo práctico: búsqueda
numeros = [1, 3, 5, 7, 9]
objetivo = 6

for num in numeros:
    if num == objetivo:
        print(f"Encontrado: {num}")
        break
else:
    print("No encontrado")  # Se ejecuta porque no hubo break
```

## Iteración sobre estructuras de datos

### Diccionarios

```{code-cell}
# Solo claves
datos = {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"}

for clave in datos:
  print(clave)
```

```{code-cell}
# Solo valores
datos = {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"}

for valor in datos.values():
  print(valor)
```

```{code-cell}
# Claves y valores
datos = {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"}

for clave, valor in datos.items():
  print(f"{clave}: {valor}")
```

### Listas con múltiples variables

```{code-cell}
# Desempaquetado en ciclos
puntos = [(1, 2), (3, 4), (5, 6)]

for x, y in puntos:
  print(f"x={x}, y={y}")
```

```{code-cell}
# Con enumerate para índice + desempaquetado
puntos = [(1, 2), (3, 4), (5, 6)]
for i, (x, y) in enumerate(puntos):
  print(f"Punto {i}: ({x}, {y})")
```

## No hay `switch` 

Python 3.10+ tiene match-case, pero la siguiente construcción usando `if-elif` es más común.

```{code-cell}
opcion = "b"

if opcion == "a":
    resultado = "Opción A"
elif opcion == "b":
    resultado = "Opción B"
elif opcion in ["c", "d"]:
    resultado = "Opción C o D"
else:
    resultado = "Opción desconocida"

print(resultado)
```

## Ejemplo práctico: Procesamiento de datos

```{code-cell}
# Procesamiento típico de datos en Python
empleados = [
    {"nombre": "Ana", "salario": 50000, "departamento": "IT"},
    {"nombre": "Carlos", "salario": 45000, "departamento": "Ventas"},
    {"nombre": "María", "salario": 55000, "departamento": "IT"},
    {"nombre": "Juan", "salario": 40000, "departamento": "RRHH"}
]

# Filtrar y procesar con sintaxis pythónica
for empleado in empleados:
    nombre = empleado["nombre"]
    salario = empleado["salario"]
    
    # Determinar categoría y bonus
    if salario >= 50000:
        categoria = "Senior"
        bonus = salario * 0.15
    elif salario >= 45000:
        categoria = "Mid"
        bonus = salario * 0.10
    else:
        categoria = "Junior"
        bonus = salario * 0.05
    
    print(f"{nombre}: {categoria} - Bonus: ${bonus:,.2f}")
```

## Diferencias sintácticas resumidas

| Característica | Python | Java/Go |
|---------------|--------|---------|
| Delimitadores | Indentación | `{ }` |
| Operadores lógicos | `and`, `or`, `not` | `&&`, `\|\|`, `!` |
| Ciclo for | `for item in collection:` | `for (type item : collection)` |
| else en ciclos | ✅ Disponible | ❌ No disponible |
| Operador ternario | `value_if_true if condition else value_if_false` | `condition ? value_if_true : value_if_false` |
| switch/match | `if-elif` o `match-case` (3.10+) | `switch` |

La sintaxis de Python prioriza la legibilidad y expresividad, usando palabras en inglés en lugar de símbolos cuando es posible.