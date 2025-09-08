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

## Clases y Objetos

En Python, una clase es una plantilla para crear objetos, similar a los `struct`{l=go} de Go, una clase permite definir nuevos tipos de datos. Un objeto, en cambio, es una instancia de una clase y puede tener atributos (datos) y métodos (funciones). Pueden existir múltiples objetos de la misma clase, cada uno con sus propios valores para los atributos.

```{code-cell} python
---
tags: [hide-output]
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

En el fragmento de código anterior, se define una clase `Persona`{l=python} con un constructor (`__init__`{l=python}) que inicializa los atributos `nombre`{l=python} y `edad`{l=python}. También se define un método `saludar`{l=python} que imprime un saludo. Luego, se crea un objeto `persona1`{l=python} de la clase `Persona`{l=python} y se llama al método `saludar`{l=python}.

El constructor en Python siempre es `__init__`{l=python} y se utiliza para inicializar los atributos del objeto. Si no se declara explícitamente, Python proporcionará un constructor por defecto que no hace nada.

El primer parámetro de los métodos de instancia es siempre `self`{l=python}, que se refiere a la instancia actual del objeto. Esto permite acceder a los atributos y métodos del objeto dentro de la clase. Es similar al `this`{l=python} de Java.

## Herencia

Una clase puede heredar de otra clase, o dicho de otra manera, puede extender otra clase. Esto permite que una clase herede atributos y métodos de su ancestro, y los pueda utilizar directamente sin tener que declararlos nuevamente, lo que facilita la reutilización de código y la creación de jerarquías de clases.

```{code-cell} python
---
tags: [hide-output]

mystnb:
  number_source_lines: true
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

En el ejemplo anterior, la clase `Docente`{l=python} hereda de la clase `Persona`{l=python}. Es decir un `Docente`{l=python} ***es una*** `Persona`{l=python} y por lo tanto tiene todos los atributos y métodos de cualquier `Persona`{l=python} y además tiene nuevos atributos y métodos como `Docente`

El constructor de la clase `Docente`{l=python} espera todos los parámetros para poder instanciar un nuevo objeto del tipo `Docente`{l=python}, esto es el `nombre`{l=python} y la `edad`{l=python} de la `Persona`{l=python} y la `materia`{l=python} de la que es `Docente`{l=python}.

Lo primero que hace el constructor de la clase `Docente`{l=python} es llamar al constructor de la clase base `Persona`{l=python} (línea 3) utilizando `super().__init__(nombre, edad)`. Esto asegura que los atributos `nombre`{l=python} y `edad`{l=python} se inicialicen correctamente en el objeto `Docente`{l=python}.

`super()` es una función que permite llamar a métodos de la clase base desde una subclase. Cuando se invoca `super().__init__(nombre, edad)`, se está llamando al constructor de la clase base `Persona`{l=python}.

En este caso como tanto `Docente`{l=python} como `Persona`{l=python} tienen un constructor, `__init__`{l=python}, es necesario usar `super()` para llamar al constructor de la clase base, caso contrario, se estaría llamando al constructor de la clase `Docente`{l=python}.

Con esta estrategia se evita la duplicación de código y se asegura que los atributos de la clase base se inicialicen correctamente. Además, si por algún motivo hay que modificar el constructor de la clase base, no es necesario cambiar el código de la subclase.

En el método `presentar`{l=python}, se llama al método `saludar`{l=python} de la clase base `Persona`{l=python} utilizando `self.saludar()`, lo que permite reutilizar el comportamiento definido en la clase base. En este caso como el método `saludar`{l=python} no fue ***sobreescrito*** en la clase `Docente`{l=python}, directamente se puede utilizar `self.saludar()` para llamar al método de la clase base, sin problemas.

### Herencia Múltiple

Python va más allá que otros lenguajes de programación orientados a objetos y permite la herencia múltiple, lo que significa que una clase puede heredar de múltiples clases al mismo tiempo. Esto se logra especificando múltiples clases base en la definición de la clase.

```{code-cell} python
---
tags: [hide-output]

mystnb:
  number_source_lines: true
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

En el fragmento anterior se definen cuatro clases: `Persona`{l=python}, `Docente`{l=python}, `Estudiante`{l=python} y `Ayudante`{l=python}. `Docente`{l=python} y `Estudiante`{l=python} heredan de `Persona`{l=python}, mientras que `Ayudante`{l=python} hereda de `Estudiante`{l=python} y `Docente`{l=python} a través de la herencia múltiple. Lo que le permite a un `Ayudante`{l=python} heredar el comportamiento de ambas clases además de sumar sus propios atributos y métodos.

En el siguiente *diagrama de clases* se puede observar la relación entre las clases y los atributos y métodos de cada una.

```{figure} ../assets/images/diagrama_ayudante.png
---
name: ayudante-diagrama
---
Diagrama de clases de Ayudante
```

```{Note}
Un ***diagrama de clases***, es un diagrama estático que muestra la estructura de un sistema mediante las clases que lo componen y sus relaciones. Una flecha con una línea continua y un triángulo en la punta indica herencia, y en cada clase se pueden ver los atributos y métodos que se definen en cada una. En general no se muestran los atributos y métodos heredados, ni los constructores, pero si los métodos que se sobrescriben, es decir, que se redefinen en una subclase. En el diagrama anterior el método `presentar`{l=python} de la clase `Ayudante`{l=python} sobrescribe el método `presentar`{l=python} de las clases `Docente`{l=python} y `Estudiante`{l=python}.
```

Cuando hay herencia múltiple se recomienda utilizar el nombre de la clase base explícitamente en el constructor de la subclase en lugar de `super()`. En la clase `Docente`{l=python}, línea 12 se utiliza directamente `Persona`{l=python} en lugar de usar `super()`, y en la línea 26 de la clase `Estudiante`{l=python} también, para evitar ambigüedades en la resolución de métodos y atributos.

En el ejemplo anterior, tanto `Docente`{l=python} como `Estudiante`{l=python} tienen un atributo `legajo`{l=python}, por lo que al crear un objeto de la clase `Ayudante`{l=python}, se debe especificar explícitamente a qué clase base se está llamando.

`Ayudante`{l=python} hereda de ambas clases que tienen un atributo `legajo`{l=python}, sin embargo el atributo `legajo`{l=python} no se duplica en un objeto de la clase `Ayudante`{l=python}. Lo que permite que con el mismo `legajo`{l=python} de `Estudiante`{l=python} se pueda pagar al `Docente`{l=python}.

El siguiente fragmento de código inspecciona los atributos del objeto `ayudante1`{l=python} y los imprime en la consola (En [Instrospección](1-8-introspeccion.md) veremos más en detalle como los objetos pueden observarse y modificarse a si mismos en tiempo de ejecución)

```{code-cell} python
---
tags: [hide-output]
---
print("Atributos de ayudante1:")
atributos = vars(ayudante1)
for key, value in atributos.items():
    print(f"{key}: {value}")
```

## Polimorfismo

El polimorfismo es un concepto clave en la POO que permite que diferentes clases implementen métodos con el mismo nombre, pero con comportamientos diferentes. Esto significa que se puede tratar a objetos de diferentes clases de manera uniforme, utilizando el mismo nombre de método.

En el ejemplo anterior el método `presentar`{l=python} se define tanto en `Docente`{l=python} como en `Estudiante`{l=python}. La clase `Ayudante`{l=python} hereda ambos métodos y además lo sobreescribe.

Cuando hay herencia múltiple se debe tener cuidado como se resuelve el polimorfismo, ya que puede haber ambigüedades si dos clases base tienen un método con el mismo nombre. En Python, se utiliza el **Orden de Resolución de Métodos (MRO)** para determinar qué método se llama en caso de ambigüedad.

```{code-cell} python
---
tags: [hide-output]
---
print("Orden de Resolución de Métodos (MRO) de Ayudante:")
orden = Ayudante.__mro__
for cls in orden:
    print(cls.__name__)
```

Es decir cuando se invoca un método cualquier de un objeto de la clase `Ayudante`{l=python}, Python primero busca el método en la propia clase `Ayudante`{l=python}, luego en `Estudiante`{l=python}, luego en `Docente`{l=python}, luego en `Persona`{l=python} y finalmente en `object`{l=python}.

Por ese motivo no se puede usar `super()` en el constructor de la clase `Estudiante`{l=python} ya que si se hiciera, se generaría una ambigüedad en la resolución del método a llamar, ya que `super()` buscaría el siguiente método en la jerarquía de clases, que en este caso sería el constructor de `Docente`{l=python}, lo que no es lo que se desea.

```{Note}
`object`{l=python} es la clase base de todas las clases en Python. Todas las clases heredan de `object`{l=python}, lo que significa que todas las instancias de clases en Python son también instancias de `object`{l=python}. Esto proporciona una serie de métodos y atributos comunes a todas las clases.

Por eso cuando se dice que en Python todo es un objeto, se refiere a que todas las clases heredan de `object`{l=python}, y por lo tanto, todas las instancias de clases son también instancias de `object`{l=python}. Esto permite que todas las clases tengan un comportamiento común, como la capacidad de ser comparadas, impresas, etc.
```

### Duck Typing

El **Duck Typing** es un concepto en Python que se basa en la idea de que el tipo de un objeto se determina por su comportamiento en lugar de su clase. Es decir, si un objeto tiene los métodos y atributos necesarios para realizar una tarea, se puede tratar como si fuera de un tipo específico, sin necesidad de verificar su clase.

```{epigraph}
"Si camina como un pato, nada como un pato y grazna como un pato, entonces probablemente sea un pato."
---
Principio fundamental del Duck Typing en Python
```

Este concepto es muy poderoso en Python, ya que permite que diferentes objetos puedan ser utilizados de manera intercambiable si cumplen con la interfaz esperada, sin necesidad de heredar de una clase específica. Todo ocurre de manera implícita, sin necesidad de declarar explícitamente que un objeto es de un tipo específico y sin necesidad de especificar interfaces o clases abstractas como en Java o Go. Esta versatilidad es gracias al sistema de tipos dinámico de Python.

### Ejemplo

En el siguiente ejemplo, cuyo diagrama de clases se muestra a continuación. Primero se define `Punto`{l=python} que representa un punto en el plano cartesiano y luego se definen las Figuras Geométricas `Cuadrado`{l=python}, `Punto`{l=python} `Elipse`{l=python}y `Punto`{l=python} que están ***compuestas*** por `Punto`{l=python}. Cada figura tiene un método `area`{l=python} que calcula su área, pero cada figura lo implementa de manera diferente.

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
tags: [hide-input, remove-input, hide-output]
---
%run ../_static/code/figuras/main.py
```

[Descargar código completo de Figuras Geométricas](https://github.com/untref-edd/apuntes/tree/main/contenidos/_static/code/figuras){target="\_blank"}

## Recursos para profundizar

- [Tutorial de Python - Clases](https://docs.python.org/es/3.13/tutorial/classes.html){target="\_blank"}
- [Programación Orientada a Objetos (Hektor Profe)](https://hektorprofe.github.io/python/programacion-orientada-a-objetos/){target="\_blank"}
- [Python - Clases y Objetos (W3Schools)](https://www.w3schools.com/python/python_classes.asp){target="\_blank"}
