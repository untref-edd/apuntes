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
description: Programación Orientada a Objetos (POO), herencia múltiple
---

# Programación Orientada a Objetos (POO)

La Programación Orientada a Objetos (POO) es un paradigma de programación que utiliza "objetos" para representar datos y comportamientos. En Python, la POO se implementa a través de clases e instancias de esas clases, los objetos.

Las clases permiten definir nuevos tipos de datos, encapsulando atributos (datos) y métodos (funciones) que operan sobre esos datos. Esto facilita la organización del código, la reutilización y la creación de programas más complejos de manera estructurada.

## Algunos conceptos clave de la POO

Atributos
: Son variables que pertenecen a un objeto y representan su estado interno. Los atributos pueden ser de diferentes tipos, como enteros, cadenas, listas, otros objetos, etc. Cada objeto en memoria tiene sus propios valores para estos atributos. Estos atributos determinan el estado del objeto.

Métodos de instancia
: Son funciones definidas en una clase que operan sobre los atributos del objeto (su estado interno).

Métodos de clase
: Son métodos que pertenecen a la clase en sí, no a las instancias de la clase. Es decir, son funciones que pueden ser llamadas sin necesidad de crear un objeto de la clase. Al ejecutarse en el contexto de la clase, no tiene un vínculo con las instancias que se hayan creado.

Comportamiento
: Se refiere al conjunto de métodos a los que puede responder un objeto. Los métodos definen cómo interactúa el objeto con otros objetos y cómo se comporta en diferentes situaciones.

Herencia
: Permite que una clase herede atributos y métodos de otra clase, lo que facilita la reutilización de código y la creación de jerarquías de clases.
: La clase que hereda se llama "subclase" o "clase derivada", mientras que la clase de la que hereda se llama "superclase" o "clase base". Python soporta herencia múltiple, lo que significa que una clase puede heredar de múltiples clases al mismo tiempo.

Constructor
: Es un método especial que se llama automáticamente cuando se crea un objeto de la clase. La finalidad del constructor es inicializar los atributos del objeto.

## Clases y objetos

En Python, una clase es una plantilla para crear objetos, similar a los `struct` de Go, una clase permite definir nuevos tipos de datos. Un objeto, en cambio, es una instancia de una clase y puede tener atributos (datos) y métodos (funciones). Pueden existir múltiples objetos de la misma clase, cada uno con sus propios valores para los atributos.

```{code-cell} python
---
tags: remove-output
---
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años.")
```

Creamos un objeto de la clase `Persona`.

```{code-cell} python
---
tags: hide-output
---
persona1 = Persona("Alice", 30)
persona1.saludar()
```

Si consultamos el tipo de `persona1` veremos que es la clase `Persona`.

```{code-cell} python
---
tags: hide-output
---
type(persona1)
```

En el ejemplo de código anterior, se define una clase `Persona` con un constructor (`__init__`) que inicializa los atributos `nombre` y `edad`. También se define un método `saludar` que imprime un saludo. Luego, se crea un objeto `persona1` de la clase `Persona` y se llama al método `saludar`.

El constructor en Python siempre es `__init__` y se utiliza para inicializar los atributos del objeto. Si no se declara explícitamente, Python proporcionará un constructor por defecto que no hace nada.

````{important}
El primer parámetro de los métodos de instancia es siempre `self`, que se refiere a la instancia actual del objeto. Esto permite acceder a los atributos y métodos del objeto dentro de la clase. Es similar al `this` de Java, o más parecido a como Go declara el "receptor" al momento de declarar métodos para un tipo de dato creado por nosotros.

```java
public void saludar() {
    // La referencia `this` está disponible de forma implicita.
}
```

```go
func (p *Persona) Saludar() {
    // La referencia a la "instancia" la nombramos nosotros,
    // por convención usamos las iniciales del nombre del tipo
    // que declaramos.
}
```

```python
def saludar(self):
    """
    `self` es equivalente a `this` y a `p` en los ejemplos anteriores.
    Se declara de forma explicita, como si fuera el primer argumento del método.
    """
```
````

## Herencia

Una clase puede heredar de otra clase, o dicho de otra manera, puede extender otra clase. Esto permite que una clase herede atributos y métodos de su ancestro, y los pueda utilizar directamente sin tener que declararlos nuevamente, lo que facilita la reutilización de código y la creación de jerarquías de clases.

```{code-cell} python
---
tags: remove-output
---
class Docente(Persona):
    def __init__(self, nombre, edad, materia):
        super().__init__(nombre, edad)  # Llama al constructor de la clase base
        self.materia = materia

    def presentar(self):
        self.saludar()  # Usa método heredado
        print(f"Soy docente de {self.materia}.")
```

Creamos un objeto de la clase Docente.

```{code-cell} python
---
tags: hide-output
---
docente1 = Docente("Juan", 25, "Algoritmos y Programación")
docente1.presentar()
```

También podemos consultar su tipo.

```{code-cell} python
---
tags: hide-output
---
type(docente1)
```

En el ejemplo anterior, la clase `Docente` hereda de la clase `Persona`. Es decir un `Docente` **_es una_** `Persona` y por lo tanto tiene todos los atributos y métodos de cualquier `Persona` y además tiene nuevos atributos y métodos como `Docente`.

El constructor de la clase `Docente` espera todos los parámetros para poder instanciar un nuevo objeto del tipo `Docente`, esto es el `nombre` y la `edad` de la `Persona` y la `materia` de la que es `Docente`.

Lo primero que hace el constructor de la clase `Docente` es llamar al constructor de la clase base `Persona` utilizando `super().__init__(nombre, edad)` Esto asegura que los atributos `nombre` y `edad` se inicialicen correctamente en el objeto `Docente`.

`super()` es una función que permite llamar a métodos de la clase base desde una subclase. Cuando se invoca `super().__init__(nombre, edad)`, se está llamando al constructor de la clase base `Persona`.

En este caso como tanto `Docente` como `Persona` tienen un constructor, `__init__`, es necesario usar `super()` para llamar al constructor de la clase base, caso contrario, se estaría llamando al constructor de la clase `Docente`.

Con esta estrategia se evita la duplicación de código y se asegura que los atributos de la clase base se inicialicen correctamente. Además, si por algún motivo hay que modificar el constructor de la clase base, no es necesario cambiar el código de la subclase.

En el método `presentar`, se llama al método `saludar` de la clase base `Persona` utilizando `self.saludar()`, lo que permite reutilizar el comportamiento definido en la clase base. En este caso como el método `saludar` no fue **_sobreescrito_** en la clase `Docente`, directamente se puede utilizar `self.saludar()` para llamar al método de la clase base, sin problemas.

### Herencia múltiple

Python va más allá que otros lenguajes de programación orientados a objetos y permite la herencia múltiple, lo que significa que una clase puede heredar de múltiples clases al mismo tiempo. Esto se logra especificando múltiples clases base en la definición de la clase.

```{code-cell} python
---
tags: remove-output
---
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años")


class Docente(Persona):
    def __init__(self, legajo, nombre, edad, materia):
        Persona.__init__(self, nombre, edad)
        self.legajo = legajo  # legajo del Docente como Empleado
        self.materia = materia

    def presentar(self):
        self.saludar()
        print(f"Soy docente de {self.materia}")

    def pagar(self):
        print(f"Pago realizado al docente {self.nombre}, "
              f"con legajo {self.legajo}.")


class Estudiante(Persona):
    def __init__(self, legajo, nombre, edad, carrera):
        Persona.__init__(self, nombre, edad)
        self.legajo = legajo  # legajo del Estudiante como Alumno
        self.carrera = carrera

    def presentar(self):
        self.saludar()
        print(f"Soy estudiante de {self.carrera}")

    def mostrar_legajo(self):
        print(f"Legajo: {self.legajo}, Nombre: {self.nombre}.")

    def actualizar_legajo(self, nuevo_legajo):
        self.legajo = nuevo_legajo
        print(f"Legajo actualizado a: {self.legajo}")


class Ayudante(Estudiante, Docente):
    def __init__(self, legajo, nombre, edad, materia, carrera):
        Estudiante.__init__(self, legajo, nombre, edad, carrera)
        Docente.__init__(self, legajo, nombre, edad, materia)

    def presentar(self):
        self.saludar()
        print(f"Soy estudiante de {self.carrera} y ayudante en "
              f"{self.materia}")
```

Creamos un objeto de la clase Docente.

```{code-cell} python
---
tags: hide-output
---
docente1 = Docente(64781, "Juan", 30, "Algoritmos y Programación")
docente1.presentar()
```

Creamos un objeto de la clase Estudiante.

```{code-cell} python
---
tags: hide-output
---
estudiante1 = Estudiante(30415, "Ana", 20, "Ingeniería en Computación")
estudiante1.presentar()
```

Creamos un objeto de la clase Ayudante.

```{code-cell} python
---
tags: hide-output
---
ayudante1 = Ayudante(
    29478, "Luis", 23, "Algoritmos y Programación", "Ingeniería en Sonido"
)
ayudante1.presentar()
```

```{code-cell} python
---
tags: hide-output
---
type(ayudante1)
```

```{code-cell} python
---
tags: hide-output
---
print("Pagar a docentes")

for docente in [docente1, ayudante1]:
    docente.pagar()
```

```{code-cell} python
---
tags: hide-output
---
print("Mostrar legajo de estudiantes")

for estudiante in [estudiante1, ayudante1]:
    estudiante.mostrar_legajo()
```

Actualizamos el legajo del ayudante

```{code-cell} python
---
tags: hide-output
---
ayudante1.actualizar_legajo(12345)
ayudante1.pagar()
```

Hemos definido cuatro clases: `Persona`, `Docente`, `Estudiante` y `Ayudante`. `Docente` y `Estudiante` heredan de `Persona`, mientras que `Ayudante` hereda de `Estudiante` y `Docente` a través de la herencia múltiple. Lo que le permite a un `Ayudante` heredar el comportamiento de ambas clases además de sumar sus propios atributos y métodos.

En el siguiente _diagrama de clases_ se puede observar la relación entre las clases y los atributos y métodos de cada una.

```{figure} ../_static/figures/1-taller-de-python/1-6-poo/diagrama_ayudante_light.svg
---
class: only-light-mode
---
Diagrama de clases de Ayudante
```

```{figure} ../_static/figures/1-taller-de-python/1-6-poo/diagrama_ayudante_dark.svg
---
class: only-dark-mode
---
Diagrama de clases de Ayudante
```

```{admonition} Diagrama de clases
---
class: hint
---
Un **_diagrama de clases_**, es un diagrama estático que muestra la estructura de un sistema mediante las clases que lo componen y sus relaciones. Una flecha con una línea continua y un triángulo en la punta indica herencia, y en cada clase se pueden ver los atributos y métodos que se definen en cada una.

En general no se muestran los atributos y métodos heredados, ni los constructores, pero si los métodos que se sobrescriben, es decir, que se redefinen en una subclase. En el diagrama anterior el método `presentar` de la clase `Ayudante` sobrescribe el método `presentar` de las clases `Docente` y `Estudiante`.

La relación de herencia se puede leer desde abajo hacia arriba como "es un", es decir, "Ayudante es un Docente" y "Ayudante es un Estudiante" ambas cosas al mismo tiempo y desde arriba hacia abajo como "hereda de" es decir, "Ayudante hereda de Docente" y "Ayudante hereda de Estudiante".
```

Cuando hay herencia múltiple se recomienda utilizar el nombre de la clase base explícitamente en el constructor de la subclase en lugar de `super()`. En la clase `Docente`, se utiliza directamente `Persona` en lugar de usar `super()`, y en la clase `Estudiante` también, para evitar ambigüedades en la resolución de métodos y atributos.

En el ejemplo anterior, tanto `Docente` como `Estudiante` tienen un atributo `legajo`, por lo que al crear un objeto de la clase `Ayudante`, se debe especificar explícitamente a qué clase base se está llamando.

`Ayudante` hereda de ambas clases que tienen un atributo `legajo`, sin embargo el atributo `legajo` no se duplica en un objeto de la clase `Ayudante`. Lo que permite que con el mismo `legajo` de `Estudiante` se pueda pagar al `Docente`.

El siguiente fragmento de código inspecciona los atributos del objeto `ayudante1` y los imprime en la consola (En [Instrospección](1-8-introspeccion.md) veremos más en detalle como los objetos pueden observarse y modificarse a sí mismos en tiempo de ejecución)

```{code-cell} python
---
tags: hide-output
---
print("Atributos de ayudante1:")

atributos = vars(ayudante1)

for key, value in atributos.items():
    print(f"\t- {key}: {value}")
```

## Polimorfismo

El polimorfismo es un concepto clave en la POO que permite que diferentes clases implementen métodos con el mismo nombre, pero con comportamientos diferentes. Esto significa que se puede tratar a objetos de diferentes clases de manera uniforme, utilizando el mismo nombre de método.

En el ejemplo anterior el método `presentar` se define tanto en `Docente` como en `Estudiante`. La clase `Ayudante` hereda ambos métodos y además lo sobreescribe.

Cuando hay herencia múltiple se debe tener cuidado como se resuelve el polimorfismo, ya que puede haber ambigüedades si dos clases base tienen un método con el mismo nombre. En Python, se utiliza el **Orden de Resolución de Métodos (MRO)** para determinar qué método se llama en caso de ambigüedad.

```{code-cell} python
---
tags: hide-output
---
print("Orden de Resolución de Métodos (MRO) de Ayudante:")

orden = Ayudante.__mro__

for cls in orden:
    print(f"\t- {cls.__name__}")
```

Es decir cuando un objeto de la clase `Ayudante` invoca a un método, Python primero busca el método en la propia clase `Ayudante`, luego en `Estudiante`, luego en `Docente`, luego en `Persona` y finalmente en `object`.

Por eso no se puede usar `super()` en el constructor de la clase `Estudiante` ya que si se hiciera, se generaría una ambigüedad en la resolución del método a llamar, ya que `super()` buscaría el siguiente método en la jerarquía de clases, que en este caso sería el constructor de `Docente`. Por lo tanto, se debe usar el nombre de la clase base explícitamente en el constructor de la subclase.

```{hint} <code>object</code>
`object` es la clase base de todas las clases en Python. Todas las clases heredan de `object`, lo que significa que todas las instancias de clases en Python son también instancias de `object`. Esto proporciona una serie de métodos y atributos comunes a todas las clases.

Por eso cuando se dice que en Python todo es un objeto, se refiere a que todas las clases heredan de `object`, y por lo tanto, todas las instancias de clases son también instancias de `object`. Esto permite que todas las clases tengan un comportamiento común, como la capacidad de ser comparadas, impresas, etc.
```

### _Duck typing_

El **_duck typing_** es un concepto en Python que se basa en la idea de que el tipo de un objeto se determina por su comportamiento en lugar de su clase. Es decir, si un objeto tiene los métodos y atributos necesarios para realizar una tarea, se puede tratar como si fuera de un tipo específico, sin necesidad de verificar su clase.

```{epigraph}
"Si camina como un pato, nada como un pato y grazna como un pato, entonces probablemente sea un pato."

-- Principio fundamental del _duck typing_ en Python
```

Este concepto es muy poderoso en Python, ya que permite que diferentes objetos puedan ser utilizados de manera intercambiable si cumplen con la interfaz esperada, sin necesidad de heredar de una clase específica. Todo ocurre de manera implícita, sin necesidad de declarar explícitamente que un objeto es de un tipo específico y sin necesidad de especificar interfaces o clases abstractas como en Java o Go. Esta versatilidad es gracias al sistema de tipos dinámico de Python.

### Ejemplo

En el siguiente ejemplo, cuyo diagrama de clases se muestra a continuación. Primero se define `Punto` que representa un punto en el plano cartesiano y luego se definen las Figuras Geométricas `Cuadrado`, `Punto`, `Elipse` y `Punto` que están **_compuestas_** por `Punto`. Cada figura tiene un método `area` que calcula su área, pero cada figura lo implementa de manera diferente.

```{figure} ../_static/figures/1-taller-de-python/1-6-poo/diagrama_figuras_light.svg
---
class: only-light-mode
---
Diagrama de clases de Figuras Geométricas
```

```{figure} ../_static/figures/1-taller-de-python/1-6-poo/diagrama_figuras_dark.svg
---
class: only-dark-mode
---
Diagrama de clases de Figuras Geométricas
```

```{admonition} Diagrama de clases de Figuras Geométricas
---
class: hint
---
El diagrama de clases de Figuras Geométricas ilustra la relación de **composición** entre la clase `Punto` y las clases `Cuadrado`, `Círculo` y `Elipse`.  Un diamante relleno en el extremo que toca a `Cuadrado`, `Círculo` y `Elipse` y una línea que conecta a estas figuras con `Punto` indica que estas figuras están compuestas por uno o más `Punto`.

La **composición** es un tipo fuerte de relación "tiene un" (has-a), donde un objeto es parte de otro objeto más grande. Por ejemplo, un `Cuadrado` "tiene un" `Punto` que representa su esquina superior izquierda, un `Círculo` y una `Elipse` "tienen un" `Punto` que representa su centro. En este tipo de relación, el objeto "parte" (`Punto`) no puede existir de forma independiente sin el objeto "todo" (`Cuadrado`, `Círculo`, `Elipse`). La vida útil del objeto `Punto` está ligada a la vida útil de la figura geométrica que lo contiene.

En el código, esto se refleja en los constructores de `Cuadrado`, `Círculo` y `Elipse`, que reciben uno o más `Punto` como parámetros para inicializar sus atributos de posición.
```

```{literalinclude} ../_static/code/figuras/main.py
---
language: python
name: figuras
caption: Programación Orientada a Objetos - Figuras Geométricas
---
```

```{code-cell} python
---
tags: remove-input, hide-output
---
%run ../_static/code/figuras/main.py
```

[Descargar código completo de Figuras Geométricas](https://github.com/untref-edd/apuntes/tree/main/contenidos/_static/code/figuras)

## Jerarquías de clases

El siguiente fragmento de código muestra la jerarquía de clases en Python:

```{code-cell} python
---
tags: hide-output
---
import builtins


def print_class_tree(cls, prefix="", is_last=True, current_depth=0, max_depth=4):
    """
    Imprime el árbol de herencia de clases.

    :param cls: La clase raíz desde donde empezar.
    :param prefix: Prefijo para el formato visual (usado en recursión).
    :param is_last: Si es el último nodo de su rama (usado en recursión).
    :param current_depth: Profundidad actual (usado en recursión).
    :param max_depth: Nivel máximo de profundidad a mostrar.
    """

    # Si superamos la profundidad máxima, paramos esta rama
    if current_depth > max_depth:
        return

    # Imprimir el nodo actual
    if current_depth == 0:
        print(cls.__name__)
        new_prefix = ""
    else:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{cls.__name__}")
        new_prefix = prefix + ("    " if is_last else "│   ")

    # Obtener subclases directas
    try:
        subclasses = cls.__subclasses__()
    except TypeError:
        return

    # Filtrar solo clases del módulo 'builtins' (nativas de Python)
    # Esto elimina clases de librerías externas que ensucian el árbol.
    subclasses = [s for s in subclasses if s.__module__ == "builtins"]

    # Ordenar alfabéticamente para que la salida sea predecible
    subclasses.sort(key=lambda x: x.__name__)

    # Llamada recursiva para los hijos
    count = len(subclasses)
    for i, sub in enumerate(subclasses):
        is_last_sub = i == count - 1
        print_class_tree(sub, new_prefix, is_last_sub, current_depth + 1, max_depth)


# --- Ejecución ---
if __name__ == "__main__":
    # max_depth=4 muestra hasta Exception -> ArithmeticError -> ZeroDivisionError
    print_class_tree(object, max_depth=4)
```

## Recursos para profundizar

- [Tutorial de Python - Clases](https://docs.python.org/es/3.13/tutorial/classes.html)
- [Programación Orientada a Objetos (Hektor Profe)](https://hektorprofe.github.io/python/programacion-orientada-a-objetos/)
- [Python - Clases y Objetos (W3Schools)](https://www.w3schools.com/python/python_classes.asp)
