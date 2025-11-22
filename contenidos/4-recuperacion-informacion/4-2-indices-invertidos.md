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

# Índices Invertidos

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp/edd_indices_invertidos"""
import os
import shutil

tmp_dir = "/tmp/edd_indices_invertidos"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir, exist_ok=True)
os.chdir(tmp_dir)
```

Los **índices invertidos** son la estructura de datos fundamental en los sistemas de recuperación de información modernos. Son utilizados por motores de búsqueda, sistemas de búsqueda en documentos, y cualquier aplicación que necesite encontrar documentos que contengan ciertos términos de manera eficiente.

La idea central es simple pero poderosa: en lugar de ir de documento a documento buscando términos (búsqueda secuencial), creamos una estructura que va de término a documentos. Es decir, para cada término del vocabulario, mantenemos una lista de los documentos donde aparece.

Nos podemos imaginar que un índice invertido es una especie de diccionario, donde las claves son las palabras (términos) y los valores son listas de id de documentos (postings) que contienen esas palabras. Donde previamente, a cada documento que forma parte de la colección se le asignó un identificador único (doc_id).

## Motivación

Imaginemos que tenemos una colección de documentos y queremos buscar aquellos que contienen la palabra "Python". Sin un índice, tendríamos que:

1. Leer cada documento completo
2. Buscar la palabra "Python" en cada uno
3. Guardar los documentos que la contengan

Este proceso es extremadamente ineficiente para colecciones grandes. Con un índice invertido, simplemente buscamos "python" en el diccionario y obtenemos directamente la lista de documentos que lo contienen.

```{code-cell} python
---
tags: hide-output
---
# Ejemplo: búsqueda sin índice (ineficiente)
documentos = {
    1: "Python es un lenguaje de programación",
    2: "Java es un lenguaje orientado a objetos",
    3: "Python y Java son lenguajes populares",
    4: "Machine learning con Python",
}


def buscar_sin_indice(termino, documentos):
    """Busca documentos que contienen un término (búsqueda secuencial)"""
    resultado = []
    for doc_id, contenido in documentos.items():
        if termino.lower() in contenido.lower():
            resultado.append(doc_id)
    return resultado


# Buscar documentos con "Python"
docs_con_python = buscar_sin_indice("Python", documentos)
print(f"Documentos con 'Python': {docs_con_python}")
```

Como se puede ver, este método requiere examinar cada documento completo. Para colecciones con millones de documentos, si cada vez que realizamos una búsqueda hay que leer todos los documentos el método resulta impracticable.

La idea detrás de los índices invertidos es leer una sola vez todos los documentos para construir el índice, y luego usar ese índice para responder consultas de manera eficiente.

## Recuperación Booleana

La **recuperación booleana** es el modelo más simple de recuperación de información. En este modelo, las consultas se formulan como expresiones booleanas con operadores AND, OR y NOT.

Por ejemplo la siguiente matriz representa la incidencia de términos en documentos, donde las filas son términos (palbabras) y las columnas son las páginas de este apuntes (documentos), en cada celda indica si el término aparece (1) o no (0) en el documento correspondiente:

```{table}
---
name: matriz_incidiencia
---
|   | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| XML | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| regex | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| haskell | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| invertido | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| java | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

```

Ejemplos de consultas booleanas:

- `XML AND java`: documentos que contienen ambos términos

```text
XML:        100101101000000
                           AND
java:       000010001000000
            ---------------
            000000001000000 → documento 23
```

- `regex OR invertido`: documentos que contienen al menos uno de los términos

```text
regex:      000010001000000
                           OR
invertido:  000010011000000
            ----------------
            000010011000000 → documentos 19, 23, 24
```

- `XML AND NOT Java`: documentos que contienen "XML" pero no "Java"

```text
XML:        100101101000000
                           AND
NOT java:   111101110111111
            ----------------
            100101100000000 → documentos 15, 18, 20, 21
```

El modelo booleano es determinístico: un documento o bien coincide con la consulta o no. No hay noción de "cuán bien" coincide un documento.

## Estructura del Índice Invertido

Un índice invertido consta de dos componentes principales:

1. **Diccionario (o vocabulario)**: Contiene todos los términos únicos que aparecen en la colección
2. **Listas de postings**: Para cada término del diccionario, una lista de documentos donde aparece

```{figure} ../_static/figures/indice_invertido_light.svg
:class: only-light-mode
:width: 100%
Estructura de un índice invertido
```

```{figure} ../_static/figures/indice_invertido_dark.svg
:class: only-dark-mode
:width: 100%
Estructura de un índice invertido
```

A continuación se muestra una implementación simple de un índice invertido en Python que permite agregar documentos y realizar búsquedas booleanas.

En esta primera implementación, suponemos que tanto los documentos, como el índice caben en memoria. No se indexan stopwords.

```{admonition} Definición de Stopwords
Las stopwords son palabras comunes que no se indexan porque aportan poco valor semántico en las búsquedas. En general no se indexan artículos, preposiciones, pronombres, adverbios comunes, algunos verbos conjugados, etc.
```

```{code-cell} python
---
tags: hide-output
---
from collections import defaultdict

# Palabras que NO se deben indexar (stopwords indicadas)
STOPWORDS = {
    "es",
    "un",
    "de",
    "a",
    "son",
    "con",
    "y",
    "la",
    "el",
    "en",
    "los",
    "las",
    "por",
    "para",
}


class IndiceInvertido:
    """Implementación simple de un índice invertido"""

    def __init__(self):
        # Diccionario: término -> conjunto de IDs de documentos
        self.indice = defaultdict(set)
        # Almacena los documentos originales
        self.documentos = {}

    def agregar_documento(self, doc_id, texto):
        """Agrega un documento al índice (no indexa palabras en STOPWORDS)"""
        self.documentos[doc_id] = texto

        # Tokenizar o separar el documento como una lista de palabras
        # Las palabras se normalizan a minúsculas y se eliminan signos
        # de puntuación básicos
        palabras = texto.lower().split()

        # Agregar cada palabra al índice salvo las stopwords indicadas
        for palabra in palabras:
            # Eliminar puntuación básica alrededor de la palabra
            palabra = palabra.strip(".,;:!?()[]{}\"'")
            if not palabra:
                continue
            if palabra in STOPWORDS:
                continue
            self.indice[palabra].add(doc_id)

    def buscar(self, termino):
        """Busca documentos que contienen el término 
        (normaliza a minúsculas)"""
        termino = termino.lower().strip(".,;:!?()[]{}\"'")
        return self.indice.get(termino, set())

    def buscar_and(self, termino1, termino2):
        """Busca documentos que contienen ambos términos"""
        docs1 = self.buscar(termino1)
        docs2 = self.buscar(termino2)
        return docs1 & docs2

    def buscar_or(self, termino1, termino2):
        """Busca documentos que contienen al menos uno de los términos"""
        docs1 = self.buscar(termino1)
        docs2 = self.buscar(termino2)
        return docs1 | docs2

    def buscar_not(self, termino1, termino2):
        """Busca documentos que contienen termino1 pero no termino2"""
        docs1 = self.buscar(termino1)
        docs2 = self.buscar(termino2)
        return docs1 - docs2

    def __repr__(self):
        """Representación del índice para inspección"""
        resultado = []
        for termino in self.indice.keys():
            docs = self.indice[termino]
            resultado.append(f"{termino}: {docs}")
        return "\n".join(resultado)


# Crear el índice
indice = IndiceInvertido()
indice.agregar_documento(1, "Python es un lenguaje de programación")
indice.agregar_documento(2, "Java es un lenguaje orientado a objetos")
indice.agregar_documento(3, "Python y Java son lenguajes populares")
indice.agregar_documento(4, "Machine learning con Python")

# Mostrar el índice
print("Índice invertido:")
print(indice)
```

```{note} Nota
`defaultdict` de la librería estándar de Python se utiliza para simplificar la creación del diccionario de listas de postings. Cada vez que se accede a una clave que no existe, se crea automáticamente un conjunto vacío sin necesidad de inicializarlo con `setdefault` como un diccionario estándar.

Para realizar búsquedas booleanas, conviene representar las listas de postings como conjuntos (`set`) para aprovechar las operaciones de intersección, unión y diferencia que son eficientes en conjuntos.
```

### Búsquedas con el Índice

Ahora podemos realizar búsquedas muy eficientemente:

```{code-cell} python
---
tags: hide-output
---
# Búsquedas simples
print(f"\nDocumentos con 'python': {indice.buscar('python')}")
print(f"Documentos con 'lenguaje': {indice.buscar('lenguaje')}")

# Búsquedas booleanas
print(f"\nPython AND Java: {indice.buscar_and('python', 'java')}")
print(f"Python OR Machine: {indice.buscar_or('python', 'machine')}")
print(f"Python AND NOT Java: {indice.buscar_not('python', 'java')}")
```

## El Vocabulario y Procesamiento de Términos

En la práctica, el procesamiento de términos es más sofisticado que simplemente convertir a minúsculas y separar por espacios. Los sistemas reales aplican varias técnicas para mejorar la calidad del índice y la recuperación, entre ellas "normalización", "tokenización", "eliminación de stopwords" y "stemming/lematización". A continuación se muestran ejemplos de cada técnica usando la librería NLTK en Python.

### NLTK

NLTK (Natural Language Toolkit) es una librería popular en Python para procesamiento de lenguaje natural. Proporciona herramientas para tokenización, stemming, lematización, y manejo de stopwords, entre otras funcionalidades.

Para instalar NLTK, ejecutar en la terminal:

```bash
pip install nltk
```

Luego es necesario descargar algunos recursos adicionales (stopwords, modelos de tokenización) usando:

```python
import nltk

nltk.download()
```

Se abrirá una ventana gráfica para seleccionar los recursos a descargar. Alternativamente, se pueden descargar recursos específicos directamente en el código como se muestra en los ejemplos a continuación.

```python
import nltk

nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)
```

## Procesamiento de Términos con NLTK

### Normalización

El proceso de normalización consiste en convertir el texto a una forma estándar. Aquí se muestra un ejemplo básico de normalización usando NLTK para tokenizar y limpiar el texto.

```{code-cell} python
---
tags: hide-output
---
import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab", quiet=True)


def normalizar_texto(texto):
    """Normaliza un texto para indexación usando NLTK para tokenizar."""
    # Convertir a minúsculas
    texto = texto.lower()
    # Reemplazar signos de puntuación por espacios
    # (dejando letras, números y espacios)
    texto = re.sub(r"[^\w\s]", " ", texto)
    # Tokenizar con NLTK (maneja mejor cliticos, contracciones, etc.)
    tokens = word_tokenize(texto, language="spanish")
    # Reconstruir string normalizado (tokens separados por espacio)
    return " ".join(tokens)


# Ejemplo
texto = "¡Python es GENIAL! ¿No lo crees? Dímelo."

print(f"Original: {texto}")
print(f"Normalizado: {normalizar_texto(texto)}")
```

### Tokenización

Es el proceso de dividir el texto en unidades (tokens).

```{code-cell} python
---
tags: hide-output
---
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab", quiet=True)


def tokenizar(texto):
    """Tokeniza un texto en palabras usando NLTK (Spanish punkt)."""
    texto_normalizado = texto.lower()
    tokens = word_tokenize(texto_normalizado, language="spanish")
    return tokens


texto = "Python 3.9 es la versión más reciente"
tokens = tokenizar(texto)
print(f"Tokens: {tokens}")
```

### Eliminación de Stopwords

NLTK proporciona listas de stopwords para varios idiomas, incluyendo español.

```{code-cell} python
---
tags: hide-output
---
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)


STOPWORDS_NLTK = set(stopwords.words("spanish"))


def eliminar_stopwords(tokens):
    """Elimina stopwords usando la lista de NLTK para español."""
    return [t for t in tokens if t not in STOPWORDS_NLTK]


# Ejemplo
texto = "Python es un lenguaje de programación muy popular"
tokens = word_tokenize(texto.lower(), language="spanish")
tokens_sin_stop = eliminar_stopwords(tokens)

print(f"Tokens originales: {tokens}")
print(f"Sin stopwords: {tokens_sin_stop}")
```

```{code-cell} python
---
tags: hide-output
---
import textwrap
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

STOPWORDS_NLTK = set(stopwords.words("spanish"))

print("Stopwords en español (NLTK):")
palabras = sorted(STOPWORDS_NLTK)
texto = ", ".join(palabras)
for linea in textwrap.wrap(texto, width=80):
    print(linea)
```

### Stemming y Lematización

El proceso de stemming consiste en reducir las palabras a su raíz o forma base. La lematización es un proceso más sofisticado, que para recortar las palabras utiliza el contexto.

Se muestra stemming en español con SnowballStemmer (disponible en NLTK). NLTK no ofrece un lematizador robusto en español, por lo quee incluye un ejemplo de lematización en inglés con WordNet (por si hay textos en inglés).

```{code-cell} python
---
tags: hide-output
---
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("wordnet", quiet=True)

# Stemmer para español
stemmer_es = SnowballStemmer("spanish")

# Lemmatizer para inglés (WordNet)
lemmatizer_en = WordNetLemmatizer()


def stem_tokens_es(tokens):
    """Aplica SnowballStemmer (español) a una lista de tokens."""
    return [stemmer_es.stem(t) for t in tokens]


def lemmatize_tokens_en(tokens):
    """Ejemplo de lematización en inglés con WordNetLemmatizer."""
    return [lemmatizer_en.lemmatize(t) for t in tokens]


# Ejemplos
pal_es = ["programación","programar","programador","estudiante","estudiar"]
stems = stem_tokens_es(pal_es)
print("Stemming (es):")
for p, s in zip(pal_es, stems):
    print(f"{p} → {s}")

pal_en = ["runners", "run", "philosophy", "philosophical", "philosopher"]
lemmas_en = lemmatize_tokens_en(pal_en)
print("\nLematización (en, WordNet):")
for p, l in zip(pal_en, lemmas_en):
    print(f"{p} → {l}")
```

Tanto el stemming como la lematización ayudan a agrupar diferentes formas de una misma palabra, reduciendo el tamaño del vocabulario y mejorando la recuperación al costo de perdida de la información, ya que diferentes palabras pueden mapear al mismo stem o lema.

En el ejemplo anterior, "programación", "programar" y "programador" se reducen al mismo stem "program". Esto puede ser beneficioso para la recuperación, pero también puede causar ambigüedad lo que conduce a resultados menos precisos. Una decisión de diseño importante en la construcción del índice es elegir entre usar stemming, lematización o ninguna de las dos técnicas, dependiendo de los requisitos específicos de la aplicación.

Una técnica común es experimentar con diferentes configuraciones y evaluar su impacto en la precisión y recall de las búsquedas.

Por ejemplo se puede utilizar un stemmer o lematizador durante la fase de construcción del índice para normalizar los términos, y luego aplicar el mismo proceso a las consultas de los usuarios para asegurar que coincidan con los términos indexados.

#### spaCy

Otra librería popular para procesamiento de lenguaje natural es **spaCy**, que ofrece modelos robustos para varios idiomas, incluyendo español. SpaCy proporciona tokenización, lematización, y reconocimiento de entidades nombradas, entre otras funcionalidades avanzadas. Para instalar spaCy y el modelo en español, ejecutar:

```bash
pip install spacy
python -m spacy download es_core_news_sm
```

o de forma alternativa se puede descargar el modelo desde Python con:

```{code-cell} python
---
tags: remove-output
---
import spacy

spacy.cli.download("es_core_news_sm")
```

A continuación se muestra un ejemplo de uso de spaCy para tokenización y lematización en español.

```{code-cell} python
---
tags: hide-output
---
import spacy
import textwrap  # Para imprimir en 77 columnas

# Cargar modelo en español
nlp = spacy.load("es_core_news_sm")

# Texto de ejemplo (puede reutilizarse el texto definido anteriormente)
texto = """La recuperación de la información en Python combina técnicas de
procesamiento de texto con estructuras de datos eficientes para permitir
búsquedas rápidas y relevantes sobre colecciones de documentos. En la práctica
se sigue un pipeline que incluye: 1) extracción y normalización del texto
(minúsculas, eliminación de acentos y puntuación), 2) tokenización (dividir en
tokens o palabras), 3) eliminación de stopwords, 4) stemming o lematización
para agrupar formas de una misma palabra, y 5) construcción de una estructura
de índice invertido que asocia cada término a una lista de documentos
(postings).

Para implementar esto en Python existen herramientas y bibliotecas útiles:
NLTK y spaCy para tokenización, stopwords y lematización; scikit-learn para
transformar colecciones en matrices TF-IDF y calcular similitud coseno;
y bibliotecas especializadas como Whoosh o clientes para motores externos
(Elasticsearch) cuando la escala crece. Un índice invertido básico se puede
representar con dicts y sets (término -> set(doc_id)) o con listas ordenadas
de postings para operaciones booleanas y de fusión eficientes.

En el modelo de recuperación ponderada, se suele representar cada documento
como un vector en un espacio de términos usando TF-IDF. Con scikit-learn,
TfidfVectorizer facilita la tokenización, normalización y cálculo de pesos;
luego, para una consulta, se transforma la consulta al mismo espacio y se
calculan similitudes (por ejemplo, coseno) para ordenar resultados por
relevancia. Para colecciones grandes se deben considerar técnicas de
dimensionalidad y búsqueda aproximada (ANN) para acelerar consultas.

Cuando la colección no cabe en memoria, se aplican algoritmos como BSBI y SPIMI
para construir índices por bloques y luego fusionarlos; en entornos
distribuidos se emplea MapReduce o motores distribuidos (Elasticsearch, Solr)
que gestionan particionado, replicación y tolerancia a fallos. Además, la
compresión de postings (delta encoding, gamma codes, varint) reduce
drásticamente el espacio en disco y mejora la transferencia I/O.

En proyectos reales conviene mantener separación clara entre fases:
extracción (parsing de documentos), normalización y tokenización (pipelines
reutilizables), construcción del índice (API clara para agregar/eliminar
documentos) y la capa de búsqueda (consultas booleanas y ponderadas, paginación
y highlights). También es crucial añadir pruebas automáticas, métricas de
evaluación (precisión, recall, MAP, NDCG) y pipelines de validación para
comparar variantes de preprocesamiento y ponderación.

Finalmente, en Python es habitual prototipar con estructuras sencillas
(dicts, sets) para validar ideas y luego migrar a soluciones más robustas:
persistencia del índice (SQLite, LevelDB, archivos binarios), servicios de
búsqueda (Elasticsearch) o bindings a Lucene para producción. Estas decisiones
dependen de requisitos de latencia, volumen de datos y la necesidad de
actualizaciones en tiempo real."""

# Procesar texto
doc = nlp(texto)

# Filtrar tokens y lemas: excluir stopwords, puntuación y tokens no alfabéticos
tokens_sin_stop = [
    token.text for token in doc if not token.is_stop and token.is_alpha]
lemmas_sin_stop = [
    token.lemma_ for token in doc if not token.is_stop and token.is_alpha
]


label = "Tokens (sin stopwords): "
s = ", ".join(tokens_sin_stop)
print(
    textwrap.fill(s, width=77,
    initial_indent=label,
    subsequent_indent=" " * len(label))
)

label = "Lemas (sin stopwords): "
s = ", ".join(lemmas_sin_stop)
print(
    textwrap.fill(s, width=77,
    initial_indent=label,
    subsequent_indent=" " * len(label))
)
```

## Algoritmos de Construcción de Índices

Cuando trabajamos con colecciones grandes de documentos que no caben en memoria RAM, necesitamos algoritmos especializados para construir el índice invertido. Existen tres enfoques principales: BSBI, SPIMI, y construcción distribuida con MapReduce.

### BSBI (Blocked Sort-Based Indexing)

El algoritmo **BSBI** (Blocked Sort-Based Indexing) es una técnica que construye índices cuando la colección de documentos no cabe en memoria. Divide el procesamiento en dos fases:

**Fase 1: Generación de bloques ordenados**

1. Lee documentos en bloques que sí caben en memoria
2. Para cada bloque, extrae pares (término, doc_id)
3. Ordena los pares en memoria, agrupando por términos
4. Escribe el bloque ordenado a disco

**Fase 2: Fusión de bloques (merge de k-vías)**

1. Abre todos los archivos de bloques simultáneamente
2. Usa un heap para fusionar eficientemente
3. Produce el índice final ordenado

#### Pseudocódigo BSBI

```text
ALGORITMO BSBI(colección_documentos)
    bloques = []
    buffer = []

    // Fase 1: Crear bloques ordenados
    PARA CADA documento EN colección_documentos:
        pares = ParsearDocumento(documento)
        buffer.agregar(pares)

        SI buffer.tamaño >= TAMAÑO_BLOQUE:
            índice_bloque = InvertirYOrdenar(buffer)
            archivo_bloque = EscribirADisco(índice_bloque)
            bloques.agregar(archivo_bloque)
            buffer.limpiar()
    FIN PARA

    // Procesar último bloque si existe
    SI buffer NO está vacío:
        índice_bloque = InvertirYOrdenar(buffer)
        archivo_bloque = EscribirADisco(índice_bloque)
        bloques.agregar(archivo_bloque)
    FIN SI

    // Fase 2: Fusionar todos los bloques
    índice_final = FusionarBloques(bloques)
    RETORNAR índice_final
FIN ALGORITMO


FUNCIÓN InvertirYOrdenar(pares_término_docid):
    // Ordena los pares por (término, doc_id)
    pares_ordenados = Ordenar(pares_término_docid)

    // Construye diccionario término -> [doc_ids]
    índice = diccionario_vacío()
    PARA CADA (término, doc_id) EN pares_ordenados:
        índice[término].agregar(doc_id)
    FIN PARA

    RETORNAR índice
FIN FUNCIÓN


FUNCIÓN FusionarBloques(lista_bloques):
    // Merge de k-vías usando un heap
    heap = heap_vacío()
    archivos = []

    // Inicializar heap con primera línea de cada bloque
    PARA CADA bloque EN lista_bloques:
        archivo = Abrir(bloque)
        archivos.agregar(archivo)
        (término, postings) = LeerLínea(archivo)
        heap.insertar((término, postings, archivo))
    FIN PARA

    índice_final = diccionario_vacío()
    término_actual = NULL
    postings_acumulados = []

    MIENTRAS heap NO vacío:
        (término, postings, archivo) = heap.extraer_mínimo()

        SI término ≠ término_actual Y término_actual ≠ NULL:
            índice_final[término_actual] = postings_acumulados
            postings_acumulados = []
        FIN SI

        término_actual = término
        postings_acumulados.agregar(postings)

        // Leer siguiente línea del mismo archivo
        SI NO archivo.fin():
            (término, postings) = LeerLínea(archivo)
            heap.insertar((término, postings, archivo))
        FIN SI
    FIN MIENTRAS

    // Guardar último término
    SI término_actual ≠ NULL:
        índice_final[término_actual] = postings_acumulados
    FIN SI

    RETORNAR índice_final
FIN FUNCIÓN
```

#### Complejidad de BSBI

- **Tiempo**: O(T log T) donde T es el número total de pares (término, doc_id)
  - Ordenamiento de bloques: O(T log T)
  - Merge de k bloques: O(T log k)
- **Espacio**: O(B) donde B es el tamaño del bloque en memoria
- **I/O**: Cada par (término, doc_id) se lee y escribe una vez

#### Ventajas y Desventajas de BSBI

**Ventajas:**

- Simple de implementar
- Funciona bien con colecciones que no caben en memoria
- El ordenamiento garantiza postings ordenados
- Eficiente uso de I/O secuencial

**Desventajas:**

- Requiere espacio en disco para bloques intermedios
- El merge de k-vías puede ser complejo con muchos bloques
- Manejo de términos muy frecuentes puede ser ineficiente

### SPIMI (Single-Pass In-Memory Indexing)

El algoritmo **SPIMI** mejora BSBI al generar directamente un diccionario de términos → postings en cada bloque, en lugar de generar y ordenar pares. Esto es más eficiente en memoria.

#### Pseudocódigo SPIMI

```text
ALGORITMO SPIMI(flujo_tokens)
    bloques = []
    diccionario = diccionario_vacío()

    MIENTRAS hay_más_tokens():
        MIENTRAS hay_memoria_disponible():
            (término, doc_id) = siguiente_token()

            SI término NO EN diccionario:
                diccionario[término] = nueva_lista_postings()
                AgregarADiccionario(término)
            FIN SI

            SI doc_id NO EN diccionario[término]:
                diccionario[término].agregar(doc_id)
            FIN SI
        FIN MIENTRAS

        // Memoria llena, escribir bloque a disco
        bloque = OrdenarTérminos(diccionario)
        archivo = EscribirBloque(bloque)
        bloques.agregar(archivo)
        diccionario.limpiar()
    FIN MIENTRAS

    // Fusionar bloques
    índice_final = FusionarBloques(bloques)
    RETORNAR índice_final
FIN ALGORITMO
```

#### Ventajas y Desventajas de SPIMI

**Ventajas:**

- Más eficiente en memoria que BSBI
- Una sola pasada por los datos
- No requiere ordenamiento explícito de pares
- Genera postings ordenados por doc_id naturalmente

**Desventajas:**

- Requiere estructura de datos dinámica (diccionario)
- Puede fragmentar memoria si hay muchos términos
- Más complejo que BSBI

### Construcción Distribuida con MapReduce

Para colecciones masivas (terabytes o petabytes), se usa procesamiento distribuido con el paradigma **MapReduce**. Este enfoque distribuye el trabajo entre múltiples máquinas.

#### Diagrama MapReduce para Construcción de Índices

```{figure} ../_static/figures/map_reduce_dark.svg
:class: only-dark-mode
Indexado con Map-Reduce
```

```{figure} ../_static/figures/map_reduce_light.svg
:class: only-light-mode
Indexado con Map-Reduce
```


#### Componentes de MapReduce

**Fase Map:**

- **Entrada**: Documento completo
- **Proceso**: Tokeniza y normaliza el texto
- **Salida**: Pares (término, doc_id) para cada término en el documento

**Fase Shuffle & Sort:**

- **Entrada**: Todos los pares (término, doc_id) de todos los mappers
- **Proceso**: Agrupa todos los doc_ids por término y los ordena
- **Salida**: Pares (término, lista_doc_ids) agrupados por término

**Fase Reduce:**

- **Entrada**: (término, lista_doc_ids) para un subconjunto de términos
- **Proceso**: Consolida y ordena la lista de doc_ids
- **Salida**: Entradas del índice invertido final

#### Pseudocódigo MapReduce

```text
FUNCIÓN Map(doc_id, contenido_documento):
    términos = Tokenizar(contenido_documento)
    PARA CADA término EN términos:
        término_normalizado = Normalizar(término)
        EMITIR (término_normalizado, doc_id)
    FIN PARA
FIN FUNCIÓN


FUNCIÓN Reduce(término, lista_doc_ids):
    // Recibe: término y todos los doc_ids donde aparece
    postings = []

    PARA CADA doc_id EN lista_doc_ids:
        SI doc_id NO EN postings:
            postings.agregar(doc_id)
        FIN SI
    FIN PARA

    postings_ordenados = Ordenar(postings)
    EMITIR (término, postings_ordenados)
FIN FUNCIÓN
```

#### Proceso de Indexación Paso a Paso con MapReduce

1. **Particionamiento**: La colección se divide en splits (bloques) de documentos

2. **Map en paralelo**: Cada mapper procesa un split:

   - Lee documentos asignados
   - Tokeniza y normaliza términos
   - Emite pares (término, doc_id)

3. **Shuffle**: El framework agrupa automáticamente:

   - Todos los pares con el mismo término van al mismo reducer
   - Los doc_ids se agrupan en listas

4. **Reduce en paralelo**: Cada reducer procesa un rango de términos:

   - Recibe (término, [doc_id₁, doc_id₂, ..., doc_idₙ])
   - Elimina duplicados y ordena la lista
   - Escribe el índice parcial a disco

5. **Consolidación**: Los índices parciales se combinan en el índice final

#### Ventajas y Desventajas de MapReduce

**Ventajas:**

- Escalabilidad masiva (miles de máquinas)
- Tolerancia a fallos automática
- Procesamiento paralelo eficiente
- Ideal para colecciones enormes (TB/PB)

**Desventajas:**

- Overhead de comunicación entre nodos
- Requiere infraestructura distribuida
- Más complejo de implementar y depurar
- Overkill para colecciones pequeñas

### Tabla Comparativa de Algoritmos

| Característica                 | BSBI                                     | SPIMI                             | MapReduce                               |
| ------------------------------ | ---------------------------------------- | --------------------------------- | --------------------------------------- |
| **Tamaño de colección**        | Mediano (GB)                             | Mediano (GB)                      | Masivo (TB-PB)                          |
| **Requisito de memoria**       | Bajo (tamaño de bloque)                  | Medio (diccionario dinámico)      | Distribuido                             |
| **Complejidad implementación** | Baja                                     | Media                             | Alta                                    |
| **Velocidad (single machine)** | Media                                    | Alta                              | N/A                                     |
| **Escalabilidad**              | Limitada                                 | Limitada                          | Excelente                               |
| **Tolerancia a fallos**        | Manual                                   | Manual                            | Automática                              |
| **I/O en disco**               | 2 pasadas (leer + escribir)              | 2 pasadas                         | Red + disco                             |
| **Uso de CPU**                 | Alto (ordenamiento)                      | Medio                             | Distribuido                             |
| **Mejor caso de uso**          | Colecciones medianas, recursos limitados | Colecciones medianas, más memoria | Colecciones masivas, cluster disponible |

### Consideraciones Prácticas

Al elegir un algoritmo de construcción de índices se debe considerar:

1. **Tamaño de la colección**:

   - < 1 GB: Construcción en memoria simple.
   - 1-100 GB: BSBI o SPIMI.
   - \> 100 GB: MapReduce o sistemas especializados.

2. **Recursos disponibles**:

   - RAM limitada: BSBI (menor uso de memoria).
   - RAM abundante: SPIMI (más rápido).
   - Cluster disponible: MapReduce.

3. **Frecuencia de actualización**:

   - Actualizaciones frecuentes: Índices incrementales.
   - Reconstrucción completa: Batch processing.

4. **Requisitos de tiempo**:

   - Tiempo real: Índices incrementales.
   - Batch: Cualquier algoritmo según tamaño.

#### Diseño del índice

En general se habla de términos y documentos, en la práctica hay que definir que es un documento para la aplicación específica. Por ejemplo si se quiere indexar un libro completo, ¿se indexa como un solo documento o se divide en capítulos o páginas? La granularidad afecta el tamaño del índice y la precisión de las búsquedas.

Si por el contrario se quiere indexar una colección de tweets, cada tweet puede ser un documento individual. La elección depende del caso de uso y los requisitos de recuperación.

## Implementación con BSBI

En el siguiente enlace se encuentra una implementación en Python del algoritmo BSBI para construir un índice invertido a partir de una colección de documentos. Esta implementación incluye procesamiento básico de texto (normalización, tokenización, eliminación de stopwords y stemming) y compresión del índice.

[https://github.com/untref-edd/IndiceInvertido](https://github.com/untref-edd/IndiceInvertido)

### Complejidad

La construcción de un índice tiene complejidad:

- **Tiempo**: $O(n × m)$ donde n es el número de documentos y m es el promedio de términos por documento.
- **Espacio**: $O(T)$ donde T es el número total de términos únicos en la colección.

Para colecciones muy grandes que no caben en memoria, se utilizan técnicas como:

- **Construcción por bloques**: Dividir la colección en bloques, crear índices parciales y luego fusionarlos.
- **Ordenamiento externo**: Usar algoritmos de ordenamiento que funcionen con datos en disco.
- **Procesamiento distribuido**: Utilizar frameworks como MapReduce para procesar en paralelo.

## Resumen

Los índices invertidos son esenciales para la recuperación eficiente de información:

- Permiten búsquedas rápidas al ir de término a documentos
- Consisten en un diccionario de términos y listas de postings
- El procesamiento de texto (normalización, tokenización, stopwords, stemming) mejora la efectividad
- Algoritmos como BSBI, SPIMI y MapReduce permiten construir índices para colecciones grandes
- Se utilizan en todos los motores de búsqueda modernos
- La construcción para colecciones grandes requiere técnicas especiales

En el siguiente capítulo veremos cómo comprimir estos índices para reducir el espacio que ocupan, lo cual es crucial cuando trabajamos con colecciones de millones de documentos.

## Aplicaciones Prácticas

Los índices invertidos se utilizan en:

- **Motores de búsqueda web**: Google, Bing, etc.
- **Búsqueda en documentos**: Elasticsearch, Solr, Lucene
- **Búsqueda en código**: GitHub Code Search
- **Bases de datos full-text**: PostgreSQL, MongoDB con índices de texto
- **Sistemas de recomendación**: Para encontrar ítems similares
- **Detección de plagio**: Comparar documentos eficientemente

## Referencias y Recursos Adicionales

### Bibliografía Principal

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. Capítulos 1, 2, 3 y 4.{cite:p}`irbook`
- Modern Information Retrieval: The Concepts and Technology behind Search. {cite:p}`baeza2011`
- Information Retrieval: Implementing and Evaluating Search Engines. {cite:p}`buttcher2010`
