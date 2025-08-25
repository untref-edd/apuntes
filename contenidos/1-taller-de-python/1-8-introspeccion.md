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

# Introspección y Reflexión

## Definiciones

Introspección
: Es la capacidad de un programa para **examinar su propia estructura y estado en tiempo de ejecución**.\
: En Python, gracias a su naturaleza dinámica, podemos inspeccionar tipos, atributos y métodos de objetos, incluso sin conocerlos de antemano.

Reflexión
: Va un paso más allá: no solo inspecciona, sino que **modifica el comportamiento o la estructura** de objetos, clases o módulos en tiempo de ejecución.

```{note}
En **Java** estas capacidades existen mediante *Reflection API*, mientras que en **Go** se logran con el paquete `reflect`{l=python}. En Python, estas herramientas están integradas en el propio lenguaje y son mucho más accesibles.
```

## Herramientas comunes de introspección y reflexión

| Función                         | Descripción                                             |
| ------------------------------- | ------------------------------------------------------- |
| `type(obj)`                     | Devuelve el tipo del objeto.                            |
| `dir(obj)`                      | Lista atributos y métodos disponibles.                  |
| `id(obj)`                       | Identificador único en memoria.                         |
| `vars(obj)`                     | Diccionario de atributos de instancia.                  |
| `getattr(obj, name[, default])` | Obtiene un atributo dinámicamente.                      |
| `setattr(obj, name, value)`     | Asigna un atributo dinámicamente.                       |
| `hasattr(obj, name)`            | Verifica si un atributo existe.                         |
| `callable(obj)`                 | Indica si el objeto es invocable como función o método. |
| `help(obj)`                     | Muestra la documentación.                               |

______________________________________________________________________

## Ejemplo básico de introspección

```{code-cell} python
---
tags: [hide-output]
---
class Persona:
    """Clase simple para ejemplo de introspección."""

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")


# Crear instancia
persona = Persona("Alice", 30)

# Inspección
print("Tipo de objeto:", type(persona))
print("Atributos de instancia:", vars(persona))
print("ID (memoria):", id(persona))
print("¿Tiene atributo 'nombre'?", hasattr(persona, "nombre"))
print("Nombre:", getattr(persona, "nombre"))

# Modificación controlada
setattr(persona, "edad", 31)
print("Edad actualizada:", getattr(persona, "edad"))

# Verificar invocabilidad
print("¿Es 'persona' invocable?", callable(persona))
print("¿Es 'persona.saludar' invocable?", callable(persona.saludar))
```

## Ejemplo de reflexión con cautela

En Python es posible agregar atributos o métodos a un objeto existente en tiempo de ejecución.
Esto otorga flexibilidad, pero puede volver el código difícil de mantener si se abusa.

```{code-cell} python
---
tags: [hide-output]
---
import types


class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")


juan = Persona("Juan", 40)
ana = Persona("Ana", 35)

# Agregar atributos en tiempo de ejecución
juan.telefono = "123-456-7890"
ana.domicilio = "La Merced 123"


# Agregar un método personalizado solo a 'juan'
def saludar_con_telefono(self):
    print(
        f"Hola, soy {self.nombre}, tengo {self.edad} años y mi teléfono es {self.telefono}."
    )


juan.saludar = types.MethodType(saludar_con_telefono, juan)

# Uso
juan.saludar()
ana.saludar()
```

## Uso de `help()` para documentación

`help()` es una función incorporada en Python que proporciona información sobre objetos, funciones y módulos. Es especialmente útil para obtener documentación sobre cómo usar un objeto o qué métodos y atributos tiene.

```{code-cell} python
---
tags: [hide-output]
---
class Persona:
    """Clase simple para ejemplo de documentación."""

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        """Método para saludar."""
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")


# Crear instancia
alice = Persona("Alice", 30)

# Usar help()
help(alice)
```

## Uso de `eval()` para evaluar expresiones

La función `eval()` permite ejecutar expresiones Python desde una cadena de texto. Esto puede ser útil para evaluar dinámicamente código, pero **debe usarse con extrema precaución** debido a implicaciones de seguridad.

Por ejemplo, el siguiente código es peligroso si la variable `expresion`{l=python} proviene de un usuario no confiable:

```python
expresion = input("Introduce una expresión: ")
resultado = eval(
    expresion
)  # ¡Peligroso! El usuario puede ejecutar cualquier código Python.
print("Resultado de la expresión:", resultado)
```

```{Important} Advertencia de seguridad
Nunca se debe utilizar `eval()` con entradas que provengan de usuarios o fuentes no confiables. Hacerlo puede permitir la ejecución de código malicioso y comprometer la seguridad del sistema.
```

```{code-cell} python
---
tags: [hide-output]
---
x = 10
expresion = "x * 2"
resultado = eval(expresion)
print("Resultado de la expresión:", resultado)
```

## Buenas Prácticas

La introspección y reflexión son herramientas poderosas pero que se deben utilizar con responsabilidad para construir ***código flexible*** y no ***código frágil***. Algunas recomendaciones son:

- Usar introspección para depuración
- No usar introspección y reflexión como sustituto de un buen diseño
- Evitar abusar de la reflexión para modificar clases/objetos, ya que reduce la previsibilidad del código.
- Documentar cambios dinámicos para facilitar mantenimiento.
- Si se requiere reflexión, documentar claramente y mantener el cambio localizado.
- En proyectos grandes, preferir patrones de diseño que hagan explícitas las extensiones (por ejemplo, decoradores).
- Preferir alternativas explícitas (herencia, interfaces, polimorfismo) cuando sea posible.

## Recursos para profundizar

- [Documentación oficial de Python sobre introspección](https://docs.python.org/es/3.13/library/inspect.html){target="\_blank"}
- [Artículos sobre metaprogramación en Python (Real Python)](https://realpython.com/learning-paths/metaprogramming-in-python/){target="\_blank"}
