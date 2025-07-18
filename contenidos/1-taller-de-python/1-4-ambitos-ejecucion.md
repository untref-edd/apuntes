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
Este capítulo profundizaremos sobre el manejo de variables en Python, contrastándolo con los paradigmas que ya conocemos de Go y Java. Aunque los conceptos fundamentales de variables son universales, Python introduce matices importantes en su gestión, especialmente en lo que respecta a la inmutabilidad de ciertos tipos de datos, los ámbitos de ejecución y la poderosa característica de las clausuras.

## Variables y Asignación

En Go y Java, la declaración de variables a menudo implica especificar explícitamente el tipo de dato (aunque Go ofrece inferencia de tipo). Python, por otro lado, es un lenguaje de tipado dinámico. Esto significa que no se declara el tipo de una variable; el tipo se infiere en tiempo de ejecución según el valor que se le asigna.

Una diferencia clave es que en Python, las variables son esencialmente referencias a objetos en memoria. Cuando se reasigna  una variable, simplemente esa referencia pasa a apuntar a un objeto diferente, en lugar de cambiar el valor (esto es crucial para entender la inmutabilidad de ciertos tipos).

```{code-cell}
x = 10  # x referencia al objeto int 10
y = x   # y también referencia al objeto int 10
x = 20  # x ahora referencia al objeto int 20; y sigue referenciando a 10
print(f"x: {x}, y: {y}")
```

Cada vez que se asigna un valor a una variable, Python sigue los siguientes pasos:
1. Crea un objeto en memoria (si no existe ya).
2. Asigna una referencia a ese objeto en la variable.
3. Si la variable ya tenía una referencia a otro objeto, esa referencia se pierde (el objeto anterior puede ser recolectado por el recolector de basura si no hay otras referencias a él).



<iframe
  src="https://docs.google.com/presentation/d/16eRVowRXKly65Pu93VRUdydho_hgS7xRemlzFHvzYoc/embed"
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

### Tipos Inmutables (como los "primitivos" en Java/Go):

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

En este fragmento, `s1` y `s2` inicialmente referencian al mismo objeto cadena "hola". Al modificar `s1`, se crea un nuevo objeto cadena "hola mundo", y `s1` ahora apunta a este nuevo objeto, mientras que `s2` sigue apuntando al antiguo objeto "hola".


### Tipos Mutables (como los objetos en Java/Go):

- Listas (list)Diccionarios (dict)
- Conjuntos (set)
- Objetos de clases personalizadas
 
Cuando se modifica un objeto mutable, se altera el objeto en su lugar. Si múltiples variables referencian al mismo objeto mutable, todas verán los cambios.

```{code-cell}
lista1 = [1, 2, 3]
lista2 = lista1 # lista1 y lista2 referencian a la misma lista
lista1.append(4) # Modifica la lista original
print(f"lista1: {lista1}, lista2: {lista2}") 
```

En este caso, `lista1` y `lista2` referencian al mismo objeto lista. Al modificar `lista1`, `lista2` refleja el cambio porque ambas variables apuntan al mismo objeto en memoria.

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

```{figure} ../assets/images/ambitos.svg
---
name: ambitos
---
Ámbitos de Ejecución
```

### Ámbito Local (L)
Las variables definidas fuera de toda función son globales al módulo y por lo tanto son visibles desde cualquier parte del mismo. En particular se pueden acceder desde dentro de una función, aunque en principio no se pueden modificar.

```{code-cell}
mensaje = "Hola desde el ámbito global" # Variable global
def mi_funcion():
    print(mensaje) # Acceso a la variable global

mi_funcion() # Llama a la función que imprime el mensaje global
print(mensaje) # Acceso a la variable global
```

Las variables declaradas dentro de una función son locales a esa función. No son accesibles desde fuera de ella y si hay variables globales definidas con el mismo nombre las **ocultan**. Esto se conoce como **Ocultamiento** de variables (_shadowing_).

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

El contexto en el cual se ejecuta una función anidada se conoce como **ámbito enclosing**. Este ámbito es el que contiene las variables que la función anidada puede acceder, pero no modificar directamente a menos que se use `nonlocal` (similar a `global` pero para el ámbito enclosing).

```{code-cell}
def funcion_externa(x):
    y = 10  # Variable del ámbito enclosing
    def funcion_interna(z):
        return x + y + z  # Accede a x y y del ámbito enclosing
    return funcion_interna  # Retorna la función interna    

 Clausuras (Closures): El Poder de Enclosing Scope (E)Aquí es donde Python brilla y puede ser un concepto más novedoso para programadores acostumbrados a Go y Java si no han trabajado extensivamente con programación funcional o funciones anónimas/lambda con captura de contexto.Una clausura es una función anidada que "recuerda" el entorno en el que fue creada, incluso si la función externa ya terminó su ejecución. Esto significa que la función anidada puede acceder y manipular variables del ámbito enclosing (el ámbito de la función que la contiene), incluso después de que la función externa haya retornado.Para que una función sea una clausura, debe cumplir dos condiciones:Debe ser una función anidada (una función definida dentro de otra función).Debe referenciar variables de su ámbito externo (no global, no local a ella misma).Ejemplo Básico de Clausura:
 
 def crear_saludador(prefijo):
    # 'prefijo' es una variable del ámbito enclosing
    def saludar(nombre):
        return f"{prefijo}, {nombre}!"
    return saludar

# 'saludar_hola' es una clausura que "recuerda" que prefijo era "Hola"
saludar_hola = crear_saludador("Hola")
# 'saludar_adios' es otra clausura que "recuerda" que prefijo era "Adiós"
saludar_adios = crear_saludador("Adiós")

print(saludar_hola("Juan"))  # Salida: Hola, Juan!
print(saludar_adios("María")) # Salida: Adiós, María!
En este ejemplo, saludar es la función anidada. Captura la variable prefijo de su ámbito envolvente (crear_saludador). Cuando crear_saludador termina, prefijo no desaparece; es "recordado" por las clausuras saludar_hola y saludar_adios.4.1. nonlocal: Modificando Variables del Ámbito EnclosingSimilar a global para variables globales, Python 3 introdujo la palabra clave nonlocal para modificar variables en un ámbito enclosing pero no global. Esto es esencial si tu clausura necesita alterar el estado del ámbito externo.def contador_generador():
    cuenta = 0 # Variable del ámbito enclosing

    def incrementar():
        nonlocal cuenta # Declara que 'cuenta' se refiere a la de 'contador_generador'
        cuenta += 1
        return cuenta

    return incrementar

contador1 = contador_generador()
print(contador1()) # Salida: 1
print(contador1()) # Salida: 2

contador2 = contador_generador() # Crea un nuevo contador independiente
print(contador2()) # Salida: 1
Sin nonlocal, la línea cuenta += 1 dentro de incrementar crearía una nueva variable local cuenta, ocultando la del ámbito envolvente, y el contador no funcionaría como se espera.4.2. Usos Comunes de las Clausuras:Las clausuras son increíblemente útiles para:Fábricas de funciones: Crear funciones personalizadas sobre la marcha, como en el ejemplo crear_saludador.Decoradores: Los decoradores en Python son un caso de uso muy común de las clausuras, donde una función envuelve a otra para añadir funcionalidad.Programación funcional: Mantener estado en un contexto funcional sin usar clases.Callbacks y Event Handlers: Cuando necesitas pasar una función que necesita acceso a cierto estado.Ejemplo de Decorador Simple (usando clausura):def log_llamadas(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__} con argumentos: {args}, {kwargs}")
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} retornó: {resultado}")
        return resultado
    return wrapper

@log_llamadas
def sumar(a, b):
    return a + b

@log_llamadas
def multiplicar(a, b):
    return a * b

print(sumar(5, 3))
print(multiplicar(4, 2))
En este ejemplo, wrapper es una clausura que captura func de su ámbito envolvente (log_llamadas).ConclusiónAunque los conceptos de variables en Python comparten similitudes con Go y Java, el tipado dinámico, la distinción entre mutabilidad/inmutabilidad y el sofisticado sistema de ámbitos (LEGB) con su soporte para clausuras, ofrecen herramientas poderosas y patrones de diseño únicos. Comprender estos matices te permitirá escribir código Python más idiomático, eficiente y robusto, aprovechando al máximo las capacidades del lenguaje. El dominio de las clausuras, en particular, abre la puerta a patrones de programación funcional y la creación de código más flexible y modular.