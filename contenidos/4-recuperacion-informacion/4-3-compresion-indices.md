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

# Compresión de índices

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp/edd_compresion_indices"""

import os
import shutil

tmp_dir = "/tmp/edd_compresion_indices"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir, exist_ok=True)
os.chdir(tmp_dir)
```

La **compresión de índices** es una técnica fundamental para reducir el espacio ocupado por índices invertidos. Cuando trabajamos con colecciones grandes de documentos (como un motor de búsqueda web que indexa miles de millones de páginas), el tamaño del índice puede ser enorme. Comprimir el índice no solo ahorra espacio en disco, sino que también puede mejorar el rendimiento al reducir las transferencias de datos entre disco y memoria.

## Motivación

Consideremos un ejemplo real: un motor de búsqueda que indexa mil millones de páginas web. Si cada página contiene en promedio $1.000$ términos únicos, y cada término aparece en promedio en $10.000$ páginas, el índice invertido necesitaría almacenar aproximadamente:

Diccionario

$$
10.000.000 \text{ de terminos} \times 10 \text{ bytes} = \mathbf{95{,}36} \, \mathbf{MB}
$$

Listas de postings

$$
10.000.000 \text{ de terminos} \times 10.000 \text{ documentos} \times 4 \text{ bytes} = \mathbf{372{,}53} \, \mathbf{GB}
$$

con compresión típica (factor x4):

$$
372{,}53 \, \mathrm{GB} \div 4 = \mathbf{93{,}13} \, \mathbf{GB}
$$

dando un ahorro de expación de:

$$
372{,}53 \, \mathrm{GB} - 93{,}13 \, \mathrm{GB} = \mathbf{279{,}40} \, \mathbf{GB}
$$

Esto es solo para almacenar los IDs de documentos. Agregar información adicional como frecuencias de términos o posiciones incrementa aún más el tamaño. La compresión puede reducir este espacio a una fracción del original.

Se puede comprimir tanto el diccionario de términos o Vocabulario como las listas de _postings_ asociadas a cada término.

## Compresión del diccionario de términos

El diccionario contiene todos los términos únicos. Aunque es relativamente pequeño comparado con las listas de _postings_, su compresión sigue siendo importante.

### Técnicas para comprimir el diccionario

#### Cadena única de términos

La primera técnica consiste en almacenar todos los términos como si fueran una única cadena de caracteres:

- Guardar todas las palabras del diccionario como una larga cadena de caracteres.
- Se le asocia una estructura de datos de longitud fija para la frecuencia, la referencia a la lista de apariciones (_postings_) y la referencia al término en la cadena.
- La referencia al próximo término marca el final del término corriente.

```{figure} ../_static/figures/4-recuperacion-informacion/4-3-compresion-indices/compresion_terminos_light.svg
---
class: only-light-mode
---
Compresión del diccionario de términos usando una cadena única.
```

```{figure} ../_static/figures/4-recuperacion-informacion/4-3-compresion-indices/compresion_terminos_dark.svg
---
class: only-dark-mode
---
Compresión del diccionario de términos usando una cadena única.
```

En la figura anterior se observa como se almacenan los términos `"programa"`, `"programable"`, `"programación"`, `"programador"` y `"programar"` en una sola cadena. Cada término se referencia mediante un puntero que indica su posición inicial, la palabra termina justo antes del siguiente puntero.

Con este esquema si se utilizan 4 bytes para la frecuencia, 4 bytes para la referencia a la lista de postings y 4 bytes para la referencia al término, se utilizan 12 bytes por término en el diccionario. Si el diccionario tiene 1 millón de términos, se utilizan 11,44 MB para almacenar el diccionario más el espacio necesario para la cadena de caracteres.

En memoria se carga la cadena completa y los punteros permiten acceder a cada término. Sin embargo, aún se puede mejorar la compresión del diccionario.

#### _Front Coding_

_Front Coding_ es una técnica que aprovecha los prefijos comunes entre términos consecutivos en orden lexicográfico aprovechando el hecho que, generalmente, las palabras ordenadas alfabéticamente comparten un prefijo común.

1. Se agrupan las entradas del diccionario en bloques de $k$ términos contiguos.
2. En cada bloque se almacena primero el término base completo; a continuación se coloca un separador `*` que delimita el prefijo base y marca el final de ese primer término.
3. Para los términos restantes del bloque no se repite el prefijo: se escribe un símbolo `•` que indica el punto donde termina el prefijo común y, a continuación, el sufijo que completa cada término.
4. Antes de cada término completo o de cada sufijo se guarda su longitud en un byte (1 B). En la estructura auxiliar solo se mantiene la referencia (puntero) al primer término de cada bloque; el resto de términos se recupera a partir de la cadena combinada.

Por ejemplo, si las palabras son: `algoritmo`, `alguacil`, `alguien`, `algas` y `alguno`, y $k=5$, se almacenan como:

```text
5alg*as6•oritmo5•uacil4•uien3•uno
```

- La primera palabra `algas` se almacena completa precedida por su longitud (`5`). Se añade un `*` en el medio de la palabra para indicar el final del prefijo común `alg` para todo el bloque de 5 términos.
- La segunda palabra `algoritmo` se almacena como `6•oritmo`, donde `6` es la longitud del sufijo `oritmo` y `•` indica el final del prefijo común.
- La tercera palabra `alguacil` se almacena como `5•uacil`.
- La cuarta palabra `alguien` se almacena como `4•uien`.
- La quinta palabra `alguno` se almacena como `3•uno`.

Implementación de _Front Coding_ para los bloques de ejemplo

```{code-cell} python
---
tags: remove-output
---
def common_prefix(strings: list[str]) -> str:
    """Devuelve el prefijo común más largo de una lista de strings."""
    if not strings:
        return ""

    s1, s2 = min(strings), max(strings)
    for i, char in enumerate(s1):
        if i >= len(s2) or char != s2[i]:
            return s1[:i]

    return s1


def front_encode_block(terms: list[str]) -> str:
    """
    Codifica un bloque de términos usando front coding.
    Formato: <len_base><prefijo>*<sufijo_base>{<len_suf>•<sufijo>}...
    """
    if not terms:
        return ""

    prefix = common_prefix(terms)
    base = terms[0]
    base_suffix = base[len(prefix) :]
    encoded = f"{len(base)}{prefix}*{base_suffix}"

    for term in terms[1:]:
        suf = term[len(prefix) :]
        encoded += f"{len(suf)}•{suf}"

    return encoded


def front_decode_block(encoded):
    """
    Decodifica la cadena generada por front_encode_block y devuelve la lista de
    términos.
    """
    import re

    if not encoded:
        return []

    m = re.match(r"^(\d+)", encoded)
    if not m:
        raise ValueError(
            "Formato inválido: no se encontró la longitud del término base"
        )

    base_len = int(m.group(1))
    rest = encoded[m.end() :]

    # buscar '*' que separa prefijo y sufijo del término base
    star_idx = rest.find("*")
    if star_idx == -1:
        raise ValueError("Formato inválido: falta '*'")
    prefix = rest[:star_idx]

    # calcular sufijo del base usando la longitud indicada
    base_suffix_len = base_len - len(prefix)
    base_suffix = rest[star_idx + 1 : star_idx + 1 + base_suffix_len]
    base = prefix + base_suffix
    terms = [base]
    rem = rest[star_idx + 1 + base_suffix_len :]

    i = 0
    while i < len(rem):
        # leer número de longitud del sufijo
        j = i
        while j < len(rem) and rem[j].isdigit():
            j += 1

        if j == i:
            raise ValueError("Formato inválido al leer longitud de sufijo")

        num = int(rem[i:j])
        if j >= len(rem) or rem[j] != "•":
            raise ValueError("Formato inválido: falta '•' separador")

        suf = rem[j + 1 : j + 1 + num]
        terms.append(prefix + suf)
        i = j + 1 + num

    return terms
```

Ejemplo con las palabras solicitadas

```{code-cell} python
palabras = ["algas", "algoritmo", "alguacil", "alguien", "alguno"]
encoded = front_encode_block(palabras)
decoded = front_decode_block(encoded)

print("Palabras originales:", palabras)
print("            Encoded:", encoded)
print("            Decoded:", decoded)
```

Estadísticas de compresión (bytes en UTF-8).

```{code-cell} python
original_bytes = sum(len(p.encode("utf-8")) for p in palabras)
comprimido_bytes = len(encoded.encode("utf-8"))

print(f"    Tamaño original: {original_bytes} bytes")
print(f"Tamaño front coding: {comprimido_bytes} bytes")
print(f"              Ratio: {original_bytes / comprimido_bytes:.2f}x")
```

## Compresión de listas de postings

Las listas de _postings_ contienen los IDs de documentos donde aparece cada término. La compresión de las listas de _postings_ es crucial ya que es la que tiene mayor impacto en el tamaño total del índice.

### _Gap Encoding_ (Codificación de diferencias)

En lugar de almacenar los IDs completos, almacenamos las diferencias (_gaps_) entre IDs consecutivos. Como los IDs están ordenados, los _gaps_ suelen ser números pequeños.

Ejemplo de gap encoding:

```{code-cell} python
doc_ids = [15478, 15874, 17950, 50123, 50234, 60001]

# Convertir a gaps
gaps = [curr - prev for prev, curr in zip([0] + doc_ids, doc_ids)]

print(f"    IDs originales: {doc_ids}")
print(f"Gaps (diferencias): {gaps}")
```

Comparar tamaños (asumiendo que usamos el mínimo de bits necesarios)

```{code-cell} python
import math


def bits_necesarios(n):
    """Calcula bits necesarios para representar un número"""
    return math.ceil(math.log2(n + 1)) if n != 0 else 1


bits_originales = sum(bits_necesarios(id) for id in doc_ids)
bits_gaps = sum(bits_necesarios(gap) for gap in gaps)

print(f"IDs originales: {bits_originales} bits")
print(f"      Con gaps: {bits_gaps} bits")
print(f"        Ahorro: {100 * (1 - bits_gaps / bits_originales):.1f}%")
```

### _Variable Byte encoding_ (VB)

Otra técnica popular es _Variable Byte encoding_, que usa uno o más bytes para representar un número, dependiendo de su tamaño, así la cantidad de bytes para codificar el _gap_ entre el ID de un documento y el siguiente varía según el valor del _gap_.

- Cada byte tiene 7 bits de datos y 1 bit de continuación (el bit más significativo).
- Bit de continuación == `0`: hay más bytes.
- Bit de continuación == `1`: es el último byte.

Así, por ejemplo, la representación de los siguientes gaps `[15478, 396, 2076, 32173, 111, 9767]` sería:

| Número |              Codificación VB | Cantidad de bytes |
| -----: | ---------------------------: | ----------------: |
|  15478 |          `01111000 11110110` |                 2 |
|    396 |          `00000011 10001100` |                 2 |
|   2076 |          `00010000 10011100` |                 2 |
|  32173 | `00000001 01111011 10101101` |                 3 |
|    111 |                   `11101111` |                 1 |
|   9767 |          `01001100 10100111` |                 2 |

Se parte de la representación en binario del número y se divide en grupos de 7 bits, cada grupo se almacena en un byte. El bit más significativo, es decir el primer bit de un byte de 8 bits, se usa para indicar si hay más bytes (`0`) o si es el último (`1`).

Por ejemplo $15478$ en binario es `11110001110110`. Dividido en grupos de 7 bits desde la derecha:

- `1111000 1110110`

Se utiliza el bit más significativo para indicar si hay más bytes:

- `0_1111000 1_1110110`

```{code-cell} python
---
tags: remove-output
---
def vb_encode_number(n: int) -> list[int]:
    """Codifica un número usando Variable Byte Encoding"""
    bytes_list = []
    while True:
        bytes_list = [n % 128] + bytes_list
        if n < 128:
            break
        n //= 128

    # El último byte tiene el bit de continuación en 1.
    bytes_list[-1] += 128

    return bytes_list


def vb_encode(numbers: list[int]) -> list[list[int]]:
    return [vb_encode_number(n) for n in numbers]


def vb_decode_number(bytes_list: list[int]) -> int:
    """Decodifica una lista de bytes en Variable Byte Encoding"""
    n = 0
    for byte in bytes_list:
        if byte < 128:
            n = n * 128 + byte
        else:
            n = n * 128 + (byte - 128)

    return n


def vb_decode(bytestream):
    return [vb_decode_number(bytes_list) for bytes_list in bytestream]
```

```{code-cell} python
numbers = [15478, 396, 2076, 32173, 111, 9767]

int_size = 32  # Enteros de 32 bits (4 bytes)

print(f" {'Número':>7} {'Bytes VB':>27} {'Bits originales':>16} {'Bits VB':>8}")
print("-" * 62)

for orig, encoded in zip(numbers, vb_encode(numbers)):
    vb_size = len(encoded) * 8

    # Mostrar en binario
    encoded_bin = " ".join(format(byte, "08b") for byte in encoded)
    print(f" {orig:>7} {encoded_bin:>27} {int_size:>16} {vb_size:>8}")
```

Codificar todos los _gaps_.

```{code-cell} python
postings = [3, 12, 15, 27, 35, 89, 142, 156, 299, 312]
gaps = [curr - prev for prev, curr in zip([0] + postings, postings)]

original_postings_size = len(postings) * 4  # enteros de 32 bits
encoded_gaps = vb_encode(gaps)
encoded_gaps_size = sum(len(encoded_gap) for encoded_gap in encoded_gaps)

print(f"               Gaps: {gaps}")
print(f"           Bytes VB: {encoded_gaps}")
print(f"    Tamaño original: {original_postings_size} bytes")
print(f"  Tamaño comprimido: {encoded_gaps_size} bytes")
print(f"Ratio de compresión: {original_postings_size / encoded_gaps_size:.2f}x")
```

## _Trade-offs_ de la compresión

La compresión de índices implica compromisos:

**Ventajas:**

- Reducción significativa del espacio en disco
- Menos transferencia de datos disco-memoria
- Posible mejora en velocidad (menos I/O)

**Desventajas:**

- Overhead de CPU para comprimir/descomprimir
- Código más complejo
- No se puede acceder aleatoriamente sin descomprimir

En la práctica, técnicas como _Variable Byte Encoding_ son muy populares porque ofrecen un buen balance entre compresión y velocidad de decodificación.

## Resumen

La compresión de índices es esencial para manejar grandes colecciones de documentos. Técnicas como _Front Coding_ para el diccionario y _gap_ encoding combinado con _Variable Byte Encoding_ para las listas de postings permiten reducir significativamente el tamaño del índice mientras mantienen un rendimiento aceptable en las consultas.

La elección de técnicas depende de:

- Tamaño de la colección
- Patrones de consulta
- Balance CPU vs espacio
- Requisitos de velocidad

En sistemas reales como Lucene/Elasticsearch, se combinan múltiples técnicas para lograr compresión de 3-5x mientras mantienen excelente rendimiento de búsqueda.

## Referencias y recursos adicionales

### Colecciones de datos

- [ClueWeb Dataset](https://lemurproject.org/clueweb09/): Colección grande para experimentación
- [TREC Collections](https://trec.nist.gov/data.html): Colecciones estándar para IR
- [Lemur Project](https://www.lemurproject.org/): Herramientas y librerías para IR

### Cursos y tutoriales

- [Information Retrieval - Stanford CS276](https://web.stanford.edu/class/cs276/): Incluye material sobre compresión
- [Text Compression - University of Melbourne](https://people.eng.unimelb.edu.au/ammoffat/): Recursos de Alistair Moffat

### Bibliografía principal

- El Capítulo 5 del libro {cite:p}`irbook` presenta los conceptos de compresión de índices.
- El siguiente artículo estudia los índices para motores de búsqueda de texto.{cite:p}`zobel2006`
- En el artículo se presenta la compresión de índices e imágenes {cite:p}`witten1999`. Está disponible en internet.
