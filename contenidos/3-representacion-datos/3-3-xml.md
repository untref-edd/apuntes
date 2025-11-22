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
:class: only-light-mode
Árbol que representa la estructura del poema en XML.
```

```{figure} ../_static/figures/poema_xml_dark.svg
:class: only-dark-mode
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

## XML y Python

Python ofrece varias bibliotecas para trabajar con XML, siendo las más comunes `xml.etree.ElementTree`, `lxml` y `xml.dom.minidom`. En los ejemplos usaremos `lxml` que es muy potente y flexible.

Para instalar `lxml`, se puede usar pip:

```bash
pip install lxml
```

```{code-cell} python
---
tags: hide-output
---
from lxml import etree

# Cargar el documento XML
tree = etree.parse("../_static/code/xml/biblioteca.xml")
root = tree.getroot()

# Realizar una consulta XPath
# Seleccionar todos los títulos de libros
titulos = root.xpath("/biblioteca/libro/titulo/text()")
print("Títulos de libros:")
for titulo in titulos:
    print(titulo)

# Seleccionar todos los autores con fecha de nacimiento
autores_con_fecha = root.xpath("//autor[@fechaNacimiento]/text()")
print("\nAutores con fecha de nacimiento:")
for autor in autores_con_fecha:
    print(autor)

# Seleccionar libros con precio menor a 300
libros_baratos = root.xpath("/biblioteca/libro[precio < 300]/titulo/text()")
print("\nLibros con precio menor a 300:")
for libro in libros_baratos:
    print(libro)
```

Otro ejemplo: Calcular el precio total de los libros

```{code-cell} python
---
tags: hide-output
---
from lxml import etree

# Cargar el documento XML
tree = etree.parse("../_static/code/xml/biblioteca.xml")
root = tree.getroot()

# Calcular el precio total de todos los libros
precios = root.xpath("/biblioteca/libro/precio/text()")
total_precio = sum(float(precio) for precio in precios)

print(f"\nPrecio total de todos los libros: {total_precio:.2f}")
```

### Noticias con RSS y Atom

**RSS** (Really Simple Syndication o Rich Site Summary) es un formato basado en XML que se utiliza para distribuir y compartir contenido web, como noticias, blogs, podcasts y otros tipos de información actualizada regularmente. Los archivos RSS permiten a los usuarios suscribirse a fuentes de contenido y recibir actualizaciones automáticas cuando se publica nuevo contenido. A continuación se muestra un ejemplo de lectura del feed RSS con las últimas noticias del diario Clarin:

```{code-cell} python
---
tags: hide-output
---
import feedparser

# URL del feed RSS de Clarin
rss_url = "https://www.clarin.com/rss/lo-ultimo/"

# Parsear el feed RSS
feed = feedparser.parse(rss_url)

# Mostrar los títulos y enlaces de las últimas noticias
print("Últimas noticias de Clarin:\n")
for entry in feed.entries[:5]:  # Mostrar solo las primeras 5 noticias
    print(f"Título: {entry.title}")
    print(f"Fecha de publicación: {entry.published}")
    print(f"Enlace: {entry.link}\n")
```
