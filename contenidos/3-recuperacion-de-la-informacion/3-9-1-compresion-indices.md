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

# Compresión de Índices

```{code-cell} python
---
tags: [hide-output, remove-cell]
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

La **compresión de índices** es una técnica fundamental para reducir el espacio ocupado por índices invertidos. Cuando trabajamos con colecciones grandes de documentos (como un motor de búsqueda web que indexa miles de millones de páginas), el tamaño del índice puede ser enorme. Comprimir el índice no solo ahorra espacio en disco, sino que también puede mejorar el rendimiento al reducir las transferencias de datos entre disco y memoria.

## Motivación

Consideremos un ejemplo real: un motor de búsqueda que indexa mil millones de páginas web. Si cada página contiene en promedio 1000 términos únicos, y cada término aparece en promedio en 10,000 páginas, el índice invertido necesitaría almacenar aproximadamente:

- **Diccionario**: 10 millones de términos × 10 bytes = 100 MB
- **Listas de postings**: 10 millones de términos × 10,000 documentos × 4 bytes (un entero) = 400 GB

Esto es solo para almacenar los IDs de documentos. Agregar información adicional como frecuencias de términos o posiciones incrementa aún más el tamaño. La compresión puede reducir este espacio a una fracción del original.

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo: cálculo del tamaño sin compresión
num_terminos = 10_000_000
docs_por_termino = 10_000
bytes_por_id = 4  # Entero de 32 bits

tamaño_postings_gb = (num_terminos * docs_por_termino * bytes_por_id) / (1024**3)
print(f"Tamaño estimado de postings sin compresión: {tamaño_postings_gb:.2f} GB")

# Con compresión típica (factor 4x)
tamaño_comprimido_gb = tamaño_postings_gb / 4
print(f"Tamaño con compresión: {tamaño_comprimido_gb:.2f} GB")
print(f"Ahorro: {tamaño_postings_gb - tamaño_comprimido_gb:.2f} GB")
```

Se puede comprimir tanto el diccionario de términos o Vocabulario como las listas de postings asociadas a cada término.

## Compresión del Diccionario de Términios

El diccionario contiene todos los términos únicos. Aunque es relativamente pequeño comparado con las listas de postings, su compresión sigue siendo importante.

### Técnicas para Comprimir el Diccionario

#### Cadena Única de Términos

La primera técnica consiste en almacenar todos los términos como si fueran una única cadena de caracteres:

- Guardar todas las palabras del diccionario como una larga cadena de caracteres.
- Se le asocia una estructura de datos de longitud fija para la frecuencia, la referencia a la lista de apariciones (postings) y la referencia al término en la cadena.
- La referencia al próximo término marca el final del término corriente.

```{figure} ../assets/images/IICompresionTerminos.png
---
name: ii-compresion-terminos
---
Compresión del diccionario de términos usando una cadena única.
```

En la figura anterior se observa como se almacenan los términos "programa", ***"programable"***, ***"programación"***, ***"programador"*** y ***"programar"*** en una sola cadena. Cada término se referencia mediante un puntero que indica su posición inicial, la palabra termina justo antes del siguiente puntero.

Con este esquema si se utilizan 4 bytes para la frecuencia, 4 bytes para la referencia a la lista de postings y 4 bytes para la referencia al término, se utilizan 12 bytes por término en el diccionario. Si el diccionario tiene 1 millón de términos, se utilizan 12 MB para almacenar el diccionario más el espacio necesario para la cadena de caracteres.

En memoria se carga la cadena completa y los punteros permiten acceder a cada término. Sin embargo, aún se puede mejorar la compresión del diccionario.

#### Front Coding

Front Coding es una técnica que aprovecha los prefijos comunes entre términos consecutivos en orden lexicográfico aprovechando el hecho que, generalmente, las palabras ordenadas alfabéticamente comparten un prefijo común.

Se agrupan las entradas del diccionario en bloques de k términos contiguos. En cada bloque se almacena primero el término base completo; a continuación se coloca un separador '\*' que delimita el prefijo base y marca el final de ese primer término. Para los términos restantes del bloque no se repite el prefijo: se escribe un símbolo '⋄' que indica el punto donde termina el prefijo común y, a continuación, el sufijo que completa cada término. Antes de cada término completo o de cada sufijo se guarda su longitud en un byte (1 B). En la estructura auxiliar solo se mantiene la referencia (puntero) al primer término de cada bloque; el resto de términos se recupera a partir de la cadena combinada.

Por ejemplo si las palabras son: algoritmo, alguacil, alguien, algas y alguno y k=5, se alamacenan como:

```text
5alg*as6•oritmo5•uacil4•uien3•uno
```

- La primera palabra "algas" se almacena completa precedida por su longitud (5). Se añade un "\*" en el medio de la palabra para indicar el final del prefijo común "alg" para todo el bloque de 5 términos.
- La segunda palabra "algoritmo" se almacena como "6•oritmo", donde "6" es la longitud del sufijo "oritmo" y "•" indica el final del prefijo común.
- La tercera palabra "alguacil" se almacena como "5•uacil".
- La cuarta palabra "alguien" se almacena como "4•uien".
- La quinta palabra "alguno" se almacena como "3•uno".

```{code-cell} python
---
tags: [hide-output]
---
# Implementación de Front Coding para el bloque de ejemplo

def common_prefix(strings):
    """Devuelve el prefijo común más largo de una lista de strings."""
    if not strings:
        return ""
    s1, s2 = min(strings), max(strings)
    for i, ch in enumerate(s1):
        if i >= len(s2) or ch != s2[i]:
            return s1[:i]
    return s1

def front_encode_block(terms):
    """
    Codifica un bloque de términos usando front coding.
    Formato: <len_base><prefijo>*<sufijo_base>{<len_suf>•<sufijo>}...
    """
    if not terms:
        return ""
    prefix = common_prefix(terms)
    base = terms[0]
    base_suffix = base[len(prefix):]
    encoded = f"{len(base)}{prefix}*{base_suffix}"
    for term in terms[1:]:
        suf = term[len(prefix):]
        encoded += f"{len(suf)}•{suf}"
    return encoded

def front_decode_block(encoded):
    """Decodifica la cadena generada por front_encode_block y devuelve la lista de términos."""
    import re
    if not encoded:
        return []
    m = re.match(r'(\d+)', encoded)
    if not m:
        raise ValueError("Formato inválido: no se encontró la longitud del término base")
    base_len = int(m.group(1))
    rest = encoded[m.end():]
    # buscar '*' que separa prefijo y sufijo del término base
    star_idx = rest.find('*')
    if star_idx == -1:
        raise ValueError("Formato inválido: falta '*'")
    prefix = rest[:star_idx]
    # calcular sufijo del base usando la longitud indicada
    base_suffix_len = base_len - len(prefix)
    base_suffix = rest[star_idx+1:star_idx+1+base_suffix_len]
    base = prefix + base_suffix
    terms = [base]
    rem = rest[star_idx+1+base_suffix_len:]
    i = 0
    while i < len(rem):
        # leer número de longitud del sufijo
        j = i
        while j < len(rem) and rem[j].isdigit():
            j += 1
        if j == i:
            raise ValueError("Formato inválido al leer longitud de sufijo")
        num = int(rem[i:j])
        if j >= len(rem) or rem[j] != '•':
            raise ValueError("Formato inválido: falta '•' separador")
        suf = rem[j+1:j+1+num]
        terms.append(prefix + suf)
        i = j+1+num
    return terms

# Ejemplo con las palabras solicitadas
palabras = ["algas", "algoritmo", "alguacil", "alguien", "alguno"]

encoded = front_encode_block(palabras)
decoded = front_decode_block(encoded)

print("Palabras originales:", palabras)
print("Encoded:", encoded)
print("Decoded:", decoded)
assert decoded == palabras, "La decodificación no coincide con las palabras originales"

# Estadísticas de compresión (bytes en UTF-8)
original_bytes = sum(len(p.encode('utf-8')) for p in palabras)
comprimido_bytes = len(encoded.encode('utf-8'))
print(f"\nTamaño original: {original_bytes} bytes")
print(f"Tamaño front coding: {comprimido_bytes} bytes")
print(f"Ratio: {original_bytes / comprimido_bytes:.2f}x")
```

## Compresión de Listas de Postings

Las listas de postings contienen los IDs de documentos donde aparece cada término. La compresión de las listas de postings es crucial ya que es la que tiene mayor impacto en el tamaño total del índice.

### Gap Encoding (Codificación de Diferencias)

En lugar de almacenar los IDs completos, almacenamos las diferencias (gaps) entre IDs consecutivos. Como los IDs están ordenados, los gaps suelen ser números pequeños.

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo de gap encoding
doc_ids = [15478, 15874, 17950, 50123, 50234, 60001]

print("IDs originales:")
print(doc_ids)

# Convertir a gaps
gaps = [doc_ids[0]]  # Primer ID se mantiene
for i in range(1, len(doc_ids)):
    gaps.append(doc_ids[i] - doc_ids[i-1])

print("\nGaps (diferencias):")
print(gaps)

# Comparar tamaños (asumiendo que usamos el mínimo de bits necesarios)
import math

def bits_necesarios(numero):
    """Calcula bits necesarios para representar un número"""
    if numero == 0:
        return 1
    return math.ceil(math.log2(numero + 1))

bits_originales = sum(bits_necesarios(id) for id in doc_ids)
bits_gaps = sum(bits_necesarios(gap) for gap in gaps)

print(f"\nBits necesarios:")
print(f"  IDs originales: {bits_originales} bits")
print(f"  Con gaps: {bits_gaps} bits")
print(f"  Ahorro: {100 * (1 - bits_gaps / bits_originales):.1f}%")
```

### Variable Byte Encoding (VB)

Otra técnica popular es Variable Byte encoding, que usa uno o más bytes para representar un número, dependiendo de su tamaño, así la cantidad de bytes para codificar el gap entre el id de un documento y el siguiente varía según el valor del gap.

- Cada byte tiene 7 bits de datos y 1 bit de continuación
- Bit de continuación = 1: hay más bytes
- Bit de continuación = 0: es el último byte

Asi por ejemplo la representación de los siguientes gaps `[15478, 396, 2076, 32173, 111, 9767]` sería:

- 15478 → `10000011 10111110 00101110` (3 bytes)
- 396 → `10000010 01100100` (2 bytes)
- 2076 → `10000010 00001000 00000100` (3 bytes)
- 32173 → `10000011 11111010 00101101` (3 bytes)
- 111 → `01101111` (1 byte)
- 9767 → `10000010 00101110 00000111` (3 bytes)

Se parte de la representación en binario del número y se divide en grupos de 7 bits, cada grupo se almacena en un byte. El bit más significativo, es decir el primer bit del un byte de 8 bits, se usa para indicar si hay más bytes (1) o si es el último (0).

Por ejemplo 15478 en binario es `11110001110110`. Dividido en grupos de 7 bits desde la derecha:

- `0000011_0111100_0001110`

Se utliza el bit más significativo para indicar si hay más bytes:

- `10000011_10111100_00000011`

```{code-cell} python
---
tags: [hide-output]
---
def vb_encode(numero):
    """Codifica un número usando Variable Byte encoding"""
    if numero == 0:
        return [0]
    
    bytes_list = []
    while numero > 0:
        bytes_list.insert(0, numero % 128)  # 7 bits de datos
        numero //= 128
    
    # El último byte tiene el bit de continuación en 0
    # Los demás tienen el bit en 1 (sumamos 128)
    for i in range(len(bytes_list) - 1):
        bytes_list[i] += 128
    
    return bytes_list

def vb_decode(bytes_list):
    """Decodifica una lista de bytes en Variable Byte encoding"""
    numero = 0
    for byte in bytes_list:
        if byte < 128:
            # Es el último byte
            numero = numero * 128 + byte
            break
        else:
            # Hay más bytes, quitar el bit de continuación
            numero = numero * 128 + (byte - 128)
    return numero

# Ejemplos
numeros = [5, 127, 128, 130, 1000, 16383]

print("Variable Byte Encoding:")
print(f"{'Número':<10} {'Bytes VB':<25} {'Bits originales':<20} {'Bits VB'}")
print("-" * 75)

for num in numeros:
    encoded = vb_encode(num)
    bits_orig = 32  # Entero de 32 bits típico
    bits_vb = len(encoded) * 8
    
    # Mostrar en binario
    encoded_bin = ' '.join(format(b, '08b') for b in encoded)
    print(f"{num:<10} {encoded_bin:<25} {bits_orig:<20} {bits_vb}")

# Ejemplo de compresión de una lista completa
print("\n\nCompresión de lista de postings:")
postings = [3, 12, 15, 27, 35, 89, 142, 156, 299, 312]
gaps = [postings[0]] + [postings[i] - postings[i-1] for i in range(1, len(postings))]

print(f"Postings originales: {postings}")
print(f"Gaps: {gaps}")

# Codificar todos los gaps
encoded_all = []
for gap in gaps:
    encoded_all.extend(vb_encode(gap))

print(f"\nBytes VB: {encoded_all}")
print(f"Tamaño original: {len(postings) * 4} bytes (enteros de 32 bits)")
print(f"Tamaño comprimido: {len(encoded_all)} bytes")
print(f"Ratio de compresión: {len(postings) * 4 / len(encoded_all):.2f}x")
```

## Trade-offs de la Compresión

La compresión de índices implica compromisos:

**Ventajas:**

- Reducción significativa del espacio en disco
- Menos transferencia de datos disco-memoria
- Posible mejora en velocidad (menos I/O)

**Desventajas:**

- Overhead de CPU para comprimir/descomprimir
- Código más complejo
- No se puede acceder aleatoriamente sin descomprimir

En la práctica, técnicas como Variable Byte son muy populares porque ofrecen un buen balance entre compresión y velocidad de decodificación.

## Resumen

La compresión de índices es esencial para manejar grandes colecciones de documentos. Técnicas como front coding para el diccionario y gap encoding combinado con Variable Byte para las listas de postings permiten reducir significativamente el tamaño del índice mientras mantienen un rendimiento aceptable en las consultas.

La elección de técnicas depende de:

- Tamaño de la colección
- Patrones de consulta
- Balance CPU vs espacio
- Requisitos de velocidad

En sistemas reales como Lucene/Elasticsearch, se combinan múltiples técnicas para lograr compresión de 3-5x mientras mantienen excelente rendimiento de búsqueda.

## Referencias y Recursos Adicionales

### Bibliografía Principal

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. Capítulo 5.{cite:p}`irbook`

- Zobel, J., & Moffat, A. (2006). "Inverted files for text search engines". *ACM Computing Surveys (CSUR)*, 38(2), 1-56.{cite:p}`zobel2006`

- Witten, I. H., Moffat, A., & Bell, T. C. (1999). *Managing Gigabytes: Compressing and Indexing Documents and Images*. Morgan Kaufmann. Capítulo 7.{cite:p}`witten1999`

- [ClueWeb Dataset](https://lemurproject.org/clueweb09/){target="\_blank"}: Colección grande para experimentación

- [TREC Collections](https://trec.nist.gov/data.html){target="\_blank"}: Colecciones estándar para IR

- [Lemur Project](https://www.lemurproject.org/){target="\_blank"}: Herramientas y librerías para IR

### Cursos y Tutoriales

- [Information Retrieval - Stanford CS276](https://web.stanford.edu/class/cs276/){target="\_blank"}: Incluye material sobre compresión

- [Text Compression - University of Melbourne](https://people.eng.unimelb.edu.au/ammoffat/){target="\_blank"}: Recursos de Alistair Moffat
