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

# Registros de datos

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

En esta sección vamos a ver distintos formatos para organizar la información en archivos, es decir de la organización lógica de los datos. Estos formatos son independientes del lenguaje de programación que utilicemos, y en muchos casos son independientes del software que utilicemos.

Supongamos que queremos crear una ***agenda*** para almacenar datos de contactos: **nombre**, **apellido**, **teléfono** y **email**. Una primera forma sería guardar los datos sin ningún tipo de organización, simplemente uno detrás de otro, separados por espacios o saltos de línea:
```{code-cell} python
---
tags: [hide-output]
mystnb:
    number_source_lines: true
---
class Agenda:
  def __init__(self, archivo):
    self.archivo = archivo

  def guardar_contacto(self, nombre, apellido, telefono, email):
    with open(self.archivo, "a") as datos:
      datos.write(nombre)
      datos.write(apellido)
      datos.write(telefono)
      datos.write(email)

agenda = Agenda("agenda.txt")
agenda.guardar_contacto("Ana", "Calle Falsa 123", "555-1234", "ana@example.com")
agenda.guardar_contacto("Bart", "Calle Falsa 123", "555-5678", "bart@example.com")

with open("agenda.txt") as datos:
  for linea in datos:
    print(linea)
```

Si observamos el contenido del archivo `agenda.txt`, vemos que los datos están todos juntos, sin ningún tipo de organización. Se ha perdido la integridad de los datos, ya que no sabemos dónde termina un dato y empieza otro. Además, si queremos buscar un contacto, tenemos que leer todo el archivo y buscar el nombre, lo cual es muy ineficiente.

Los datos de una entidad (en este caso un contacto) se suelen llamar **registro**. Un registro está formado por varios **campos** (en este caso nombre, apellido, teléfono y email). Existen varios formatos para organizar los registros en un archivo, veamos algunos de ellos.

## Registros de longitud fija con campos de longitud fija

Una forma de organizar los registros es asignar una longitud fija a cada campo. Por ejemplo, podemos decidir que el campo nombre tendrá 20 caracteres, el campo apellido 30 caracteres, el campo teléfono 15 caracteres y el campo email 40 caracteres. Si un dato es más corto que la longitud asignada, se rellena con espacios en blanco. Si un dato es más largo, se trunca.

```{code-cell} python
---
tags: [hide-output]
mystnb:
    number_source_lines: true
---
import os
import struct

class Agenda:
  def __init__(self, archivo, len_nombre=20, len_apellido=30, len_telefono=15, len_email=40):
      self._archivo = archivo
      # Formato del registro con campos de longitud fija
      self._formato = "%ds%ds%ds%ds" % (len_nombre, len_apellido, len_telefono, len_email)
      # Longitud total del registro
      self._len_registro = struct.calcsize(self._formato)

      # cantidad de registros presentes en la agenda
      try:
          # devuelve tamaño del archivo, si no existe levanta FileNotFoundException
          tam_archivo = os.path.getsize(archivo)
          self._cant_registros = tam_archivo / self._len_registro
      except FileNotFoundError:
          self._cant_registros = 0

  def guardar_contacto(self, nombre, apellido, telefono="", email=""):
      """Permite guardar un registro, nombre y apellido son obligatorios"""
      if not nombre or not apellido:
          raise ValueError("Nombre y apellido son obligatorios")

      # abre el archivo en modo append binario. Si el archivo no existe lo crea.
      with open(self._archivo, "ab") as registros:
          # empaqueta los datos en un registro de longitud fija
          registro = struct.pack(self._formato, nombre.encode(), apellido.encode(), telefono.encode(), email.encode())
          # escribe el registro al final del archivo
          registros.write(registro)

      self._cant_registros += 1

  def cantidad_registros(self):
      """Devuelve la cantidad de registros que hay en la agenda"""
      return self._cant_registros

  def __iter__(self):
      """Devuelve un iterador para la agenda"""
      return AgendaIterator(self)
```
A continuación definimos el iterador para la agenda:
```{code-cell} python
---
mystnb:
    number_source_lines: true
---
class AgendaIterator:
  """Iterador para la agenda"""

  def __init__(self, agenda):
    self._agenda = agenda
    # posicion actual para iterar
    self._index = 0

  def __next__(self):
    if self._index < self._agenda._cant_registros:
      with open(self._agenda._archivo, "rb") as registros:
          # posicion en bytes del registro actual
          posicion = self._index * self._agenda._len_registro

          registros.seek(posicion)

          registro = registros.read(self._agenda._len_registro)
          self._index += 1

          # chequea la integridad del registro leído
          if len(registro) == self._agenda._len_registro:
            (b_nombre, b_apellido, b_telefono, b_email) = struct.unpack(self._agenda._formato, registro)
            return b_nombre.decode().strip(), b_apellido.decode().strip(), b_telefono.decode().strip(), b_email.decode().strip()
          else:
            return "", "", "", "" # registro corrupto
    else:
        raise StopIteration
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: [hide-output]
---
agenda = Agenda("agenda_fixed.dat")
agenda.guardar_contacto("March", "Simpson", "555-1234", "march@example.com")
agenda.guardar_contacto("Bart", "Simpson", "555-5678", "bart@example.com")
agenda.guardar_contacto("Homero", "Simpson", "555-8765", "homero@example.com")
agenda.guardar_contacto("Lisa", "Simpson")  # sin teléfono ni email

print(f"Cantidad de registros: {agenda.cantidad_registros()}")  
for nombre, apellido, telefono, email in agenda:
    print(f"{nombre}, {apellido}\n")
    print(f"Teléfono: {telefono}\n")
    print(f"Email: {email}\n")
    print("-----")
```

Si observamos el contenido del archivo `agenda_fixed.dat` con un editor hexadecimal, vemos que los datos están organizados en bloques de longitud fija, y cada campo ocupa la cantidad de bytes asignada, rellenando con nulos si es necesario.

```{code-cell} python
---
tags: [hide-output]
---
with open("agenda_fixed.dat", "rb") as f:
    contenido = f.read()
    print(contenido)
``` 
Los nulos se representan con el byte `\x00`. Se observa que cada registro ocupa 105 bytes (20 + 30 + 15 + 40) y la mayoría de los caracteres son valores nulos.

Este formato tiene la ventaja de que es muy sencillo calcular la posición de un registro en el archivo, ya que todos los registros tienen la misma longitud. Por ejemplo, el registro `n` empieza en la posición `n * len_registro`. Esto permite acceder a un registro directamente sin tener que leer todo el archivo. Sin embargo, tiene la desventaja de que se desperdicia espacio si los datos son más cortos que la longitud asignada, y no es flexible si se quieren agregar nuevos campos o cambiar la longitud de los campos.

Tampoco permite almacenar datos que superen la longitud asignada, ya que se truncan. Por ejemplo, si intentamos guardar un nombre con más de 20 caracteres, se perderán los caracteres adicionales.

## Registros de longitud fija y campos de longitud variable

Otra forma de organizar los registros es asignar una longitud fija a cada registro, pero permitir que los campos tengan longitud variable. Para ello, se puede utilizar un delimitador para separar los campos dentro del registro. Por ejemplo, podemos utilizar el carácter `|` como delimitador.

```{code-cell} python
---
tags: [hide-output]
mystnb:
    number_source_lines: true
---
class Agenda:
  def __init__(self, archivo, len_registro=100):
      self._archivo = archivo
      self._len_registro = len_registro
      try:
          tam_archivo = os.path.getsize(archivo)
          self._cant_registros = tam_archivo / self._len_registro
      except FileNotFoundError:
          self._cant_registros = 0
  def guardar_contacto(self, nombre, apellido, telefono="", email=""):
      """Permite guardar un registro, nombre y apellido son obligatorios"""
      if not nombre or not apellido:
          raise ValueError("Nombre y apellido son obligatorios")
      registro = f"{nombre}|{apellido}|{telefono}|{email}"
      if len(registro.encode()) > self._len_registro:
          raise ValueError("El registro es demasiado largo")
      registro = registro.encode()
      registro = registro.ljust(self._len_registro, b'\x00')
      with open(self._archivo, "ab") as registros:
          registros.write(registro)
      self._cant_registros += 1
  def cantidad_registros(self):
      """Devuelve la cantidad de registros que hay en la agenda"""
      return self._cant_registros
  def __iter__(self):
      """Devuelve un iterador para la agenda"""
      return AgendaIterator(self)
```

`registro.encode()`{l=python} convierte la cadena a bytes, y `ljust`{l=python} rellena con nulos a la derecha, hasta alcanzar la longitud fija del registro. Algunos caracteres como vocales con tildes o la letra ñ pueden ocupar más de un byte (por ejemplo `é` se condifica como `b'\xc3\xa9'`), por lo que es importante medir la longitud en bytes y no en caracteres (linea 15).

A continuación definimos el iterador para la agenda:

```{code-cell} python
---
tags: [hide-input]
mystnb:
    number_source_lines: true
---
class AgendaIterator:
  """Iterador para la agenda"""
  def __init__(self, agenda):
      self._agenda = agenda
      self._indice = 0
  def __iter__(self):
      return self
  def __next__(self):
      if self._indice < self._agenda.cantidad_registros():
          registro = self.obtener_registro(self._indice)
          self._indice += 1
          return registro
      else:
          raise StopIteration
  def obtener_registro(self, indice):
      with open(self._agenda._archivo, "rb") as registros:
          posicion = indice * self._agenda._len_registro
          registros.seek(posicion)
          registro = registros.read(self._agenda._len_registro)
          if len(registro) == self._agenda._len_registro:
              registro = registro.decode().rstrip('\x00')
              campos = registro.split('|')
              if len(campos) == 4:
                  return campos[0], campos[1], campos[2], campos[3]
              else:
                  return None, None, None, None  # registro corrupto
          else:
              return None, None, None, None  # registro corrupto
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: [hide-output]
---
agenda = Agenda("agenda.dat")
agenda.guardar_contacto("Juan", "Pérez", "123456789", "juan@example.com")
agenda.guardar_contacto("Ana", "Gómez", "987654321", "ana@example.com")
for contacto in agenda:
    print(contacto)
    print("-----")
```

Si observamos el contenido del archivo `agenda.dat` con un editor hexadecimal, vemos que los datos están organizados en bloques de longitud fija, y cada campo está separado por el carácter `|`, rellenando con nulos si es necesario.

```{code-cell} python
---
tags: [hide-output]
---
with open("agenda.dat", "rb") as f:
    contenido = f.read()
    print(contenido)
``` 

Cada registro ocupa 100 bytes y los campos están separados por el byte `0x7c` que corresponde al carácter `|`.

Este formato tiene la ventaja de que permite almacenar campos de longitud variable dentro de un registro de longitud fija, lo cual es más eficiente en términos de espacio. Además, es sencillo calcular la posición de un registro en el archivo, ya que todos los registros tienen la misma longitud. Sin embargo, tiene la desventaja de que se desperdicia espacio si los registros son más cortos que la longitud asignada, y no es flexible si se quieren agregar nuevos campos o cambiar la longitud de los campos. Tampoco permite almacenar registros que superen la longitud asignada, ya que se truncan.

## Registros de longitud variable y campos de longitud variable

Para implementar este tipo de registro se puede preceder cada registro con un entero que indique la longitud del registro en bytes. De esta forma, al leer el archivo, se lee primero la longitud del registro y luego se lee el registro completo. Analogamente, se puede preceder cada campo con un entero que indique la longitud del campo en bytes.

