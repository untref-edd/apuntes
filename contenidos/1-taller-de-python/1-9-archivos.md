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
# Archivos

En casi cualquier lenguaje de programación, interactuar con archivos es fundamental.  
En **Java** y **Go**, esto se hace a través de librerías específicas (`java.io`, `os`), pero en **Python** es mucho más directo y expresivo.

## Representación de archivos y carpetas

En un sistema operativo (SO), un **archivo** es básicamente una secuencia de bytes almacenada en un medio físico (disco, SSD, memoria externa). Por lo general los archivos se encuentran en el disco dentro de un **sistema de archivos** o **filesystem**. Este **sistema de archivo** depende de cada sistema operativo. Por ejemplo Linux utiliza un **sistema de archivos** denominado ***ext4***, mientras que Windows utiliza ***NTFS***.

La principal diferencia entre distintos sistemas de archivos es como se gestionan los metadatos (información sobre el archivo, como su nombre, tamaño, permisos, etc.) y la estructura de directorios.

Archivo
: Contiene datos (texto, imágenes, binarios, etc.).

Carpeta (o directorio)
: Estructura que agrupa archivos y otras carpetas.

Para que una aplicación o programa pueda crear, leer o escribir un archivo o carpeta debe realizar una solicitud al SO, principal responsable de la gestión del hardware.

El SO responde a la petición con un ***descriptor de archivo*** (*file descriptor*). Este ***descriptor de archivo*** es un número entero que identifica de manera única un archivo abierto en ese momento.

Mientras la aplicación tiene el archivo abierto, puede leer y escribir en él. Cuando la aplicación ya no necesita más el archivo debe *cerrarlo*. Al cerrar el archivo se notifica al SO que se terminó de utilizar y por lo tanto queda disponible para que otra aplicación o programa pueda manipularlo.

### Lectura y escritura

Cuando abrimos un archivo:

1. El S.O. localiza el archivo y asigna un *file descriptor*.
2. Python crea un **objeto archivo** que envuelve ese descriptor.
3. Las operaciones de lectura/escritura se hacen en **buffers** (bloques de memoria intermedia) para optimizar el rendimiento.

Ejemplo: si quiere leer un archivo grande, Python no trae todo de golpe, sino trozos que se van entregando al programa. Lo mismo ocurre al escribir, en lugar de escribir todo de una vez, Python lo hace en partes.

Cuando se cierra un archivo en el que se escribieron datos, Python se asegura que todos los datos se hayan escrito correctamente en el disco, volcando toda la información de los buffers.

En este contexto es fundamental usar los bloques `try / finally` para garantizar que los archivos se cierren adecuadamente, incluso si ocurre un error durante la lectura o escritura. Como el bloque `finally` se ejecuta siempre, podemos asegurarnos de que el archivo se cierre en cualquier situación, incluso si hay excepciones, y que todos los datos escritos se guarden correctamente, liberando el archivo para su uso futuro o parte de otro programa.

### Archivos de texto vs binarios

Texto
: Interpretan bytes según una codificación (por ejemplo UTF-8).  
: Ejemplo: `"hola"` → `68 6f 6c 61` (bytes) interpretados como caracteres.

Binarios
: Los bytes se usan tal cual (imágenes, ejecutables, audio, etc.).

En Python, esto se define al abrir el archivo con `'t'` (texto) o `'b'` (binario). En general si se omite el modo, se abrirá en modo texto.

### Saltos de línea: `\n` vs `\r\n`

En **Linux y macOS** los saltos de línea se representan con el caracter `\n`, mientras que en **Windows** se usan dos caracteres `\r\n`. Python **traduce automáticamente** al trabajar en modo texto, así que no hay que preocuparse si el programa se ejecuta en un entorno **Windows**, **Linux** o **macOS**, salvo que estemos manipulando el archivo en modo binario, donde es responsabilidad del programador.

## Operaciones con carpetas

Para manipular carpetas y rutas, Python ofrece los módulos **`os`** y **`pathlib`**.

### Rutas o Paths absolutos y relativos

Path Absoluto
: Especifica toda la ruta desde la raíz.  
: Por ejemplo: `/home/usuario/archivo.txt` o `C:\Users\Usuario\archivo.txt`

Path Relativo
: Se interpreta desde el directorio donde se ejecuta el programa.  
: Por ejemplo: `datos/archivo.txt`

El caracter especial `.` representa el directorio actual, mientras que `..` representa el directorio padre, con lo cual se pueden gestionar rutas relativas de manera más sencilla.

Algunas funciones útiles del módulo `os` para manipular archivos y carpetas son:

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `os.getcwd()` | Obtiene el directorio de trabajo actual | `'/home/usuario/proyecto'` |
| `os.chdir(path)` | Cambia el directorio de trabajo actual | `os.chdir('/home/usuario/docs')` |
| `os.listdir(path)` | Lista archivos y carpetas en un directorio | `['archivo1.txt', 'carpeta1', 'imagen.png']` |
| `os.mkdir(path)` | Crea un directorio | `os.mkdir('nueva_carpeta')` |
| `os.makedirs(path)` | Crea directorios anidados (recursivo) | `os.makedirs('carpeta/subcarpeta')` |
| `os.rmdir(path)` | Elimina un directorio vacío | `os.rmdir('carpeta_vacia')` |
| `os.removedirs(path)` | Elimina directorios vacíos recursivamente | `os.removedirs('carpeta/subcarpeta')` |
| `os.remove(path)` | Elimina un archivo | `os.remove('archivo.txt')` |
| `os.rename(old, new)` | Renombra archivo o directorio | `os.rename('viejo.txt', 'nuevo.txt')` |
| `os.stat(path)` | Obtiene información del archivo (tamaño, permisos, etc.) | `os.stat('archivo.txt')` |
| `os.path.exists(path)` | Verifica si existe archivo o directorio | `True` o `False` |
| `os.path.isfile(path)` | Verifica si es un archivo | `True` o `False` |
| `os.path.isdir(path)` | Verifica si es un directorio | `True` o `False` |
| `os.path.join(...)` | Une partes de una ruta de forma portable | `os.path.join('carpeta', 'archivo.txt')` |
| `os.path.basename(path)` | Obtiene el nombre del archivo | `'archivo.txt'` de `'/ruta/archivo.txt'` |
| `os.path.dirname(path)` | Obtiene el directorio padre | `'/ruta'` de `'/ruta/archivo.txt'` |
| `os.path.splitext(path)` | Separa nombre y extensión | `('archivo', '.txt')` |
| `os.path.abspath(path)` | Convierte ruta relativa a absoluta | `'/home/usuario/archivo.txt'` |
| `os.path.getsize(path)` | Obtiene tamaño del archivo en bytes | `1024` |

```{code-cell} python
:tags: [hide-output]

import os

# Ejemplo práctico de uso
directorio_actual = os.getcwd()
print(f"Directorio actual: {directorio_actual}")
print("Archivos en directorio actual:")
for archivo in os.listdir('.'):
    print(f" - {archivo}")

os.chdir('/tmp') # Cambia al directorio temporal
# Crear estructura de carpetas
if not os.path.exists('datos'):
    os.makedirs('datos/procesados')
    print(f"Estructura de carpetas creada: {os.path.abspath('datos/procesados')}")

# Trabajar con rutas
# Construir una ruta a un archivo.
# Se recomienda usar os.path.join y no concatenar cadenas
# ya que el módulo os puede construir rutas de forma portable para 
# cualquier sistema operativo. Es decir este programa funcionará
# en cualquier sistema operativo sin modificaciones
ruta_archivo = os.path.join('datos', 'archivo.txt')
print(f"Ruta construida: {ruta_archivo}")
print(f"Ruta absoluta: {os.path.abspath(ruta_archivo)}")
print(f"¿Existe la ruta?: {os.path.exists(ruta_archivo)}")
os.chdir(directorio_actual)

```

### Módulo `pathlib` (Recomendado para proyectos nuevos)

Python 3.4+ incluye `pathlib`, que ofrece una interfaz más moderna y orientada a objetos:

| Función/Método | Descripción | Ejemplo |
|----------------|-------------|---------|
| `Path.cwd()` | Directorio actual | `Path.cwd()` |
| `Path.home()` | Directorio home del usuario | `Path.home()` |
| `Path.exists()` | Verifica existencia | `Path('archivo.txt').exists()` |
| `Path.is_file()` | Verifica si es archivo | `Path('archivo.txt').is_file()` |
| `Path.is_dir()` | Verifica si es directorio | `Path('carpeta').is_dir()` |
| `Path.mkdir()` | Crea directorio | `Path('nueva').mkdir(parents=True)` |
| `Path.unlink()` | Elimina archivo | `Path('archivo.txt').unlink()` |
| `Path.rmdir()` | Elimina directorio vacío | `Path('carpeta').rmdir()` |
| `Path.iterdir()` | Itera sobre contenido | `list(Path('.').iterdir())` |
| `Path.glob(pattern)` | Busca archivos por patrón | `Path('.').glob('*.txt')` |
| `Path.chdir(path)` | Cambia el directorio actual | `Path.chdir('/nueva/ruta')` |

```{code-cell} python
:tags: [hide-output]

from pathlib import Path

# Ejemplo con pathlib (más pythónico)
directorio_actual = Path.cwd()
print(f"Directorio act: {directorio_actual}")

# Crear ruta de forma elegante
archivo = Path('/tmp') / "datos" / "ejemplo.txt"
print(f"Ruta del archivo: {archivo}")

# Crear directorio si no existe
archivo.parent.mkdir(parents=True, exist_ok=True)
print(f"Directorio creado: {archivo.parent}")

# Buscar archivos por patrón
archivos_md = list(Path('.').glob('**/*.md'))
print(f"Archivos Markdown encontrados: {len(archivos_md)}")
```

```{admonition} Recomendación
Para código nuevo, se recomienda usar `pathlib` ya que es más legible y moderno. Para compatibilidad con código antiguo o scripts simples, `os.path` sigue siendo válido.
```

### ***Caminar*** por el sistema de archivos

`os.walk()` permite recorrer todas las carpetas y archivos a partir de una ubicación dada

```{code-cell}
:tags: [hide-output]

import os

# Ejemplo de uso de os.walk()
for raiz, dirs, archivos in os.walk('.'):
    print(f"Carpeta: {raiz}")
    for archivo in archivos:
        print(f" - {archivo}")
        print(f"   Ruta absoluta: {os.path.abspath(archivo)}")

        # Obtener información del archivo
        info = os.stat(archivo)
        print(f"   Tamaño: {info.st_size} bytes")
        print(f"   Última modificación: {info.st_mtime}")
        print(f"   Permisos: {info.st_mode}")
        print(f"   Propietario: {info.st_uid}")
        print(f"   Grupo: {info.st_gid}")
        print()
```

## Operaciones básicas sobre archivos

### Apertura de archivos

La función básica para abrir archivos es open():

```{code-block} python
open(nombre, modo, encoding)
```

| Modo   | Significado                           | Crea archivo si no existe | Borra contenido previo |
| ------ | ------------------------------------- | ------------------------- | ---------------------- |
| `'r'`  | read (lectura)                        | No                        | No                     |
| `'w'`  | write (escritura)                     | Si                        | Si                     |
| `'a'`  | append (agregar)                      | Si                        | No                     |
| `'x'`  | exclusive write (escritura exclusiva) | Si                        | -                      |

El modo `'x'` es similar a `'w'`, pero **lanza una excepción** si el archivo ya existe. Se usa para asegurarse que no estamos borrando el contenido de un archivo creado previamente.

El modo `'a'` permite agregar contenido al final del archivo sin borrar el contenido existente. Si el archivo no existe previamente, se crea.

Los modos de apertura de archivos por defecto abren los archivos como texto, si se trata de un archivo binario se debe especificar el modo `'b'`. Por ejemplo: `'rb'` para lectura binaria o `'wb'` para escritura binaria.

```{code-cell}
:tags: [hide-output]
help(open)
```

### Lectura de archivos

Una vez abierto un archivo hay varias formas de leerlo, se puede leer completamente y cargarlo en memoria, o leerlo línea por línea, o posicionar el cursor en una parte específica del archivo para leer desde allí la cantidad de caracteres deseada, etc.

El archivo de texto que vamos a usar de prueba tiene texto en castellano y en chino tradicional, con caracteres especiales.

#### Leer todo el documento en una variable

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'r', encoding='utf-8') # Puede levantar FileNotFoundError
  contenido = f.read() # Puede levantar otras excepciones
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print(contenido)
finally:
  f.close()
```

#### Leer línea por línea en una lista

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'r', encoding='utf-8') # Puede levantar FileNotFoundError
  contenido = f.readlines() # Puede levantar otras excepciones
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print(contenido)
finally:
  f.close()
```

#### Iterar línea por línea

```{code-cell}
:tags: [hide-output]
# Iterar con while

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'r', encoding='utf-8') # Puede levantar FileNotFoundError
  while (linea := f.readline()):
    print(linea)
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
finally:
  f.close()
```

```{code-cell}
:tags: [hide-output]
# Iterar con for

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'r', encoding='utf-8') # Puede levantar FileNotFoundError
  for linea in f:
    print(linea)
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
finally:
  f.close()
```

#### Leer una porción específica del archivo

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'r', encoding='utf-8') # Puede levantar FileNotFoundError
  f.seek(100) # Posicionar el cursor en el caracter 100
  print("Leer desde la posición 100\n")
  print(f.read(100)) # Leer 100 caracteres a partir de la posición 100
  print("\nLeer desde el inicio\n")
  f.seek(0) # Volver al inicio del archivo
  print(f.read(100)) # Leer 100 caracteres desde el inicio
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
finally:
  f.close()
```

#### Leer un archivo binario

Si leemos el mismo archivo de texto pero en formato binario veremos dígitos en hexadecimal que se usan para representar los caracteres especiales.

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/edd.txt'

try:
  f=open(archivo, 'rb') # Puede levantar FileNotFoundError
  contenido = f.read() # Puede levantar otras excepciones
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print(contenido)
finally:
  f.close()
```

### Escritura de archivos

De forma similar a la lectura, podemos escribir en un archivo utilizando el modo de apertura 'w' (write) o 'a' (append). El modo 'w' sobrescribe el archivo si ya existe, mientras que 'a' agrega contenido al final del archivo.

#### Escribir todo el contenido de una vez

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/texto.txt'

try:
  f=open(archivo, 'w', encoding='utf-8') 
  f.write("Nuevo contenido para el archivo\n")
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print("Contenido escrito correctamente")
finally:
  f.close()
```

#### Escribir línea por línea

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/texto.txt'

try:
  f=open(archivo, 'w', encoding='utf-8') 
  lista =[]
  for i in range(5):
    lista.append(f"Línea {i}\n")
  f.writelines(lista)
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print("Contenido escrito correctamente")
finally:
  f.close()
```

```{code-cell}
:tags: [hide-output]

archivo = '../_static/code/archivos/texto.txt'

try:
  f=open(archivo, 'a', encoding='utf-8') 
  lista =[]
  for i in range(5):
    lista.append(f"Línea {i}\n")
  f.writelines(lista)
  f.write("學科基礎\n")
except FileNotFoundError:
  print("Archivo no encontrado")
except Exception as e:
  print(f"Error inesperado: {e}")
else:
  print("Contenido agregado correctamente")
finally:
  f.close()
```

### Entorno seguro para manipular archivos

Python provee un entorno seguro para manipular archivos con la sentencia `with` que nos asegura que siempre se cierra el archivo cuando se sale del bloque.

```{code-cell}
:tags: [hide-output]

def copiar_archivo(origen, destino):
    with open(origen, "r") as f_origen, open(destino, "w") as f_destino:
        while bloque := f_origen.read(1024):
            f_destino.write(bloque)

def mostrar_archivo(archivo):
    with open(archivo, "r") as f:
        for linea in f:
            print(linea)

# Copiamos texto.txt a copia.txt
copiar_archivo("../_static/code/archivos/texto.txt", \
               "../_static/code/archivos/copia.txt")
mostrar_archivo("../_static/code/archivos/copia.txt")
```

El siguiente script nos permite comparar byte a byte dos archivos para ver si son iguales

```{code-cell}
:tags: [hide-output]

def comparar_archivos(archivo1, archivo2):
    with open(archivo1, "rb") as f1, open(archivo2, "rb") as f2:
        while True:
            bloque1 = f1.read(1024)
            bloque2 = f2.read(1024)
            if bloque1 != bloque2:
                print("Los archivos son diferentes")
                return
            if not bloque1:
                break
    print("Los archivos son iguales")

# Comparamos texto.txt con copia.txt
comparar_archivos("../_static/code/archivos/texto.txt", \
                  "../_static/code/archivos/copia.txt")
```

## Recursos para profundizar

- [Documentación oficial de Python sobre manejo de archivos](https://docs.python.org/es/3.13/tutorial/inputoutput.html#reading-and-writing-files){target="_blank"}
- [Módulo os](https://docs.python.org/es/3.13/library/os.html){target="_blank"}
- [Módulo pathlib](https://docs.python.org/es/3.13/library/pathlib.html){target="_blank"}
- [Módulo shutil: copia y eliminación de archivos](https://docs.python.org/es/3.13/library/shutil.html){target="_blank"}
