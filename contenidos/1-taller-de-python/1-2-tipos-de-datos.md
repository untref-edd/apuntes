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
# Tipos de Datos

Python tiene varios tipos de datos integrados. A continuación, veremos los más usados: **números**, **cadenas**, **listas**, **tuplas** y **diccionarios**.

## Tipos Numéricos

`int`
: Números enteros positivos o negativos, de cualquier tamaño. Los enteros se representan en memoria como una secuencia de bits, limitados por la memoria disponible

`float`
: Números con parte decimal, representados en memoria como un conjunto de bits en punto flotante

`complex`
: Números complejos, representados en memoria como dos números de punto flotante

### Ejemplos

```python
a = 5          # int
b = 3.14       # float
c = 2 + 3j     # complex
```

### Operaciones comunes

```python
import math
x = 10 + 5          # suma
y = 10 / 3          # división (devuelve float)
u = 10 // 3         # división entera
w = 2 ** 3          # potencia
v = 10 % 3          # módulo (resto de la división)
z = math.sqrt(-1)   # Núemero complejo (0+j)
z2 = complex(0, 1)  # También se puede crear un número complejo directamente
z3 = 1j             # Representación alternativa de un número complejo
```

### Conversión de tipos

En python los tipos númericos se pueden convertir entre sí, ya sea de forma explícita o implícita. 

```{code-cell}
float(5)
```

```{code-cell}
int(3.7)
```

```{code-cell}
x = 10 + 5.5 # Implicitamente convierte el int a float
print(x)
```

Un operador útil para verificar el tipo de una variable es `type()`:

```{code-cell}
y = 10 + (2-3j)  # (12-3j)
print(type(y))
```

No hay que confundir la conversión implícita de tipos con tipado dinámico. En Python, el tipo de una variable se determina en tiempo de ejecución, pero las operaciones entre tipos incompatibles generarán un error.

```{code-cell}
# Esto generará un error de tipo
x = 5 + "10"
```

## Cadenas de caracteres (`str`)

Una cadena es una secuencia **inmutable** de caracteres.

Inmutable
: Un objeto inmutable es aquel cuyo contenido no puede ser modificado una vez creado. En el caso de las cadenas, esto significa que no se pueden cambiar los caracteres individuales de una cadena después de su creación.

```{code-cell}
mensaje = 'Hola, mundo'
mensaje[0] = 'h'  # Esto generará un error
```

Si quiero modificar una cadena, debo crear una nueva cadena con el contenido deseado:

```{code-cell}
mensaje = 'Hola, mundo'
mensaje = 'h' + mensaje[1:]  # Crea una nueva cadena
print(mensaje)
```

### Indexado y slicing

Las cadenas de caracteres están indexadas, es decir, que se puede manipular cada carácter por su posición. El primer carácter tiene índice 0, el segundo 1, y así sucesivamente. También se pueden usar índices negativos para acceder a los caracteres desde el final de la cadena y tajadas o slicing para obtener subcadenas. En las tajadas, el primer parámetro es el índice inicial y el segundo es el índice final (no incluido), similar a Go.

```{code-cell}
nombre = "Python"
print(nombre[0])
```

```{code-cell}
nombre = "Python"
print(nombre[-1])
```

```{code-cell}
nombre = "Python"
print(nombre[1:4])
```

```{code-cell}
nombre = "Python"
print(nombre[:2])
```

```{code-cell}
nombre = "Python"
print(nombre[2:])
```

```{code-cell}
nombre = "Python"
print(nombre[-3:])    
```

Las tajadas o slices en python tienen un tercer parámetro opcional que indica el paso entre los índices. Por ejemplo, `nombre[::2]` devuelve cada segundo carácter de la cadena.

```{code-cell}
nombre = "Python"
print(nombre[::2])       # cadena con paso 2
```

```{code-cell}
nombre = "Python"
print(nombre[::-1])      # invierte la cadena
```

### Métodos útiles para manipular cadenas

```{code-cell}
texto = "Hola mundo"
print(texto.upper()) # Convierte a mayúsculas
```

```{code-cell}
texto = "Hola mundo"
print(texto.lower()) # Convierte a minúsculas
```

```{code-cell}
texto = "Hola mundo"
print(texto.replace("mundo", "Python")) # Reemplaza las apariciones de "mundo"
                                        # por "Python"
```

```{code-cell}
texto = "Hola mundo"
print(texto.split())  # Divide la cadena en una lista de palabras, separando por espacios
```

```{code-cell}
texto = "Hola mundo"
print("Python" in texto)  # verifica si 'Python' está en texto
```

```{code-cell}
texto = "Hola mundo"
len(texto)  # devuelve la longitud de la cadena
```

### Concatenación

Las cadenas se pueden concatenar usando el operador `+` o multiplicar por un número entero para repetirlas.

```{code-cell}
saludo = "Hola " + "mundo"
print(saludo)
```

```{code-cell}
saludo = "Hola mundo"
saludo2 = saludo*3    # saludo+saludo+saludo
print(saludo2)
```

```{code-cell}
saludo = "Hola mundo"
saludo3 = (saludo + ". ") * 3  # Agrega un punto y un espacio al final
print(saludo3)
```

### Iteración

Las cadenas de caracteres son iterables, lo que significa que se pueden recorrer carácter por carácter usando un bucle `for`.

```{code-cell}
for caracter in "Python":
  print(caracter)
```

### Formateo de cadenas

El formateo de cadenas permite insertar valores en una cadena de texto de manera más legible y flexible. Hay varias formas de hacerlo:

- Usando el método `format()`

```{code-cell}
nombre = "Juan"
edad = 30
mensaje = "Hola, mi nombre es {} y tengo {} años.".format(nombre, edad)
print(mensaje)
```

- Usando f-strings (Python 3.6+)

```{code-cell}
nombre = "Ana"
edad = 32
mensaje = f"Hola, mi nombre es {nombre} y tengo {edad} años."
print(mensaje)
```

La letra `f` antes de la cadena indica que es una f-string, lo que permite insertar variables directamente dentro de llaves `{}`.

- Usando el operador `%` (menos recomendado)

```{code-cell}
nombre = "Eva"
edad = 28
mensaje = "Hola, mi nombre es %s y tengo %d años." % (nombre, edad)
print(mensaje)
```

El caracter `%` se usa para formatear cadenas, donde `%s` es un marcador de posición para una cadena y `%d` para un número entero, pero es menos legible y flexible que las otras opciones.

El caracter de escape `\` se utiliza para insertar caracteres especiales en una cadena, como comillas, saltos de línea o tabulaciones.

```{code-cell}
mensaje = "Hola, \"mundo\".\n¿Cómo estás?"
print(mensaje)
```
`\n` inserta un salto de línea, y `\"` permite incluir comillas dobles dentro de una cadena delimitada por comillas dobles.

Otra forma de usar comillas dobles en una cadena es usar comillas simples para delimitar la cadena:

```{code-cell}
mensaje = 'Hola, "mundo".\n¿Cómo estás?'
print(mensaje)
```

```{code-cell}
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

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
numeros.append(5)       # Añade un elemento al final
print(numeros)
```

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
print(numeros[0])
```

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
print(numeros[1:3])
```

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
numeros.remove(3)       # Elimina el primer elemento que coincida con el valor
print(numeros)
```

```{code-cell}
mezcla = [1, "dos", 3.0, True]  # Lista con diferentes tipos de datos
mezcla[0] = "uno"  # Modifica el primer elemento
print(mezcla)
```

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
mezcla = [1, "dos", 3.0, True]  # Lista con diferentes tipos de datos
mezcla = mezcla + numeros  # Concatenación de listas
print(mezcla)
```

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
numeros = numeros * 2  # Repite la lista
print(numeros)
```

La lista vacía se puede definir con corchetes vacíos `[]` o con la función `list()`:

```{code-cell}
lista_vacia = []  # Lista vacía
print(lista_vacia)
```

```{code-cell}
lista_vacia2 = list()  # Otra forma de crear una lista vacía
print(lista_vacia2)
```

### Iteración

```{code-cell}
numeros = [1, 2, 3, 4]  # Lista de números
for n in numeros:
  print(n)
```

## 4. Tuplas (`tuple`)

Son similares a las listas, **ordenadas** y **polimórficas**, pero **inmutables**, es decir, una vez creada no se puede modificar.

```{code-cell}
coordenadas = (10.0, 20.5, 1)
print(type(coordenadas))
```

Se definen con paréntesis y pueden contener diferentes tipos de datos, mientras que las listas se definen con corchetes.

### Acceso

```{code-cell}
coordenadas = (10.0, 20.5, 1)
print(coordenadas[0])     
```

```{code-cell}
coordenadas = (10.0, 20.5, 1)
print(coordenadas[-1])     
```

```{code-cell}
coordenadas = (10.0, 20.5, 1)
print(coordenadas[1:])
```

### Ventajas:

- Más livianas que las listas.
- Se pueden usar como claves en diccionarios y se pueden empaquetar varios valores en una sola variable, lo que permite que las funciones puedan devolver múltiples valores, o usar tuplas como claves en diccionarios, entre otros usos.

La forma de empaquetar y desempaquetar tuplas es similar a las listas:

```{code-cell}
coordenadas = (10.0, 20.5, 1)
a, b, c = coordenadas  # Desempaquetado
print("a = ", a)
print("b = ", b)
print("c = ", c)
```

```{code-cell}
a = 10.0
b = 20.5
c = 1
tupla2 = (a, b, c)  # Empaquetado
print(tupla2)
```

La tupla vacía se puede definir con paréntesis vacíos `()` o con la función `tuple()`:

```{code-cell}
tupla_vacia = ()  # Tupla vacía
print(tupla_vacia)
```

```{code-cell}
tupla_vacia2 = tuple()  # Otra forma de crear una tupla vacía
print(tupla_vacia2)
```

### Anidamiento

Tanto las listas como las tuplas se pueden anidar, es decir, se pueden incluir dentro de otras listas o tuplas.

```{code-cell}
tupla_anidada = (1, 2, (3, 4), [5, 6])
for elemento in tupla_anidada:
    print(elemento)
```

```{code-cell}
tupla_anidada = (1, 2, (3, 4), [5, 6])
print(tupla_anidada[3][0]) # Accede al primer elemento de la lista anidada
```

```{code-cell}
tupla_anidada = (1, 2, (3, 4), [5, 6])
tupla_anidada[3].append(7)  # Modifica la lista anidada
print(tupla_anidada)
```

La tupla no se modificó, sigue teniendo 4 elementos, pero la lista que está adentro de la tupla si se puede modificar.

Las tuplas se pueden iterar de la misma manera que las listas.

## 5. Diccionarios (`dict`)

Almacenan pares clave-valor. Las claves deben ser únicas e inmutables (por ejemplo, strings, números o tuplas).


```{code-cell}
d = dict()  # Crear un diccionario vacío
d["clave1"] = "valor1"  # Añadir un par clave-valor
d[25] = "valor2"
d[(1, 2)] = "valor3"    # Añadir una clave de tipo tupla
print(d)
```

También se pueden crear diccionarios, de forma explícita, usando llaves `{}`:

```{code-cell}
persona = {"nombre": "Ana", "edad": 30}
print(persona)
```

### Acceso y modificación:

Los diccionarios permiten acceder a los valores mediante sus claves. También se pueden modificar, añadir o eliminar pares clave-valor. La sintáxis es similar a las listas o tuplas, pero en lugar de índices, se utilizan claves.

```{code-cell}
persona = {"nombre": "Ana", "edad": 30}
print(persona["nombre"])
```

```{code-cell}
persona = {"nombre": "Ana", "edad": 30}
persona["edad"] = 31 # Modifica el valor asociado a la clave "edad"
print(persona)
```

```{code-cell}
persona = {"nombre": "Ana", "edad": 30}
persona["email"] = "ana@mail.com" # Añade una nueva clave-valor
print(persona)
```

```{code-cell}
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
del persona["edad"]  # Elimina la clave "edad"
print(persona)
```

### Métodos útiles:

```{code-cell}
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.keys()) # Devuelve una lista con las claves del diccionario
```

```{code-cell}
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.values()) # Devuelve una lista con los valores del diccionario
```

```{code-cell}
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.items()) # Devuelve una lista de tuplas con los pares clave-valor
```

Un método muy útil es `get()`, que permite acceder a un valor sin generar un error si la clave no existe:

```{code-cell}
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.get("nombre", "No encontrado"))  # Devuelve "Ana"
print(persona.get("edad", "No encontrado"))    # Devuelve "No encontrado"
```

`setdefault()` es otro método que permite acceder a un valor y, si la clave no existe, añadirla con un valor por defecto:

```{code-cell}
persona = {"nombre": "Ana", "email": "ana@mail.com"}
print(persona.setdefault("edad", 30)) # Devuelve 30 y añade la clave "edad" con valor 30
print(persona)
```

```{code-cell}
persona = {"nombre": "Ana", "edad": 30, "email": "ana@mail.com"}
lista=persona.setdefault("telefonos",[]) # Añade la clave "telefonos" con una lista vacía
lista.append("123-456-7890")  # Añade un teléfono a la lista
print(persona)
```

### Iteración

Los diccionarios se pueden iterar para acceder a las claves y valores.

```{code-cell}
for clave, valor in persona.items():  # Itera sobre los pares clave-valor
  print(f"{clave}: {valor}")
```



## Conjuntos (`set`)
Los conjuntos son colecciones **no ordenadas** de elementos únicos. No permiten duplicados y no tienen un índice asociado a sus elementos.

```{code-cell}
conjunto = {1, 2, 3, 4, 5}
print(conjunto)
```

El conjunto vacío se puede definir con la función `set()`:

```{code-cell}
conjunto_vacio = set()  # Conjunto vacío
print(type(conjunto_vacio))
```

```{code-cell}
conjunto_vacio2 = {}  # Esto crea un diccionario vacío, no un conjunto
print(type(conjunto_vacio2))
``` 

Para agregar un elemento a un conjunto, se utiliza el método `add()`:

```{code-cell}
conjunto = {1, 2, 3, 4, 5}
conjunto.add(6)  # Añade el elemento 6 al conjunto
print(conjunto)
```

Si intentamos agregar un elemento que ya existe, no se producirá un error, pero el conjunto no cambiará:

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.add(6)  # No se añade, ya que 6 ya está en el conjunto
print(conjunto)
```

Se puede crear un conjunto a partir de una lista o tupla usando la función `set()`:

```{code-cell}
lista = [1, 2, 3, 4, 5, 5]
conjunto_desde_lista = set(lista)  # Crea un conjunto a partir de una lista
print(conjunto_desde_lista)  # Elimina duplicados automáticamente
```

Para eliminar un elemento de un conjunto, se utiliza el método `remove()` o `discard()`. La diferencia es que `remove()` genera un error si el elemento no existe, mientras que `discard()` no lo hace:

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.remove(7) # Genera un error, ya que 7 no está en el conjunto
print(conjunto)
```

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
conjunto.discard(7)  # No genera error
print(conjunto)
```

el operador `in` se puede usar para verificar si un elemento está en un conjunto:

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
print(3 in conjunto)
```

No se puede acceder a los elementos de un conjunto por índice, ya que no están ordenados. Sin embargo, se pueden iterar:

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
for elemento in conjunto:
  print(elemento)
```

Los conjuntos son útiles para realizar operaciones matemáticas como unión, intersección, diferencia y diferencia simétrica.

### Operaciones con conjuntos
```{code-cell}
# Unión
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print (conjunto1, " union ", conjunto2, "=", conjunto1 | conjunto2)
```

```{code-cell}
# Intersección
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print(conjunto1, " interseccion ", conjunto2, "=", conjunto1 & conjunto2)
```

```{code-cell}
# Diferencia
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print(conjunto1, " diferencia ", conjunto2, "=", conjunto1 - conjunto2)
print(conjunto2, " diferencia ", conjunto1, "=", conjunto2 - conjunto1)
```

```{code-cell}
# Diferencia simétrica
conjunto1 = {1, 2, 3, 4, 5, 6}
conjunto2 = {4, 5, 6, 7}
print(conjunto1, " diferencia simetrica ", conjunto2, "=", conjunto1 ^ conjunto2)
print(conjunto2, " diferencia simetrica ", conjunto1, "=", conjunto2 ^ conjunto1)
```

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
# Subconjunto
es_subconjunto = {1, 2} <= conjunto
print("{1, 2} es subconjunto de", conjunto, "?: ", es_subconjunto)
```

```{code-cell}
conjunto = {1, 2, 3, 4, 5, 6}
# Superconjunto
es_superconjunto = {1, 2} >= conjunto
print("{1, 2} es superconjunto de", conjunto, "?: ", es_superconjunto)
```

Existen otros tipos de conjuntos que permiten almacenar elementos únicos, pero que una vez creados no se pueden modificar, se llaman **conjuntos inmutables** o **frozensets**. Se crean usando la función `frozenset()`:

```{code-cell}
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
print(conjunto_inmutable)
``` 

Los conjuntos inmutables son útiles cuando se necesita un conjunto que no cambie a lo largo del tiempo, por ejemplo, como claves en un diccionario o elementos en otro conjunto.

Los métodos de los conjuntos inmutables son limitados, ya que no se pueden modificar. Por ejemplo, no se pueden usar `add()` o `remove()`, pero sí se pueden usar operaciones como unión, intersección y diferencia.

```{code-cell}
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
conjunto2 = frozenset([4, 5, 6, 7])
print(conjunto_inmutable | conjunto2)  # Unión
print(conjunto_inmutable & conjunto2)  # Intersección
print(conjunto_inmutable - conjunto2)  # Diferencia
print(conjunto2 - conjunto_inmutable)  # Diferencia
print(conjunto_inmutable ^ conjunto2)  # Diferencia simétrica
```

El resultado de estas operaciones es un nuevo conjunto inmutable, ya que el conjunto original no se modifica.
