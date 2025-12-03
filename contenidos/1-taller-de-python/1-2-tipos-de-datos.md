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

### Operaciones comunes

```python
import math

x = 10 + 5  # suma
y = 10 / 3  # división (devuelve float)
u = 10 // 3  # división entera
w = 2**3  # potencia
v = 10 % 3  # módulo (resto de la división)
z = math.sqrt(-1)  # Número complejo (0+j)
z2 = complex(0, 1)  # También se puede crear un número complejo directamente
z3 = 1j  # Representación alternativa de un número complejo
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
x = 10 + 5.5  # Implícitamente convierte el int a float
print(x)
```

Un operador útil para verificar el tipo de una variable es `type()`:

```{code-cell} python
---
tags: hide-output
---
y = 10 + (2 - 3j)  # (12-3j)
print(type(y))
```

Es importante no confundir el tipado dinámico de Python con un tipado débil. Aunque el tipo de una variable se determina en tiempo de ejecución, Python es un lenguaje fuertemente tipado, lo que significa que las operaciones entre tipos incompatibles generarán un error.


```{code-cell} python
---
tags: hide-output, raises-exception
---
# Esto generará un error de tipo
x = 5 + "10"
```

````{admonition} Tipado débil vs fuertemente tipado
:class: hint
El tipado débil se puede definir, por oposición a fuertemente tipado, como la capacidad de realizar operaciones entre tipos incompatibles. Por ejemplo en lenguajes como JavaScript, se puede sumar un número con una cadena de caracteres.
```{code-block} javascript
x = 5 + "10"
console.log("El valor de x es:", x);
console.log("El tipo de dato de x es:", typeof x);
```
```text
El valor de x es: 510
El tipo de dato de x es: string
```
````

## Cadenas de caracteres (`str`)

Una cadena es una secuencia **inmutable** de caracteres.

Un objeto **inmutable** es aquel cuyo contenido no puede ser modificado una vez creado. En el caso de las cadenas, esto significa que no se pueden cambiar los caracteres individuales de una cadena después de su creación.

```{code-cell} python
---
tags: hide-output, raises-exception
---
mensaje = "Hola, mundo"
mensaje[0] = "h"  # Esto generará un error
```

Si quiero modificar una cadena, debo crear una nueva cadena con el contenido deseado:

```{code-cell} python
---
tags: hide-output
---
mensaje = "Hola, mundo"
mensaje = "h" + mensaje[1:]  # Crea una nueva cadena
print(mensaje) # 'hola, mundo'
```

En la segunda línea se crea una nueva cadena con el contenido deseado y se asigna nuevamente a la variable `mensaje`, lo que da la sensación de que se ha modificado la cadena original, pero en realidad se ha creado una nueva cadena, y el contenido original de `mensaje` se ha perdido.

### Indexado y _slicing_

Las cadenas de caracteres están indexadas, es decir, que se puede manipular cada carácter por su posición. El primer carácter tiene índice 0, el segundo 1, y así sucesivamente. También se pueden usar índices negativos para acceder a los caracteres desde el final de la cadena, y tajadas o *slicing* para obtener subcadenas. En las tajadas, el primer parámetro es el índice inicial y el segundo es el índice final (no incluido), similar a Go.

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[0]) # 'P'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[-1]) # 'n'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[1:4]) # 'yth'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[:2]) # 'Py'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[2:]) # 'thon'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[-3:]) # 'hon'
```

Las tajadas o _slices_ en Python tienen un tercer parámetro opcional que indica el paso entre los índices. Por ejemplo, `nombre[::2]` devuelve cada segundo carácter de la cadena.

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[::2])  # cadena con paso 2: 'Pto'
```

```{code-cell} python
---
tags: hide-output
---
nombre = "Python"
print(nombre[::-1])  # invierte la cadena: 'nohtyP'
```

### Métodos útiles para manipular cadenas

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
print(texto.upper())  # Convierte a mayúsculas: 'HOLA MUNDO'
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
print(texto.lower())  # Convierte a minúsculas: 'hola mundo'
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
# Reemplaza las apariciones de "mundo" por "Python"
print(texto.replace("mundo", "Python"))
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
# Divide la cadena en una lista de palabras, separando por espacios
print(texto.split()) # ['Hola', 'mundo']
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
print("Python" in texto)  # verifica si 'Python' está en texto
```

```{code-cell} python
---
tags: hide-output
---
texto = "Hola mundo"
len(texto)  # devuelve la longitud de la cadena
```

### Concatenación

Las cadenas se pueden concatenar usando el operador `+` o multiplicar por un número entero para repetirlas.

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola " + "mundo"
print(saludo) # 'Hola mundo'
```

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola mundo"
saludo2 = saludo * 3  # saludo+saludo+saludo
print(saludo2) # 'Hola mundoHola mundoHola mundo'
```

```{code-cell} python
---
tags: hide-output
---
saludo = "Hola mundo"
saludo3 = (saludo + ". ") * 3  # Agrega un punto y un espacio al final
print(saludo3) # 'Hola mundo. Hola mundo. Hola mundo. '
```

### Iteración sobre cadenas de caracteres

Las cadenas de caracteres son **iterables**, lo que significa que se pueden recorrer carácter por carácter usando un bucle `for`.

```{code-cell} python
---
tags: hide-output
---
for caracter in "Python":
    print(caracter) # 'P', 'y', 't', 'h', 'o', 'n'
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
mensaje = "Hola, mi nombre es {} y tengo {} años.".format(nombre, edad)
print(mensaje) # 'Hola, mi nombre es Juan y tengo 30 años.'
```

- Usando f-strings (Python 3.6+)

```{code-cell} python
---
tags: hide-output
---
nombre = "Ana"
edad = 32
mensaje = f"Hola, mi nombre es {nombre} y tengo {edad} años."
print(mensaje) # 'Hola, mi nombre es Ana y tengo 32 años.'
```

La letra `f` antes de la cadena indica que es una f-string, lo que permite insertar variables directamente dentro de llaves `{}`.

- Usando el operador `%` (menos recomendado)

```{code-cell} python
---
tags: hide-output
---
nombre = "Eva"
edad = 28
mensaje = "Hola, mi nombre es %s y tengo %d años." % (nombre, edad)
print(mensaje) # 'Hola, mi nombre es Eva y tengo 28 años.'
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
mensaje = "Hola, \tmundo."  # \t inserta una tabulación
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
numeros = [1, 2, 3, 4]  # Lista de números
numeros.append(5)  # Añade un elemento al final
print(numeros) # [1, 2, 3, 4, 5]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
print(numeros[0]) # 1
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
print(numeros[1:3]) # [2, 3]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
numeros.remove(3)  # Elimina el primer elemento que coincida con el valor
print(numeros) # [1, 2, 4]
```

```{code-cell} python
---
tags: hide-output
---
mezcla = [1, "dos", 3.0, True]  # Lista con diferentes tipos de datos
mezcla[0] = "uno"  # Modifica el primer elemento
print(mezcla) # ['uno', 'dos', 3.0, True]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
mezcla = [1, "dos", 3.0, True]  # Lista con diferentes tipos de datos
mezcla = mezcla + numeros  # Concatenación de listas
print(mezcla) # [1, 'dos', 3.0, True, 1, 2, 3, 4]
```

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
numeros = numeros * 2  # Repite la lista
print(numeros) # [1, 2, 3, 4, 1, 2, 3, 4]
```

La lista vacía se puede definir con corchetes vacíos `[]` o con la función `list()`:

```{code-cell} python
---
tags: hide-output
---
lista_vacia = []  # Lista vacía
print(lista_vacia) # []
```

```{code-cell} python
---
tags: hide-output
---
lista_vacia2 = list()  # Otra forma de crear una lista vacía
print(lista_vacia2) # []
```

### Iteración sobre listas

```{code-cell} python
---
tags: hide-output
---
numeros = [1, 2, 3, 4]  # Lista de números
for n in numeros:
    print(n) # 1, 2, 3, 4
```

## Tuplas (`tuple`)

Son similares a las listas, **ordenadas** y **polimórficas**, pero **inmutables**, es decir, una vez creada no se puede modificar.

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)
print(type(coordenadas)) # <class 'tuple'>
```

Se definen con paréntesis y pueden contener diferentes tipos de datos, mientras que las listas se definen con corchetes.

### Acceso

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)
print(coordenadas[0]) # 10.0
```

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)
print(coordenadas[-1]) # 1
```

```{code-cell} python
---
tags: hide-output
---
coordenadas = (10.0, 20.5, 1)
print(coordenadas[1:]) # (20.5, 1)
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
a, b, c = coordenadas  # Desempaquetado
print("a = ", a) # 10.0
print("b = ", b) # 20.5
print("c = ", c) # 1
```

```{code-cell} python
---
tags: hide-output
---
a = 10.0
b = 20.5
c = 1
tupla2 = (a, b, c)  # Empaquetado
print(tupla2) # (10.0, 20.5, 1)
```

La tupla vacía se puede definir con paréntesis vacíos `()` o con la función `tuple()`:

```{code-cell} python
---
tags: hide-output
---
tupla_vacia = ()  # Tupla vacía
print(tupla_vacia) # ()
```

```{code-cell} python
---
tags: hide-output
---
tupla_vacia2 = tuple()  # Otra forma de crear una tupla vacía
print(tupla_vacia2) # ()
```

### Anidamiento

Tanto las listas como las tuplas se pueden anidar, es decir, se pueden incluir dentro de otras listas o tuplas.

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])
for elemento in tupla_anidada:
    print(elemento) # 1, 2, (3, 4), [5, 6]
```

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])
print(tupla_anidada[3][0])  # Accede al primer elemento de la lista anidada: 5
```

```{code-cell} python
---
tags: hide-output
---
tupla_anidada = (1, 2, (3, 4), [5, 6])
tupla_anidada[3].append(7)  # Modifica la lista anidada
print(tupla_anidada) # (1, 2, (3, 4), [5, 6, 7])
```

La tupla no se modificó, sigue teniendo 4 elementos, pero la lista que está adentro de la tupla sí se puede modificar.

Las tuplas se pueden iterar de la misma manera que las listas.

## Diccionarios (`dict`)

Almacenan pares clave-valor. Las claves deben ser únicas e inmutables (por ejemplo, strings, números o tuplas).

```{code-cell} python
---
tags: hide-output
---
d = dict()  # Crear un diccionario vacío
d["clave1"] = "valor1"  # Añadir un par clave-valor
d[25] = "valor2"
d[(1, 2)] = "valor3"  # Añadir una clave de tipo tupla
print(d) # {'clave1': 'valor1', 25: 'valor2', (1, 2): 'valor3'}
```

También se pueden crear diccionarios, de forma explícita, usando llaves `{}`:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
print(persona) # {'nombre': 'Ana', 'edad': 30}
```

### Acceso y modificación

Los diccionarios permiten acceder a los valores mediante sus claves. También se pueden modificar, añadir o eliminar pares clave-valor. La sintaxis es similar a las listas o tuplas, pero en lugar de índices, se utilizan claves.

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
print(persona["nombre"]) # Ana
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
persona["edad"] = 31  # Modifica el valor asociado a la clave "edad"
print(persona) # {'nombre': 'Ana', 'edad': 31}
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30}
persona["email"] = "ana@mail.com"  # Añade una nueva clave-valor
print(persona) # {'nombre': 'Ana', 'edad': 31, 'email': 'ana@mail.com'}
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
del persona["edad"]  # Elimina la clave "edad"
print(persona) # {'nombre': 'Ana', 'email': 'ana@mail.com'}
```

### Métodos útiles

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}
# Devuelve una lista con las claves del diccionario
print(persona.keys())  # dict_keys(['nombre', 'email'])
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.values())  # Devuelve una lista con los valores del diccionario
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}
# Devuelve una lista de tuplas con los pares clave-valor
print(persona.items())  # dict_items([('nombre', 'Ana'), ('email', 'ana@mail.com')])
```

Un método muy útil es `get()`, que permite acceder a un valor sin generar un error si la clave no existe:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.get("nombre", "No encontrado"))  # Devuelve "Ana"
print(persona.get("edad", "No encontrado"))  # Devuelve "No encontrado"
```

`setdefault()` es otro método que permite acceder a un valor y, si la clave no existe, añadirla con un valor por defecto:

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "email": "ana@mail.com"}
# Devuelve 30 y añade la clave "edad" con valor 30
print(persona.setdefault("edad", 30))
print(persona) # {'nombre': 'Ana', 'email': 'ana@mail.com', 'edad': 30}
```

```{code-cell} python
---
tags: hide-output
---
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
# Añade la clave "telefonos" con una lista vacía
lista = persona.setdefault("telefonos", [])
lista.append("123-456-7890")  # Añade un teléfono a la lista
print(persona)
```

### Iteración sobre diccionarios

Los diccionarios se pueden iterar para acceder a las claves y valores.

```{code-cell} python
---
tags: hide-output
---
for clave, valor in persona.items():  # Itera sobre los pares clave-valor
    print(f"{clave}: {valor}") # nombre: Ana, email: ana@mail.com, edad: 30
```

## Conjuntos (`set`)

Los conjuntos son colecciones **no ordenadas** de elementos únicos. No permiten duplicados y no tienen un índice asociado a sus elementos.

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5}
print(conjunto) # {1, 2, 3, 4, 5}
```

El conjunto vacío se puede definir con la función `set()`:

```{code-cell} python
---
tags: hide-output
---
conjunto_vacio = set()  # Conjunto vacío
print(conjunto_vacio) # set()
```

```{code-cell} python
---
tags: hide-output
---
conjunto_vacio2 = {}  # Esto crea un diccionario vacío, no un conjunto
print(conjunto_vacio2) # {}
```

Para agregar un elemento a un conjunto, se utiliza el método `add()`:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5}
conjunto.add(6)  # Añade el elemento 6 al conjunto
print(conjunto) # {1, 2, 3, 4, 5, 6}
```

Si intentamos agregar un elemento que ya existe, no se producirá un error, pero el conjunto no cambiará:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.add(6)  # No se añade, ya que 6 ya está en el conjunto
print(conjunto) # {1, 2, 3, 4, 5, 6}
```

Se puede crear un conjunto a partir de una lista o tupla usando la función `set()`:

```{code-cell} python
---
tags: hide-output
---
lista = [1, 2, 3, 4, 5, 5]
conjunto_desde_lista = set(lista)  # Crea un conjunto a partir de una lista
print(conjunto_desde_lista)  # Elimina duplicados automáticamente
```

Para eliminar un elemento de un conjunto, se utiliza el método `remove()` o `discard()`. La diferencia es que `remove()` genera un error si el elemento no existe, mientras que `discard()` no lo hace:

```{code-cell} python
---
tags: hide-output, raises-exception
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.remove(7)  # Genera un error, ya que 7 no está en el conjunto
print(conjunto)
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.discard(7)  # No genera error
print(conjunto) # {1, 2, 3, 4, 5, 6}
```

El operador `in` se puede usar para verificar si un elemento está en un conjunto:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
print(3 in conjunto) # True
```

No se puede acceder a los elementos de un conjunto por índice, ya que no están ordenados. Sin embargo, se pueden iterar:

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
for elemento in conjunto:
    print(elemento) # 1, 2, 3, 4, 5, 6
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
# {1, 2, 3, 4, 5, 6, 7}
```

```{code-cell} python
---
tags: hide-output
---
# Intersección
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print(conjunto1, " interseccion ", conjunto2, "=", conjunto1 & conjunto2)
# {4, 5, 6}
```

```{code-cell} python
---
tags: hide-output
---
# Diferencia
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print(conjunto1, " diferencia ", conjunto2, "=", conjunto1 - conjunto2)
# {1, 2, 3}
print(conjunto2, " diferencia ", conjunto1, "=", conjunto2 - conjunto1)
# {7}
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
# {1, 2, 3, 7}
print(f"{conjunto2} diferencia simetrica {conjunto1} = "
      f"{conjunto2 ^ conjunto1}")
# {1, 2, 3, 7}
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
# Subconjunto
es_subconjunto = {1, 2} <= conjunto
print("{1, 2} es subconjunto de", conjunto, "?: ", es_subconjunto)
# True
```

```{code-cell} python
---
tags: hide-output
---
conjunto = {1, 2, 3, 4, 5, 6}
# Superconjunto
es_superconjunto = {1, 2} >= conjunto
print("{1, 2} es superconjunto de", conjunto, "?: ", es_superconjunto)
# False
```

Existen otros tipos de conjuntos que permiten almacenar elementos únicos, pero que una vez creados no se pueden modificar, se llaman **conjuntos inmutables** o **frozensets**. Se crean usando la función `frozenset()`:

```{code-cell} python
---
tags: hide-output
---
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
print(conjunto_inmutable)
# frozenset({1, 2, 3, 4, 5})
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
numeros = [x for x in range(1, 6)]  # Lista de números del 1 al 5
cuadrados = [x**2 for x in numeros]
print(cuadrados)  #  [1, 4, 9, 16, 25]
```

Si en lugar de corchetes `[]` se usan paréntesis `()`, se crea un **generador**, no una tupla. Para obtener una tupla, debemos usar el constructor `tuple()`:

```{code-cell} python
---
tags: hide-output
---
numeros = tuple(x for x in range(1, 6))  # Tupla de números del 1 al 5
cuadrados = tuple(x**2 for x in numeros)
print(cuadrados)  # (1, 4, 9, 16, 25)
```

Si se usan llaves `{}`, se crea un conjunto o un diccionario, dependiendo de si se especifica una clave o un par clave-valor:

```{code-cell} python
---
tags: hide-output
---
numeros = {x for x in range(1, 6)}  # Conjunto de números del 1 al 5
cuadrados = {x**2 for x in numeros}
print(cuadrados)  # {1, 4, 9, 16, 25}
```

```{code-cell} python
---
tags: hide-output
---
numeros = {"uno": 1, "dos": 2, "tres": 3}
cuadrados = {clave: valor**2 for clave, valor in numeros.items()}
print(cuadrados)  # {'uno': 1, 'dos': 4, 'tres': 9}
```

```{code-cell} python
---
tags: hide-output
---
diccionario = {"nombre": "Ana", "edad": 30, "email": "ana@example.com"}
tuplas = [(clave, valor) for clave, valor in diccionario.items()]
print(tuplas) # [('nombre', 'Ana'), ('edad', 30), ('email', 'ana@example.com')]
```

La comprensión es una característica funcional de Python muy poderosa.

## Recursos para profundizar

- [Tutorial de Python - Estructuras de datos](https://docs.python.org/es/3/tutorial/datastructures.html)
- [`setdefault()` (KeepCoding)](https://keepcoding.io/blog/que-es-dict-setdefault-en-python-y-su-uso/)
- [Comprensiones de listas (Python Docs)](https://docs.python.org/es/3/tutorial/datastructures.html#list-comprehensions)
- [Comprensión de listas (Hektor Profe)](https://hektorprofe.github.io/python/funcionalidades-avanzadas/comprension-de-listas/)
- [Operadores Encadenados (Hektor Profe)](https://hektorprofe.github.io/python/funcionalidades-avanzadas/operadores-encadenados/)
- [Intérprete Python, para entender como funciona](https://pythontutor.com/python-compiler.html#mode=edit)
