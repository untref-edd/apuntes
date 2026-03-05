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
description: Tipos de datos fundamentales en Python.
---

# Tipos de datos

Python tiene varios tipos de datos integrados. A continuación, veremos los más usados: **números**, **cadenas**, **listas**, **tuplas** y **diccionarios**.

## Tipos numéricos

`int`
: Números enteros positivos o negativos, de cualquier tamaño. Los enteros se representan en memoria como una secuencia de bits, limitados por la memoria disponible

`float`
: Números con parte decimal, representados en memoria como un conjunto de bits en punto flotante

`complex`
: Números complejos, representados en memoria como dos números de punto flotante

### Ejemplos

```python
a = 5  # int
b = 3.14  # float
c = 2 + 3j  # complex
```

Existen varias maneras de representar o crear números complejos

```python
import math

z1 = math.sqrt(-1)  # Número complejo (0+j)
```

```python
z2 = complex(0, 1)  # También se puede crear un número complejo directamente
```

```python
z3 = 1j  # Representación alternativa de un número complejo
```

### Operaciones comunes

```python
x = 10 + 5
y = 10 / 3  # división real
u = 10 // 3  # división entera
w = 2**3  # potencia
v = 10 % 3  # módulo
```

### Conversión de tipos

En Python los tipos numéricos se pueden convertir entre sí, ya sea de forma explícita o implícita.

```{code-cell} python
---
tags: hide-output
---
float(5)
```

```{code-cell} python
---
tags: hide-output
---
int(3.7)
```

```{code-cell} python
---
tags: hide-output
---
x = 10 + 5.5

x
```

Un operador útil para verificar el tipo de una variable es `type()`:

```{code-cell} python
---
tags: hide-output
---
y = 10 + (2 - 3j)

type(y)
```

Es importante no confundir el tipado dinámico de Python con un tipado débil. Aunque el tipo de una variable se determina en tiempo de ejecución, Python es un lenguaje fuertemente tipado, lo que significa que las operaciones entre tipos incompatibles generarán un error.

```{code-cell} python
---
tags: raises-exception
---
x = 5 + "10"
```

````{admonition} Tipado débil vs fuertemente tipado
---
class: hint
---
El tipado débil se puede definir, por oposición a fuertemente tipado, como la capacidad de realizar operaciones entre tipos incompatibles. Por ejemplo en lenguajes como JavaScript, se puede sumar un número con una cadena de caracteres.

```javascript
x = 5 + "10"

console.log("El valor de x es:", x);
console.log("El tipo de dato de x es:", typeof x);
```

```output
El valor de x es: 510
El tipo de dato de x es: string
```
````

## Cadenas de caracteres (`str`)

Una cadena es una secuencia **inmutable** de caracteres.

Un objeto **inmutable** es aquel cuyo contenido no puede ser modificado una vez creado. En el caso de las cadenas, esto significa que no se pueden cambiar los caracteres individuales de una cadena después de su creación.

```{code-cell} python
---
tags: raises-exception
---
mensaje = "Hola, mundo"
mensaje[0] = "h"
```

Si quiero modificar una cadena, debo crear una nueva cadena con el contenido deseado:

```{code-cell} python
---
tags: hide-output
---
mensaje = "Hola, mundo"
mensaje = "h" + mensaje[1:]

mensaje
```

En la segunda línea se crea una nueva cadena con el contenido deseado y se asigna nuevamente a la variable `mensaje`, lo que da la sensación de que se ha modificado la cadena original, pero en realidad se ha creado una nueva cadena, y el contenido original de `mensaje` se ha perdido.

### Indexado y _slicing_

Las cadenas de caracteres están indexadas, es decir, que se puede manipular cada carácter por su posición. El primer carácter tiene índice 0, el segundo 1, y así sucesivamente. También se pueden usar índices negativos para acceder a los caracteres desde el final de la cadena, y tajadas o _slicing_ para obtener subcadenas. En las tajadas, el primer parámetro es el índice inicial y el segundo es el índice final (sin incluir), similar a Go.

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[0]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[-1]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[1:4]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[:2]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[2:]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[-3:]
```

Las tajadas o _slices_ en Python tienen un tercer parámetro opcional que indica el paso entre los índices. Por ejemplo, `nombre[::2]` devuelve cada segundo carácter de la cadena.

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[::2]
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"

nombre[::-1]
```

### Métodos útiles para manipular cadenas

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

texto.upper()
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

texto.lower()
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

texto.replace("mundo", "Python")
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

texto.split()
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

"Python" in texto
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"

len(texto)
```

### Concatenación

Las cadenas se pueden concatenar usando el operador `+` o multiplicar por un número entero para repetirlas.

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola " + "mundo"

saludo
```

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola mundo"

saludo * 3
```

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola mundo"

(saludo + ". ") * 3
```

### Iteración sobre cadenas de caracteres

Las cadenas de caracteres son **iterables**, lo que significa que se pueden recorrer carácter por carácter usando un bucle `for`.

```{code-cell} python
---
tags: hide-output
---
for caracter in "Python":
    print(caracter)
```

### Formateo de cadenas

El formateo de cadenas permite insertar valores en una cadena de texto de manera más legible y flexible. Hay varias formas de hacerlo:

- Usando el método `format()`

```{code-cell} python
---
tags: hide-output
---
nombre = "Juan"
edad = 30

"Hola, mi nombre es {} y tengo {} años.".format(nombre, edad)
```

- Usando f-strings (Python 3.6+)

```{code-cell} python
---
tags: hide-output
---
nombre = "Ana"
edad = 32

f"Hola, mi nombre es {nombre} y tengo {edad} años."
```

La letra `f` antes de la cadena indica que es una f-string, lo que permite insertar variables directamente dentro de llaves `{}`.

- Usando el operador `%` (menos recomendado)

```{code-cell} python
---
tags: hide-output
---
nombre = "Eva"
edad = 28

"Hola, mi nombre es %s y tengo %d años." % (nombre, edad)
```

El carácter `%` se usa para formatear cadenas, donde `%s` es un marcador de posición para una cadena y `%d` para un número entero, pero es menos legible y flexible que las otras opciones.

El carácter de escape `\` se utiliza para insertar caracteres especiales en una cadena, como comillas, saltos de línea o tabulaciones.

```{code-cell} python
---
tags: hide-output
---
mensaje = "Hola, \"mundo\".\n¿Cómo estás?"

print(mensaje)
```

`\n` inserta un salto de línea, y `\"` permite incluir comillas dobles dentro de una cadena delimitada por comillas dobles.

Otra forma de usar comillas dobles en una cadena es usar comillas simples para delimitar la cadena:

```{code-cell} python
---
tags: hide-output
---
mensaje = 'Hola, "mundo".\n¿Cómo estás?'

print(mensaje)
```

```{code-cell} python
---
tags: hide-output
---
mensaje = "Hola, \tmundo."

print(mensaje)
```

## Listas (`list`)

Las listas son colecciones **ordenadas**, **polimórficas** y **mutables** de elementos.

Ordenadas
: Los elementos de una lista tienen un orden definido, dado por su posición.

Polimórficas
: Las listas pueden contener elementos de diferentes tipos, como enteros, cadenas, flotantes, etc.

Mutables
: Los elementos de una lista pueden ser modificados, añadidos o eliminados después de su creación.

### Operaciones básicas

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]
numeros.append(5)

numeros
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]

numeros[0]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]

numeros[1:3]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]
numeros.remove(3)

numeros
```

```{code-cell} python
---
tags: hide-output
---
mezcla = [1, "dos", 3.0, True]
mezcla[0] = "uno"

mezcla
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]
mezcla = [1, "dos", 3.0, True]

mezcla + numeros
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]

numeros * 2
```

La lista vacía se puede definir con corchetes vacíos `[]` o con la función `list()`:

```{code-cell} python
---
tags: hide-output
---
lista_vacia = []

lista_vacia
```

```{code-cell} python
---
tags: hide-output
---
lista_vacia2 = list()

lista_vacia2
```

### Iteración sobre listas

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]

for n in numeros:
    print(n)
```

## Tuplas (`tuple`)

Son similares a las listas, **ordenadas** y **polimórficas**, pero **inmutables**, es decir, una vez creada no se puede modificar.

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)

type(coordenadas)
```

Se definen con paréntesis y pueden contener diferentes tipos de datos, mientras que las listas se definen con corchetes.

### Acceso

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)

coordenadas[0]
```

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)

coordenadas[-1]
```

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)

coordenadas[1:]
```

### Ventajas

- Más livianas que las listas.
- Se pueden usar como claves en diccionarios y se pueden empaquetar varios valores en una sola variable, lo que permite que las funciones puedan devolver múltiples valores, o usar tuplas como claves en diccionarios, entre otros usos.

La forma de empaquetar y desempaquetar tuplas es similar a las listas:

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)
a, b, c = coordenadas

print("a =", a)
print("b =", b)
print("c =", c)
```

```{code-cell} python
---
tags: hide-output
---
a = 10.0
b = 20.5
c = 1

(a, b, c)
```

La tupla vacía se puede definir con paréntesis vacíos `()` o con la función `tuple()`:

```{code-cell} python
---
tags: hide-output
---
tupla_vacia = ()

tupla_vacia
```

```{code-cell} python
---
tags: hide-output
---
tupla_vacia2 = tuple()

tupla_vacia2
```

### Anidamiento

Tanto las listas como las tuplas se pueden anidar, es decir, se pueden incluir dentro de otras listas o tuplas.

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])

for elemento in tupla_anidada:
    print(elemento)
```

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])

tupla_anidada[3][0]
```

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])
tupla_anidada[3].append(7)

tupla_anidada
```

La tupla no se modificó, sigue teniendo 4 elementos, pero la lista que está adentro de la tupla sí se puede modificar.

Las tuplas se pueden iterar de la misma manera que las listas.

## Diccionarios (`dict`)

Almacenan pares clave-valor. Las claves deben ser únicas e inmutables (por ejemplo, strings, números o tuplas).

```{code-cell} python
---
tags: hide-output
---
d = dict()
d["clave1"] = "valor1"
d[25] = "valor2"
d[(1, 2)] = "valor3"

d
```

También se pueden crear diccionarios, de forma explícita, usando llaves `{}`:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}

persona
```

### Acceso y modificación

Los diccionarios permiten acceder a los valores mediante sus claves. También se pueden modificar, añadir o eliminar pares clave-valor. La sintaxis es similar a las listas o tuplas, pero en lugar de índices, se utilizan claves.

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}

persona["nombre"]
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
persona["edad"] = 31

persona
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
persona["email"] = "ana@mail.com"

persona
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
del persona["edad"]

persona
```

### Métodos útiles

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}

persona.keys()
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}

persona.values()
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}

persona.items()
```

Un método muy útil es `get()`, que permite acceder a un valor sin generar un error si la clave no existe:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}

print(persona.get("nombre", "No encontrado"))
print(persona.get("edad", "No encontrado"))
```

`setdefault()` es otro método que permite acceder a un valor y, si la clave no existe, añadirla con un valor por defecto:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}

print(persona.setdefault("edad", 30))

persona
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
lista = persona.setdefault("telefonos", [])
lista.append("123-456-7890")

persona
```

### Iteración sobre diccionarios

Los diccionarios se pueden iterar para acceder a las claves y valores.

```{code-cell} python
---
tags: hide-output
---
for clave, valor in persona.items():
    print(f"{clave}: {valor}")
```

## Conjuntos (`set`)

Los conjuntos son colecciones **no ordenadas** de elementos únicos. No permiten duplicados y no tienen un índice asociado a sus elementos.

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5}

conjunto
```

El conjunto vacío se puede definir con la función `set()`:

```{code-cell} python
---
tags: hide-output
---
conjunto_vacio = set()

conjunto_vacio
```

```{code-cell} python
---
tags: hide-output
---
conjunto_vacio2 = {}

type(conjunto_vacio2)
```

Para agregar un elemento a un conjunto, se utiliza el método `add()`:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5}
conjunto.add(6)

conjunto
```

Si intentamos agregar un elemento que ya existe, no se producirá un error, pero el conjunto no cambiará:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.add(6)

conjunto
```

Se puede crear un conjunto a partir de una lista o tupla usando la función `set()`:

```{code-cell} python
---
tags: hide-output
---
lista = [1, 2, 3, 4, 5, 5]
conjunto_desde_lista = set(lista)

conjunto_desde_lista
```

Para eliminar un elemento de un conjunto, se utiliza el método `remove()` o `discard()`. La diferencia es que `remove()` genera un error si el elemento no existe, mientras que `discard()` no lo hace:

```{code-cell} python
---
tags: raises-exception
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.remove(7)
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.discard(7)  # No genera error

conjunto
```

El operador `in` se puede usar para verificar si un elemento está en un conjunto:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}

3 in conjunto
```

No se puede acceder a los elementos de un conjunto por índice, ya que no están ordenados. Sin embargo, se pueden iterar:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}

for elemento in conjunto:
    print(elemento)
```

Los conjuntos son útiles para realizar operaciones matemáticas como unión, intersección, diferencia y diferencia simétrica.

### Operaciones con conjuntos

```{code-cell} python
---
tags: hide-output
---
# Unión
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}

print(conjunto1, " union ", conjunto2, "=", conjunto1 | conjunto2)
```

```{code-cell} python
---
tags: hide-output
---
# Intersección
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}

print(conjunto1, " interseccion ", conjunto2, "=", conjunto1 & conjunto2)
```

```{code-cell} python
---
tags: hide-output
---
# Diferencia
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}

print(conjunto1, " diferencia ", conjunto2, "=", conjunto1 - conjunto2)
print(conjunto2, " diferencia ", conjunto1, "=", conjunto2 - conjunto1)
```

```{code-cell} python
---
tags: hide-output
---
# Diferencia simétrica
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}

print(f"{conjunto1} diferencia simetrica {conjunto2} = "
      f"{conjunto1 ^ conjunto2}")

print(f"{conjunto2} diferencia simetrica {conjunto1} = "
      f"{conjunto2 ^ conjunto1}")
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}

es_subconjunto = {1, 2} <= conjunto
print("{1, 2} es subconjunto de", conjunto, "?: ", es_subconjunto)
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}

es_superconjunto = {1, 2} >= conjunto
print("{1, 2} es superconjunto de", conjunto, "?: ", es_superconjunto)
```

Existen otros tipos de conjuntos que permiten almacenar elementos únicos, pero que una vez creados no se pueden modificar, se llaman **conjuntos inmutables** o **frozensets**. Se crean usando la función `frozenset()`:

```{code-cell} python
---
tags: hide-output
---
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])

conjunto_inmutable
```

Los conjuntos inmutables son útiles cuando se necesita un conjunto que no cambie a lo largo del tiempo, por ejemplo, como claves en un diccionario o elementos en otro conjunto.

Los métodos de los conjuntos inmutables son limitados, ya que no se pueden modificar. Por ejemplo, no se pueden usar `add()` o `remove()`, pero sí se pueden usar operaciones como unión, intersección y diferencia.

```{code-cell} python
---
tags: hide-output
---
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
conjunto2 = frozenset([4, 5, 6, 7])

print(conjunto_inmutable | conjunto2)  # Unión
print(conjunto_inmutable & conjunto2)  # Intersección
print(conjunto_inmutable - conjunto2)  # Diferencia
print(conjunto2 - conjunto_inmutable)  # Diferencia
print(conjunto_inmutable ^ conjunto2)  # Diferencia simétrica
```

El resultado de estas operaciones es un nuevo conjunto inmutable, ya que el conjunto original no se modifica.

## Generación de colecciones de datos por comprensión (_comprehension_)

Las comprensiones de listas, tuplas y diccionarios son una forma concisa de crear colecciones en Python. Permiten aplicar una expresión a cada elemento de una colección existente, filtrando o transformando los elementos según sea necesario.

```{code-cell} python
---
tags: hide-output
---
numeros = [x for x in range(1, 6)]

[x**2 for x in numeros]
```

Si en lugar de corchetes `[]` se usan paréntesis `()`, se crea un **generador**, no una tupla. Para obtener una tupla, debemos usar el constructor `tuple()`:

```{code-cell} python
---
tags: hide-output
---
numeros = tuple(x for x in range(1, 6))

tuple(x**2 for x in numeros)
```

Si se usan llaves `{}`, se crea un conjunto o un diccionario, dependiendo de si se especifica una clave o un par clave-valor:

```{code-cell} python
---
tags: hide-output
---
numeros = {x for x in range(1, 6)}

{x**2 for x in numeros}
```

```{code-cell} python
---
tags: hide-output
---
numeros = {"uno": 1, "dos": 2, "tres": 3}

{clave: valor**2 for clave, valor in numeros.items()}
```

```{code-cell} python
---
tags: hide-output
---
diccionario = {"nombre": "Ana", "edad": 30, "email": "ana@example.com"}

[(clave, valor) for clave, valor in diccionario.items()]
```

La comprensión es una característica funcional de Python muy poderosa.

## Recursos para profundizar

- [Tutorial de Python - Estructuras de datos](https://docs.python.org/es/3/tutorial/datastructures.html)
- [`setdefault()` (KeepCoding)](https://keepcoding.io/blog/que-es-dict-setdefault-en-python-y-su-uso/)
- [Comprensiones de listas (Python Docs)](https://docs.python.org/es/3/tutorial/datastructures.html#list-comprehensions)
- [Comprensión de listas (Hektor Profe)](https://hektorprofe.github.io/python/funcionalidades-avanzadas/comprension-de-listas/)
- [Operadores Encadenados (Hektor Profe)](https://hektorprofe.github.io/python/funcionalidades-avanzadas/operadores-encadenados/)
- [Intérprete Python, para entender como funciona](https://pythontutor.com/python-compiler.html#mode=edit)
