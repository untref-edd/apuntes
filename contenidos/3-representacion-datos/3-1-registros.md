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
description: Registros de datos, organización lógica de datos, archivos
---

# Registros de datos

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp/edd_registros"""
import os
import shutil

tmp_dir = "/tmp/edd_registros"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir, exist_ok=True)
os.chdir(tmp_dir)
```

En esta sección vamos a ver distintos formatos para organizar la información en archivos, es decir de la organización lógica de los datos. Estos formatos son independientes del lenguaje de programación que utilicemos, y en muchos casos son independientes del software que utilicemos.

Los registros permiten estructurar la información de una forma que facilita su almacenamiento, recuperación y manipulación.

```{admonition} Definición
Un **registro** es un conjunto de datos relacionados entre sí, que se almacenan juntos y representan una entidad o un objeto específico. Cada **registro** está compuesto por varios **campos**, donde cada **campo** contiene un dato específico.
```

Supongamos que queremos crear una **agenda** para almacenar datos de contactos: **nombre**, **apellido**, **teléfono** y **email**. En este caso un registro sería el conjunto de datos de un contacto, y los campos serían nombre, apellido, teléfono y email.

Una primera aproximación sería guardar los datos sin ningún tipo de organización, simplemente uno detrás de otro:

```{code-cell} python
---
tags: hide-output
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
agenda.guardar_contacto(
    "Ana", "Calle Falsa 123", "555-1234", "ana@example.com"
)
agenda.guardar_contacto(
    "Bart", "Calle Falsa 123", "555-5678", "bart@example.com"
)

with open("agenda.txt") as datos:
    for linea in datos:
        print(linea)
```

Si observamos el contenido del archivo `agenda.txt`, vemos que los datos están todos juntos, sin ningún tipo de organización. Se ha perdido **la integridad de los datos**, ya que no sabemos dónde termina un dato y empieza otro. Además, si queremos buscar un contacto, tenemos que leer todo el archivo y buscar el nombre, lo cual es muy ineficiente.

```{important} Integridad de datos
La **integridad de datos** se refiere a la exactitud, consistencia y confiabilidad de la información. En el contexto de la organización de archivos, mantener la integridad significa asegurar que la estructura elegida permita recuperar cada campo y cada registro de manera unívoca, sin ambigüedades ni pérdida de información.
```

Existen varios formatos para organizar los registros en un archivo, veamos algunos de ellos.

## Registros de longitud fija con campos de longitud fija

Una forma de organizar los registros es asignar una longitud fija a cada campo. Por ejemplo, podemos decidir que el campo **nombre** tendrá 20 caracteres, el campo **apellido** 30 caracteres, el campo **teléfono** 15 caracteres y el campo **email** 40 caracteres. Si un dato es más corto que la longitud asignada, se rellena con espacios en blanco o nulos. Si un dato es más largo, se trunca.

```{code-cell} python
import os
import struct


class Agenda:
    def __init__(
        self,
        archivo,
        len_nombre=20,
        len_apellido=30,
        len_telefono=15,
        len_email=40,
    ):
        self._archivo = archivo
        # Formato del registro: cada campo tiene longitud fija en bytes.
        # Ejemplo: "20s30s15s40s" para nombre, apellido, teléfono y email.
        # En total 105 bytes por registro.
        self._formato = "%ds%ds%ds%ds" % (
            len_nombre,
            len_apellido,
            len_telefono,
            len_email,
        )
        # Calcula la longitud total del registro en bytes.
        # struct.calcsize calcula el tamaño en bytes del formato especificado.
        self._len_registro = struct.calcsize(self._formato)

        # Calcula la cantidad de registros presentes en la agenda.
        try:
            tam_archivo = os.path.getsize(archivo)
            # Divide el tamaño del archivo por la longitud de cada registro.
            self._cant_registros = tam_archivo // self._len_registro
        except FileNotFoundError:
            self._cant_registros = 0

    def guardar_contacto(
        self, nombre, apellido, telefono="", email=""
    ):
        """
        Guarda un registro en el archivo.
        Nombre y apellido son obligatorios.
        """
        if not nombre or not apellido:
            raise ValueError("Nombre y apellido son obligatorios")

        # Abre el archivo en modo append binario. Lo crea si no existe.
        with open(self._archivo, "ab") as registros:
            # struct.pack convierte los datos en una secuencia de bytes
            # según el formato definido. Cada campo se codifica y se
            # rellena o trunca para ocupar la cantidad de bytes
            # especificada.
            registro = struct.pack(
                self._formato,
                nombre.encode(),
                apellido.encode(),
                telefono.encode(),
                email.encode(),
            )
            # Escribe el registro al final del archivo.
            registros.write(registro)

        self._cant_registros += 1

    def cantidad_registros(self):
        """Devuelve la cantidad de registros que hay en la agenda."""
        return self._cant_registros

    def __iter__(self):
        """Devuelve un iterador para la agenda."""
        return AgendaIterator(self)
```

```{note} Nota
Los métodos `encode()` y `decode()` convierten entre cadenas de texto y secuencias de bytes. Por defecto utilizan la codificación UTF-8, que es capaz de representar todos los caracteres Unicode. Si se utilizan caracteres especiales (como tildes o ñ), es importante asegurarse de que la codificación sea la misma al guardar y al leer los datos.
```

A continuación definimos el iterador para la agenda:

```{code-cell} python
class AgendaIterator:
    """Iterador para la agenda de registros de longitud fija"""

    def __init__(self, agenda):
        self._agenda = agenda
        self._index = 0  # Índice del registro actual

    def __iter__(self):
        return self

    def __next__(self):
        """
        Devuelve:
          dict: Un diccionario con el siguiente conjunto de datos o
                valores en la iteración.
        """
        # Si no quedan más registros finalizamos la iteración
        if self._index >= self._agenda._cant_registros:
            raise StopIteration()

        with open(self._agenda._archivo, "rb") as registros:
            # Calcula la posición en bytes del registro actual
            posicion = self._index * self._agenda._len_registro
            registros.seek(posicion)
            # Lee el bloque de bytes correspondiente al registro
            registro = registros.read(self._agenda._len_registro)

        self._index += 1

        # Verifica que se haya leído un registro completo
        if len(registro) != self._agenda._len_registro:
            # Si el registro está corrupto, devuelve campos vacíos
            return "", "", "", ""

        # struct.unpack convierte los bytes en tuplas de campos
        # según el formato definido en la agenda
        b_nombre, b_apellido, b_telefono, b_email = struct.unpack(
            self._agenda._formato, registro
        )

        # Decodifica los bytes y elimina espacios/nulos extra
        return (
            b_nombre.decode().strip(),
            b_apellido.decode().strip(),
            b_telefono.decode().strip(),
            b_email.decode().strip(),
        )
```

```{note} Nota
El método `strip()` elimina espacios en blanco y caracteres de nueva línea al inicio y al final de una cadena. En este caso, se utiliza para eliminar los caracteres nulos (`\x00`) que se utilizan para rellenar los campos cuando son más cortos que la longitud asignada.
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: hide-output
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
tags: hide-output
---
with open("agenda_fixed.dat", "rb") as f:
    contenido = f.read()
    print(contenido)

print(f"Longitud del registro: {agenda._len_registro} bytes")
print(f"Formato del registro: {agenda._formato} (105 bytes)")
print(f"Cantidad de registros: {agenda.cantidad_registros()}")
print(
    f"Cantidad de bytes en el archivo: {len(contenido)} "
    f"(105 * {agenda.cantidad_registros()})"
)
```

Este tipo de registros, no permite almacenar datos que superen la longitud asignada, ya que se truncan. Por ejemplo, si intentamos guardar un nombre con más de 20 caracteres, se perderán los caracteres adicionales. Por otro lado, si el dato es más corto que la longitud asignada, se rellena con nulos. En el archivo anterior observamos que la mayoría de los caracteres escritos son nulos `x00`.

## Registros de longitud fija y campos de longitud variable

Otra forma de organizar los registros es asignar una longitud fija a cada registro, pero permitir que los campos tengan longitud variable. Para ello, se puede utilizar un delimitador para separar los campos dentro del registro. Por ejemplo, podemos utilizar el carácter `|` como delimitador. Este tipo de organización es más eficiente en términos de espacio, ya que no se desperdicia espacio si los campos son más cortos que la longitud asignada. Sin embargo, tiene la desventaja de que no se pueden almacenar registros que superen la longitud asignada, ya que se truncan.

```{note} Nota
El carácter delimitador no puede aparecer en los datos, ya que se interpretaría como el final de un campo. Si es necesario que este caracter sea parte de los datos, se puede utilizar un mecanismo de escape, como por ejemplo, duplicar el carácter (`||` se interpreta como un solo `|` en los datos).
```

```{code-cell} python
class Agenda:
    def __init__(self, archivo, campos, len_registro=100):
        self._archivo = archivo
        self._len_registro = len_registro
        self._campos = campos  # lista de nombres de campos
        try:
            tam_archivo = os.path.getsize(archivo)
            self._cant_registros = tam_archivo // self._len_registro
        except FileNotFoundError:
            self._cant_registros = 0

    def guardar_contacto(self, *valores):
        """
        Guarda un registro en el archivo.
        La cantidad de valores debe coincidir con la cantidad de campos.
        """
        if len(valores) != len(self._campos):
            raise ValueError("Cantidad de valores incorrecta")

        if not valores[0] or not valores[1]:
            raise ValueError("Nombre y apellido son obligatorios")

        # Une los valores usando '|' como delimitador
        registro = "|".join(str(valor) for valor in valores)

        # Verifica que el registro no supere la longitud máxima
        if len(registro.encode()) > self._len_registro:
            raise ValueError("El registro es demasiado largo")

        # Convierte el registro a bytes y lo rellena con nulos si es necesario
        registro = registro.encode()
        registro = registro.ljust(self._len_registro, b"\x00")

        # Escribe el registro al final del archivo
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

```{note} Nota
`registro.encode()` convierte la cadena a bytes, y `ljust` rellena con nulos a la derecha, hasta alcanzar la longitud fija del registro. Algunos caracteres como vocales con tildes o la letra ñ pueden ocupar más de un byte (por ejemplo `é` se codifica como `b'\xc3\xa9'`), por lo que es importante medir la longitud en bytes y no en caracteres (línea 27).
```

A continuación definimos el iterador para la agenda:

```{code-cell} python
class AgendaIterator:
    """Iterador para la agenda de registros de longitud fija y campos de
    longitud variable
    """

    def __init__(self, agenda):
        self._agenda = agenda
        self._index = 0  # Índice del registro actual

    def __iter__(self):
        return self

    def __next__(self):
        """
        Devuelve:
          dict: Un diccionario con el siguiente conjunto de datos o valores
                en la iteración.
        """
        # Si no quedan más registros finalizamos la iteración
        if self._index >= self._agenda._cant_registros:
            raise StopIteration()

        with open(self._agenda._archivo, "rb") as registros:
            # Calcula la posición en bytes del registro actual.
            # Cada registro ocupa self._agenda._len_registro bytes,
            # por lo tanto la posición es índice * longitud_registro.
            posicion = int(self._index * self._agenda._len_registro)
            registros.seek(posicion)
            registro = registros.read(self._agenda._len_registro)

        self._index += 1

        if len(registro) != self._agenda._len_registro:
            # Registro corrupto
            return dict((campo, "") for campo in self._agenda._campos)

        registro = registro.rstrip(b"\x00").decode(errors="replace")
        campos = registro.split("|")

        # Rellenar campos faltantes con cadenas vacías
        while len(campos) < len(self._agenda._campos):
            campos.append("")

        # Devuelve un diccionario con claves nombre de los campos
        return dict(zip(self._agenda._campos,
                        campos[: len(self._agenda._campos)]))
```

```{note} Nota
El método `rstrip(b'\x00')` elimina los caracteres nulos (`\x00`) al final de la cadena de bytes, que se utilizan para rellenar el registro cuando es más corto que la longitud asignada. Luego, `decode(errors="replace")` convierte los bytes a una cadena de texto, reemplazando cualquier byte inválido con el carácter de reemplazo (`�`).

La función `zip` combina dos listas en una lista de tuplas, donde cada tupla contiene un elemento de cada lista. En este caso, se utiliza para combinar la lista de nombres de campos con la lista de valores correspondientes, y luego se convierte en un diccionario.
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: hide-output
---
agenda = Agenda("agenda.dat", ["nombre", "apellido", "telefono", "email"])
agenda.guardar_contacto("Juan", "Pérez", "123456789", "juan@example.com")
agenda.guardar_contacto("Ana", "Gómez", "987654321", "ana@example.com")

for contacto in agenda:
    print(contacto)
    print("-----")
```

Si observamos el contenido del archivo `agenda.dat` con un editor hexadecimal, vemos que los datos están organizados en bloques de longitud fija, y cada campo está separado por el carácter `|`, rellenando con nulos si es necesario.

```{code-cell} python
---
tags: hide-output
---
with open("agenda.dat", "rb") as f:
    contenido = f.read()
    print(contenido)

print(f"Longitud del registro: {agenda._len_registro} bytes")
print(f"Cantidad de registros: {agenda.cantidad_registros()}")
print(
    f"Cantidad de bytes en el archivo: {len(contenido)} "
    f"({agenda._len_registro} * {agenda.cantidad_registros()})"
)
```

## Registros de longitud variable y campos de longitud variable

Para implementar este tipo de registro se puede preceder cada registro con un entero que indique la longitud del registro en bytes. De esta forma, al leer el archivo, se lee primero la longitud del registro y luego se lee el registro completo. Analogamente, se puede preceder cada campo con un entero que indique la longitud del campo en bytes.

```{code-cell} python
import struct
import os


class Agenda:
    def __init__(self, archivo, campos):
        self._archivo = archivo
        self._campos = campos  # lista de nombres de campos

        try:
            tam_archivo = os.path.getsize(archivo)
            self._cant_registros = 0

            with open(archivo, "rb") as f:
                pos = 0
                # Recorre el archivo desde el inicio hasta el final
                while pos < tam_archivo:
                    f.seek(pos)
                    # Los primeros 4 bytes indican la longitud del registro
                    # 4 bytes para un entero sin signo (unsigned int)
                    len_bytes = f.read(4)

                    if len(len_bytes) < 4:
                        break  # fin de archivo o registro corrupto

                    # Convierte los 4 bytes en un int (longitud del registro)
                    (len_registro,) = struct.unpack("I", len_bytes)
                    # Avanza la pos: 4 bytes + longitud del registro
                    pos += 4 + len_registro
                    # Incrementa el contador de registros
                    self._cant_registros += 1
        except FileNotFoundError:
            # Si el archivo no existe, no hay registros
            self._cant_registros = 0

    def guardar_contacto(self, *campos):
        """
        Guarda un registro en el archivo.
        La cantidad de campos debe coincidir con la definición.
        """
        if len(campos) != len(self._campos):
            raise ValueError(
                "La cantidad de campos no coincide con la " "definición"
            )

        registro = b""
        for campo in campos:
            campo_bytes = campo.encode()
            len_campo = len(campo_bytes)
            # struct.pack("I", len_campo) convierte el entero en 4 bytes
            # Luego se concatenan los 4 bytes de longitud y los bytes del campo
            registro += struct.pack("I", len_campo) + campo_bytes
        len_registro = len(registro)

        with open(self._archivo, "ab") as registros:
            # Se concatenan los 4 bytes de longitud y los bytes del registro
            registros.write(struct.pack("I", len_registro))
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
class AgendaIterator:
    """Iterador para la agenda de registros de longitud variable"""

    def __init__(self, agenda):
        self._agenda = agenda
        self._pos = 0
        self._tam_archivo = os.path.getsize(self._agenda._archivo)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Devuelve:
          dict: Un diccionario con el siguiente conjunto de datos o
          valores en la iteración.
        """
        # Si quedan registros por leer
        if self._pos >= self._tam_archivo:
            raise StopIteration()

        with open(self._agenda._archivo, "rb") as f:
            f.seek(self._pos)
            len_bytes = f.read(4)

            if len(len_bytes) < 4:
                raise StopIteration()

            (len_registro,) = struct.unpack("I", len_bytes)
            registro_bytes = f.read(len_registro)

            if len(registro_bytes) < len_registro:
                raise StopIteration()

        self._pos += 4 + len_registro
        campos = []

        # offset es la posición dentro del registro
        offset = 0
        while (offset < len_registro) and \
              (len(campos) < len(self._agenda._campos)):
            len_campo_bytes = registro_bytes[offset : offset + 4]

            if len(len_campo_bytes) < 4:
                break

            (len_campo,) = struct.unpack("I", len_campo_bytes)
            offset += 4
            campo_bytes = registro_bytes[offset : offset + len_campo]
            campo = campo_bytes.decode()
            campos.append(campo)
            offset += len_campo

        # Rellenar campos faltantes con cadenas vacías
        while len(campos) < len(self._agenda._campos):
            campos.append("")

        return dict(zip(self._agenda._campos, campos))
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: hide-output
---
campos = ["nombre", "apellido", "telefono", "email"]
agenda = Agenda("agenda_var.dat", campos)
agenda.guardar_contacto("Juan", "Pérez", "123456789", "juan.perez@example.com")
agenda.guardar_contacto("Ana", "Gómez", "987654321", "ana.gomez@example.com")
agenda.guardar_contacto("Homero", "Simpson", "555-8765", "")  # sin email
agenda.guardar_contacto(
    "Lisa", "Simpson", "", "lisa.simpson@example.com"
)  # sin teléfono

for contacto in agenda:
    print(contacto)
    print("-----")
```

Si observamos el contenido del archivo `agenda_var.dat` con un editor hexadecimal, vemos que los datos están organizados en bloques de longitud variable, y cada campo está precedido por un entero que indica la longitud del campo en bytes.

```{code-cell} python
---
tags: hide-output
---
with open("agenda_var.dat", "rb") as f:
    contenido = f.read()
    print(contenido)

print(f"Cantidad de bytes en el archivo: {len(contenido)}")
print(f"Cantidad de registros: {agenda.cantidad_registros()}")
```

Esta forma de organizar los registros es la más flexible, ya que permite almacenar datos de cualquier longitud sin desperdiciar espacio. Sin embargo, tiene la desventaja de que el acceso a los registros es secuencial, ya que no se puede calcular la posición de un registro en función de su índice. Además, la implementación es más compleja, ya que se deben manejar las longitudes de los registros y campos.

## Otras formas de organizar registros

Se puede usar índices para acceder rápidamente a los registros, para lo que se crea un archivo de índices que contenga la posición de cada registro en el archivo de datos. De esta forma, se puede acceder rápidamente a un registro específico sin tener que leer todo el archivo.

```{figure} ../_static/figures/archivo_indices_light.svg
---
class: only-light-mode
---
Archivo de índices
```

```{figure} ../_static/figures/archivo_indices_dark.svg
---
class: only-dark-mode
---
Archivo de índices
```

Los índices permiten acelerar la búsqueda de registros, ya que se puede calcular la posición de un registro en función de su índice.

Cada una de estas formas tiene sus ventajas y desventajas, y la elección depende de las necesidades específicas de la aplicación. En general cuanto mayor flexibilidad se requiere en función del espacio ocupado, mayor es la complejidad de la implementación.

## Archivos CSV

Otra forma común de organizar los registros es utilizar el formato CSV (*Comma-Separated Values*). En este formato, cada registro se almacena en una línea del archivo, y los campos dentro del registro están separados por comas. Si un campo contiene una coma, se encierra entre comillas dobles. Si un campo contiene comillas dobles, se escapan con otra comilla doble.

Python cuenta con un módulo estándar llamado `csv` que facilita la lectura y escritura de archivos en formato CSV. Veamos cómo implementar la clase `Agenda` utilizando este formato.

```{note} Nota
La primera línea del archivo puede contener los nombres de los campos, lo cual facilita la interpretación de los datos. El módulo `csv` puede manejar esto automáticamente si se utiliza la clase `DictReader` para leer y `DictWriter` para escribir.
```

```{code-cell} python
import csv
import os


class Agenda:
    def __init__(self, archivo, campos, separador=","):
        self._archivo = archivo
        self._campos = campos  # lista de nombres de campos
        self._cant_registros = 0
        self._separador = separador

        # Escribir cabecera si el archivo no existe o está vacío
        if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
            with open(archivo, "w", newline="") as f:
                # Escribir el encabezado usando los nombres de los campos
                writer = csv.DictWriter(f, fieldnames=campos,\
                                        delimiter=separador)
                writer.writeheader()  # escribe la cabecera en la primera línea

        # Contar registros (excluyendo la cabecera)
        try:
            with open(archivo, "r", newline="") as f:
                reader = csv.DictReader(f, fieldnames=campos,\
                                        delimiter=separador)

                next(reader, None)  # saltar cabecera

                for _ in reader:
                    self._cant_registros += 1
        except FileNotFoundError:
            self._cant_registros = 0

    def guardar_contacto(self, *valores):
        """
        Guarda un registro. La cantidad de valores debe coincidir con
        la cantidad de campos.
        Se arma el registro como un diccionario: {campo: valor}
        """
        if len(valores) != len(self._campos):
            raise ValueError("Cantidad de valores incorrecta")

        if not valores[0] or not valores[1]:
            raise ValueError("Nombre y apellido son obligatorios")

        registro = dict(zip(self._campos, valores)) # registro como dict

        with open(self._archivo, "a", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=self._campos, delimiter=self._separador
            )
            writer.writerow(registro)  # escribe el registro como fila dict

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
class AgendaIterator:
    """Iterador para la agenda de registros en formato CSV con cabecera"""

    def __init__(self, agenda):
        self._agenda = agenda
        # Abrir el archivo en modo lectura
        self._file = open(self._agenda._archivo, "r", newline="")
        # Usar DictReader para leer registros como diccionarios
        self._reader = csv.DictReader(
            self._file,
            fieldnames=self._agenda._campos,
            delimiter=self._agenda._separador,
        )
        next(self._reader, None)  # Saltar la cabecera

    def __iter__(self):
        return self

    def __next__(self):
        try:
            # Cada registro se obtiene como un diccionario {campo: valor}
            registro = next(self._reader)
            # Si faltan campos, se rellenan con cadenas vacías
            for campo in self._agenda._campos:
                if campo not in registro or registro[campo] is None:
                    registro[campo] = ""
            # Devuelve el registro parseado en campos
            return registro
        except StopIteration:
            self._file.close()
            raise StopIteration
```

Ejemplo de uso con el iterador

```{code-cell} python
---
tags: hide-output
---
campos = ["nombre", "apellido", "telefono", "email"]
agenda = Agenda("agenda.csv", campos)
agenda.guardar_contacto("Juan", "Pérez", "123456789", "juan.perez@example.com")
agenda.guardar_contacto("Ana", "Gómez", "987654321", "ana.gomez@example.com")
agenda.guardar_contacto("Homero", "Simpson", "555-8765", "")  # sin email
agenda.guardar_contacto("Lisa", "Simpson", "", "lisa.simpson@example.com")

for contacto in agenda:
    print(contacto)
    print("-----")
```

Si observamos el contenido del archivo `agenda.csv`, vemos que los datos están organizados en líneas, y cada campo está separado por comas. La primera línea contiene los nombres de los campos.

```{code-cell} python
---
tags: hide-output
---
with open("agenda.csv", "r") as f:
    contenido = f.read()
    print(contenido)

print(f"Cantidad de registros: {agenda.cantidad_registros()}")
```

## Comparación de formatos de registros

| Tipo de registro | Descripción | Ventajas | Desventajas |
| :--- | :--- | :--- | :--- |
| **Longitud fija** | Cada campo y registro ocupa una cantidad predefinida de bytes. | Acceso directo (random access) muy rápido. Implementación simple. | Desperdicio de espacio (fragmentación). Truncamiento de datos que exceden el tamaño. |
| **Delimitadores (CSV)** | Los campos se separan por un carácter especial (coma, punto y coma) y los registros por saltos de línea. | Alta flexibilidad y legibilidad humana. Fácil de editar y compatible con muchas herramientas. | Acceso secuencial (lento para grandes volúmenes). Requiere manejo de escapes si el delimitador aparece en los datos. |
| **Indicadores de longitud** | Cada campo o registro es precedido por un valor numérico que indica su tamaño en bytes. | Uso eficiente del espacio. Permite almacenar cualquier tipo de dato (incluyendo binarios) sin conflictos. | Implementación más compleja. Acceso secuencial. Sobrecarga de almacenamiento por los metadatos de longitud. |
