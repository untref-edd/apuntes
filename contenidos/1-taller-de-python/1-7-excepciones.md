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

# Manejo de excepciones

Las excepciones son eventos que ocurren durante la ejecución de un programa y que interrumpen su flujo normal. Este mecanismo no solo permite manejar errores en tiempo de ejecución, sino que también permite gestionar otras situaciones excepcionales que pueden surgir.

El mecanismo de manejo de excepciones se basa en el uso de bloques `try`{l=python}, `except`{l=python}, `else`{l=python} y `finally`{l=python}. Por cada bloque `try`{l=python} puede haber uno o varios bloques `except`{l=python}, uno por cada tipo de excepción que se quiera manejar. A continuación, se describen cada uno de estos bloques

```{code-block} python
try:
    # Bloque protegido: Código que puede generar una excepciones
    llamado_a_funcion_que_puede_fallar()

except ExceptionType1:
    print("ocurrió una excepción del tipo ExceptionType1")

except (ExceptionType2, ExceptionType3):
    print("ocurrió una excepción que puede ser de tipo ExceptionType2 o ExcepcionType3")

except ExceptionType4 as e:
    # Manejador de excepciones del tipo ExceptionType4. `e` es una variable con
    # información sobre la excepción que se puede usar dentro del handler
    print("ocurrió un error del tipo ExceptionType4 con mensaje", e)

except:
    print("se produjo una excepción no controlada")

else:
    print("no ocurrió ninguna excepción")

finally:
    print("este bloque se ejecutará siempre")
```

`try`{l=python}
: Este bloque contiene el código que podría generar una excepción. Mientras se ejecuta este bloque, Python *“vigila”* la aparición de errores.
: Si se produce una excepción, la ejecución del bloque `try`{l=python} se interrumpe inmediatamente y se transfiere el control al primer `except`{l=python} que pueda manejarla.
: Se suele decir que el código dentro de un `try`{l=python} está ***protegido***, porque ante un error no provoca que el programa finalice abruptamente, sino que permite reaccionar y manejar la situación. Por ejemplo, si debemos dividir dos números cuyo valor no conocemos de antemano, existe la posibilidad de una división por cero; por eso el cálculo puede colocarse dentro de un bloque `try`{l=python} para atraparlo y manejarlo.

`except`{l=python}
: En Python, un bloque `except`{l=python} se ejecuta solo si ocurre una excepción en el bloque `try`{l=python} asociado. Este bloque actúa como un ***manejador de excepciones*** (*exception handler*) y puede realizar diversas acciones: registrar el error en un log, mostrar un mensaje al usuario, o incluso intentar recuperarse ejecutando una operación alternativa.
: El comportamiento del `except`{l=python} depende del tipo de excepción y de la lógica del programa. Por ejemplo, si se produce una división por cero (`ZeroDivisionError`{l=python}), el `except`{l=python} podría mostrar un mensaje de error o sustituir el divisor por un valor por defecto para continuar la ejecución.
: Si no ocurre ninguna excepción en el bloque `try`{l=python}, ningún `except`{l=python} se ejecuta y el flujo continúa normalmente después del `try`{l=python}/`except`{l=python}.
: Cuando se lanza una excepción, Python busca el primer bloque `except`{l=python} que pueda manejarla.
: La búsqueda se hace de arriba hacia abajo en el orden en que están escritos, por lo que conviene colocar primero los `except`{l=python} que capturan excepciones más específicas y dejar al final un `except`{l=python} genérico.
: El `except`{l=python} genérico no especifica un tipo de excepción y atrapa cualquier excepción que sea instancia de `Exception`{l=python}.

`else`{l=python}
: Es un bloque opcional que se ejecuta solo si el bloque `try`{l=python} termina sin generar excepciones.
: Se usa para colocar el código que depende de que la operación haya salido bien, pero que no conviene poner directamente en el `try`{l=python} para no atrapar errores de forma innecesaria.
: En otras palabras: `try`{l=python} → si no hay error → `else`{l=python}. Si hay error → `except`{l=python} (y el `else`{l=python} no se ejecuta).

`finally`{l=python}
: Es un bloque opcional que se ejecuta siempre, sin importar si el `try`{l=python} terminó con o sin excepción.
: Sirve para ejecutar tareas de limpieza o liberación de recursos que deben realizarse pase lo que pase, como cerrar un archivo, liberar memoria o cerrar una conexión de red.
: Incluso si en el `try`{l=python} o `except`{l=python} se usa `return`{l=python} o se lanza una nueva excepción, el `finally`{l=python} siempre se ejecuta antes de que el flujo salga del bloque.

```{code-cell} python
---
tags: [hide-output]
---
divisor = "10"  # cadena de caracteres

try:
    # Código que puede generar excepciones
    resultado = 10 // int(divisor)  # // División entera

except ZeroDivisionError as e:
    # Manejo de la excepción división por cero
    print(f"No se puede dividir por cero: {e}")

except ValueError as e:
    # Manejo de la excepción para valores no numéricos
    print(f"Error: {e}")

except:
    # Manejador de excepciones genérico
    print("Se produjo una excepción no controlada")

else:
    # Este bloque se ejecuta si no hay excepciones
    print("La división fue exitosa:", resultado)

finally:
    # Este bloque se ejecuta siempre
    print("Bloque finally ejecutado")
```

```{hint}
Activa **Live Code** (icono de un cohete en la parte superior derecha) para ejecutar el código anterior. Por ejemplo podés probar asignando distintos valores a `divisor`{l=python} como ser "0", la cadena "cero", números enteros, números decimales, y todo lo que se te ocurra.

¿Qué pasa en cada caso? ¿Es buena idea tener un bloque `except`{l=python} genérico?
```

## Jerarquía de excepciones

En Python existen muchas excepciones predefinidas que están organizadas en forma jerárquica. Es decir que algunas excepciones son subclases de otras. Por ejemplo, `ZeroDivisionError`{l=python} es una subclase de `ArithmeticError`{l=python}, que a su vez es una subclase de `Exception`{l=python}. Esto significa que si se captura una excepción de tipo `ArithmeticError`{l=python}, también se capturarán las excepciones de tipo `ZeroDivisionError`{l=python}.

La jerarquia de excepciones permite manejar las excepciones de manera más específica y detallada. Por ejemplo, si se desea manejar todas las excepciones relacionadas con operaciones aritméticas, se puede capturar la excepción `ArithmeticError`{l=python}. Si se desea manejar solo las excepciones de división por cero, se puede capturar la excepción `ZeroDivisionError`{l=python}.

````{admonition} Click para ver la jerarquía de excepciones
---
class: dropdown
---
```
BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
```
````

`KeyboardInterrupt`{l=python}
: Esta excepción se genera cuando el usuario interrumpe la ejecución del programa, generalmente presionando `Ctrl+C` en la consola. Es una subclase de `BaseException`{l=python}, lo que significa que no es una excepción común y no se debe capturar a menos que se tenga un motivo específico para hacerlo.

`SystemExit`{l=python}
: Esta excepción se genera cuando se llama a la función `sys.exit()`{l=python}. Se utiliza para finalizar un programa de manera controlada. Al igual que `KeyboardInterrupt`{l=python}, es una subclase de `BaseException`{l=python}, por lo que no se debe capturar a menos que se tenga un motivo específico para hacerlo.

`Exception`{l=python}
: Esta es la clase base para todas las excepciones que no son errores del sistema. Todas las excepciones que se generan durante la ejecución de un programa son subclases de `Exception`{l=python}.

`Warning`{l=python}
: Esta clase base se utiliza para advertencias que no son errores, pero que pueden indicar problemas potenciales en el código. Las advertencias no interrumpen la ejecución del programa, pero pueden ser útiles para identificar problemas que podrían surgir en el futuro. Por ejemplo, si se utiliza una función que está obsoleta, Python generará una advertencia de deprecación. Las advertencias se pueden capturar y manejar de manera similar a las excepciones, pero generalmente no se recomienda hacerlo, ya que las advertencias son más informativas que críticas.

En el siguiente fragmento de código se observa un bucle donde se le pide al usuario que ingrese un número entero por teclado y se acumula la suma para finalmente mostrarla. Para salir del bucle el usuario debe presionar `Ctrl-C`

```{literalinclude} ../_static/code/excepciones/excepciones.py
```

## Excepciones creadas por el usuario

Además de las excepciones predefinidas, Python permite a los desarrolladores crear sus propias excepciones personalizadas. Esto es útil cuando se desea manejar situaciones específicas que no están cubiertas por las excepciones predefinidas. Por ejemplo si tenemos una clase pila, podríamos querer lanzar una excepción si se intenta desapilar un elemento de una pila vacía. Podemos crear una excepción personalizada llamada `StackException`{l=python} para manejar esta situación. Para crear una excepción personalizada, se debe definir una nueva clase que herede de la clase `Exception`{l=python} o de alguna de sus subclases. En general se recomienda heredar directamente de `Exception`{l=python}, a menos que se tenga un motivo específico para hacerlo de otra manera, por ejemplo si se desea crear una jerarquía de excepciones personalizadas.

El cuerpo de la clase puede estar vacío, ya que la funcionalidad principal de la excepción se hereda de la clase base. Sin embargo, se pueden agregar atributos o métodos adicionales si se desea proporcionar información adicional sobre la excepción.

```{literalinclude} ../_static/code/stack/stack_exception.py
```

### ¿Porqué crear excepciones personalizadas?

Crear excepciones personalizadas tiene varias ventajas, entre ellas:

Claridad
: Las excepciones personalizadas pueden tener nombres descriptivos que indican claramente el tipo de error que ha ocurrido. Esto facilita la comprensión del código y la identificación de problemas. Por ejemplo si se produce una excepción al intentar desapilar de una pila vacía que está implementada usando listas, una excepción personalizada llamada `StackException`{l=python} es más clara que una excepción genérica como `IndexError`{l=python}.

Manejo específico
: Al crear excepciones personalizadas, se puede manejar de manera específica cada tipo de error. Esto permite implementar lógica de manejo de errores más precisa y adecuada para cada situación.

Jerarquía de excepciones
: Al crear una jerarquía de excepciones personalizadas, se puede organizar y estructurar el manejo de errores de manera más efectiva. Por ejemplo, se puede crear una excepción base para un módulo o una clase, y luego crear subclases para manejar errores específicos dentro de ese contexto.

Reutilización
: Las excepciones personalizadas pueden ser reutilizadas en diferentes partes del código o en diferentes proyectos, lo que facilita la consistencia en el manejo de errores.

Documentación
: Las excepciones personalizadas pueden incluir documentación adicional que explique cuándo y por qué se deben lanzar, lo que ayuda a otros desarrolladores a entender su propósito y uso.

## Lanzando excepciones

Las excepciones se lanzan utilizando la instrucción `raise`{l=python}, seguida de una instancia de la excepción que se desea lanzar. Por ejemplo, si se desea lanzar una excepción personalizada llamada `StackException`{l=python}, se puede hacer de la siguiente manera:

```python
raise StackException("La pila está vacía")
```

En el manejo de excepciones hay dos momentos bien definidos, cuando se ***lanza una excepción*** y cuando se ***captura una excepción***.

El lanzamiento se realiza cuando surge una situación excepcional que el programa no puede manejar de manera normal. En este punto, se utiliza la instrucción `raise`{l=python} para generar la excepción y transferir el control a un bloque `except`{l=python} correspondiente.

La captura la realiza el *usuario* de nuestro programa. Este *usuario* puede intentar manejar la excepción y recuperarse. Si una excepción no se captura, entonces el programa se detendrá y mostrará un mensaje de error.

```{important}
Si nuestro programa lanza una excepción y la atrapa en el mismo módulo es probable que la lógica de manejo de excepciones no sea adecuada. Ya que si lanzó un excepción es porque no podía manejar la situación, entonces si luego en el mismo bloque la atrapa entonces desde el principio no era una situación inmanejable como para lanzar una excepción
```

Otra forma de lanzar una excepción en forma condicional es con la sentencia `assert`{l=python}.

`assert`{l=python} es una declaración que se utiliza para realizar pruebas de afirmaciones en el código. Si la afirmación es falsa, se lanza una excepción `AssertionError`{l=python}. Esto puede ser útil para verificar condiciones que deberían ser verdaderas en un punto determinado del programa. Por ejemplo para chequear se cumplan las precondiciones cuando se llama a una función.

```{code-cell} python
---
tags: [hide-output]
---
def dividir(a, b):
    assert b != 0, "El divisor no puede ser cero"
    return a / b


if __name__ == "__main__":
    try:
        resultado = dividir(10, 0)
    except AssertionError as e:
        print(f"Error: {e}")
```

## Consideraciones en el diseño y uso de excepciones en Python

Limitar el alcance del bloque`try`{l=python}
: Colocar dentro del`try`{l=python} solo el código que pueda generar la excepción que se desea manejar para evitar atrapar errores no relacionados y facilitar la identificación de la causa.

Evitar atrapar excepciones genéricas sin necesidad
: No usar `except Exception:`{l=python} ni `except:`{l=python} a menos que realmente se quiera interceptar cualquier excepción. Atrapar todo oculta errores y dificulta el depurado.

Usar excepciones específicas primero
: Ordenar los`except`{l=python} de más específico a más genérico, ya que Python ejecuta el primero que coincide. Ejemplo:

```{code-block} python
except FileNotFoundError:
    ...
except OSError:
    ...
except Exception:
    ...
```

No usar excepciones para control de flujo normal
: Las excepciones son para manejar situaciones excepcionales, no para reemplazar estructuras de control (if, for, etc.).

Registrar o informar el error
: Si la excepción se maneja sin mostrar o registrar nada, puede ser difícil saber qué ocurrió. Se recomienda usar `logging`{l=python} o `print`{l=python} (en entornos simples) para tener contexto de la excepción.

Liberar recursos siempre
: Usar `finally`{l=python} para cerrar archivos, conexiones, o liberar memoria, sin importar si hubo excepción o no.

No silenciar excepciones sin justificación
: Evitar `except: pass`{l=python} sin explicación. Si es necesario ignorar un error, se debe documentar por qué.

Relanzar cuando sea necesario
: Si el bloque `except`{l=python} no puede manejar la excepción de manera útil, se debe volver a lanzarla (raise) para que sea tratada en un nivel superior.

Mantener el bloque `except`{l=python} lo más simple posible
: Los `handlers`{l=python} deben ser bloques de código simple, ya que un nuevo error que se generé allí podría ocultar la situación excepcional original.

Personalizar excepciones si es necesario
: Crear clases de excepciones propias cuando la aplicación puede tener errores específicos, para que sea más fácil distinguirlos. Por ejemplo `StackException`{l=python}.

Usar `else`{l=python} para el código dependiente de éxito
: Colocar en `else`{l=python} las operaciones que deben ejecutarse solo si no hubo excepción, en lugar de ponerlas en el `try`{l=python}. Esto ayuda a mantener el código más claro y a separar la lógica de manejo de errores de la lógica normal del programa.

## Recursos para profundizar

- [Documentación oficial de Python sobre manejo de excepciones](https://docs.python.org/es/3.13/tutorial/errors.html){target="\_blank"}
- [Excepciones incorporadas en Python](https://docs.python.org/es/3/library/exceptions.html){target="\_blank"}
- [Errores y Excepciones (Hektor Profe)](https://hektorprofe.github.io/python/errores-y-excepciones/){target="\_blank"}
- [Python Exceptions: An Introduction (Real Python)](https://realpython.com/python-exceptions/){target="\_blank"}
