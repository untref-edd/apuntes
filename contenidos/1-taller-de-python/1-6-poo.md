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
: Son variables que pertenecen a una clase y representan el estado del objeto. Los atributos pueden ser de diferentes tipos, como enteros, cadenas, listas, etc. Cada objeto en memoria tiene sus propios valores para estos atributos. Estos atributos determinan el estado del objeto.

Métodos de Instancia
: Son funciones definidas dentro de una clase que operan sobre los atributos del objeto.

Métodos de Clase
: Son métodos que pertenecen a la clase en sí, no a las instancias de la clase. Es decir, son funciones que pueden ser llamadas sin necesidad de crear un objeto de la clase.

Comportamiento
: Se refiere al conjunto de métodos a los que puede responder un objeto. Los métodos definen cómo interactúa el objeto con otros objetos y cómo se comporta en diferentes situaciones.

Herencia
: Permite que una clase herede atributos y métodos de otra clase, lo que facilita la reutilización de código y la creación de jerarquías de clases. La clase que hereda se llama "subclase" o "clase derivada", mientras que la clase de la que hereda se llama "superclase" o "clase base". Python soporta herencia múltiple, lo que significa que una clase puede heredar de múltiples clases al mismo tiempo.

Constructor
: Es un método especial que se llama automáticamente cuando se crea un objeto de la clase. La finalidad del constructor es inicializar los atributos del objeto.

## Clases y objetos

En Python, una clase es una plantilla para crear objetos, similar a los `struct` de Go, una clase permite definir nuevos tipos de datos. Un objeto, en cambio, es una instancia de una clase y puede tener atributos (datos) y métodos (funciones). Pueden existir múltiples objetos de la misma clase, cada uno con sus propios valores para los atributos.

```{code-cell} python
---
tags: hide-output
---
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años.")


# Crear un objeto de la clase Persona
persona1 = Persona("Alice", 30)
persona1.saludar()
print(type(persona1))
```

En el fragmento de código anterior, se define una clase `Persona` con un constructor (`__init__`) que inicializa los atributos `nombre` y `edad`. También se define un método `saludar` que imprime un saludo. Luego, se crea un objeto `persona1` de la clase `Persona` y se llama al método `saludar`.

El constructor en Python siempre es `__init__` y se utiliza para inicializar los atributos del objeto. Si no se declara explícitamente, Python proporcionará un constructor por defecto que no hace nada.

El primer parámetro de los métodos de instancia es siempre `self`, que se refiere a la instancia actual del objeto. Esto permite acceder a los atributos y métodos del objeto dentro de la clase. Es similar al `this` de Java.

## Herencia

Una clase puede heredar de otra clase, o dicho de otra manera, puede extender otra clase. Esto permite que una clase herede atributos y métodos de su ancestro, y los pueda utilizar directamente sin tener que declararlos nuevamente, lo que facilita la reutilización de código y la creación de jerarquías de clases.

```{code-cell} python
---
tags: hide-output
---
class Docente(Persona):
    def __init__(self, nombre, edad, materia):
        super().__init__(nombre, edad)  # Llama al constructor de la clase base
        self.materia = materia

    def presentar(self):
        self.saludar()  # Usa método heredado
        print(f"Soy docente de {self.materia}.")


# Crear un objeto de la clase Docente
docente1 = Docente("Juan", 25, "Algoritmos y Programación")
docente1.presentar()
print(type(docente1))
```

En el ejemplo anterior, la clase `Docente` hereda de la clase `Persona`. Es decir un `Docente` ***es una*** `Persona` y por lo tanto tiene todos los atributos y métodos de cualquier `Persona` y además tiene nuevos atributos y métodos como `Docente`.

El constructor de la clase `Docente` espera todos los parámetros para poder instanciar un nuevo objeto del tipo `Docente`, esto es el `nombre` y la `edad` de la `Persona` y la `materia` de la que es `Docente`.

Lo primero que hace el constructor de la clase `Docente` es llamar al constructor de la clase base `Persona` (línea 3) utilizando `super().__init__(nombre, edad)` Esto asegura que los atributos `nombre` y `edad` se inicialicen correctamente en el objeto `Docente`.

`super()` es una función que permite llamar a métodos de la clase base desde una subclase. Cuando se invoca `super().__init__(nombre, edad)`, se está llamando al constructor de la clase base `Persona`.

En este caso como tanto `Docente` como `Persona` tienen un constructor, `__init__`, es necesario usar `super()` para llamar al constructor de la clase base, caso contrario, se estaría llamando al constructor de la clase `Docente`.

Con esta estrategia se evita la duplicación de código y se asegura que los atributos de la clase base se inicialicen correctamente. Además, si por algún motivo hay que modificar el constructor de la clase base, no es necesario cambiar el código de la subclase.

En el método `presentar`, se llama al método `saludar` de la clase base `Persona` utilizando `self.saludar()`, lo que permite reutilizar el comportamiento definido en la clase base. En este caso como el método `saludar` no fue ***sobreescrito*** en la clase `Docente`, directamente se puede utilizar `self.saludar()` para llamar al método de la clase base, sin problemas.

### Herencia múltiple

Python va más allá que otros lenguajes de programación orientados a objetos y permite la herencia múltiple, lo que significa que una clase puede heredar de múltiples clases al mismo tiempo. Esto se logra especificando múltiples clases base en la definición de la clase.

```{code-cell} python
---
tags: hide-output
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
        print(f"Pago realizado al docente {self.nombre}, con legajo {self.legajo}.")


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
        print(f"Soy estudiante de {self.carrera} y ayudante en {self.materia}")


# Crear un objeto de la clase Docente
docente1 = Docente(64781, "Juan", 30, "Algoritmos y Programación")
docente1.presentar()
print()

# Crear un objeto de la clase Estudiante
estudiante1 = Estudiante(30415, "Ana", 20, "Ingeniería en Computación")
estudiante1.presentar()
print()

# Crear un objeto de la clase Ayudante
ayudante1 = Ayudante(
    29478, "Luis", 23, "Algoritmos y Programación", "Ingeniería en Sonido"
)
ayudante1.presentar()
print()
print(type(ayudante1))

print("Pagar a docentes")
for docente in [docente1, ayudante1]:
    docente.pagar()  # Llama al método pagar de Docente
print()

print("Mostrar legajo de estudiantes")
for estudiante in [estudiante1, ayudante1]:
    estudiante.mostrar_legajo()
print()

# Actualizamos el legajo del ayudante
ayudante1.actualizar_legajo(12345)
ayudante1.pagar()
```

En el fragmento anterior se definen cuatro clases: `Persona`, `Docente`, `Estudiante` y `Ayudante`. `Docente` y `Estudiante` heredan de `Persona`, mientras que `Ayudante` hereda de `Estudiante` y `Docente` a través de la herencia múltiple. Lo que le permite a un `Ayudante` heredar el comportamiento de ambas clases además de sumar sus propios atributos y métodos.

En el siguiente *diagrama de clases* se puede observar la relación entre las clases y los atributos y métodos de cada una.

```{figure} ../assets/images/diagrama_ayudante.png
---
name: ayudante-diagrama
---
Diagrama de clases de Ayudante
```

```{note} Nota
Un ***diagrama de clases***, es un diagrama estático que muestra la estructura de un sistema mediante las clases que lo componen y sus relaciones. Una flecha con una línea continua y un triángulo en la punta indica herencia, y en cada clase se pueden ver los atributos y métodos que se definen en cada una. En general no se muestran los atributos y métodos heredados, ni los constructores, pero si los métodos que se sobrescriben, es decir, que se redefinen en una subclase. En el diagrama anterior el método `presentar` de la clase `Ayudante` sobrescribe el método `presentar` de las clases `Docente` y `Estudiante`.
```

Cuando hay herencia múltiple se recomienda utilizar el nombre de la clase base explícitamente en el constructor de la subclase en lugar de `super()`. En la clase `Docente`, línea 12 se utiliza directamente `Persona` en lugar de usar `super()`, y en la línea 26 de la clase `Estudiante` también, para evitar ambigüedades en la resolución de métodos y atributos.

En el ejemplo anterior, tanto `Docente` como `Estudiante` tienen un atributo `legajo`, por lo que al crear un objeto de la clase `Ayudante`, se debe especificar explícitamente a qué clase base se está llamando.

`Ayudante` hereda de ambas clases que tienen un atributo `legajo`, sin embargo el atributo `legajo` no se duplica en un objeto de la clase `Ayudante`. Lo que permite que con el mismo `legajo` de `Estudiante` se pueda pagar al `Docente`.

El siguiente fragmento de código inspecciona los atributos del objeto `ayudante1` y los imprime en la consola (En [Instrospección](1-8-introspeccion.md) veremos más en detalle como los objetos pueden observarse y modificarse a si mismos en tiempo de ejecución)

```{code-cell} python
---
tags: hide-output
---
print("Atributos de ayudante1:")
atributos = vars(ayudante1)
for key, value in atributos.items():
    print(f"{key}: {value}")
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
    print(cls.__name__)
```

Es decir cuando se invoca un método cualquier de un objeto de la clase `Ayudante`, Python primero busca el método en la propia clase `Ayudante`, luego en `Estudiante`, luego en `Docente`, luego en `Persona` y finalmente en `object`.

Por ese motivo no se puede usar `super()` en el constructor de la clase `Estudiante` ya que si se hiciera, se generaría una ambigüedad en la resolución del método a llamar, ya que `super()` buscaría el siguiente método en la jerarquía de clases, que en este caso sería el constructor de `Docente`, lo que no es lo que se desea.

```{note} Nota
`object` es la clase base de todas las clases en Python. Todas las clases heredan de `object`, lo que significa que todas las instancias de clases en Python son también instancias de `object`. Esto proporciona una serie de métodos y atributos comunes a todas las clases.

Por eso cuando se dice que en Python todo es un objeto, se refiere a que todas las clases heredan de `object`, y por lo tanto, todas las instancias de clases son también instancias de `object`. Esto permite que todas las clases tengan un comportamiento común, como la capacidad de ser comparadas, impresas, etc.
```

### *Duck typing*

El ***duck typing*** es un concepto en Python que se basa en la idea de que el tipo de un objeto se determina por su comportamiento en lugar de su clase. Es decir, si un objeto tiene los métodos y atributos necesarios para realizar una tarea, se puede tratar como si fuera de un tipo específico, sin necesidad de verificar su clase.

```{epigraph}
"Si camina como un pato, nada como un pato y grazna como un pato, entonces probablemente sea un pato."
---
Principio fundamental del _duck typing_ en Python
```

Este concepto es muy poderoso en Python, ya que permite que diferentes objetos puedan ser utilizados de manera intercambiable si cumplen con la interfaz esperada, sin necesidad de heredar de una clase específica. Todo ocurre de manera implícita, sin necesidad de declarar explícitamente que un objeto es de un tipo específico y sin necesidad de especificar interfaces o clases abstractas como en Java o Go. Esta versatilidad es gracias al sistema de tipos dinámico de Python.

### Ejemplo

En el siguiente ejemplo, cuyo diagrama de clases se muestra a continuación. Primero se define `Punto` que representa un punto en el plano cartesiano y luego se definen las Figuras Geométricas `Cuadrado`, `Punto` `Elipse`y `Punto` que están ***compuestas*** por `Punto`. Cada figura tiene un método `area` que calcula su área, pero cada figura lo implementa de manera diferente.

```{figure} ../assets/images/diagrama_figuras.png
---
name: figuras-diagrama
---
Diagrama de clases de Figuras Geométricas
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

## Recursos para profundizar

- [Tutorial de Python - Clases](https://docs.python.org/es/3.13/tutorial/classes.html)
- [Programación Orientada a Objetos (Hektor Profe)](https://hektorprofe.github.io/python/programacion-orientada-a-objetos/)
- [Python - Clases y Objetos (W3Schools)](https://www.w3schools.com/python/python_classes.asp)
