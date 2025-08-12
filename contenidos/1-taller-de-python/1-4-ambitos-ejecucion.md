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
# Ámbitos de Ejecución

Este capítulo profundizaremos sobre el manejo de variables en Python, contrastándolo con lo que ya conocemos de Go y Java. Aunque los conceptos fundamentales de variables son universales, Python introduce matices importantes en su gestión, especialmente en lo que respecta a la inmutabilidad de ciertos tipos de datos, los ámbitos de ejecución y la poderosa característica de las clausuras.

## Variables y Asignación

En Go y Java, la declaración de variables a menudo implica especificar explícitamente el tipo de dato (aunque Go ofrece inferencia de tipo). Python, por otro lado, es un lenguaje de tipado dinámico. Esto significa que no se declara el tipo de una variable; el tipo se infiere en tiempo de ejecución según el valor que se le asigna.

Una diferencia clave es que en Python, las variables son esencialmente referencias a objetos en memoria. Cuando se reasigna  una variable, simplemente esa referencia pasa a apuntar a un objeto diferente, en lugar de cambiar el valor (esto es crucial para entender la inmutabilidad de ciertos tipos).

Cada vez que se asigna un valor a una variable, Python sigue los siguientes pasos:

1. Crea un objeto en memoria (si no existe ya).
2. Asigna una referencia a ese objeto.

Python garantiza que los pasos anteriores para asignar una variable son **_atómicos_**, es decir se ejecutan uno tras otro sin interrupciones, lo que asegura la consistencia del estado de las variables en un entorno multihilo.

Si la variable ya tenía una referencia a otro objeto, esa referencia se pierde (el objeto anterior puede ser desalojado de la memoria por el recolector de basura si no hay otras referencias a él).

<iframe
    src="../_static/ppts/1-AsignacionDeVariables.pdf#page=1&toolbar=0&navpanes=0&scrollbar=0&view=FitH"
    frameborder="0"
    width="100%"
    height="569"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
</iframe>

Esto contrasta con Go y Java, donde la asignación de una variable puede implicar la creación de una copia del valor (especialmente para tipos primitivos).

## Tipos de Datos y Mutabilidad

En Python **todo es un objeto**, por lo tanto tanto podemos pensar que todas las variables son referencias a objetos en el _heap_. La distinción importante es si un objeto es mutable o inmutable.

### Tipos Inmutables (como los "primitivos" en Java/Go)

- Booleanos (`bool`)
- Números (`int`, `float`, `complex`)
- Cadenas (`str`)
- Tuplas (`tuple`)
- Rangos (`range`)
- Conjuntos congelados (`frozenset`)

Cuando a una variable que ya tenía asignado un objeto inmutable, se le asigna otro valor, en realidad se crea un nuevo objeto inmutable en memoria y la referencia anterior se pierde.

```{code-cell}
s1 = "hola"
s2 = s1
s1 += " mundo" # Esto crea una nueva cadena "hola mundo" y s1 ahora referencia a ella
print(f"s1: {s1}, s2: {s2}") # Salida: s1: hola mundo, s2: hola
```

<iframe
    src="../_static/ppts/2-DatosInmutables.pdf#page=1&toolbar=0&navpanes=0&scrollbar=0&view=FitH"
    frameborder="0"
    width="100%"
    height="569"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
</iframe>

En este fragmento, `s1` y `s2` inicialmente referencian al mismo objeto, la cadena "hola". Al modificar `s1`, se crea un nuevo objeto cadena "hola mundo", y `s1` ahora apunta a este nuevo objeto, mientras que `s2` sigue apuntando al antiguo objeto "hola".

### Tipos Mutables (como los objetos en Java/Go)

- Listas (list)
- Diccionarios (dict)
- Conjuntos (set)
- Objetos de clases personalizadas

Cuando se modifica un objeto mutable, se altera el objeto en su lugar. Si múltiples variables referencian al mismo objeto mutable, todas verán los cambios.

```{code-cell}
lista1 = [1, 2, 3]
lista2 = lista1 # lista1 y lista2 referencian a la misma lista
lista1.append(4) # Modifica la lista original
print(f"lista1: {lista1}, lista2: {lista2}") 
```

<iframe
    src="../_static/ppts/3-DatosMutables.pdf#page=1&toolbar=0&navpanes=0&scrollbar=0&view=FitH"
    frameborder="0"
    width="100%"
    height="569"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
</iframe>

En este caso, `lista1` y `lista2` referencian al mismo objeto lista. Al modificar `lista1`, `lista2` refleja el cambio porque ambas variables apuntan al mismo objeto en memoria.

## Visibilidad de Variables

En Python no existe el concepto de público, privado o protegido como en Java. En cambio, se utiliza una convención de nomenclatura para indicar la visibilidad de las variables:

Variables públicas
: Se definen sin guiones bajos al inicio del nombre. Son accesibles desde cualquier parte del código (ej. `mi_variable`).

Variables protegidas
: Se definen con un guion bajo al inicio del nombre (ej. `_variable`). Indica que la variable es para uso interno del módulo o clase, pero aún es accesible desde fuera.

Variables privadas
: Se definen con dos guiones bajos al inicio del nombre (ej. `__variable`). Esto activa el _name mangling_, lo que significa que el nombre de la variable se modifica internamente para evitar conflictos con nombres en subclases.

Variables especiales
: Se definen con dos guiones bajos al inicio y al final del nombre (ej. `__init__`). Estas son utilizadas por Python para definir métodos especiales y no deben ser modificadas directamente.

```{Warning}
Todas las variables en Python son accesibles desde fuera del módulo o clase, incluso las privadas. La convención de nomenclatura es solo una guía para los desarrolladores y no impide el acceso a las variables.
```

## Ámbitos de Ejecución (Scopes): La Regla LEGB

Python define un sistema de ámbitos para resolver nombres (variables, funciones, clases, etc.). Este sistema se conoce comúnmente como la regla LEGB:

Local (L)
: Nombres definidos dentro de una función.

Enclosing (E) / Clausura
: Nombres en el ámbito de una función externa (función "envolvente"). Este ámbito define el contexto de ejecución de una función anidada.

Global (G)
: Nombres definidos en el nivel superior de un módulo (archivo .py).

Built-in (B)
: Nombres preasignados por Python (ej. open, range, print).

Cuando Python busca un nombre, sigue este orden: primero busca en el ámbito Local, luego en el Enclosing, después en el Global y finalmente en el Built-in.

```{figure} ../assets/images/ambitos.png
---
name: ambitos
---
Ámbitos de Ejecución
```

### Ámbito Local (L)

Las variables definidas dentro de una función son locales a esa función. Esto significa que solo son accesibles dentro de la función y no pueden ser accedidas desde fuera de ella. Una vez que la función termina su ejecución, las variables locales se eliminan de la memoria.

Si hay variables globales definidas con el mismo nombre de las variables locales, entonces las locales **ocultan** las globales. Esto se conoce como **Ocultamiento** de variables (_shadowing_).

```{code-cell}
mensaje = "Hola desde el ámbito global" # Variable global
def mi_funcion():
    mensaje = "Hola desde la función" # Variable local
    print(mensaje)

mi_funcion() # Llama a la función que imprime el mensaje local
print(mensaje) # Acceso a la variable global
```

La variable local `mensaje` dentro de `mi_funcion` oculta la variable global del mismo nombre. Cuando se llama a `mi_funcion`, imprime el mensaje local, mientras que fuera de la función se accede a la variable global.

Si se necesita modificar una variable global desde dentro de una función, se debe usar la palabra clave `global` para indicar que se quiere referenciar a la variable global.

```{code-cell}
mensaje = "Hola desde el ámbito global" # Variable global
def mi_funcion():
    global mensaje # Indica que se quiere usar la variable global
    mensaje = "Hola desde la función" # Modifica la variable global
    print(mensaje)
mi_funcion() # Llama a la función que modifica el mensaje global
print(mensaje) # Acceso a la variable global modificada
```

```{Warning}
El uso excesivo de global o de ocultamiento de variables puede llevar a código difícil de mantener y depurar. Preferiblemente, se deben pasar las variables como argumentos a las funciones y las funciones deben devolver valores explicitos.
```

### Ámbito Enclosing (E) / Clausuras

En Python, las funciones son ciudadanos de primera clase, lo que significa que Python las trata como a un objeto más y por lo tanto se pueden asignar funciones a variables, pasarlas como argumentos y retornarlas desde otras funciones y también se pueden **anidar**, esto es definir funciones dentro de otras funciones.

Esta versatilidad de poder definir una función dentro de otra lleva a las clausuras, que son una característica poderosa y distintiva de Python. Las clausuras permiten que una función anidada acceda a variables del ámbito de su función envolvente, incluso después de que la función envolvente haya terminado su ejecución.

Para que una función sea una clausura, debe cumplir dos condiciones:

- Debe ser una función anidada (una función definida dentro de otra función).
- Debe referenciar variables de su ámbito externo (no global, no local a ella misma). Estas variables se conocen como **referencias externas**.
  
```{code-cell}
---
mystnb:
  number_source_lines: true
---
def fabrica_incrementos(y):
    def incrementar(x):
        return x + y  # y está encapsulada en la función interna
    return incrementar  # Retorna la función interna  

incrementar_2 = fabrica_incrementos(2)  # Crea una función que incrementa en 2
print(incrementar_2(5))  # Salida: 7
```

Al ejecutar el fragmento anterior ocurre lo siguiente:

1. En la línea 1 se define la función `fabrica_incrementos` que recibe un parámetro `y`. El código de la función (hasta la línea 4) se guarda en memoria. Es un valor más. El nombre de la función `fabrica_incrementos` se guarda en el ámbito global y es la referencia que permite acceder al objeto función.

2. En la línea 6 se llama a `fabrica_incrementos(2)` y el resultado de esa operación (la función interna `incrementar`) se va a asignar a la variable `incrementar_2`. En este momento, `y` tiene el valor 2 y se guarda en la clausura de la función interna `incrementar`.

3. El valor devuelto por `fabrica_incrementos` es una función que queda ligada a la variable `incrementar_2`. `incrementar_2` contiene el valor de `y`, al momento de su creación, en su clausura. Esto significa que `incrementar_2` "recuerda" el valor de `y` aunque `fabrica_incrementos` ya haya terminado su ejecución.

4. En la línea 7, se ejecuta `incrementar_2`. `incrementar_2` toma un parámetro `x` y retorna la suma de `x` más `y`. Si bien `fabrica_incrementos` ya ha terminado su ejecución y por lo tanto los valores de sus parámetros no están en la memoria, la referencia a `y` se mantiene en la clausura. La función realiza la operación `5 + 2`, donde `5` es el valor ligado al parámetro `x` y `2` es el valor de `y`, al momento de la creación de `incrementar_2`que se guardó en la clausura.

5. `incrementar_2(5)` retorna 7 al ámbito global, y `print` lo muestra en la salida.

```{Important}
Para Python todas las variables son referencias, incluido los nombres de las funciones. Al colocar paréntesis luego del nombre de la misma, se invoca la función y se ejecuta el código que contiene. Si no se colocan paréntesis, se obtiene una referencia a la función, que es un objeto más en memoria.
```

### Ámbito Global (G)

El ámbito global se refiere a las variables definidas en el nivel superior de un módulo. Estas variables son accesibles desde cualquier parte del módulo, incluidas las funciones.

Al declarar un módulo se puede incluir variables y constantes globales que pueden ser utilizadas en todo el código del módulo. A modo de ejemplo podemos ver las constantes matemáticas definidas en el módulo `math`, como `math.pi` o `math.e`.

```{code-cell}
import math  # Importa el módulo math
print("Constantes matemáticas:")
print(math.pi)  # Imprime el valor de pi
print(math.e)  # Imprime el valor de e
print(math.tau)  # Imprime el valor de tau
print(math.inf)  # Imprime el valor de infinito
print(math.nan)  # Imprime el valor de NaN (Not a Number)
```

Para definir un módulo propio se crea un archivo con extensión `.py` y se pueden definir variables y funciones que serán accesibles desde otros módulos al importarlos. El nombre del módulo es el nombre del archivo sin la extensión `.py`.

A modo de ejemplo, se muestra un módulo simple que implementa una pila (_stack_) utilizando una lista y Objetos. Más adelante veremos en detalle la [Programación Orientada a Objetos (POO)](1-6-poo.md) en Python, pero aquí se muestra un ejemplo de un módulo y como se documenta cada parte del código.
`
````{admonition} Click para ver el código
:class: dropdown

```{literalinclude} ../_static/code/stack/stack.py
```

````

A partir de la función `demo_stack`, se muestra cómo se puede utilizar el módulo `stack` para crear una pila, agregar elementos y eliminarlos.

Es común que los módulos tengan un bloque de código al final que se ejecuta solo si el módulo se ejecuta directamente, no cuando se importa. Esto se logra utilizando la siguiente estructura:

```python
if __name__ == "__main__":
    demo_stack()
```

Si el módulo se importa desde otro módulo, el bloque `if __name__ == "__main__":` no se ejecuta, lo que permite que el código de demostración no interfiera con el uso del módulo como biblioteca.

### Ámbito Built-in (B)

El ámbito built-in contiene nombres predefinidos por Python, como funciones y excepciones que están disponibles en todos los módulos sin necesidad de importarlos. Estos nombres son parte del núcleo del lenguaje y se pueden utilizar directamente en cualquier parte del código. Algunos ejemplos son `print`, `len`, `range`, `int`, `str`, entre otros.

Si se intenta redefinir un nombre built-in, se creará una variable local o global que ocultará temporalmente el nombre built-in, pero no se eliminará del ámbito built-in.

```{Warning}
No se recomienda bajo ningún punto de vista, redefinir nombres built-in, ya que esto puede causar confusión y errores difíciles de depurar. Es mejor utilizar nombres descriptivos y evitar conflictos con los nombres predefinidos de Python.
```

```{code-cell}
print(len("Hola"))  # Llama a la función built-in len
def mi_funcion():
    len = 4
    print(len("Mundo"))  # Error
mi_funcion()  # Llama a la función que imprime la longitud de "Mundo"
```

## Recursos para profundizar

- [Tutorial de Python - Ámbitos de ejecución](https://docs.python.org/es/3/tutorial/classes.html#scopes-and-namespaces){target="_blank"}
- [Python Scopes and Namespaces (W3Schools)](https://www.w3schools.com/python/python_scope.asp){target="_blank"}
- [Python Built-in Functions (W3Schools)](https://www.w3schools.com/python/python_ref_functions.asp){target="_blank"}
  