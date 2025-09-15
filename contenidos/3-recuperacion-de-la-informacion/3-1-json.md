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

# Java Script Object Notation (JSON)

```{code-cell} python
---
tags: [hide-output, remove-cell]

---
"""Borra todos los archivos y carpetas en /tmp
"""
import os
import shutil

tmp_dir = "/tmp"
os.chdir(tmp_dir)
for filename in os.listdir(tmp_dir):
  file_path = os.path.join(tmp_dir, filename)
  try:
    if os.path.isfile(file_path) or os.path.islink(file_path):
      os.remove(file_path)
    elif os.path.isdir(file_path):
      shutil.rmtree(file_path)
  except Exception as e:
    print(f"No se pudo borrar {file_path}: {e}")
```

JSON (JavaScript Object Notation) es un formato ligero de intercambio de datos que es fácil de leer y escribir para los humanos, y fácil de parsear y generar para las máquinas. Es un formato de texto que utiliza una sintaxis basada en objetos y arrays, similar a la de JavaScript.

## Estructura de JSON

Un archivo JSON está compuesto por una serie de pares clave-valor, donde cada clave es una cadena de texto y cada valor puede ser un número, una cadena de texto, un booleano, un array o un objeto. Los objetos se representan mediante llaves `{}` y los arrays mediante corchetes `[]`.

```json
{
  "nombre": "Juan",
  "edad": 30,
  "es_estudiante": false,
  "cursos": ["Matemáticas", "Física", "Química"],
  "direccion": {
    "calle": "Calle Falsa 123",
    "ciudad": "Springfield",
    "pais": "USA"
  }
}
```

Este formato es muy utilizado para el intercambio de datos entre aplicaciones web y servidores, ya que es fácil de parsear y generar en la mayoría de los lenguajes de programación.

En la sección de [Persistencia de Datos](../1-taller-de-python/1-10-persistencia.md) vimos cómo trabajar con archivos JSON en Python utilizando la librería estándar `json`. Aquí veremos cómo utilizar JSON para organizar registros en un archivo.

## Organizando registros con JSON

Una forma común de organizar registros en un archivo JSON es utilizar una lista de objetos, donde cada objeto representa un registro. Por ejemplo, si queremos almacenar una agenda de contactos, podemos utilizar la siguiente estructura:

```json
[
  {
    "nombre": "Juan",
    "telefono": "123456789",
    "email": "juan@example.com"
  },
  {
    "nombre": "Ana",
    "telefono": "987654321",
    "email": "ana@example.com"
  }
]
```

Cada objeto en la lista representa un contacto, con campos para el nombre, teléfono y correo electrónico. Podemos agregar, eliminar o modificar contactos simplemente manipulando la lista de objetos.

En Python, podemos trabajar con este archivo JSON utilizando la librería `json` de la siguiente manera

## Agenda en formato JSON

A continuación se muestra cómo definir una clase `Agenda` que almacena los contactos en un archivo `.json`, junto con su iterador y ejemplos de uso.

```{code-cell} python
import json
import os

class Agenda:
  def __init__(self, archivo):
    self._archivo = archivo
    # Si el archivo no existe, lo crea con una lista vacía
    if not os.path.exists(archivo):
      with open(archivo, "w") as f:
        json.dump([], f)
    # Carga los contactos existentes
    with open(archivo, "r") as f:
      self._contactos = json.load(f)

  def guardar_contacto(self, nombre, telefono="", email=""):
    if not nombre:
      raise ValueError("El nombre es obligatorio")
    contacto = {
      "nombre": nombre,
      "telefono": telefono,
      "email": email
    }
    self._contactos.append(contacto)
    with open(self._archivo, "w") as f:
      json.dump(self._contactos, f, ensure_ascii=False, indent=2)

  def cantidad_registros(self):
    return len(self._contactos)

  def __iter__(self):
    return AgendaIterator(self)
```

Definimos el iterador para la agenda:

```{code-cell} python
class AgendaIterator:
  """Iterador para la agenda de contactos en formato JSON"""
  def __init__(self, agenda):
    self._agenda = agenda
    self._index = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self._index < len(self._agenda._contactos):
      contacto = self._agenda._contactos[self._index]
      self._index += 1
      return contacto
    else:
      raise StopIteration
```

Ejemplo de uso:

```{code-cell} python
---
tags: [hide-output]
---
agenda = Agenda("agenda.json")
agenda.guardar_contacto("Juan", "123456789", "juan@example.com")
agenda.guardar_contacto("Ana", "987654321", "ana@example.com")
agenda.guardar_contacto("Homero", "555-8765", "")
agenda.guardar_contacto("Lisa", "", "lisa.simpson@example.com")

print(f"Cantidad de registros: {agenda.cantidad_registros()}")
for contacto in agenda:
  print(contacto)
  print("-----")
```

Si vemos el contenido del archivo `agenda.json`, se observa que los datos están guardados en formato de texto legible, seguiendo el estándar JSON

```{code-cell} python
---
tags: [hide-output]
---
with open("agenda.json", "r") as f:
  contenido = f.read()
  print(contenido)
```

La principal ventaja de utilizar JSON para organizar registros es que es un formato ampliamente soportado y fácil de leer y escribir. Además, permite almacenar datos estructurados de manera flexible, ya que los objetos pueden tener diferentes campos y tipos de datos.

A continuación se define una agenda general donde solo los campos nombres y apellidos son obligatorios, y donde cada registro puede tener incluso campos diferentes.

```{code-cell} python
class AgendaGeneral:
  def __init__(self, archivo):
    self._archivo = archivo
    if not os.path.exists(archivo):
      with open(archivo, "w") as f:
        json.dump([], f)
    with open(archivo, "r") as f:
      self._contactos = json.load(f)

  def guardar_contacto(self, **kwargs):
    if "nombre" not in kwargs or "apellido" not in kwargs:
      raise ValueError("Los campos 'nombre' y 'apellido' son obligatorios")
    self._contactos.append(kwargs)
    with open(self._archivo, "w") as f:
      json.dump(self._contactos, f, ensure_ascii=False, indent=2)

  def cantidad_registros(self):
    return len(self._contactos)

  def __iter__(self):
    return AgendaIterator(self)
```

Ejemplo de uso:

```{code-cell} python
---
tags: [hide-output]
---
agenda = AgendaGeneral("agenda_general.json")
agenda.guardar_contacto(
  nombre="Juan",
  apellido="Pérez",
  telefono="123456789",
  email="juan.perez@example.com"
)
agenda.guardar_contacto(
  nombre="Ana",
  apellido="García",
  telefono="987654321",
  cumpleaños="1990-01-01"
)
agenda.guardar_contacto(
  nombre="Homero",
  apellido="Simpson",
  direccion={
    "calle": "742 Evergreen Terrace",
    "ciudad": "Springfield"
  },
  telefono="555-8765"
)
agenda.guardar_contacto(
  nombre="Lisa",
  apellido="Simpson",
  email="lisa.simpson@example.com",
  hobbies=["saxofón", "política"]
)
agenda.guardar_contacto(
  nombre="Bart",
  apellido="Simpson",
  telefono="555-1234",
  email="bart.simpson@example.com"
)
for contacto in agenda:
  # Imprime nombre y apellido en la primera línea
  nombre = contacto.get("nombre", "")
  apellido = contacto.get("apellido", "")
  print(f"{nombre} {apellido}")
  # Función recursiva para imprimir campos
  def imprimir_campos(d, indent=2):
    for clave, valor in d.items():
      if clave in ("nombre", "apellido"):
        continue
      if isinstance(valor, dict):
        print(" " * indent + f"{clave}:")
        imprimir_campos(valor, indent + 2)
      elif isinstance(valor, list):
        print(" " * indent + f"{clave}: [")
        for item in valor:
          if isinstance(item, dict):
            imprimir_campos(item, indent + 4)
          else:
            print(" " * (indent + 2) + f"- {item}")
        print(" " * indent + "]")
      else:
        print(" " * indent + f"{clave}: {valor}")
  imprimir_campos(contacto)
  print("-----")
```

Archivo `agenda_general.json`:

```{code-cell} python
---
tags: [hide-output]
---
with open("agenda_general.json", "r") as f:
  contenido = f.read()
  print(contenido)
print(f"Cantidad de bytes en el archivo: {len(contenido)}")
print(f"Cantidad de registros: {agenda.cantidad_registros()}")
```
