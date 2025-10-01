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

# EXtensible Markup Language (XML)

## Introducción

La **recuperación de la información** es una disciplina que estudia cómo obtener información relevante a partir de grandes volúmenes de datos.Esta área se centra en el diseño de sistemas que permitan a los usuarios encontrar documentos o fragmentos de información que satisfagan una necesidad informativa específica.

La información puede presentarse en diferentes formas:

Información estructurada
: Datos organizados en un formato predefinido, como bases de datos relacionales, donde los datos se almacenan en tablas con filas y columnas claramente definidas. La consulta y recuperación en este contexto suele realizarse mediante lenguajes como SQL. Los registros y campos que vimos anteriormente son ejemplos de información estructurada. 

Información semi estructurada
: Datos que no siguen un esquema rígido, pero contienen etiquetas o marcadores que facilitan su organización y búsqueda. Ejemplos comunes incluyen documentos HTML o XML, donde la estructura es flexible pero existen elementos identificables.

Información no estructurada
: Consiste principalmente en texto libre, como artículos, correos electrónicos o páginas web, donde la organización interna es mínima o inexistente. La recuperación en este caso requiere técnicas especializadas de procesamiento de lenguaje natural y modelado de relevancia.

El objetivo principal de la recuperación de la información es diseñar sistemas capaces de localizar, filtrar y presentar datos relevantes a partir de consultas realizadas por los usuarios, considerando la naturaleza y estructura de la información disponible. Para lograrlo, se emplean distintos modelos y algoritmos que evalúan la relevancia de los documentos en función de la consulta.

Además, el proceso de recuperación de la información implica tareas como el preprocesamiento de texto (tokenización, eliminación de palabras vacías, lematización), la indexación eficiente de grandes volúmenes de datos y la evaluación de la calidad de los resultados mediante métricas como la precisión y la exhaustividad. Estos conceptos forman la base de los motores de búsqueda modernos y sistemas de recomendación de información.

## XML

**XML** (eXtensible Markup Language) es un lenguaje de marcado que define un conjunto de reglas para la codificación de documentos en un formato que es tanto legible por humanos como por máquinas. Fue diseñado para almacenar y transportar datos, y es ampliamente utilizado en aplicaciones web, servicios web y sistemas de intercambio de datos.

XML permite a los usuarios definir sus propias etiquetas y estructuras de datos, lo que lo hace muy flexible y adaptable a diferentes necesidades. A diferencia de HTML, que tiene un conjunto fijo de etiquetas predefinidas, XML permite crear etiquetas personalizadas que describen el contenido de manera más precisa.

Se puede decir que HTML es un subconjunto de XML, ya que HTML utiliza etiquetas predefinidas para estructurar el contenido de una página web, mientras que XML permite la creación de etiquetas personalizadas para describir datos de manera más específica. Dicho de otro modo un documento HTML es un documento XML, pero no todos los documentos XML son HTML.

XML es un estándar abierto mantenido por el [World Wide Web Consortium (W3C)](https://www.w3.org/XML/){target="\_blank"} y es ampliamente utilizado en diversas aplicaciones, incluyendo:

- Intercambio de datos entre sistemas diferentes.
- Configuración de aplicaciones.
- Almacenamiento de datos estructurados.
- Representación de documentos complejos (como docx, xlsx, etc.)
- Difusión de Noticias (RSS, Atom).

### Estructura de un documento XML

Un documento XML está compuesto por varios elementos clave:

Prólogo
: Es la parte inicial del documento que puede incluir una declaración XML y otras instrucciones, como la definición de la codificación de caracteres. La declaración XML es opcional pero recomendada, y suele verse así: `<?xml version="1.0" encoding="UTF-8"?>`{l=xml}.

Elementos
: Son las unidades básicas de un documento XML y están delimitados por etiquetas de apertura y cierre. Por ejemplo, `<nombre>Juan</nombre>`{l=xml} es un elemento que contiene el texto "Juan".

Atributos
: Son pares clave-valor que proporcionan información adicional sobre un elemento. Se incluyen dentro de la etiqueta de apertura. Por ejemplo, `<persona id="123">`{l=xml} tiene un atributo `id`{l=xml} con el valor "123".

Contenido
: Es el texto o los datos que se encuentran entre las etiquetas de apertura y cierre de un elemento.

Comentarios
: Se pueden incluir comentarios en un documento XML utilizando la sintaxis `<!-- Comentario -->`{l=xml}.

El siguiente fragmento muestra un poema estructurado en XML

```{literalinclude} ../_static/code/xml/poema.xml
---
language: xml
---
```

donde se pueden distinguir claramente los diferentes elementos:

- `poema`{l=xml}
- `titulo`{l=xml}
- `verso`{l=xml}

y los atributos de poema

- `@fecha`{l=xml}
- `@lugar`{l=xml}

Como se puede observar XML permite estructurar la información en forma jerárquica, como si fuera un árbol, donde los elementos pueden contener otros elementos anidados.  Un archivo XML bien formado debe cumplir con ciertas reglas, como tener un único elemento raíz que contenga todos los demás elementos, y todas las etiquetas deben estar correctamente cerradas y anidadas.

Los atributos en XML permiten agregar metadatos o información adicional a los elementos, lo que puede ser útil para describir propiedades o características específicas de los datos. Sin embargo, es importante usarlos con moderación y de manera coherente para evitar complicaciones en la interpretación del documento.

```{figure} ../assets/images/poema-xml.png
---
name: xml_tree
align: center
---
Árbol que representa la estructura del poema en XML.
```

Existen varios sitios en internet que permiten visualizar el árbol asociado. Por ejemplo [https://codebeautify.org/xmlviewer](https://codebeautify.org/xmlviewer?input=%3Cpoema%20fecha=%22Abril%20de%201915%22%20lugar=%22Granada%22%3E%3Ctitulo%3EAlba%3C/titulo%3E%3Cverso%3EMi%20coraz%C3%B3n%20oprimido%3C/verso%3E%3Cverso%3Esiente%20junto%20a%20la%20alborada%3C/verso%3E%3Cverso%3Eel%20dolor%20de%20sus%20amores%3C/verso%3E%3Cverso%3Ey%20el%20sue%C3%B1o%20de%20las%20distancias.%20%3C/verso%3E%3C/poema%3E){target="\_blank"}.

En el ejemplo anterior, el elemento raíz es `poema`{l=xml}, que contiene como elementos hijos: `titulo`{l=xml} y varios elementos `verso`{l=xml}. El elemento `poema`{l=xml} también tiene dos atributos: `fecha`{l=xml} y `lugar`{l=xml}, que proporcionan información adicional sobre el poema.

Que un documento XML se pueda representar como un árbol simplifica la consulta y manipulación de los datos, ya que se pueden utilizar técnicas de recorrido de árboles para acceder a elementos específicos o extraer información relevante.

## XPath: XML Path Language

**XPath** (XML Path Language) es un lenguaje de consulta utilizado para navegar y seleccionar nodos en documentos XML. Proporciona una sintaxis para definir rutas que permiten localizar elementos, atributos y otros nodos dentro de la estructura jerárquica de un documento XML.

Permite describir caminos a través del árbol XML utilizando una notación similar a la de los sistemas de archivos. Por ejemplo, la expresión `/poema/titulo`{l=xml} selecciona el elemento `titulo`{l=xml} que es hijo directo del elemento raíz `poema`{l=xml}. Evaluar una expresión XPath es buscar **elementos** o **atributos** en un documento XML que coincidan con los criterios especificados en la expresión. El resultado son todos los nodos que cumplen con esos criterios.

Por ejemplo, la expresión `//verso`{l=xml} selecciona todos los elementos `verso`{l=xml} en el documento, independientemente de su posición en la jerarquía. La expresión `//verso[text()="Mi corazón oprimido"]`{l=xml} selecciona el elemento `verso`{l=xml} que contiene el texto exacto "Mi corazón oprimido".

En los ejemplos a continuación usaremos el siguiente documento XML que representa una biblioteca con varios libros y autores.

```{literalinclude} ../_static/code/xml/biblioteca.xml
---
language: xml
---
```

### Expresiones XPath para seleccionar nodos

| Expresión | Descripción |
| :- | :- |
| `/` | Si está al principio de la expresión, indica el nodo raíz, si no, indica "hijo"|
| `//` | Camino. Permite seleccionar nodos en un camino descendiente a partir de la posición actual |
| `.` | Nodo actual |
| `..` | Padre del nodo actual |
| `@nombre_atributo` | Atributo |

### Predicados

Los predicados pueden ser usados para filtrar un conjunto de nodos en base a una condición dada.

Los predicados se escriben entre corchetes (`[`, `]`).

| Expresión | Resultado |
| :- | :- |
| `/biblioteca/libro[position() = 1]` | Selecciona libro en la posición 1, hijo de biblioteca |
| `/biblioteca/libro[1]` | La misma condición en su versión resumida |
| `/biblioteca/libro[last()]` | Selecciona el último nodo libro, hijo de biblioteca |
| `/biblioteca/libro[last() - 1]` | Selecciona el ante último nodo libro, hijo de biblioteca | 
| `/biblioteca/libro[position() < 3]` | Selecciona los dos primeros nodos libro, hijo de biblioteca |
| `//autor[@fechaNacimiento]` | Selecciona todos los nodos autor, que tengan un atributo fechaNacimiento |
| `//autor[not(@fechaNacimiento)]` | Selecciona todos los nodos autor, que **no** tengan un atributo fechaNacimiento |
| `//autor[@fechaNacimiento="28/03/1936"]` | Selecciona todos los nodos autor, que tengan un atributo fechaNacimiento con un valor específico |
| `/biblioteca//libro[precio < 350]` | Selecciona todos los nodos libros, que tengan como hijo directo un elemento precio con valor menor a 350 |
| `/biblioteca//libro[precio < 350]/titulo` | Selecciona todos los nodos titulo, hijos de nodos libros que tengan como hijo directo un elemento precio con valor menor a 350 |

### Selectores y comodines

| Expresión | Resultado |
| :- | :- |
| `/biblioteca/*` | Selecciona todos los elementos hijos directos de biblioteca |
| `/biblioteca//*` | Selecciona todos los elementos descendientes de biblioteca |
| `//autor[@*]` | Selecciona todos los elementos autor que tengan algún atributo |
| `node()` | Selecciona todos los elementos autor que tengan algún atributo |
| `//titulo/text()` | Selecciona el texto (no el nodo completo) de los títulos |

### Selección de varios caminos

El operador `|` es el operador de unión.

| Expresión | Resultado |
| :- | :- |
| `//libro/titulo \| //libro/precio` | Selecciona todos los nodos titulo y precio hijos de libro |

### Comparaciones

| Operador | Descripción | Ejemplo |
| :- | :- | :- |
| `=` | Igualdad | `precio = 541.78` |
| `!=` | Distinto | `precio != 541.78` |
| `<` | Menor estricto | `precio < 500` |
| `<=` | Menor o igual | `precio <= 541.78` |
| `>` | Mayor estricto | `precio > 500` |
| `<=` | Mayor o igual | `precio >= 541.78` |

### Operadores

| Operador | Descripción | Ejemplo |
| :- | :- | :- |
| `+` | Suma | `6 + 4` |
| `-` | Sustracción | `6 - 4` |
| `*` | Multiplicación | `6 * 4` |
| `div` | División | `8 div 4` |
| `or` | Disyunción | `precio = 541.78 or precio = 214.48` |
| `and` | Conjunción | `precio > 300 and precio <= 541.78` |
| `mod` | Módulo (resto de la división entera) | `5 mod 2` |