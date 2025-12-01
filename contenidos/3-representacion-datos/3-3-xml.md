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
description: XML y XPath
---

# EXtensible Markup Language (XML)

## XML

**XML** (_eXtensible Markup Language_) es un lenguaje de marcado que define un conjunto de reglas para la codificación de documentos en un formato que es tanto legible por humanos como por máquinas. Fue diseñado para almacenar y transportar datos, y es ampliamente utilizado en aplicaciones web, servicios web y sistemas de intercambio de datos.

XML permite a los usuarios definir sus propias etiquetas y estructuras de datos, lo que lo hace muy flexible y adaptable a diferentes necesidades. A diferencia de HTML, que tiene un conjunto fijo de etiquetas predefinidas, XML permite crear etiquetas personalizadas que describen el contenido de manera más precisa.

XML es un estándar abierto mantenido por el [World Wide Web Consortium (W3C)](https://www.w3.org/XML/) y es ampliamente utilizado en diversas aplicaciones, incluyendo:

- Intercambio de datos entre sistemas diferentes.
- Configuración de aplicaciones.
- Almacenamiento de datos estructurados.
- Representación de documentos complejos (como docx, xlsx, etc.)
- Difusión de Noticias (RSS, Atom).

### Estructura de un documento XML

Un documento XML está compuesto por varios elementos clave:

Prólogo
: Es la parte inicial del documento que puede incluir una declaración XML y otras instrucciones, como la definición de la codificación de caracteres. La declaración XML es opcional pero recomendada, y suele verse así: `<?xml version="1.0" encoding="UTF-8"?>`.

Elementos
: Son las unidades básicas de un documento XML y están delimitados por etiquetas de apertura y cierre. Por ejemplo, `<nombre>Juan</nombre>` es un elemento que contiene el texto "Juan".

Atributos
: Son pares clave-valor que proporcionan información adicional sobre un elemento. Se incluyen dentro de la etiqueta de apertura. Por ejemplo, `<persona id="123">` tiene un atributo `id` con el valor "123".

Contenido
: Es el texto o los datos que se encuentran entre las etiquetas de apertura y cierre de un elemento.

Comentarios
: Se pueden incluir comentarios en un documento XML utilizando la sintaxis `<!-- Comentario -->`.

El siguiente fragmento muestra un poema estructurado en XML

```{literalinclude} ../_static/code/xml/poema.xml
---
language: xml
---
```

donde se pueden distinguir claramente los diferentes elementos:

- `poema`
- `titulo`
- `verso`

y los atributos de poema

- `@fecha`
- `@lugar`

Como se puede observar XML permite estructurar la información en forma jerárquica, como si fuera un árbol, donde los elementos pueden contener otros elementos anidados. Un archivo XML bien formado debe cumplir con ciertas reglas, como tener un único elemento raíz que contenga todos los demás elementos, y todas las etiquetas deben estar correctamente cerradas y anidadas.

Los atributos en XML permiten agregar metadatos o información adicional a los elementos, lo que puede ser útil para describir propiedades o características específicas de los datos. Sin embargo, es importante usarlos con moderación y de manera coherente para evitar complicaciones en la interpretación del documento.

```{figure} ../_static/figures/poema_xml_light.svg
---
class: only-light-mode
---
Árbol que representa la estructura del poema en XML.
```

```{figure} ../_static/figures/poema_xml_dark.svg
---
class: only-dark-mode
---
Árbol que representa la estructura del poema en XML.
```

Existen varios sitios en internet que permiten visualizar el árbol asociado. Por ejemplo [https://codebeautify.org/xmlviewer](https://codebeautify.org/xmlviewer?input=%3Cpoema%20fecha=%22Abril%20de%201915%22%20lugar=%22Granada%22%3E%3Ctitulo%3EAlba%3C/titulo%3E%3Cverso%3EMi%20coraz%C3%B3n%20oprimido%3C/verso%3E%3Cverso%3Esiente%20junto%20a%20la%20alborada%3C/verso%3E%3Cverso%3Eel%20dolor%20de%20sus%20amores%3C/verso%3E%3Cverso%3Ey%20el%20sue%C3%B1o%20de%20las%20distancias.%20%3C/verso%3E%3C/poema%3E).

En el ejemplo anterior, el elemento raíz es `poema`, que contiene como elementos hijos: `titulo` y varios elementos `verso`. El elemento `poema` también tiene dos atributos: `fecha` y `lugar`, que proporcionan información adicional sobre el poema.

Que un documento XML se pueda representar como un árbol simplifica la consulta y manipulación de los datos, ya que se pueden utilizar técnicas de recorrido de árboles para acceder a elementos específicos o extraer información relevante.

## XPath: XML Path Language

**XPath** (_XML Path Language_) es un lenguaje de consulta utilizado para navegar y seleccionar nodos en documentos XML. Proporciona una sintaxis para definir rutas que permiten localizar elementos, atributos y otros nodos dentro de la estructura jerárquica de un documento XML.

Permite describir caminos a través del árbol XML utilizando una notación similar a la de los sistemas de archivos. Por ejemplo, la expresión `/poema/titulo` selecciona el elemento `titulo` que es hijo directo del elemento raíz `poema`. Evaluar una expresión XPath es buscar **elementos** o **atributos** en un documento XML que coincidan con los criterios especificados en la expresión. El resultado son todos los nodos que cumplen con esos criterios.

Por ejemplo, la expresión `//verso` selecciona todos los elementos `verso` en el documento, independientemente de su posición en la jerarquía. La expresión `//verso[text()="Mi corazón oprimido"]` selecciona el elemento `verso` que contiene el texto exacto "Mi corazón oprimido".

En los ejemplos a continuación usaremos el siguiente documento XML que representa una biblioteca con varios libros y autores.

```{literalinclude} ../_static/code/xml/biblioteca.xml
---
language: xml
---
```

### Expresiones XPath para seleccionar nodos

| Expresión          | Descripción                                                                                |
| :----------------- | :----------------------------------------------------------------------------------------- |
| `/`                | Si está al principio de la expresión, indica el nodo raíz, si no, indica "hijo"            |
| `//`               | Camino. Permite seleccionar nodos en un camino descendiente a partir de la posición actual |
| `.`                | Nodo actual                                                                                |
| `..`               | Padre del nodo actual                                                                      |
| `@nombre_atributo` | Atributo                                                                                   |

Cada consulta XPath devuelve un conjunto de nodos que cumplen con los criterios especificados en la expresión. Se recomienda realizar pruebas en [XPath Tester](https://codebeautify.org/Xpath-Tester?input=%3Cbiblioteca%3E%0A%20%20%3Clibro%3E%0A%20%20%20%20%3Ctitulo%3ELa%20vida%20est%C3%A1%20en%20otra%20parte%3C/titulo%3E%0A%20%20%20%20%3Cautor%3EMilan%20Kundera%3C/autor%3E%0A%20%20%20%20%3CfechaPublicacion%20a%C3%B1o%3D%221973%22%20/%3E%0A%20%20%20%20%3Cprecio%3E305.50%3C/precio%3E%0A%20%20%3C/libro%3E%0A%20%20%3Crevista%3E%0A%20%20%20%20%3Ctitulo%3EComputer%20Gaming%20World%3C/titulo%3E%0A%20%20%20%20%3Ceditorial%3EGolden%20Empire%20Publications%3C/editorial%3E%0A%20%20%20%20%3CfechaPublicacion%20a%C3%B1o%3D%221981%22%20/%3E%0A%20%20%20%20%3Cprecio%3E669.99%3C/precio%3E%0A%20%20%3C/revista%3E%0A%20%20%3Clibro%3E%0A%20%20%20%20%3Ctitulo%3EPantale%C3%B3n%20y%20las%20visitadoras%3C/titulo%3E%0A%20%20%20%20%3Cautor%20fechaNacimiento%3D%2228/03/1936%22%3EMario%20Vargas%20Llosa%3C/autor%3E%0A%20%20%20%20%3CfechaPublicacion%20a%C3%B1o%3D%221973%22%20/%3E%0A%20%20%20%20%3Cprecio%3E214.48%3C/precio%3E%0A%20%20%3C/libro%3E%0A%20%20%3Clibro%3E%0A%20%20%20%20%3Ctitulo%3EConversaci%C3%B3n%20en%20la%20catedral%3C/titulo%3E%0A%20%20%20%20%3Cautor%20fechaNacimiento%3D%2228/03/1936%22%3EMario%20Vargas%20Llosa%3C/autor%3E%0A%20%20%20%20%3CfechaPublicacion%20a%C3%B1o%3D%221969%22%20/%3E%0A%20%20%20%20%3Cprecio%3E541.78%3C/precio%3E%0A%20%20%3C/libro%3E%0A%20%20%3Crevista%3E%0A%20%20%20%20%3Ctitulo%3EPC%20Users%3C/titulo%3E%0A%20%20%20%20%3Ceditorial%3ERedUsers%3C/editorial%3E%0A%20%20%20%20%3CfechaPublicacion%20a%C3%B1o%3D%222000%22%20/%3E%0A%20%20%20%20%3Cprecio%3E220.50%3C/precio%3E%0A%20%20%3C/revista%3E%0A%3C/biblioteca%3E).

`/biblioteca`
: Selecciona el nodo raíz `biblioteca`.

`/biblioteca/libro`
: Selecciona todos los nodos `libro` que son hijos directos de `biblioteca`.

`//autor`
: Selecciona todos los nodos `autor` en el documento, independientemente de su posición en la jerarquía.

`/biblioteca//titulo`
: Selecciona todos los nodos `titulo` que son descendientes de `biblioteca`, sin importar cuántos niveles haya entre ellos. En este caso, selecciona los títulos de libros y revistas.

`//libro/precio`
: Selecciona todos los nodos `precio` que son hijos directos de cualquier nodo `libro`.

`//editorial/..`
: Selecciona el nodo padre de todos los nodos `editorial`, que en este caso son nodos `revista`.

`//autor[@fechaNacimiento]`
: Selecciona todos los nodos `autor` que tengan un atributo `fechaNacimiento`.

### Predicados

Los predicados pueden ser usados para filtrar un conjunto de nodos en base a una condición dada.

Los predicados se escriben entre corchetes (`[`, `]`).
`/biblioteca/libro[position() = 1]`
: Selecciona el primer nodo `libro` hijo de `biblioteca`.

`/biblioteca/libro[1]`
: Equivalente a la expresión anterior, selecciona el primer nodo `libro` hijo de `biblioteca`.

`/biblioteca/libro[last()]`
: Selecciona el último nodo `libro` hijo de `biblioteca`.

`/biblioteca/libro[last() - 1]`
: Selecciona el penúltimo nodo `libro` hijo de `biblioteca`.

`/biblioteca/libro[position() < 3]`
: Selecciona los dos primeros nodos `libro` hijos de `biblioteca`.

`//autor[not(@fechaNacimiento)]`
: Selecciona todos los nodos `autor` que **no** tengan un atributo `fechaNacimiento`.

`//autor[@fechaNacimiento="28/03/1936"]`
: Selecciona todos los nodos `autor` cuyo atributo `fechaNacimiento` tenga el valor "28/03/1936".

### Selectores y comodines

| Expresión | Resultado                              |
| :-------- | :------------------------------------- |
| `*`       | Todos los elementos en el nivel actual |
| `@*`      | Todos los atributos del nodo actual    |
| `text()`  | El contenido de texto de un nodo       |

`/biblioteca/*`
: Selecciona todos los elementos hijos directos de biblioteca.

`/biblioteca//*`
: Selecciona todos los elementos descendientes de biblioteca.

`//autor[@*]`
: Selecciona todos los elementos autor que tengan algún atributo.

`node()`
: Selecciona todos los nodos del documento.

`//titulo/text()`
: Selecciona el texto (no el nodo completo) de los títulos.

### Selección de varios caminos

El operador `|` es el operador de unión permite seleccionar distintos caminos en el documento.

`//libro/titulo | //libro/precio`
: Selecciona todos los nodos titulo y todos los nodos precio hijos de libro |

### Comparaciones

| Operador | Descripción    | Ejemplo            |
| :------- | :------------- | :----------------- |
| `=`      | Igualdad       | `precio = 541.78`  |
| `!=`     | Distinto       | `precio != 541.78` |
| `<`      | Menor estricto | `precio < 500`     |
| `<=`     | Menor o igual  | `precio <= 541.78` |
| `>`      | Mayor estricto | `precio > 500`     |
| `>=`     | Mayor o igual  | `precio >= 541.78` |

`/biblioteca//libro[precio < 350]`
: Selecciona todos los nodos `libro` que tengan como hijo directo un elemento `precio` con valor menor a 350.

`/biblioteca//libro[precio < 350]/titulo`
: Selecciona todos los nodos `titulo` hijos de nodos `libro` que tengan como hijo directo un elemento `precio` con valor menor a 350.

### Operadores

| Operador | Descripción                          | Ejemplo                              |
| :------- | :----------------------------------- | :----------------------------------- |
| `+`      | Suma                                 | `6 + 4`                              |
| `-`      | Sustracción                          | `6 - 4`                              |
| `*`      | Multiplicación                       | `6 * 4`                              |
| `div`    | División                             | `8 div 4`                            |
| `or`     | Disyunción                           | `precio = 541.78 or precio = 214.48` |
| `and`    | Conjunción                           | `precio > 300 and precio <= 541.78`  |
| `mod`    | Módulo (resto de la división entera) | `5 mod 2`                            |

`/biblioteca//libro[precio > 300 and precio <= 541.78]`
: Selecciona todos los nodos `libro` que tengan como hijo directo un elemento `precio` con valor mayor a 300 y menor o igual a 541.78.

`/biblioteca//libro[precio = 541.78 or precio = 214.48]`
: Selecciona todos los nodos `libro` que tengan como hijo directo un elemento `precio` con valor igual a 541.78 o 214.48.

`/biblioteca//libro[precio + 100 > 600]`
: Selecciona los nodos `libro` donde el valor del elemento `precio` sumado a 100 es mayor que 600.

## Características de XPath 2.0

XPath 2.0 introduce mejoras significativas sobre la versión 1.0, incluyendo un sistema de tipos más rico, soporte para secuencias, expresiones condicionales y cuantificadores, así como una amplia biblioteca de funciones.

```{note} Nota
Para utilizar estas características en Python, es necesario usar bibliotecas que soporten XPath 2.0, como `elementpath`. La biblioteca estándar `xml.etree.ElementTree` solo soporta un subconjunto de XPath 1.0.
```

### Funciones integradas

XPath 2.0 ofrece una gran cantidad de funciones para manipular cadenas, números, fechas y secuencias.

| Función | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `count(nodos)` | Cuenta el número de nodos en una secuencia | `count(//libro)` |
| `sum(nodos)` | Suma los valores numéricos de los nodos | `sum(//precio)` |
| `avg(nodos)` | Calcula el promedio de los valores | `avg(//precio)` |
| `min(nodos)` | Devuelve el valor mínimo | `min(//precio)` |
| `max(nodos)` | Devuelve el valor máximo | `max(//precio)` |
| `contains(s1, s2)` | Verdadero si s1 contiene s2 | `contains(titulo, 'XML')` |
| `starts-with(s1, s2)` | Verdadero si s1 empieza con s2 | `starts-with(titulo, 'A')` |
| `ends-with(s1, s2)` | Verdadero si s1 termina con s2 | `ends-with(titulo, '.')` |
| `upper-case(s)` | Convierte la cadena a mayúsculas | `upper-case('hola')` |
| `string-length(s)` | Devuelve la longitud de la cadena | `string-length('abc')` |
| `matches(s, regex)` | Verdadero si la cadena cumple con la expresión regular | `matches('123', '^\d+$')` |

### Secuencias

En XPath 2.0, todo es una secuencia. Un valor simple es una secuencia de un solo elemento. Las secuencias se pueden construir con paréntesis y comas.

- `(1, 2, 3)`: Una secuencia de tres enteros.
- `(1 to 5)`: Genera la secuencia `(1, 2, 3, 4, 5)`.
- `//libro/titulo`: Devuelve una secuencia con todos los nodos título.

### Expresiones condicionales (`if-then-else`)

Permiten evaluar condiciones y devolver diferentes resultados.

```xpath
if (@precio > 500) then 'Caro' else 'Barato'
```

### Cuantificadores (`some` y `every`)

Permiten verificar si alguno o todos los elementos de una secuencia cumplen una condición.

- **some**: Verdadero si al menos un elemento cumple la condición.
  ```xpath
  some $x in //precio satisfies $x > 1000
  ```

- **every**: Verdadero si todos los elementos cumplen la condición.
  ```xpath
  every $x in //precio satisfies $x > 0
  ```

### Tablas de referencia rápida

Descargar la [Hoja de Referencia de XPath 2.0](../_static/docs/referencias_xpath.pdf) en PDF.


## XML y Python

Python ofrece varias bibliotecas para trabajar con XML, siendo las más comunes `xml.etree.ElementTree` (nativa), `lxml` y `xml.dom.minidom`.

Si bien `xml.etree.ElementTree` es parte de la biblioteca estándar, su soporte para XPath es limitado (solo soporta XPath 1.0 simplificado). Para utilizar todas las capacidades de XPath 2.0 (incluyendo funciones), utilizaremos la biblioteca `elementpath` en conjunto con `xml.etree.ElementTree`.

[`elementpath`](https://elementpath.readthedocs.io/en/latest/) es una biblioteca de Python que implementa completamente el estándar XPath 2.0 (y versiones posteriores) para la navegación y consulta de documentos XML. Complementa a `xml.etree.ElementTree` al permitir el uso de expresiones XPath más complejas y potentes que las que soporta la implementación nativa de Python.

Para instalar `elementpath`, se puede usar pip:

```bash
pip install elementpath
```

```{code-cell} python
---
tags: hide-output
---
from xml.etree import ElementTree
import elementpath

# Cargar el documento XML
tree = ElementTree.parse("../_static/code/xml/biblioteca.xml")
root = tree.getroot()

# Realizar una consulta XPath
# Seleccionar todos los títulos de libros
titulos = elementpath.select(root, "/biblioteca/libro/titulo/text()")
print("Títulos de libros:")
for titulo in titulos:
    print(titulo)

# Seleccionar todos los autores con fecha de nacimiento
autores_con_fecha = elementpath.select(
    root, "//autor[@fechaNacimiento]/text()")
print("\nAutores con fecha de nacimiento:")
for autor in autores_con_fecha:
    print(autor)

# Seleccionar libros con precio menor a 300
libros_baratos = elementpath.select(
    root, "/biblioteca/libro[precio < 300]/titulo/text()")
print("\nLibros con precio menor a 300:")
for libro in libros_baratos:
    print(libro)
```

Otro ejemplo: Calcular el precio total de los libros

```{code-cell} python
---
tags: hide-output
---

# Calcular el precio total de todos los libros usando la función sum
# de XPath 2.0
total_precio = elementpath.select(root, "sum(/biblioteca/libro/precio)")

print(f"\nPrecio total de todos los libros: {total_precio:.2f}")
```

### Ejemplos avanzados con XPath 2.0

A continuación, veremos cómo utilizar funciones avanzadas, cuantificadores y expresiones condicionales con `elementpath`.

```{code-cell} python
---
tags: hide-output
---
# Funciones de cadena: starts-with
# Seleccionar libros cuyo título comienza con "La"
libros_la = elementpath.select(
    root, "/biblioteca/libro[starts-with(titulo, 'La')]/titulo/text()"
)
print("Libros que empiezan con 'La':")
for libro in libros_la:
    print(f"- {libro}")

print("\n---")

# Cuantificadores: some
# Verificar si hay algún libro con precio mayor a 500
hay_caros = elementpath.select(root, "some $x in //precio satisfies $x > 500")
print(f"¿Hay libros caros (>500)? {hay_caros}")

# Cuantificadores: every
# Verificar si todos los precios son positivos
todos_positivos = elementpath.select(root, "every $x in //precio satisfies $x > 0")
print(f"¿Todos los precios son positivos? {todos_positivos}")

print("\n---")

# Expresiones condicionales: if-then-else
# Categorizar libros según su precio
categorias = elementpath.select(root,
    "for $libro in /biblioteca/libro return "
    "concat($libro/titulo, ': ', "
    "if ($libro/precio > 500) then 'Caro' else 'Barato')"
)
print("Categorización de libros:")
for cat in categorias:
    print(f"- {cat}")
```

### Sindicación de Contenidos: RSS y Atom

La sindicación de contenidos es una forma de distribuir información actualizada de sitios web a usuarios que se han suscrito a ellos. Los dos formatos más populares para esto son **RSS** y **Atom**, ambos basados en XML.

```{note} Sindicación de contenidos
La sindicación de contenidos es el proceso mediante el cual el contenido de un sitio web se pone a disposición de otros sitios o usuarios de forma automatizada.
```

#### RSS (Really Simple Syndication)

RSS es una familia de formatos de fuentes web estandarizados que se utilizan para publicar trabajos actualizados con frecuencia, como entradas de blogs, titulares de noticias, audio y vídeo. El formato RSS permite a los editores sindicar datos de forma automática. La versión actual es RSS 2.0.

#### Atom

Atom es un estándar más reciente, desarrollado como una alternativa a RSS para solucionar algunas de sus ambigüedades y limitaciones. Fue estandarizado por el IETF ([RFC 4287](https://datatracker.ietf.org/doc/html/rfc4287)). Atom suele ser más robusto y consistente en su estructura.

#### Comparación: RSS vs Atom

| Característica | RSS 2.0 | Atom 1.0 |
| :--- | :--- | :--- |
| **Estandarización** | No estandarizado formalmente (mantenido por Harvard) | Estándar IETF (RFC 4287) |
| **Fecha de publicación** | Elemento `<pubDate>` (formato RFC 822) | Elemento `<updated>` (formato ISO 8601) |
| **Contenido** | Solo soporta texto plano o HTML escapado | Soporta texto, HTML, XHTML y contenido binario (Base64) |
| **Identificación** | `<guid>` (opcional) | `<id>` (obligatorio y único) |
| **Autor** | `<author>` (email del autor) | `<author>` (estructura con nombre, email, uri) |

#### Lectura de Feeds con Python

La biblioteca `feedparser` es la herramienta estándar en Python para analizar tanto feeds RSS como Atom de manera transparente.

Para instalar `feedparser`:

```bash
pip install feedparser
```

##### Ejemplo 1: Leyendo noticias (RSS)

```{code-cell} python
---
tags: hide-output
---
import feedparser

# URL del feed RSS de Clarin
rss_url = "https://www.clarin.com/rss/lo-ultimo/"

# Parsear el feed
feed = feedparser.parse(rss_url)

print(f"Fuente: {feed.feed.title}")
print("Últimas noticias:\n")

for entry in feed.entries[:3]:
    print(f"Título: {entry.title}")
    print(f"Link: {entry.link}")
    print("---")
```

##### Ejemplo 2: Leyendo Gmail (Atom)

Gmail proporciona un feed Atom de los correos no leídos. Dado que requiere autenticación, este ejemplo muestra cómo se estructuraría la petición (nota: por seguridad, Gmail requiere contraseñas de aplicación si tienes 2FA activado).

```{code-block}python

import feedparser

# Reemplazar con tus credenciales (usar contraseña de aplicación)
username = "tu_usuario@gmail.com"
password = "tu_contraseña_de_aplicacion"

# URL del feed Atom de Gmail
gmail_url = f"https://{username}:{password}@mail.google.com/mail/feed/atom"

# Parsear el feed
feed = feedparser.parse(gmail_url)

print(f"Correos no leídos en: {feed.feed.title}")
print(f"Cantidad: {feed.feed.fullcount}\n")

for entry in feed.entries[:3]:
    print(f"De: {entry.author}")
    print(f"Asunto: {entry.title}")
    print(f"Resumen: {entry.summary}")
    print("---")
```
