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
description: Persistencia de datos, serialización y deserialización, pickle, dill, json
---

# Persistencia de datos

En programación, **persistencia** se refiere a la capacidad de un programa para **almacenar datos más allá de su ejecución**. Cuando un programa finaliza, normalmente los datos almacenados en memoria (RAM) se pierden. Para conservarlos, es necesario guardarlos en un medio de almacenamiento **persistente** como un archivo, una base de datos o la nube.

Ejemplos comunes de persistencia:

- Guardar configuraciones de usuario en un archivo.
- Registrar el progreso de un videojuego.
- Almacenar datos temporales de un análisis para retomarlo luego.
- Guardar resultados de una simulación que tardó horas en correr.

En general, para poder persistir datos de objetos en memoria, primero se deben **serializar.**

## ¿Qué es la serialización?

La **serialización** es el proceso de **convertir un objeto en memoria en una secuencia de bytes o en un formato estándar (como texto JSON)**, de modo que pueda:

- Guardarse en un archivo.
- Transmitirse por una red.
- Reconstruirse posteriormente en su estado original (**deserialización**).

En otras palabras:

Serialización
: **Objeto** → **Bytes/Texto** (para guardar o enviar).

Deserialización
: **Bytes/Texto** → **Objeto en memoria**

Sin serialización, no podríamos almacenar **objetos vivos** con un estado determinado por el valor de sus atributos y métodos en un momento dado.

## Persistencia y serialización en Python

Python incluye varios módulos que permiten serializar y persistir datos de manera sencilla. Los más conocidos son:

[`pickle`](https://docs.python.org/es/3.13/library/pickle.html)
: Serialización binaria de objetos de Python.

[`dill`](https://pypi.org/project/dill/)
: Extensión de `pickle` con mayor cobertura de tipos.

[`json`](https://docs.python.org/es/3.13/library/json.html)
: Serialización en formato **texto legible** y estándar.

## Módulo `pickle`

`pickle` convierte objetos de Python en una representación binaria que puede guardarse en un archivo o transmitirse. No es interoperable con otros lenguajes, es decir los objetos serializados y persistidos con `pickle` no pueden ser leídos por programas en otros lenguajes.

Como se puede intuir, efectivamente constituye una brecha de seguridad cuando se usa fuera del ámbito de una computadora privada (en redes o en Internet, por ejemplo), ya que los datos pueden ser manipulados o leídos por terceros no autorizados.

Se puede hacer un `pickle` con:

- `None`, `True`, `False`.
- Enteros, números en punto flotante y complejos.
- Cadenas, bytes, array de bytes, tuplas, listas y diccionarios que contienen sólo objetos con los que se puede hacer un `pickle`.
- Funciones definidas en el nivel más externo de un módulo (usando `def` y no `lambda`).
- Clases (con algunas limitaciones) definidas en el nivel más externo de un módulo.

```{code-cell} python
---
tags: hide-output
---
import pickle


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        """Permite que al imprimir una instancia de Persona
        se muestre su nombre."""
        return self.nombre


if __name__ == "__main__":
    ana = Persona("Ana Suarez")
    juan = Persona("Juan Perez")
    carla = Persona("Carla Sanchez")

    with open(
        "../_static/tmp/personas.p", "wb"
    ) as contenedor:
        pickle.dump(ana, contenedor)
        pickle.dump(juan, contenedor)
        pickle.dump(carla, contenedor)

    with open(
        "../_static/tmp/personas.p", "rb"
    ) as contenedor:
        for linea in contenedor:
            print(linea)
            print()
```

En el ejemplo anterior se crean tres personas y se serializan en un archivo utilizando el módulo `pickle`. Luego, se lee el archivo tal como está guardado, mostrando los bytes en su forma cruda. Para deserializar los objetos, se debe usar `pickle.load()` en lugar de intentar leer el archivo directamente. `pickle.load()` se encarga de reconstruir el objeto original a partir de su representación en bytes.

```{code-cell} python
---
tags: hide-output
---
import pickle

lista = []

with open("../_static/tmp/personas.p", "rb") as contenedor:
    try:
        while contenedor:
            obj = pickle.load(contenedor)
            lista.append(obj)
    except EOFError:
        pass
    except:
        raise

for p in lista:
    print(f"Persona: {p}. Tipo: {type(p)}")
```

Ahora se modifica la clase `Persona`, se elimina el atributo `nombre` y se agrega el atributo `dni`.

```{code-cell} python
---
tags: hide-output
---
import pickle


class Persona:
    """Nueva versión de la clase Persona, se agrega el atributo dni y el método
    get_dni"""

    def __init__(self, dni=""):
        self.dni = dni

    def __str__(self):
        """Permite que al imprimir una instancia de Persona se muestre su
        dni."""

        return self.dni

    def get_dni(self):
        return self.dni


lista = []

with open("../_static/tmp/personas.p", "rb") as contenedor:
    try:
        while contenedor:
            obj = pickle.load(contenedor)
            lista.append(obj)
    except EOFError:
        pass
    except:
        raise

ana = lista[0]
juan = lista[1]
carla = lista[2]

for atributo, valor in vars(ana).items():
    print(atributo + ": " + valor)
```

Vemos que debido a que Python es un lenguaje dinámico no tiene ningún problema en leer los objetos del archivo y recrearlos en memoria como fueron serializados, aún después de que la clase `Persona` ha cambiado. Esto es posible porque `pickle` almacena la información necesaria para reconstruir el objeto, incluyendo su estructura y atributos, lo que permite que los cambios en la implementación de la clase no afecten la capacidad de deserializar objetos previamente serializados. Sin embargo, es importante tener en cuenta que si se eliminan atributos o se cambian sus tipos, esto puede causar problemas al intentar acceder a esos atributos en objetos deserializados.

### Algunos detalles de la serialización con `pickle`

- De las funciones (tanto del sistema como definidas por el usuario) lo único que se conserva es su nombre, no su valor. O sea que en el momento de recuperarlas hay que tener acceso a su valor (cuerpo de la función) para poderlas ejecutar.
- Cuando se conserva una instancia de clase como `pickle`, lo único que se guardan son los valores de los atributos, no su código asociado, de modo tal que se puedan luego recuperar instancias que se crearon en versiones anteriores de la clase sin problema.

### Funciones más usadas con `pickle`

## Funciones más usadas del módulo `pickle`

| Función / Elemento                                              | Descripción breve                                                                                                        | Documentación oficial (español)                                                                   |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `pickle.dump`                                                   | Serializa un objeto y lo escribe en el archivo binario. Permite opcionalmente especificar el protocolo de serialización. | [Documentación de `dump`](https://docs.python.org/es/3/library/pickle.html#pickle.dump)           |
| `pickle.dumps`                                                  | Serializa un objeto, retornándolo como un objeto `bytes`. Ideal para enviar por red o guardar en memoria.                | [Documentación de `dumps`](https://docs.python.org/es/3/library/pickle.html#pickle.dumps)         |
| `pickle.load`                                                   | Lee datos serializados desde un archivo binario y reconstruye el objeto original.                                        | [Documentación de `load`](https://docs.python.org/es/3/library/pickle.html#pickle.load)           |
| `pickle.loads`                                                  | Reconstruye un objeto Python a partir de datos serializados en bytes.                                                    | [Documentación de `loads`](https://docs.python.org/es/3/library/pickle.html#pickle.loads)         |
| `pickle.Pickler`                                                | Clase que serializa objetos en un flujo controlado. Permite mayor control sobre el proceso de serialización.             | [Documentación de `Pickler`](https://docs.python.org/es/3/library/pickle.html#pickle.Pickler)     |
| `pickle.Unpickler`                                              | Clase que deserializa objetos desde un flujo de datos. Proporciona control avanzado sobre el proceso de deserialización. | [Documentación de `Unpickler`](https://docs.python.org/es/3/library/pickle.html#pickle.Unpickler) |
| Excepciones (`PickleError`, `PicklingError`, `UnpicklingError`) | Clases de excepciones específicas para errores durante la serialización y deserialización.                               | [Documentación de excepciones en pickle](https://docs.python.org/es/3/library/pickle.html)        |

## Módulo `dill`

El módulo `dill` es una extensión del módulo `pickle` que permite la serialización de una gama más amplia de objetos de Python, incluyendo funciones, funciones `lambda`, clases y módulos. Esto lo hace especialmente útil en situaciones donde se necesita serializar objetos más complejos que no son compatibles con `pickle`.

`dill` no es un módulo estándar de Python. Para utilizarlo, primero hay que instalarlo:

```console
pip install dill
```

A continuación se serializa y persiste una función que en cuya clausura se encuentra un mensaje cifrado y la clave para descifrarlo.

```{code-cell} python
---
tags: hide-output
---
import dill


def cifrar_mensaje(msj, password):
    def descifrar(x):
        if x == password:
            return msj
        else:
            return None

    return descifrar


mensaje_cifrado = cifrar_mensaje("Este es el mensaje cifrado", "secreto")

with open("../_static/tmp/msj_cifrado.dill", "wb") as contenedor:
    dill.dump(mensaje_cifrado, contenedor)
```

Si leemos el archivo creado `msj_cifrado.dill`, veremos que contiene una representación binaria del objeto serializado, que incluye la función `descifrar` y su clausura con el mensaje y la clave.

```text
b'\x80\x04\x95\xef\x01\x00\x00\x00\x00\x00\x00\x8c\n'
b'dill._dill\x94\x8c\x10_create_function\x94\x93\x94(h\x00\x8c\x0c_create_code\x94\x93\x94(C\x06\x04\x01\x0c\x01\x04\x02\x94K\x01K\x00K\x00K\x01K\x02K\x13C\x16>\x02\x95\x00U\x00T\x02:X\x00\x00a\x02\x00\x00T\x01$\x00g\x00\x94N\x85\x94)\x8c\x01x\x94\x85\x94\x8c"/tmp/ipykernel_22388/1380843275.py\x94\x8c\tdescifrar\x94\x8c!cifrar_mensaje.<locals>.descifrar\x94K\x04C\x12\xf8\x80\x00\xd8\x0b\x0c\x90\x08\x8b=\xd8\x13\x16\x88J\xe0\x13\x17\x94C\x00\x94\x8c\x03msj\x94\x8c\x08password\x94\x86\x94)t\x94R\x94c__builtin__\n'
b'__main__\n'
b'h\x0bNh\x00\x8c\x0c_create_cell\x94\x93\x94N\x85\x94R\x94h\x15N\x85\x94R\x94\x86\x94t\x94R\x94}\x94}\x94(\x8c\x0f__annotations__\x94}\x94\x8c\x0c__qualname__\x94h\x0cu\x86\x94b\x8c\x08builtins\x94\x8c\x07getattr\x94\x93\x94\x8c\x04dill\x94\x8c\x05_dill\x94\x93\x94\x8c\x08_setattr\x94h#\x8c\x07setattr\x94\x93\x94\x87\x94R\x94h\x19\x8c\rcell_contents\x94\x8c\x07secreto\x94\x87\x94R0h-h\x17h.\x8c\x1aEste es el mensaje cifrado\x94\x87\x94R0.'
```

```{code-cell} python
---
tags: hide-output
---
import dill

with open("../_static/tmp/msj_cifrado.dill", "rb") as contenedor:
    mensaje_cifrado = dill.load(contenedor)

print(mensaje_cifrado("incorrecto"))
print(mensaje_cifrado("secreto"))
```

## Serialización de objetos y la seguridad de la información

```{danger} Peligro
Los módulos `pickle` y `dill` no son seguros ya que se puede construir datos maliciosos que ejecuten código arbitrario durante el proceso de deserialización. Por lo tanto, es fundamental tener precaución al utilizar estos módulos y evitar cargar datos de fuentes no confiables.
```

### Ejemplo de riesgo de seguridad

A continuación se crea un archivo `log.log` en el directorio de trabajo actual para graficar como se puede ejecutar código malicioso.

```{code-cell} python
---
tags: remove-output
---
with open("../_static/tmp/log.log", "w") as f:
    f.write("Este es un archivo de registro.\n")
    f.write("La información registrada es muy sensible y se debe resguardar\n")
```

Podemos ver que el archivo existe y se puede leer.

```{code-cell} python
---
tags: hide-output
---
with open("../_static/tmp/log.log", "r") as f:
    contenido = f.read()
    print(contenido)
```

A continuación se crea un `pickle` con un objeto malicioso que ejecuta un comando.

```{code-cell} python
# Este código simula la creación de un archivo malicioso que borra log.log
import pickle
import os


class Malicioso:
    def __reduce__(self):
        return (os.remove, ("../_static/tmp/log.log",))


# Serializa el objeto malicioso
with open("../_static/tmp/malicioso.p", "wb") as f:
    pickle.dump(Malicioso(), f)
```

Si alguien deserializa este archivo sin saber su contenido borra el archivo `log.log`.

```{code-cell} python
import pickle

with open("../_static/tmp/malicioso.p", "rb") as f:
    obj = pickle.load(f)  # Esto borra log.log
```

Al intentar leer de nuevo el archivo `log.log` vemos que no existe más

```{code-cell} python
---
tags: raises-exception, hide-output
---
with open("../_static/tmp/log.log", "r") as f:
    contenido = f.read()
    print(contenido)
```

### Funciones más usadas del módulo `dill`

| Función / Elemento                                              | Descripción breve                                                                                                                | Documentación oficial (inglés)                                                                               |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `dill.dump`                                                     | Serializa un objeto y lo escribe en el archivo binario. A diferencia de `pickle`, soporta funciones, lambdas, generadores y más. | [Documentación de `dump`](https://dill.readthedocs.io/en/latest/dill.html#dill.dump)                         |
| `dill.dumps`                                                    | Serializa un objeto y lo devuelve como `bytes`. Soporta más tipos de Python que `pickle`.                                        | [Documentación de `dumps`](https://dill.readthedocs.io/en/latest/dill.html#dill.dumps)                       |
| `dill.load`                                                     | Lee datos serializados desde un archivo binario y reconstruye el objeto original. Puede restaurar funciones y objetos complejos. | [Documentación de `load`](https://dill.readthedocs.io/en/latest/dill.html#dill.load)                         |
| `dill.loads`                                                    | Reconstruye un objeto Python a partir de datos serializados en `bytes`.                                                          | [Documentación de `loads`](https://dill.readthedocs.io/en/latest/dill.html#dill.loads)                       |
| `dill.dump_session`                                             | Guarda el estado completo de la sesión interactiva de Python (variables, funciones, imports) en un archivo.                      | [Documentación de `dump_session`](https://dill.readthedocs.io/en/latest/dill.html#dill.dump_session)         |
| `dill.load_session`                                             | Restaura una sesión previamente guardada con `dump_session`. Muy útil en debugging y experimentación.                            | [Documentación de `load_session`](https://dill.readthedocs.io/en/latest/dill.html#dill.load_session)         |
| `dill.detect.trace`                                             | Permite depurar el proceso de serialización mostrando qué objetos pueden o no serializarse.                                      | [Documentación de `detect`](https://dill.readthedocs.io/en/latest/dill.html#module-dill.detect)              |
| Excepciones (`PickleError`, `PicklingError`, `UnpicklingError`) | `dill` reutiliza las mismas excepciones que `pickle` para manejar errores durante la serialización y deserialización.            | [Documentación de excepciones en pickle](https://docs.python.org/es/3/library/pickle.html#pickle-exceptions) |

## Módulo `json`

El módulo `json` se basa en el estandar **JSON** (JavaScript Object Notation) y presenta un enfoque diferente al de `pickle` y `dill`, ya que se basa en texto plano y no permite la ejecución de código al deserializar. Esto lo convierte en una opción más segura para la serialización y el intercambio de datos simples, como diccionarios y listas. Los archivos JSON son legibles por humanos y pueden ser fácilmente compartidos entre diferentes lenguajes de programación.

```{note} Nota
**JSON** (_JavaScript Object Notation_) es un **formato de intercambio de datos basado en texto**.
Se originó en el ecosistema de **JavaScript**, pero rápidamente se convirtió en un **estándar independiente del lenguaje** debido a su simplicidad y legibilidad.
```

Características principales de JSON:

- Está basado en una notación muy parecida a los **objetos de JavaScript**.
- Es **independiente de plataforma y lenguaje** (lo entienden Python, Java, Go, C#, etc.).
- Es **legible para humanos** y fácil de generar por máquinas.
- Es el formato más usado en **APIs REST, microservicios, configuración de aplicaciones y bases de datos NoSQL** como MongoDB.

Objetos
: Se representan como pares clave-valor (`{"clave": "valor"}`).

Arreglos
: Se representan como listas ordenadas de elementos (`["valor1", "valor2", "valorN"]`).

Valores primitivos
: Se representan como números, cadenas, booleanos (`true`, `false`) y `null` para `None`.

### Ejemplo de uso de `json`

```{code-cell} python
---
tags: hide-output
---
import json

# Datos a serializar
datos = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}

# Serializar a JSON
with open("../_static/tmp/datos.json", "w") as f:
    json.dump(datos, f)

# leer el archivo como texto
with open("../_static/tmp/datos.json", "r") as f:
    contenido = f.read()
    print(contenido)
```

```{code-cell} python
---
tags: hide-output
---
# Deserializar de JSON
with open("../_static/tmp/datos.json", "r") as f:
    datos_cargados = json.load(f)
    print(datos_cargados)
```

Un archivo **_JSON_** solo puede contener un único diccionario o una lista, por lo que si hay que guardar múltiples objetos, se deben agrupar en una lista.

```{code-cell} python
---
tags: hide-output
---
import json

usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 30},
    {"nombre": "Marta", "edad": 28},
]

# Guardamos todo en un solo archivo JSON
with open("../_static/tmp/usuarios.json", "w") as f:
    json.dump(usuarios, f, indent=4)

# Recuperamos
with open("../_static/tmp/usuarios.json", "r") as f:
    lista_usuarios = json.load(f)

print(lista_usuarios)
print(lista_usuarios[0]["nombre"])  # Acceso al primer usuario
```

```{note} Nota
Existe un formato derivado de **JSON** denominado **JSONL** (_JSON Lines_), que consiste en una serie de objetos JSON separados por saltos de línea. Es útil para el procesamiento de grandes volúmenes de datos, ya que permite leer y escribir un objeto a la vez.

Este enfoque es muy usado en big data y machine learning, porque permite procesar el archivo registro por registro sin necesidad de cargarlo entero en memoria.
```

### Funciones más usadas del módulo `json`

| Función / Elemento              | Descripción breve                                                                                                                   | Documentación oficial (español)                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `json.dump`                     | Serializa un objeto Python y lo escribe en un archivo en formato JSON. Opcionalmente permite configurar indentación y codificación. | [Documentación de `dump`](https://docs.python.org/es/3/library/json.html#json.dump)                       |
| `json.dumps`                    | Serializa un objeto Python y lo devuelve como una cadena de texto JSON.                                                             | [Documentación de `dumps`](https://docs.python.org/es/3/library/json.html#json.dumps)                     |
| `json.load`                     | Lee un archivo JSON y lo convierte en el objeto Python correspondiente (diccionarios, listas, etc.).                                | [Documentación de `load`](https://docs.python.org/es/3/library/json.html#json.load)                       |
| `json.loads`                    | Convierte una cadena de texto JSON en el objeto Python correspondiente.                                                             | [Documentación de `loads`](https://docs.python.org/es/3/library/json.html#json.loads)                     |
| `json.JSONEncoder`              | Clase que define cómo convertir objetos Python en JSON. Se puede extender para serializar tipos personalizados.                     | [Documentación de `JSONEncoder`](https://docs.python.org/es/3/library/json.html#json.JSONEncoder)         |
| `json.JSONDecoder`              | Clase que define cómo convertir JSON en objetos Python. Se puede extender para deserializar estructuras personalizadas.             | [Documentación de `JSONDecoder`](https://docs.python.org/es/3/library/json.html#json.JSONDecoder)         |
| Excepciones (`JSONDecodeError`) | Excepción que se lanza cuando un documento JSON no tiene el formato correcto.                                                       | [Documentación de `JSONDecodeError`](https://docs.python.org/es/3/library/json.html#json.JSONDecodeError) |

## Tabla Comparativa: `pickle` vs `dill` vs `json`

| Característica                | `pickle`                            | `dill`                                                      | `json`                                                  |
| ----------------------------- | ----------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------- |
| **Formato**                   | Binario                             | Binario                                                     | Texto (legible por humanos)                             |
| **Compatibilidad**            | Solo Python                         | Solo Python                                                 | Multilenguaje (estándar mundial)                        |
| **Tipos soportados**          | Objetos de Python (casi todos)      | Objetos de Python (incluye funciones, lambdas, generadores) | Tipos básicos (dict, list, str, int, float, bool, null) |
| **Seguridad al deserializar** | Riesgo de ejecutar código malicioso | Riesgo de ejecutar código malicioso                         | Seguro (no ejecuta código)                              |
| **Legibilidad**               | No legible (binario)                | No legible (binario)                                        | Legible (formato JSON)                                  |
| **Usos comunes**              | Persistencia local de objetos       | Persistencia avanzada, guardar funciones                    | Intercambio de datos entre sistemas, APIs               |
| **Ventaja principal**         | Fácil y rápido para Python          | Más flexible que `pickle`                                   | Estándar universal, interoperable                       |
| **Desventaja principal**      | No interoperable, inseguro          | Igual que `pickle` (pero más pesado)                        | No soporta objetos complejos de Python                  |

## Organización de los datos

Si bien `pickle` y `dill` permiten guardar objetos complejos de Python, y `json` se limita a estructuras de datos más simples, en todos los casos los datos se almacenan como **un único objeto serializado por archivo**. Esto funciona bien para persistir estructuras completas (listas, diccionarios, clases), pero puede resultar incómodo cuando se quiere manejar una colección de objetos con acceso directo mediante una **clave**.

Para resolver esto, Python ofrece módulos como `shelve` y `dbm`, que permiten organizar la información de manera similar a una **base de datos ligera de pares clave-valor**, sin necesidad de instalar un gestor externo.

`shelve`
: Permite almacenar objetos de Python en un archivo de forma similar a un diccionario persistente. Se accede a los datos por clave, y cada valor puede ser un objeto complejo serializado automáticamente con `pickle`. Es muy útil cuando se quieren mantener estructuras de datos de Python sin necesidad de escribir el proceso de serialización/deserialización manualmente.

`dbm`
: Proporciona acceso a una familia de bases de datos simples, en las que cada clave se asocia a un valor binario. A diferencia de `shelve`, en `dbm` tanto las claves como los valores deben ser **cadenas de bytes** (`bytes`). Es más básico y portable, pero no admite directamente objetos de Python, sólo datos crudos en forma de texto o binario.

______________________________________________________________________

## Módulo `shelve`

```{admonition} Una analogía útil
---
class: note
---
Los `pickles` son conservas que se guardan en frascos; a esos frascos se les puede agregar eneldo (`dill`) para darles más sabor, y finalmente todos los frascos se organizan y etiquetan en una estantería (`shelve`).
```

Un shelve actúa como un diccionario persistente en disco, permitiendo almacenar y recuperar objetos de Python utilizando claves. Esto facilita la gestión de colecciones de objetos sin necesidad de preocuparse por la serialización manual.

```{code-cell} python
---
tags: hide-output
---
import shelve

# Abrir (o crear) una "base de datos"
with shelve.open("../_static/tmp/estudiantes.db") as db:
    db["123"] = {"nombre": "Ana", "carrera": "Ingeniería Informática"}
    db["456"] = {"nombre": "Luis", "carrera": "Computación"}

# Recuperar los datos
with shelve.open("../_static/tmp/estudiantes.db") as db:
    print(db["123"])  # {'nombre': 'Ana', 'carrera': 'Ingeniería Informática'}
```

### Ventajas de shelve

- Se maneja como un diccionario común de Python.
- Permite almacenar objetos complejos sin preocuparse por serialización.
- Persistencia automática en disco.

### Limitaciones

- No es seguro para acceso concurrente desde múltiples procesos.
- No es portable entre diferentes versiones de Python (ya que usa internamente pickle).

## Módulo `dbm`

El módulo `dbm` implementa una base de datos clave-valor simple, con distintas variantes (dbm.gnu, dbm.ndbm, etc.) dependiendo del sistema. Cada entrada se almacena como una clave y un valor, ambos en forma de cadenas de bytes. Esto lo hace más ligero y portable, pero también más limitado en cuanto a los tipos de datos que puede manejar.

```{code-cell} python
---
tags: hide-output
---
import dbm

# Crear y guardar pares clave-valor
with dbm.open("../_static/tmp/usuarios", "c") as db:
    db["ana"] = "ingenieria"
    db["luis"] = "computacion"

# Recuperar datos
with dbm.open("../_static/tmp/usuarios", "r") as db:
    print(db["ana"].decode("utf-8"))  # "ingenieria"
    print(db["luis"].decode("utf-8"))  # "computacion"
```

### Ventajas de `dbm`

- Muy rápido y ligero.
- Ideal para guardar pares clave-valor simples (cadenas).
- Compatible con múltiples implementaciones de bases de datos en sistemas Unix.

### Limitaciones de `dbm`

- Solo admite bytes como claves y valores.
- No guarda estructuras complejas de Python (habría que serializarlas manualmente).
- Menos flexible que shelve.

## Ejemplo de una agenda con `shelve` y `pickle`

Ejemplo de una agenda simple que permite gestionar contactos con nombre, apellido, correos electrónicos y teléfonos. Para copiar, modificar y ejecutar:

```{literalinclude} ../_static/code/persistencia/agenda.py
```

## Recursos para profundizar

- [Working with JSON data in Python (Real Python)](https://realpython.com/python-json/)
- [JSON de Python (W3Schools)](https://www.w3schools.com/python/python_json.asp)
- [Serialize your data with Python (Real Python)](https://realpython.com/python-serialize-data/)
- [Tutorial de Pickle en Python: Serialización de objetos (DataCamp)](https://www.datacamp.com/es/tutorial/pickle-python-tutorial)
