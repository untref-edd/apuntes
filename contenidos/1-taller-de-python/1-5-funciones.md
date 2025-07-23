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
# Funciones en Python y Paradigma Funcional

Las funciones son ciudadanos de primera clase en Python, lo que le otorga al lenguaje ciertas características del paradigma funcional. En este capítulo, exploraremos cómo definir y utilizar funciones, los diferentes tipos de pasajes de parámetros, y cómo Python implementa el paradigma funcional a través de funciones de orden superior, funciones anónimas (lambda), y más.

## Pasajes de parámetros y devolución de valores

Las funciones se definen utilizando la palabra clave `def`, seguida del nombre de la función y paréntesis que pueden contener parámetros. Las funciones pueden retornar valores utilizando la palabra clave `return`.

Python permite varios tipos de pasajes de parámetros a funciones:

```python
def funcion(posicionales, nombrados, *posicionales_variables, **nombrados_variables):
    pass # sentencia que no hace nada
```
  
Posicionales
: Los parámetros se pasan en el orden en que están definidos.

Nombrados
: Los parámetros se pasan utilizando su nombre, lo que permite especificar solo algunos de ellos.

Posicionales variables
: Se pueden pasar un número variable de argumentos posicionales utilizando `*`.

Nombrados variables
: Se pueden pasar un número variable de argumentos nombrados utilizando `**`.

### Parámetros Posicionales

Los parámetros se ligan con los argumentos de la función en el orden en que están definidos. Si se pasan menos argumentos de los esperados, se generará un error.

```{code-cell}
def concatenar_cadenas(cadena1, cadena2):
    return cadena1 + cadena2  

print(concatenar_cadenas("Hola, ", "mundo!"))  # Salida: Hola, mundo!
print(concatenar_cadenas("mundo!", "Hola, "))  # Salida: mundo!Hola, 
```

### Parámetros Nombrados

Al momento de invocar la función se pueden nombrar los parámetros y de esa forma no es necesario respetar el orden de los parámetros. Esto es útil cuando se tienen muchos parámetros y se quiere especificar solo algunos.

```{code-cell}
def concatenar_cadenas(cadena1, cadena2):
    return cadena1 + cadena2

print(concatenar_cadenas(cadena2="mundo!", cadena1="Hola, "))  # Salida: Hola, mundo!
```

### Parámetros Posicionales Variables

Los parámetros posicionales variables se definen utilizando un asterisco (`*`) antes del nombre del parámetro. Esto permite pasar un número variable de argumentos posicionales a la función. Python internamente agrupa estos argumentos en una tupla.

```{code-cell}
def sumar(*numeros):
    print(f"Se recibieron {len(numeros)} numeros")
    print(f"El tipo de numeros es: {type(numeros)}")
    suma = 0
    for num in numeros:
      suma += num
    return suma

print(sumar(1, 2, 3))  # Salida: 6
print(sumar(4, 5, 6, 7, 8))  # Salida: 30
``` 

### Parámetros Nombrados Variables

Los parámetros nombrados variables se definen utilizando dos asteriscos (`**`) antes del nombre del parámetro. Esto permite pasar un número variable de argumentos nombrados a la función. Python internamente agrupa estos argumentos en un diccionario.

```{code-cell}
def mostrar_info(**info):
    print(f"Se recibieron {len(info)} argumentos nombrados")
    print(f"El tipo de info es: {type(info)}")
    for clave, valor in info.items():
        print(f"{clave}: {valor}")

mostrar_info(nombre="Juan", edad=30, ciudad="Madrid")
```

### Parámetros por defecto

Los parámetros por defecto permiten definir valores predeterminados para los parámetros de una función. Si no se pasa un argumento para ese parámetro, se utilizará el valor por defecto.

```{code-cell}
def saludar(nombre="mundo"):
    return f"Hola, {nombre}!" 

print(saludar())  # Salida: Hola, mundo!
print(saludar("Juan"))  # Salida: Hola, Juan!
```

```{Important}
Si en una misma función se utilizan parámetros posicionnales, nombreados, posicionales variables y nombrados variables, los parámetros deben seguir el siguiente orden:
1. Parámetros posicionales
2. Parámetros nombrados
3. Parámetros posicionales variables (`*args`)
4. Parámetros nombrados variables (`**kwargs`)
```
Por ejemplo:

```{code-cell}
def funcion_ejemplo(param1, param2="valor_por_defecto", *args, **kwargs):
    print(f"param1: {param1}, param2: {param2}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

funcion_ejemplo(1, 2, 3, 4, clave1="valor1", clave2="valor2")
```

```{code-cell}
def funcion_ejemplo(param1, param2="valor_por_defecto", *args, **kwargs):
    print(f"param1: {param1}, param2: {param2}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

funcion_ejemplo(1, (2, 3), clave1="valor1", clave2="valor2")
```

```{code-cell}
def funcion_ejemplo(param1, param2="valor_por_defecto", *args, **kwargs):
    print(f"param1: {param1}, param2: {param2}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

funcion_ejemplo(1, clave1="valor1", clave2="valor2")
```

### Devolución de valores

Las funciones pueden devolver valores utilizando la palabra clave `return`. Si no se especifica un valor de retorno, la función devolverá `None` por defecto. En Python, una función puede devolver múltiples valores separados por comas, que se empaquetan en una tupla.

```{code-cell}
def division_y_resto(dividendo, divisor):
    cociente = dividendo // divisor
    resto = dividendo % divisor
    return cociente, resto

cociente, resto = division_y_resto(10, 3)
print(f"Cociente: {cociente}, Resto: {resto}")
```

Como Python tiene tipado dinámico, no es necesario especificar el tipo de retorno de una función. Sin embargo, se pueden utilizar anotaciones de tipo para documentar el tipo esperado de los parámetros y el valor de retorno.

```{code-cell}
def sumar(a: int, b: int) -> int:
    """
    Suma dos números enteros y devuelve el resultado.
    """
    return a + b    
print(sumar(3, 5))  # Salida: 8
print(sumar("a", "b"))  # Salida: ab
```

Las anotaciones de tipo son opcionales y no afectan el comportamiento de la función, pero pueden ser útiles para la documentación y la verificación de tipos en tiempo de desarrollo.

En el fragmento anterior, la función `sumar` está anotada para indicar que espera dos enteros como parámetros y devuelve un entero. Sin embargo, Python no impone estas restricciones en tiempo de ejecución, por lo que se pueden pasar otros tipos de datos sin generar un error.

## Paradigma funcional

La **programación funcional** es un paradigma de programación declarativo basado en el uso de funciones verdaderamente matemáticas. En este estilo de programación las funciones son *ciudadanas de primera clase*, porque sus expresiones pueden ser asignadas a variables como se haría con cualquier otro valor; además de que pueden crearse funciones de orden superior.

Funciones de orden superior
: Son aquellas que pueden:
  - Recibir otras funciones como argumentos.
  - Retornar una función como resultado.
  - Ser asignadas a variables.

En el paradigma funcional en general y a diferencia del imperativo, la programación consiste en especificar el **Qué** y no el **Cómo** se resuelve un problema.

Por ejemplo:

```{code-cell}
def componer(func1, func2):
    def funcion_compuesta(x):
        return func2(func1(x))
    return funcion_compuesta

def cuadrado(x):
    return x * x

def doble(x):
    return x + x

doble_cuadrado = componer(cuadrado, doble)
print(doble_cuadrado(3))  # Salida: 18
```

En este ejemplo, `componer` es una función de orden superior que toma dos funciones como argumentos y devuelve una nueva función que es la composición de las dos. Para poder elevar un número al cuadrado y luego duplicarlo, se utiliza `doble_cuadrado`, que es el resultado de componer `cuadrado` y `doble`. Hay que prestar atención a que el orden en que se componen las funciones, ya que se aplica primero `cuadrado` y luego `doble`.

### Funciones anónimas (lambda)

Las funciones anónimas, también conocidas como funciones lambda, son funciones sin nombre que se definen utilizando la palabra clave `lambda`. Son útiles para crear funciones pequeñas y rápidas sin necesidad de definirlas formalmente.

```{code-cell}
suma = lambda x, y: x + y
print(suma(3, 5))  # Salida: 8
```

Define una función que recibe dos argumentos `x` e `y` y retorna su suma. Esta función queda asociada a la variable `suma`, que se puede utilizar para invocarla.

El fragmento anterior de composición de funciones también se puede reescribir utilizando funciones lambda:

```{code-cell}
def componer(func1, func2):
    return lambda x: func2(func1(x))
doble_cuadrado = componer(lambda x: x * x, lambda x: x + x)
print(doble_cuadrado(3))  # Salida:
```

Las funciones de orden superior, las funciones anónimas, la generación de datos por comprensión y las clausuras son características del paradigma funcional que hacen de Python un lenguaje versátil y poderoso. Algunas de los usos habituales de la programación funcional en Python incluyen:

Mapeo
: Aplicar una función a cada elemento de una colección.

La función que mapea los elementos de una colección a otra debe ser una **función que toma un solo argumento y devuelve un valor**. 

```{code-cell}
def mapear(func, iterable):
    """
    Aplica la función `func` a cada elemento de `iterable`
    y devuelve una lista con los resultados.
    """
    return [func(x) for x in iterable]

numeros = [x for x in range(10)]
cuadrados = mapear(lambda x: x**2, numeros)
print(f"Cuadrados: {cuadrados}") 
```

Python proporciona la función `map` para realizar mapeo de manera más concisa y que permite devolver un iterador en lugar de una lista. Como todo iterador, una vez que se consume, es decir que se itera sobre él, no se puede volver a utilizar. Por lo tanto, es común convertirlo a una lista o tupla para conservar los resultados.

```{code-cell}
numeros = [x for x in range(10)]
cuadrados = map(lambda x: x**2, numeros)
print(type(cuadrados))  # <class 'map'>
tupla = tuple(cuadrados)  # Convierte el iterador a tupla
print(f"Cuadrados: {tupla}")
```

Filtrado
: Seleccionar elementos de una colección que cumplen con una condición.

La función que filtra los elementos de una colección debe ser una **función que toma un solo argumento y devuelve un valor booleano**. 

```{code-cell}
def filtrar(func, iterable):
    """
    Filtra los elementos de `iterable` que cumplen con la
    condición definida en `func`.
    """
    return [x for x in iterable if func(x)]

numeros = [x for x in range(10)]
pares = filtrar(lambda x: x % 2 == 0, numeros)
print(f"Números pares: {pares}")  
```

En este caso la función de filtrado es una función anónima `lambda x: x % 2 == 0`. Las funciones anónimas siempre devuelven el resultado de la última expresión evaluada, por lo que no es necesario utilizar `return`.

Python también proporciona la función `filter` para realizar filtrado de manera más concisa. `filter` devuelve un iterador que contiene los elementos de la colección que cumplen con la condición especificada por la función de filtrado. 

```{code-cell}
numeros = [x for x in range(10)]
pares = filter(lambda x: x % 2 == 0, numeros)
print(type(pares))  # <class 'filter'>
lista = list(pares)  # Convierte el iterador a lista
print(f"Números pares: {lista}")  # 
```

Reducción
: Combinar los elementos de una colección en un solo valor.  

El módulo `functools` proporciona la función `reduce`, que es una función de orden superior que puede aplicar una función de reducción a los elementos de una colección, combinándolos en un solo valor. **La función de reducción debe tomar dos argumentos y devolver un solo valor**.

En este caso, se utiliza para sumar todos los números de la lista. Aplica la suma a los dos primeros elementos, luego aplica la suma al resultado y el siguiente elemento, y así sucesivamente hasta que se procesan todos los elementos de la lista.

```{code-cell}
from functools import reduce
numeros = [x for x in range(10)]
suma_total = reduce(lambda x, y: x + y, numeros)
print(f"Suma total: {suma_total}") #(((((((((0+1)+2)+3)+4)+5)+6)+7)+8)+9) = 45
```

La función de reducción es la función anónima `lambda x, y: x + y`, que toma dos argumentos y devuelve su suma. No hace falta utilizar `return` ya que la última expresión evaluada es justamente la suma de `x` e `y`.

Otro ejemplo de reducción con cadenas de caracteres:

```{code-cell}
from functools import reduce
palabras = ["Python", "mundo", "Hola"]
frase = reduce(lambda x, y: y + " " + x, palabras)
print(f"Frase: {frase}")  
```

En este caso, la función de reducción concatena las palabras en orden inverso, creando una frase a partir de la lista de palabras. El orden inverso se debe al orden en que concatena los elementos la función de reducción.

## Funciones avanzadas

Iteradores
: Son objetos que permiten recorrer una secuencia de elementos uno a uno. En Python todas las colecciones son iterables, lo que significa que se pueden recorrer directamente utilizando un bucle `for` o se puede obtener un iterador con `iter` y luego utilizar la función `next` para obtener cada uno de los valores. Cuando `next` no tiene más elementos para devolver, lanza una excepción `StopIteration`. En los iteradores de Python no hay una función `has_next` como en otros lenguajes, sino que utiliza excepciones para detectar el final de la iteración.

```{code-cell}
numeros = [x for x in range(10)]
iterador = iter(numeros) #
while True:
    try:
        numero = next(iterador)
        print(numero)
    except StopIteration:
        break
```

```{Note}
En el capitulo [Excepciones](1-7-excepciones.md) veremos en más detalle el manejo de excepciones en Python. Por ahora basta con saber que una excepción interrumpe el flujo normal del programa protegido por un bloque `try` y pasa el control al bloque `except` correspondiente. En este caso el bloque `except` captura la excepción `StopIteration` para finalizar la iteración.

La sentencia `break`se utiliza para romper y salir del bucle infinito `while True`.
```

Decoradores
: Son funciones que modifican el comportamiento de otras funciones. Se utilizan para agregar funcionalidades adicionales a funciones existentes sin modificar su código.

```{code-cell}
---
mystnb:
  number_source_lines: true
---
def decorador(func):
    """
    Decora la función `func` para agregarle mensajes antes
    y después de su ejecución.
    """
    def funcion_decorada(*args, **kwargs):
        resultado = f"El resultado de la operación es : {func(*args, **kwargs)}"
        return resultado
    return funcion_decorada

def funcion_original(x):
    return x * 2

funcion_decorada = decorador(funcion_original)
funcion_decorada(5)  
```

La función `decorador` toma una función `func` como argumento y devuelve una nueva función, `funcion_decorada` que agrega el mensaje _"El resultado de la operación es : "_ al resultado de la función original.

```{Note}
En este ejemplo se ultiliza `*args` y `**kwargs` para permitir que la función decorada acepte cualquier número de argumentos posicionales y nombrados, lo que la hace más flexible. En la línea 7, la expresión `func(*args, **kwargs)` invoca a la función original con los argumentos que le pasaron a la función decorada.
```

Python proporciona una sintaxis especial para aplicar decoradores a funciones utilizando el símbolo `@` antes de la definición de la función. Esto es equivalente a decorar la función manualmente como se mostró anteriormente.

```{code-cell}
def decorador(func):
    def funcion_decorada(*args, **kwargs):
        resultado = f"El resultado de la operación es : {func(*args, **kwargs)}"
        return resultado
    return funcion_decorada

@decorador
def funcion_original(x):
    return x * 2
print(funcion_original(5)) 

@decorador
def funcion_suma(a, b):
    return a + b
print(funcion_suma(3, 4))
```

Generadores
: Son funciones que permiten crear iteradores de manera eficiente. Utilizan la palabra clave `yield` para devolver un valor y pausar la ejecución de la función, permitiendo que se reanude más tarde desde el mismo punto.

```{code-cell}
def contador():
    i = 0
    while True:
        yield i
        i += 1
contador_gen = contador()
print(type(contador_gen))  # <class 'generator'>
print(next(contador_gen))  # Salida: 0
print(next(contador_gen))  # Salida: 1
print(next(contador_gen))  # Salida: 2
```

Este generador nos permite, de alguna manera, tener una lista infinita de números enteros, ya que cada vez que se llama a `next`, se obtiene el siguiente número en la secuencia, lo cual es posible gracias a la palabra clave `yield`, que suspende la ejecución de la función en ese punto, devuelve el valor actual de `i`, y guarda el estado de la función para que pueda reanudarse en la siguiente llamada a `next`. En este caso `next` no levantará una excepción `StopIteration` porque el generador está diseñado para ser infinito.

También se puede utilizar la clausura para obtener un comportamiento similar a los generadores:

```{code-cell}
def contador():
    i = 0
    def siguiente():
        nonlocal i
        valor = i
        i += 1
        return valor
    return siguiente
    
siguiente = contador()
print(siguiente())  # Salida: 0
print(siguiente())  # Salida: 1
print(siguiente())  # Salida: 2
```

La clave está en utilizar `nonlocal` para modificar la variable `i` dentro de la función interna `siguiente`, permitiendo que se mantenga el estado entre llamadas. `i` se almacena en la clausura de siguiente, lo que permite que su valor persista entre invocaciones.