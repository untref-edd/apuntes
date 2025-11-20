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
description: Expresiones Regulares, regex
---

# Expresiones Regulares (Regex)

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp"""
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

Las **expresiones regulares** (también conocidas como _regex_ o _regexp_) son secuencias de caracteres que forman un patrón de búsqueda. Son una herramienta fundamental para el procesamiento de texto y la recuperación de información, permitiendo buscar, validar, extraer y manipular cadenas de texto de forma eficiente y flexible.

En el contexto de las estructuras de datos y la recuperación de información, las expresiones regulares son esenciales para:

- **Búsqueda y extracción de información** en grandes volúmenes de texto
- **Validación de datos** (emails, teléfonos, URLs, etc.)
- **Procesamiento de logs** y archivos de texto
- **Web scraping** y extracción de datos de páginas web
- **Limpieza y transformación de datos** antes de almacenarlos en estructuras de datos

## ¿Qué son las expresiones regulares?

Una expresión regular es un patrón que describe un conjunto de cadenas de texto. Por ejemplo, el patrón `r"\d{3}-\d{4}"` describe cualquier cadena que tenga tres dígitos, seguidos de un guion, seguidos de cuatro dígitos (como `"123-4567"`).

Las expresiones regulares utilizan una sintaxis especial con **metacaracteres** que tienen significados especiales. Estos metacaracteres permiten definir patrones complejos de forma concisa.

### Ejemplo simple

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Mi teléfono es 555-1234"
patron = r"\d{3}-\d{4}"

resultado = re.search(patron, texto)
if resultado:
    print(f"Encontrado: {resultado.group()}")
else:
    print("No encontrado")
```

## Sintaxis básica y metacaracteres

Las expresiones regulares utilizan caracteres especiales (metacaracteres) que tienen significados específicos. Veamos los más importantes:

### Caracteres literales

Los caracteres normales (letras, números) se buscan literalmente:

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Python es un lenguaje de programación"
patron = r"Python"

if re.search(patron, texto):
    print("Se encontró 'Python'")
```

### Metacaracteres básicos

`.` (punto)
: Coincide con cualquier carácter excepto salto de línea

`^` (circunflejo)
: Coincide con el inicio de la cadena

`$` (signo de dólar)
: Coincide con el final de la cadena

`*` (asterisco)
: Coincide con 0 o más repeticiones del patrón anterior

`+` (más)
: Coincide con 1 o más repeticiones del patrón anterior

`?` (interrogación)
: Coincide con 0 o 1 repetición del patrón anterior

`[]` (corchetes)
: Define un conjunto de caracteres

`|` (barra vertical)
: Operador OR (alternativa)

`()` (paréntesis)
: Agrupa expresiones y captura coincidencias

`\` (barra invertida)
: Escapa metacaracteres o define secuencias especiales

### Ejemplos de metacaracteres

```{code-cell} python
---
tags: hide-output
---
import re

# Punto: cualquier carácter
print(re.findall(r"c.sa", "casa cosa cesa"))  # ['casa', 'cosa', 'cesa']

# Inicio y fin de cadena
print(re.search(r"^Hola", "Hola mundo"))  # Encuentra 'Hola'
print(re.search(r"mundo$", "Hola mundo"))  # Encuentra 'mundo'

# Asterisco: 0 o más
print(re.findall(r"lo*", "l lo loo looo"))  # ['l', 'lo', 'loo', 'looo']

# Más: 1 o más
print(re.findall(r"lo+", "l lo loo looo"))  # ['lo', 'loo', 'looo']

# Interrogación: 0 o 1
print(re.findall(r"lo?", "l lo loo"))  # ['l', 'lo', 'lo']
```

### Cuantificadores

Los cuantificadores especifican cuántas veces debe aparecer el patrón anterior:

`{n}`
: Exactamente n repeticiones

`{n,}`
: Al menos n repeticiones

`{n,m}`
: Entre n y m repeticiones

```{code-cell} python
---
tags: hide-output
---
import re

texto = "El código es 12, 123, 1234 y 12345"

# Exactamente 3 dígitos
print(re.findall(r"\d{3}", texto))  # ['123', '123']

# Al menos 3 dígitos
print(re.findall(r"\d{3,}", texto))  # ['123', '1234', '12345']

# Entre 2 y 4 dígitos
print(re.findall(r"\d{2,4}", texto))  # ['12', '123', '1234', '1234']
```

### Clases de caracteres

Las clases de caracteres permiten definir conjuntos de caracteres válidos:

`[abc]`
: Cualquiera de los caracteres a, b o c

`[a-z]`
: Cualquier letra minúscula

`[A-Z]`
: Cualquier letra mayúscula

`[0-9]`
: Cualquier dígito

`[^abc]`
: Cualquier carácter excepto a, b o c

```{code-cell} python
---
tags: hide-output
---
import re

texto = "El código postal es A1234BCZ"

# Letras mayúsculas
print(re.findall(r"[A-Z]", texto))  # ['E', 'A', 'B', 'C', 'Z']

# Dígitos
print(re.findall(r"[0-9]+", texto))  # ['1234']

# Letras y números
print(re.findall(r"[A-Z0-9]+", texto))  # ['A1234BCZ']

# Todo excepto espacios
print(re.findall(r"[^ ]+", texto))  # ['El', 'código', 'postal', 'es', 'A1234BCZ']
```

### Secuencias especiales

Python proporciona atajos para clases de caracteres comunes:

`\d`
: Cualquier dígito (equivalente a `[0-9]`)

`\D`
: Cualquier no-dígito

`\w`
: Cualquier carácter de palabra: letra, dígito o guion bajo (equivalente a `[a-zA-Z0-9_]`)

`\W`
: Cualquier no-carácter de palabra

`\s`
: Cualquier espacio en blanco (espacio, tab, salto de línea)

`\S`
: Cualquier no-espacio en blanco

`\b`
: Límite de palabra

`\B`
: No-límite de palabra

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Usuario: juan_123, Email: juan@email.com"

# Dígitos
print(re.findall(r"\d+", texto))  # ['123']

# Caracteres de palabra
print(
    re.findall(r"\w+", texto)
)  # ['Usuario', 'juan_123', 'Email', 'juan', 'email', 'com']

# Límites de palabra
print(re.findall(r"\bjuan\b", texto))  # ['juan']
print(re.findall(r"\bjuan", "juanito juan"))  # ['juan', 'juan']
```

## El módulo `re` en Python

Python proporciona el módulo `re` para trabajar con expresiones regulares. Este módulo incluye varias funciones útiles:

### Funciones principales

`re.search(patron, texto)`
: Busca la primera ocurrencia del patrón en el texto

`re.match(patron, texto)`
: Busca el patrón solo al inicio del texto

`re.findall(patron, texto)`
: Devuelve todas las ocurrencias del patrón como una lista

`re.finditer(patron, texto)`
: Devuelve un iterador con todas las ocurrencias

`re.sub(patron, reemplazo, texto)`
: Reemplaza las ocurrencias del patrón

`re.split(patron, texto)`
: Divide el texto usando el patrón como separador

`re.compile(patron)`
: Compila el patrón para reutilizarlo eficientemente

### Ejemplos de uso

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Los emails son: juan@email.com, ana@empresa.com.ar y pedro@sitio.org"

# search: encuentra la primera coincidencia
resultado = re.search(r"\w+@\w+\.\w+", texto)
if resultado:
    print(f"Primer email encontrado: {resultado.group()}")

# findall: encuentra todas las coincidencias
emails = re.findall(r"\w+@[\w.]+", texto)
print(f"Todos los emails: {emails}")

# finditer: iterador sobre las coincidencias
for match in re.finditer(r"\w+@[\w.]+", texto):
    print(f"Email en posición {match.start()}-{match.end()}: {match.group()}")
```

### Compilación de patrones

Cuando se usa un patrón múltiples veces, es más eficiente compilarlo:

```{code-cell} python
---
tags: hide-output
---
import re

# Compilar el patrón una sola vez
patron_email = re.compile(r"\w+@[\w.]+")

textos = [
    "Contacto: juan@email.com",
    "Soporte: ayuda@empresa.com",
    "Ventas: ventas@sitio.org",
]

for texto in textos:
    match = patron_email.search(texto)
    if match:
        print(f"{texto} -> {match.group()}")
```

### Grupos de captura

Los paréntesis `()` crean grupos de captura que permiten extraer partes específicas del patrón:

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Fecha: 15/03/2024"
patron = r"(\d{2})/(\d{2})/(\d{4})"

match = re.search(patron, texto)
if match:
    print(f"Fecha completa: {match.group(0)}")  # Toda la coincidencia
    print(f"Día: {match.group(1)}")  # Primer grupo
    print(f"Mes: {match.group(2)}")  # Segundo grupo
    print(f"Año: {match.group(3)}")  # Tercer grupo
    print(f"Todos los grupos: {match.groups()}")  # Tupla con todos los grupos
```

### Grupos nombrados

Se pueden asignar nombres a los grupos para mayor claridad:

```{code-cell} python
---
tags: hide-output
---
import re

texto = "Producto: ABC-123 Precio: $450.50"
patron = r"(?P<codigo>[A-Z]+-\d+).*?\$(?P<precio>\d+\.\d+)"

match = re.search(patron, texto)
if match:
    print(f"Código: {match.group('codigo')}")
    print(f"Precio: {match.group('precio')}")
    print(f"Diccionario: {match.groupdict()}")
```

### Miradas alrededor

Las miradas alrededor permiten hacer coincidir un patrón solo si está precedido o seguido por otro patrón, sin incluirlo en la coincidencia:

`(?=...)`
: Mirada hacia adelante positiva (_lookahead_)

`(?!...)`
: Mirada hacia adelante negativa

`(?<=...)`
: Mirada hacia atrás positiva (_lookbehind_)

`(?<!...)`
: Mirada hacia atrás negativa

```{code-cell} python
---
tags: hide-output
---
import re

texto = "foo1 bar2 foo3 baz4"
# Mirada hacia adelante: foo seguido de un dígito
print(re.findall(r"foo(?=\d)", texto))  # ['foo', 'foo']

# Mirada hacia atrás: dígito precedido de foo
print(re.findall(r"(?<=foo)\d", texto))  # ['1', '3']
```

## Casos de uso en recuperación de información

Las expresiones regulares son fundamentales en la recuperación y procesamiento de información. Veamos casos prácticos:

### Validación de datos

```{code-cell} python
---
tags: hide-output
---
import re


def validar_email(email):
    """Valida un email con expresión regular"""
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None


def validar_telefono_argentina(telefono):
    """Valida teléfono argentino: +54 11 1234-5678"""
    patron = r"^\+54\s?\d{2}\s?\d{4}-?\d{4}$"
    return re.match(patron, telefono) is not None


def validar_url(url):
    """Valida una URL"""
    patron = r"^https?://(www\.)?[\w.-]+\.[a-z]{2,}(/[\w.-]*)*/?$"
    return re.match(patron, url) is not None


# Pruebas
print(f"Email válido: {validar_email('juan@email.com')}")
print(f"Email inválido: {validar_email('juan@email')}")
print(f"Teléfono válido: {validar_telefono_argentina('+54 11 1234-5678')}")
print(f"URL válida: {validar_url('https://www.ejemplo.com/path')}")
```

### Extracción de información

```{code-cell} python
---
tags: hide-output
---
import re

# Texto de ejemplo: log de servidor web
log = """
192.168.1.1 - - [15/Mar/2024:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234
10.0.0.5 - - [15/Mar/2024:10:31:12 +0000] "POST /api/data HTTP/1.1" 201 567
192.168.1.1 - - [15/Mar/2024:10:32:33 +0000] "GET /styles.css HTTP/1.1" 200 8910
"""

# Patrón para extraer información del log
patron = r'(\d+\.\d+\.\d+\.\d+).*?\[([^\]]+)\]\s+"(\w+)\s+([^\s]+).*?"\s+(\d+)\s+(\d+)'

for linea in log.strip().split("\n"):
    match = re.search(patron, linea)
    if match:
        ip, fecha, metodo, ruta, codigo, tamaño = match.groups()
        print(f"IP: {ip}")
        print(f"Fecha: {fecha}")
        print(f"Método: {metodo}")
        print(f"Ruta: {ruta}")
        print(f"Código: {codigo}")
        print(f"Tamaño: {tamaño} bytes")
        print("---")
```

### Limpieza y normalización de texto

```{code-cell} python
---
tags: hide-output
---
import re


def limpiar_texto(texto):
    """Limpia un texto para procesamiento"""
    # Eliminar URLs
    texto = re.sub(r"https?://\S+", "", texto)

    # Eliminar emails
    texto = re.sub(r"\S+@\S+", "", texto)

    # Eliminar múltiples espacios
    texto = re.sub(r"\s+", " ", texto)

    # Eliminar caracteres especiales (mantener letras, números y espacios)
    texto = re.sub(r"[^\w\s]", "", texto)

    return texto.strip()


texto_sucio = """
Visita https://ejemplo.com para más info!
Contacto: info@ejemplo.com
   Múltiples    espacios   aquí...
¿Caracteres especiales? @#$%
"""

print("Texto original:")
print(texto_sucio)
print("\nTexto limpio:")
print(limpiar_texto(texto_sucio))
```

### Tokenización de texto

```{code-cell} python
---
tags: hide-output
---
import re

def tokenizar(texto):
    """Divide un texto en palabras (tokens)"""
    # Encontrar todas las secuencias de caracteres de palabra
    tokens = re.findall(r"\b\w+\b", texto.lower())
    return tokens
```

```{code-cell} python
---
tags: hide-output
---
# Contar frecuencia de palabras
from collections import Counter

texto = "Python es un lenguaje de programación. ¡Es genial!"
tokens = tokenizar(texto)
print(f"Tokens: {tokens}")
print(f"Total de tokens: {len(tokens)}")

frecuencias = Counter(tokens)
print(f"Palabras más comunes: {frecuencias.most_common(3)}")
```

## Aplicaciones en procesamiento de texto

### Búsqueda de patrones en archivos

```{code-cell} python
---
tags: hide-output
---
import re

# Crear un archivo de ejemplo
contenido_archivo = """
Estructuras de datos
Python es un lenguaje de programación versátil
Expresiones regulares son herramientas poderosas
Python se usa en ciencia de datos
Las estructuras de datos son fundamentales
"""

with open("ejemplo.txt", "w") as f:
    f.write(contenido_archivo)


def buscar_en_archivo(archivo, patron):
    """Busca un patrón en un archivo y devuelve las líneas que coinciden"""
    resultados = []
    with open(archivo, "r") as f:
        for num_linea, linea in enumerate(f, 1):
            if re.search(patron, linea, re.IGNORECASE):
                resultados.append((num_linea, linea.strip()))
    return resultados


# Buscar líneas que contengan "Python" o "datos"
patron = r"Python|datos"
resultados = buscar_en_archivo("ejemplo.txt", patron)

print("Líneas encontradas:")
for num, linea in resultados:
    print(f"Línea {num}: {linea}")
```

### Extracción de datos estructurados

```{code-cell} python
---
tags: hide-output
---
import re

# HTML de ejemplo
html = """
<div class="producto">
    <h2>Laptop HP</h2>
    <p class="precio">$899.99</p>
    <p>Procesador Intel i7</p>
</div>
<div class="producto">
    <h2>Mouse Logitech</h2>
    <p class="precio">$25.50</p>
    <p>Inalámbrico</p>
</div>
"""


def extraer_productos(html):
    """Extrae información de productos del HTML"""
    # Patrón para encontrar bloques de productos
    patron_producto = (
        r'<div class="producto">.*?<h2>(.*?)</h2>.*?<p class="precio">\$([\d.]+)</p>'
    )

    productos = re.findall(patron_producto, html, re.DOTALL)

    return [{"nombre": nombre, "precio": float(precio)} for nombre, precio in productos]


productos = extraer_productos(html)
for i, prod in enumerate(productos, 1):
    print(f"Producto {i}: {prod['nombre']} - ${prod['precio']}")
```

### Reemplazo y transformación de texto

```{code-cell} python
---
tags: hide-output
---
import re


def anonimizar_datos(texto):
    """Anonimiza datos sensibles en un texto"""
    # Anonimizar emails
    texto = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", texto
    )

    # Anonimizar teléfonos (formato: xxx-xxxx o (xxx) xxx-xxxx)
    texto = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "[TELÉFONO]", texto)

    # Anonimizar números de tarjeta (grupos de 4 dígitos)
    texto = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[TARJETA]", texto)

    return texto


texto_sensible = """
Contacto: juan.perez@email.com
Teléfono: 555-1234 o (555) 555-5678
Tarjeta: 1234 5678 9012 3456
"""

print("Texto original:")
print(texto_sensible)
print("\nTexto anonimizado:")
print(anonimizar_datos(texto_sensible))
```

### Análisis de texto y extracción de métricas

```{code-cell} python
---
tags: hide-output
---
import re
from collections import Counter


def analizar_texto(texto):
    """Analiza un texto y extrae métricas"""
    # Contar oraciones (terminan en . ! ?)
    oraciones = re.split(r"[.!?]+", texto)
    num_oraciones = len([s for s in oraciones if s.strip()])

    # Contar palabras
    palabras = re.findall(r"\b\w+\b", texto.lower())
    num_palabras = len(palabras)

    # Palabras más comunes
    frecuencias = Counter(palabras)
    palabras_comunes = frecuencias.most_common(5)

    # Contar números
    numeros = re.findall(r"\b\d+\b", texto)

    # Detectar emails
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", texto)

    # Detectar URLs
    urls = re.findall(r"https?://[^\s]+", texto)

    return {
        "oraciones": num_oraciones,
        "palabras": num_palabras,
        "palabras_comunes": palabras_comunes,
        "numeros": numeros,
        "emails": emails,
        "urls": urls,
    }


texto_ejemplo = """
Python es un lenguaje de programación versátil.
Se utiliza en ciencia de datos, desarrollo web y automatización.
El curso tiene 50 estudiantes y 5 profesores!
Más información en https://ejemplo.com
Contacto: info@ejemplo.com
Python es muy popular. Python es fácil de aprender.
"""

metricas = analizar_texto(texto_ejemplo)
print("Análisis del texto:")
print(f"Oraciones: {metricas['oraciones']}")
print(f"Palabras: {metricas['palabras']}")
print(f"Palabras más comunes: {metricas['palabras_comunes']}")
print(f"Números encontrados: {metricas['numeros']}")
print(f"Emails encontrados: {metricas['emails']}")
print(f"URLs encontradas: {metricas['urls']}")
```

## Flags (modificadores)

Las expresiones regulares en Python admiten varios flags que modifican su comportamiento:

`re.IGNORECASE` o `re.I`
: Ignora mayúsculas/minúsculas

`re.MULTILINE` o `re.M`
: `^` y `$` coinciden con inicio/fin de cada línea

`re.DOTALL` o `re.S`
: `.` coincide con cualquier carácter, incluyendo saltos de línea

`re.VERBOSE` o `re.X`
: Permite escribir patrones más legibles con espacios y comentarios

```{code-cell} python
---
tags: hide-output
---
import re

# IGNORECASE
texto = "Python python PYTHON"
print(re.findall(r"python", texto, re.IGNORECASE))  # ['Python', 'python', 'PYTHON']

# MULTILINE
texto_multilinea = """Primera línea
Segunda línea
Tercera línea"""
print(re.findall(r"^.*línea", texto_multilinea, re.MULTILINE))

# VERBOSE: patrón más legible
patron_email = re.compile(
    r"""
    ^                      # Inicio de la cadena
    [a-zA-Z0-9._%+-]+      # Usuario
    @                      # @
    [a-zA-Z0-9.-]+         # Dominio
    \.                     # .
    [a-zA-Z]{2,}           # Extensión
    $                      # Fin de la cadena
    """,
    re.VERBOSE,
)

print(patron_email.match("usuario@ejemplo.com"))
```

## Ejercicios prácticos

### Ejercicio 1: Validador de contraseñas

```{code-cell} python
---
tags: hide-output
---
import re


def validar_contraseña(password):
    """
    Valida que una contraseña cumpla con:
    - Al menos 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un dígito
    - Al menos un carácter especial
    """
    if len(password) < 8:
        return False, "Debe tener al menos 8 caracteres"

    if not re.search(r"[A-Z]", password):
        return False, "Debe tener al menos una mayúscula"

    if not re.search(r"[a-z]", password):
        return False, "Debe tener al menos una minúscula"

    if not re.search(r"\d", password):
        return False, "Debe tener al menos un dígito"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Debe tener al menos un carácter especial"

    return True, "Contraseña válida"


# Pruebas
contraseñas = ["123456", "abcdefgh", "Abcdefgh", "Abcdefgh1", "Abcdefgh1!"]

for pwd in contraseñas:
    valida, mensaje = validar_contraseña(pwd)
    print(f"{pwd}: {mensaje}")
```

### Ejercicio 2: Extractor de información de texto

```{code-cell} python
---
tags: hide-output
---
import re


def extraer_informacion_contacto(texto):
    """Extrae emails, teléfonos y URLs de un texto"""

    # Patrón para emails
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", texto)

    # Patrón para teléfonos (varios formatos)
    telefonos = re.findall(
        r"\+?\d{1,3}?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}", texto
    )

    # Patrón para URLs
    urls = re.findall(r"https?://[^\s]+", texto)

    return {"emails": emails, "telefonos": telefonos, "urls": urls}


texto_contacto = """
Para más información:
- Email: contacto@empresa.com o soporte@empresa.com.ar
- Teléfono: +54 11 4567-8900 o 555-1234
- Web: https://www.empresa.com y https://soporte.empresa.com/ayuda
"""

info = extraer_informacion_contacto(texto_contacto)
print("Información extraída:")
print(f"Emails: {info['emails']}")
print(f"Teléfonos: {info['telefonos']}")
print(f"URLs: {info['urls']}")
```

### Ejercicio 3: Procesador de menciones y hashtags

```{code-cell} python
---
tags: hide-output
---
import re


def procesar_tweet(texto):
    """Extrae menciones y hashtags de un texto estilo Twitter"""

    # Menciones: @usuario
    menciones = re.findall(r"@(\w+)", texto)

    # Hashtags: #etiqueta
    hashtags = re.findall(r"#(\w+)", texto)

    # URLs
    urls = re.findall(r"https?://\S+", texto)

    # Texto limpio (sin menciones, hashtags ni URLs)
    texto_limpio = re.sub(r"@\w+|#\w+|https?://\S+", "", texto)
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()

    return {
        "menciones": menciones,
        "hashtags": hashtags,
        "urls": urls,
        "texto_limpio": texto_limpio,
    }


tweet = """
Gran clase de @profesorEDD sobre #ExpresionesRegulares!
#Python es genial para #DataScience
Más info: https://ejemplo.com/curso
cc: @estudiante1 @estudiante2
"""

resultado = procesar_tweet(tweet)
print("Análisis del tweet:")
print(f"Menciones: {resultado['menciones']}")
print(f"Hashtags: {resultado['hashtags']}")
print(f"URLs: {resultado['urls']}")
print(f"Texto limpio: {resultado['texto_limpio']}")
```

## Rendimiento y buenas prácticas

### Compilar patrones reutilizables

Cuando se usa un patrón múltiples veces, es más eficiente compilarlo:

```{code-cell} python
---
tags: hide-output
---
import re
import time

texto = "Python es genial. Python es versátil. Python es popular." * 1000

# Sin compilar
start = time.time()
for _ in range(100):
    re.findall(r"Python", texto)
tiempo_sin_compilar = time.time() - start

# Con compilación
patron = re.compile(r"Python")
start = time.time()
for _ in range(100):
    patron.findall(texto)
tiempo_con_compilar = time.time() - start

print(f"Sin compilar: {tiempo_sin_compilar:.4f} segundos")
print(f"Con compilar: {tiempo_con_compilar:.4f} segundos")
print(f"Mejora: {tiempo_sin_compilar / tiempo_con_compilar:.2f}x más rápido")
```

### Evitar backtracking excesivo

Algunas expresiones pueden causar backtracking excesivo y ser muy lentas:

```{code-cell} python
---
tags: hide-output
---
import re

# Patrón ineficiente con backtracking
# patron_malo = r"(a+)+"  # Puede ser muy lento

# Mejor: usar cuantificadores específicos
patron_bueno = r"a+"

texto = "a" * 20 + "b"
print(re.search(patron_bueno, texto))
```

### Usar raw strings

Siempre usar raw strings (`r"..."`) para evitar problemas con caracteres de escape:

```{code-cell} python
---
tags: hide-output
---
import re

# Sin raw string (necesita doble escape)
patron1 = "\\d+\\s+\\w+"

# Con raw string (más legible)
patron2 = r"\d+\s+\w+"

texto = "123 palabras"
print(re.search(patron1, texto).group())
print(re.search(patron2, texto).group())
```

## Integración con estructuras de datos

Las expresiones regulares se integran naturalmente con las estructuras de datos de Python:

### Índice invertido con regex

```{code-cell} python
---
tags: hide-output
---
import re
from collections import defaultdict


class IndiceInvertido:
    """Índice invertido que usa regex para procesar documentos"""

    def __init__(self):
        self.indice = defaultdict(set)

    def agregar_documento(self, doc_id, texto):
        """Agrega un documento al índice"""
        # Tokenizar usando regex
        palabras = re.findall(r"\b\w+\b", texto.lower())

        for palabra in palabras:
            self.indice[palabra].add(doc_id)

    def buscar(self, patron):
        """Busca documentos que contengan palabras que coincidan con el patrón"""
        patron_compilado = re.compile(patron, re.IGNORECASE)
        documentos = set()

        for palabra in self.indice.keys():
            if patron_compilado.search(palabra):
                documentos.update(self.indice[palabra])

        return documentos


# Crear índice
indice = IndiceInvertido()
indice.agregar_documento(1, "Python es un lenguaje de programación")
indice.agregar_documento(2, "Programar en Python es divertido")
indice.agregar_documento(3, "Java y JavaScript son diferentes")

# Buscar documentos que contengan palabras que empiecen con "prog"
docs = indice.buscar(r"^prog")
print(f"Documentos con palabras que empiezan con 'prog': {docs}")

# Buscar documentos con palabras que contengan "python"
docs = indice.buscar(r"python")
print(f"Documentos con 'python': {docs}")
```

### Filtrado de listas con regex

```{code-cell} python
---
tags: hide-output
---
import re

# Lista de archivos
archivos = [
    "documento1.txt",
    "imagen.png",
    "datos.csv",
    "reporte_2024.pdf",
    "script.py",
    "backup_2024_03_15.zip",
]


def filtrar_archivos(archivos, patron):
    """Filtra archivos que coincidan con el patrón"""
    patron_compilado = re.compile(patron)
    return [archivo for archivo in archivos if patron_compilado.search(archivo)]


# Filtrar archivos de texto
print("Archivos .txt:", filtrar_archivos(archivos, r"\.txt$"))

# Filtrar archivos de 2024
print("Archivos de 2024:", filtrar_archivos(archivos, r"2024"))

# Filtrar archivos Python
print("Archivos Python:", filtrar_archivos(archivos, r"\.py$"))
```

## Tablas de referencia rápida

[Descargar la versión imprimible](../_static/docs/referencias_regex.pdf)

### Caracteres

| Expresión | Significado                                                                  | Ejemplo        | Match               |
| :-------: | :--------------------------------------------------------------------------- | :------------- | :------------------ |
|   `\d`    | En la mayoría de los lenguajes un dígito 0..9                                | `file_\d\d`    | `file_25`           |
|           | En Python 3 y .Net un dígito Unicode                                         | `file_\d\d`    | `file_2੩`           |
|   `\w`    | En la mayoría de los lenguajes, un carácter de palabra: letra, dígito o '\_' | `\w-\w\w\w`    | `A-f_3`             |
|           | En Python 3, un símbolo Unicode de palabra, incluye '\_'                     | `\w-\w\w\w`    | `字-ま\_۳`          |
|           | En .NET, un símbolo Unicode de palabra, incluye conector '‿'                 | `\w-\w\w\w`    | `字-ま‿۳`           |
|   `\s`    | En la mayoría de los lenguajes caracteres de blanco estándar                 | `a\sb\sc`      | `a b c`             |
|           | En la .NET, Python 3, Javascript, caracteres de blanco Unicode               | `a\sb\sc`      | `a b c`             |
|   `\D`    | Un caracter que no es un dígito `\d` del lenguaje                            | `\D\D\D`       | `ABC`               |
|   `\W`    | Un caracter que no es un caracter de palabra `\w` del lenguaje               | `\W\W\W\W`     | `\*+=)`             |
|   `\S`    | Un caracter que no es un blanco estandar `\s` del lenguaje                   | `\S\S\S\S`     | `casa`              |
|    `.`    | Cualquier caracter, excepto saltos de líneas                                 | `a.c`          | `abc`               |
|           |                                                                              | `.*`           | `piso 2, depto "A"` |
|   `\.`    | Un punto                                                                     | `\w\.\d`       | `a.3`               |
|    `\`    | Escape de caracteres especiales                                              | `\*\?\$\^`     | `*?\$^`             |
|           |                                                                              | `\[\{\(\)\}\]` | `[{()}]`            |

### Cuantificadores

| Expresión | Significado                    | Ejemplo   | Match      |
| :-------: | :----------------------------- | :-------- | :--------- |
|    `+`    | Una o más apariciones          | `\w-\w+`  | `C-125x_1` |
|   `{3}`   | Exactamente tres apariciones   | `\D{3}`   | `ANA`      |
|  `{2,4}`  | Entre dos y cuatro apariciones | `\W{2,4}` | `{+}`      |
|    `*`    | Cero o más aparaciones         | `A*B*C*`  | `AAAACCCC` |
|    `?`    | Cero o una aparición           | `casas?`  | `casa`     |

### Lógica

| Expresión | Significado                                                       | Ejemplo             | Match                       |
| :-------: | :---------------------------------------------------------------- | :------------------ | :-------------------------- |
|   `\|`    | _Or_                                                              | `22\|33`            | `22`                        |
|  `(...)`  | Captura un grupo y lo asocia a una variable numerada              | `UN(O\|TREF)`       | `UNTREF` (y captura `TREF`) |
|   `\1`    | Lo capturado en el grupo 1                                        | `r(\w)g\1\x`        | `regex`                     |
|   `\2`    | Lo capturado en el grupo 2                                        | `(\d+)+(\d+)=\2+\1` | `25+33=33+25`               |
|  `(?:…)`  | Grupo que no se captura (se verifica la regex pero no se captura) | `A(?:na\|licia)`    | `Alicia`                    |

### Clases de caracteres

| Expresión | Significado                                                                                    | Ejemplo          | Match                               |
| :-------: | :--------------------------------------------------------------------------------------------- | :--------------- | :---------------------------------- |
|  `[...]`  | Uno de los caracteres entre corchetes                                                          | `[AEIOU]`        | `A`                                 |
|    `-`    | Indicador de rango                                                                             | `[a-z]`          | Una letra minúscula                 |
|           |                                                                                                | `[A-Z]+`         | Una o más letras mayúsculas         |
|           |                                                                                                | `[AB1-5w-z]`     | Uno de los caracteres `AB12345wxyz` |
|  `[^x]`   | Cualquier caracter distinto de `x`                                                             | `A[^a]B`         | `AxB`                               |
| `[^x-y]`  | Cualquier caracter fuera del rango `x-y`                                                       | `[^a-z]{3}`      | `A1!`                               |
| `[\xhh]`  | El caracter con código hh en hexadecimal de la tabla de símbolos [ASCII](https://ascii.cl/es/) | `[\x41-\x45]{3}` | `ABE`                               |

### Posiciones: fronteras y anclas

| Expresión | Significado                                                                                                                            | Ejemplo          | Match                            |
| :-------: | :------------------------------------------------------------------------------------------------------------------------------------- | :--------------- | :------------------------------- |
|    `^`    | Indicador de comienzo de cadena (o comienzo de línea). Tiene que estar fuera de `[` `]` (ya que adentro de `[` `]` significa negación) | `^abc.*`         | Texto que empieza con `abc`      |
|    `$`    | Fin de cadena o fin de línea                                                                                                           | `.*el final\.$`  | Texto que termina en `el final.` |
|   `\b`    | Frontera de la palabra                                                                                                                 | `Bibi.*\bes\b.*` | `Bibi es mi amiga`               |
|   `\B`    | No es frontera de palabra                                                                                                              | `Bibi.*\Bes\B.*` | `Bibi usa un vestido`            |

### Miradas alrededor (_look behind_ y _look ahead_)

No consumen caracteres, se quedan paradas donde ocurrió el matching

| Expresión | Significado                                 | Ejemplo           | Match                                                                                                          |
| :-------: | :------------------------------------------ | :---------------- | :------------------------------------------------------------------------------------------------------------- |
|  `(?=…)`  | Mirar hacia adelante con parámetro positivo | `(?=\d{10})\d{5}` | Si hacia adelante hay 10 dígitos matchear los primeros 5                                                       |
| `(?<=…)`  | Mirar hacia atrás con parámetro positivo    | `(?<=foo).*`      | Si lo que está justo detrás de la posición actual es la cadena `foo`. El matching es todo lo que sigue a `foo` |
|  `(?!…)`  | Mirar hacia adelante con parámetro negativo | `q(?!ue)`         | matchea una `q` no este seguida de `ue`                                                                        |
|           |                                             | `(?!teatro)te\w+` | cualquier palabra que empiece con `te` pero no sea `teatro`                                                    |
| `(?<!…)`  | Mirar hacia atrás con parámetro negativo    | `(?<!fut)bol`     | `bol` siempre y cuando no esté precedida por `fut`                                                             |

## Recursos adicionales

Para profundizar en expresiones regulares:

- [Documentación oficial de `re` en Python](https://docs.python.org/es/3/library/re.html)
- [Regular Expression HOWTO](https://docs.python.org/es/3/howto/regex.html)
- [Regex101](https://regex101.com/) - Herramienta online para probar regex
- [RegExr](https://regexr.com/) - Otra herramienta interactiva
- [Python Regular Expressions (Real Python)](https://realpython.com/regex-python/)

```{admonition} Resumen
Las expresiones regulares son una herramienta poderosa para:
- Validar formatos de datos
- Extraer información de textos no estructurados
- Limpiar y normalizar datos
- Procesar logs y archivos de texto
- Implementar búsquedas avanzadas en sistemas de recuperación de información

El dominio de las expresiones regulares es esencial para trabajar con grandes volúmenes de texto y construir sistemas eficientes de procesamiento de información.
```
