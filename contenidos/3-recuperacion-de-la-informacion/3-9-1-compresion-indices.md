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

Consideremos un ejemplo real: un motor de búsqueda que indexa 1 mil millones de páginas web. Si cada página contiene en promedio 1000 términos únicos, y cada término aparece en promedio en 10,000 páginas, el índice invertido necesitaría almacenar aproximadamente:

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

## Principios de Compresión

La compresión de índices se basa en dos principios fundamentales:

1. **Ley de Zipf**: En texto natural, algunos términos son mucho más frecuentes que otros. El término más frecuente aparece aproximadamente el doble de veces que el segundo más frecuente, tres veces más que el tercero, etc.

2. **Localidad**: Los IDs de documentos en las listas de postings a menudo están espacialmente relacionados, por lo que almacenar diferencias (gaps) en lugar de valores absolutos resulta en números más pequeños.

```{code-cell} python
---
tags: [hide-output]
---
import matplotlib.pyplot as plt

# Simulación de la Ley de Zipf
def generar_frecuencias_zipf(n_terminos):
    """Genera frecuencias siguiendo la Ley de Zipf"""
    frecuencias = []
    for i in range(1, n_terminos + 1):
        frecuencias.append(1 / i)
    return frecuencias

# Visualizar
n = 50
freqs = generar_frecuencias_zipf(n)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(range(1, n + 1), freqs, 'b-')
plt.xlabel('Ranking del término')
plt.ylabel('Frecuencia relativa')
plt.title('Ley de Zipf (escala lineal)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.loglog(range(1, n + 1), freqs, 'r-')
plt.xlabel('Ranking del término (log)')
plt.ylabel('Frecuencia relativa (log)')
plt.title('Ley de Zipf (escala logarítmica)')
plt.grid(True)

plt.tight_layout()
plt.savefig('/tmp/zipf.png', dpi=80, bbox_inches='tight')
plt.close()

print("La Ley de Zipf muestra que pocos términos son muy frecuentes")
print("y muchos términos son raros. Esto permite optimizar la compresión.")
```

## Compresión del Diccionario

El diccionario contiene todos los términos únicos. Aunque es relativamente pequeño comparado con las listas de postings, su compresión sigue siendo importante.

### Técnicas para Comprimir el Diccionario

1. **Prefijos compartidos**: Los términos en un diccionario ordenado alfabéticamente comparten prefijos comunes.

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo de prefijos compartidos
terminos = ['programación', 'programador', 'programar', 'programa', 'proyecto']

print("Términos originales:")
for t in terminos:
    print(f"  {t} ({len(t)} caracteres)")

print(f"\nTotal sin compresión: {sum(len(t) for t in terminos)} caracteres")

# Compresión usando prefijos compartidos
def comprimir_prefijos(terminos):
    """Comprime términos usando prefijos compartidos"""
    if not terminos:
        return []
    
    comprimido = []
    prev = ""
    
    for termino in terminos:
        # Encontrar longitud del prefijo común
        prefijo_len = 0
        for i in range(min(len(prev), len(termino))):
            if prev[i] == termino[i]:
                prefijo_len += 1
            else:
                break
        
        # Guardar: (longitud prefijo común, sufijo único)
        sufijo = termino[prefijo_len:]
        comprimido.append((prefijo_len, sufijo))
        prev = termino
    
    return comprimido

comprimido = comprimir_prefijos(terminos)
print("\nCompresión con prefijos:")
for i, (pref_len, sufijo) in enumerate(comprimido):
    print(f"  {terminos[i]}: prefijo={pref_len}, sufijo='{sufijo}'")

# Calcular ahorro
chars_comprimido = sum(len(sufijo) + 1 for _, sufijo in comprimido)  # +1 por el número
print(f"\nCaracteres después de compresión: ~{chars_comprimido}")
print(f"Reducción: ~{100 * (1 - chars_comprimido / sum(len(t) for t in terminos)):.1f}%")
```

2. **Front coding**: Una variante más eficiente que agrupa términos en bloques.

```{code-cell} python
---
tags: [hide-output]
---
def front_coding(terminos, tamaño_bloque=3):
    """Implementa front coding con bloques"""
    bloques = []
    
    for i in range(0, len(terminos), tamaño_bloque):
        bloque_terminos = terminos[i:i + tamaño_bloque]
        
        # Primer término del bloque se guarda completo
        primer_termino = bloque_terminos[0]
        bloque = [primer_termino]
        
        # Resto se guarda como diferencias
        for termino in bloque_terminos[1:]:
            prefijo_len = 0
            for j in range(min(len(primer_termino), len(termino))):
                if primer_termino[j] == termino[j]:
                    prefijo_len += 1
                else:
                    break
            sufijo = termino[prefijo_len:]
            bloque.append((prefijo_len, sufijo))
        
        bloques.append(bloque)
    
    return bloques

# Ejemplo
terminos_largos = [
    'algoritmo', 'algoritmos', 'algebra', 'algebraico',
    'buscar', 'busqueda', 'bueno', 'buenos'
]

bloques = front_coding(terminos_largos, tamaño_bloque=4)

print("Front coding con bloques de 4:")
for i, bloque in enumerate(bloques):
    print(f"\nBloque {i + 1}:")
    print(f"  Base: '{bloque[0]}'")
    for j, item in enumerate(bloque[1:], 1):
        print(f"  + ({item[0]}, '{item[1]}')")
```

## Compresión de Listas de Postings

Las listas de postings contienen los IDs de documentos donde aparece cada término. Esta es la parte más grande del índice y donde la compresión tiene mayor impacto.

### Gap Encoding (Codificación de Diferencias)

En lugar de almacenar los IDs completos, almacenamos las diferencias (gaps) entre IDs consecutivos. Como los IDs están ordenados, los gaps suelen ser números pequeños.

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo de gap encoding
doc_ids = [5, 13, 23, 34, 55, 89, 144]

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

Una técnica simple y eficiente es usar **codificación de bytes variables** donde usamos un bit de continuación para indicar si hay más bytes por leer.

- Cada byte tiene 7 bits de datos y 1 bit de continuación
- Bit de continuación = 1: hay más bytes
- Bit de continuación = 0: es el último byte

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

### Gamma Encoding (γ-codes)

Los **Gamma codes** de Elias son otra técnica que usa longitud variable óptima para números pequeños.

Para codificar un número N:
1. Encontrar la longitud L = ⌊log₂(N)⌋
2. Escribir L ceros seguidos de un 1
3. Escribir N en binario sin el bit más significativo

```{code-cell} python
---
tags: [hide-output]
---
def gamma_encode(numero):
    """Codifica un número usando Elias Gamma encoding"""
    if numero < 1:
        raise ValueError("Gamma encoding requiere números >= 1")
    
    # Encontrar longitud en binario
    longitud = numero.bit_length() - 1
    
    # Parte 1: unary code de la longitud (longitud ceros + un 1)
    unary = '0' * longitud + '1'
    
    # Parte 2: número en binario sin el bit más significativo
    if longitud > 0:
        binario = format(numero, 'b')[1:]  # Quitar el primer bit
    else:
        binario = ''
    
    return unary + binario

def gamma_decode(codigo):
    """Decodifica un string binario en Gamma encoding"""
    # Contar ceros hasta el primer 1
    longitud = 0
    i = 0
    while i < len(codigo) and codigo[i] == '0':
        longitud += 1
        i += 1
    
    # Saltar el 1
    i += 1
    
    # Leer los siguientes 'longitud' bits
    if longitud == 0:
        return 1
    
    binario = '1' + codigo[i:i + longitud]
    return int(binario, 2)

# Ejemplos
print("Gamma Encoding:")
print(f"{'Número':<10} {'Código Gamma':<20} {'Bits'}")
print("-" * 40)

for num in [1, 2, 3, 4, 5, 10, 17, 100]:
    codigo = gamma_encode(num)
    bits = len(codigo)
    print(f"{num:<10} {codigo:<20} {bits}")

# Verificar decodificación
print("\nVerificación de decodificación:")
for num in [1, 5, 17]:
    codigo = gamma_encode(num)
    decodificado = gamma_decode(codigo)
    print(f"{num} → '{codigo}' → {decodificado} {'✓' if num == decodificado else '✗'}")
```

### Delta Encoding (δ-codes)

Los **Delta codes** son una mejora sobre Gamma codes, más eficientes para números moderadamente grandes.

```{code-cell} python
---
tags: [hide-output]
---
def delta_encode(numero):
    """Codifica un número usando Elias Delta encoding"""
    if numero < 1:
        raise ValueError("Delta encoding requiere números >= 1")
    
    # Encontrar longitud del número en binario
    longitud = numero.bit_length()
    
    # Codificar la longitud usando gamma
    gamma_longitud = gamma_encode(longitud)
    
    # Número en binario sin el bit más significativo
    if longitud > 1:
        binario = format(numero, 'b')[1:]
    else:
        binario = ''
    
    return gamma_longitud + binario

# Comparar Gamma vs Delta
print("Comparación Gamma vs Delta:")
print(f"{'Número':<10} {'Gamma':<25} {'Delta':<25} {'Mejor'}")
print("-" * 75)

for num in [1, 2, 5, 10, 50, 100, 500, 1000]:
    gamma = gamma_encode(num)
    delta = delta_encode(num)
    mejor = "Gamma" if len(gamma) <= len(delta) else "Delta"
    
    print(f"{num:<10} {gamma:<25} {delta:<25} {mejor} ({abs(len(gamma) - len(delta))} bits)")
```

## Índice Invertido con Compresión

Implementemos un índice invertido que use compresión de postings:

```{code-cell} python
---
tags: [hide-output]
---
from collections import defaultdict

class IndiceInvertidoComprimido:
    """Índice invertido con compresión de postings usando VB encoding"""
    
    def __init__(self):
        self.diccionario = {}
        self.postings_comprimidas = {}
        self.documentos = {}
        self.proximo_id = 1
    
    def vb_encode_list(self, numeros):
        """Codifica una lista de números con VB encoding"""
        resultado = []
        for num in numeros:
            resultado.extend(self._vb_encode(num))
        return bytes(resultado)
    
    def vb_decode_list(self, bytes_data):
        """Decodifica bytes VB en una lista de números"""
        numeros = []
        i = 0
        while i < len(bytes_data):
            numero = 0
            while i < len(bytes_data):
                byte = bytes_data[i]
                i += 1
                if byte < 128:
                    numero = numero * 128 + byte
                    break
                else:
                    numero = numero * 128 + (byte - 128)
            numeros.append(numero)
        return numeros
    
    def _vb_encode(self, numero):
        """Encode un solo número con VB"""
        if numero == 0:
            return [0]
        bytes_list = []
        while numero > 0:
            bytes_list.insert(0, numero % 128)
            numero //= 128
        for i in range(len(bytes_list) - 1):
            bytes_list[i] += 128
        return bytes_list
    
    def agregar_documento(self, texto):
        """Agrega un documento y retorna su ID"""
        doc_id = self.proximo_id
        self.proximo_id += 1
        self.documentos[doc_id] = texto
        
        # Tokenizar
        palabras = texto.lower().split()
        
        # Agregar al índice temporal (sin comprimir aún)
        if not hasattr(self, '_indice_temp'):
            self._indice_temp = defaultdict(set)
        
        for palabra in palabras:
            palabra = palabra.strip('.,;:!?')
            if palabra:
                self._indice_temp[palabra].add(doc_id)
        
        return doc_id
    
    def construir_indice(self):
        """Construye el índice final comprimido"""
        for termino, doc_ids in self._indice_temp.items():
            # Ordenar IDs
            ids_ordenados = sorted(doc_ids)
            
            # Convertir a gaps
            gaps = [ids_ordenados[0]]
            for i in range(1, len(ids_ordenados)):
                gaps.append(ids_ordenados[i] - ids_ordenados[i-1])
            
            # Comprimir con VB
            comprimido = self.vb_encode_list(gaps)
            
            # Guardar
            self.diccionario[termino] = len(ids_ordenados)  # Frecuencia
            self.postings_comprimidas[termino] = comprimido
        
        # Limpiar índice temporal
        del self._indice_temp
    
    def buscar(self, termino):
        """Busca un término y retorna los IDs de documentos"""
        termino = termino.lower().strip('.,;:!?')
        
        if termino not in self.postings_comprimidas:
            return set()
        
        # Descomprimir
        gaps = self.vb_decode_list(self.postings_comprimidas[termino])
        
        # Reconstruir IDs desde gaps
        doc_ids = [gaps[0]]
        for i in range(1, len(gaps)):
            doc_ids.append(doc_ids[-1] + gaps[i])
        
        return set(doc_ids)
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del índice"""
        tamaño_sin_comprimir = 0
        tamaño_comprimido = 0
        
        for termino, freq in self.diccionario.items():
            tamaño_sin_comprimir += freq * 4  # 4 bytes por ID
            tamaño_comprimido += len(self.postings_comprimidas[termino])
        
        return {
            'num_terminos': len(self.diccionario),
            'num_documentos': len(self.documentos),
            'tamaño_sin_comprimir': tamaño_sin_comprimir,
            'tamaño_comprimido': tamaño_comprimido,
            'ratio_compresion': tamaño_sin_comprimir / tamaño_comprimido if tamaño_comprimido > 0 else 0
        }


# Crear y probar el índice comprimido
print("=== Índice Invertido con Compresión ===\n")

indice_comp = IndiceInvertidoComprimido()

# Agregar documentos
documentos_texto = [
    "Python es un lenguaje de programación interpretado",
    "Java es un lenguaje de programación compilado",
    "Python y Java son lenguajes orientados a objetos",
    "JavaScript es diferente de Java",
    "Python se usa mucho en ciencia de datos",
    "Machine learning con Python y TensorFlow",
    "Django es un framework web de Python",
    "Spring es un framework de Java",
    "Python tiene sintaxis simple y clara",
    "Java requiere más código que Python"
]

for texto in documentos_texto:
    indice_comp.agregar_documento(texto)

# Construir índice comprimido
indice_comp.construir_indice()

# Estadísticas
stats = indice_comp.obtener_estadisticas()
print(f"Documentos indexados: {stats['num_documentos']}")
print(f"Términos únicos: {stats['num_terminos']}")
print(f"\nTamaño sin compresión: {stats['tamaño_sin_comprimir']} bytes")
print(f"Tamaño comprimido: {stats['tamaño_comprimido']} bytes")
print(f"Ratio de compresión: {stats['ratio_compresion']:.2f}x")
print(f"Ahorro: {100 * (1 - 1/stats['ratio_compresion']):.1f}%")

# Probar búsquedas
print("\n=== Búsquedas ===")
terminos_busqueda = ["python", "java", "framework"]
for termino in terminos_busqueda:
    docs = indice_comp.buscar(termino)
    print(f"\n'{termino}': encontrado en documentos {sorted(docs)}")
    for doc_id in sorted(docs):
        print(f"  [{doc_id}] {indice_comp.documentos[doc_id]}")
```

## Comparación de Técnicas

Cada técnica de compresión tiene sus ventajas:

```{code-cell} python
---
tags: [hide-output]
---
import sys

# Función auxiliar para VB encoding
def vb_encode_numero(numero):
    """Codifica un número con VB encoding"""
    if numero == 0:
        return [0]
    bytes_list = []
    while numero > 0:
        bytes_list.insert(0, numero % 128)
        numero //= 128
    for i in range(len(bytes_list) - 1):
        bytes_list[i] += 128
    return bytes_list

# Comparar técnicas para una lista de postings típica
postings = [1, 5, 8, 15, 23, 45, 67, 89, 123, 156, 234, 456, 789, 1234]
gaps = [postings[0]] + [postings[i] - postings[i-1] for i in range(1, len(postings))]

print("Comparación de técnicas de compresión:\n")
print(f"Postings: {postings}")
print(f"Gaps: {gaps}\n")

# Sin compresión (32 bits por número)
sin_compresion = len(postings) * 4
print(f"Sin compresión: {sin_compresion} bytes ({sin_compresion * 8} bits)")

# Variable Byte
vb_bytes = []
for gap in gaps:
    vb_bytes.extend(vb_encode_numero(gap))

print(f"Variable Byte: {len(vb_bytes)} bytes ({len(vb_bytes) * 8} bits)")
print(f"  Ratio: {sin_compresion / len(vb_bytes):.2f}x")

# Gamma encoding
gamma_bits = 0
for gap in gaps:
    if gap > 0:
        longitud = gap.bit_length() - 1
        gamma_bits += 2 * longitud + 1

gamma_bytes = (gamma_bits + 7) // 8  # Redondear hacia arriba
print(f"Gamma encoding: {gamma_bytes} bytes ({gamma_bits} bits)")
print(f"  Ratio: {sin_compresion / gamma_bytes:.2f}x")

# Delta encoding  
delta_bits = 0
for gap in gaps:
    if gap > 0:
        longitud = gap.bit_length()
        # Longitud codificada en gamma
        len_longitud = longitud.bit_length() - 1
        gamma_longitud_bits = 2 * len_longitud + 1
        # Más el número sin el bit más significativo
        numero_bits = longitud - 1 if longitud > 1 else 0
        delta_bits += gamma_longitud_bits + numero_bits

delta_bytes = (delta_bits + 7) // 8
print(f"Delta encoding: {delta_bytes} bytes ({delta_bits} bits)")
print(f"  Ratio: {sin_compresion / delta_bytes:.2f}x")

print("\n=== Resumen ===")
print("Variable Byte: Simple, rápida, buena para números pequeños-medianos")
print("Gamma: Óptima para números muy pequeños, más compleja")
print("Delta: Mejor que Gamma para números más grandes, más compleja")
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

## Optimizaciones Adicionales

### Skip Lists

Para listas de postings muy largas, se pueden agregar **skip pointers** que permiten saltar secciones durante la búsqueda:

```{code-cell} python
---
tags: [hide-output]
---
class PostingListConSkips:
    """Lista de postings con skip pointers para búsquedas eficientes"""
    
    def __init__(self, doc_ids, skip_interval=3):
        self.doc_ids = sorted(doc_ids)
        self.skip_interval = skip_interval
        self.skip_pointers = {}
        
        # Crear skip pointers
        for i in range(0, len(self.doc_ids), skip_interval):
            if i + skip_interval < len(self.doc_ids):
                self.skip_pointers[i] = i + skip_interval
    
    def intersect(self, other):
        """Intersección con otra lista usando skip pointers"""
        resultado = []
        i, j = 0, 0
        
        comparaciones = 0  # Para medir eficiencia
        
        while i < len(self.doc_ids) and j < len(other.doc_ids):
            comparaciones += 1
            
            if self.doc_ids[i] == other.doc_ids[j]:
                resultado.append(self.doc_ids[i])
                i += 1
                j += 1
            elif self.doc_ids[i] < other.doc_ids[j]:
                # Intentar usar skip pointer
                if i in self.skip_pointers and \
                   self.doc_ids[self.skip_pointers[i]] <= other.doc_ids[j]:
                    i = self.skip_pointers[i]
                else:
                    i += 1
            else:
                # Intentar usar skip pointer en other
                if j in other.skip_pointers and \
                   other.doc_ids[other.skip_pointers[j]] <= self.doc_ids[i]:
                    j = other.skip_pointers[j]
                else:
                    j += 1
        
        return resultado, comparaciones


# Ejemplo
list1 = PostingListConSkips([1, 3, 5, 8, 12, 15, 23, 34, 45, 56, 67, 78])
list2 = PostingListConSkips([2, 5, 8, 15, 23, 45, 67, 89])

resultado, comps = list1.intersect(list2)
print(f"Intersección: {resultado}")
print(f"Comparaciones realizadas: {comps}")
print(f"Comparaciones sin skips: {len(list1.doc_ids) + len(list2.doc_ids)}")
```

### Compresión del Diccionario con Front Coding

Ya vimos front coding anteriormente. En índices reales, se combina con otras técnicas:

```{code-cell} python
---
tags: [hide-output]
---
class DiccionarioComprimido:
    """Diccionario con front coding"""
    
    def __init__(self):
        self.bloques = []
        self.termino_a_bloque = {}
    
    def agregar_terminos(self, terminos, tamaño_bloque=4):
        """Agrega términos usando front coding"""
        terminos_ordenados = sorted(terminos)
        
        for i in range(0, len(terminos_ordenados), tamaño_bloque):
            bloque_terminos = terminos_ordenados[i:i + tamaño_bloque]
            bloque_id = len(self.bloques)
            
            # Crear bloque con front coding
            bloque = [bloque_terminos[0]]  # Término base
            
            for termino in bloque_terminos[1:]:
                # Encontrar prefijo común con el término base
                base = bloque[0]
                prefijo_len = 0
                for j in range(min(len(base), len(termino))):
                    if base[j] == termino[j]:
                        prefijo_len += 1
                    else:
                        break
                
                sufijo = termino[prefijo_len:]
                bloque.append((prefijo_len, sufijo))
            
            self.bloques.append(bloque)
            
            # Indexar términos a bloques
            for termino in bloque_terminos:
                self.termino_a_bloque[termino] = bloque_id
    
    def buscar(self, termino):
        """Busca un término en el diccionario"""
        if termino not in self.termino_a_bloque:
            return None
        
        bloque_id = self.termino_a_bloque[termino]
        return bloque_id
    
    def calcular_compresion(self, terminos):
        """Calcula estadísticas de compresión"""
        bytes_sin_comprimir = sum(len(t) for t in terminos)
        
        bytes_comprimidos = 0
        for bloque in self.bloques:
            bytes_comprimidos += len(bloque[0])  # Término base
            for item in bloque[1:]:
                if isinstance(item, tuple):
                    bytes_comprimidos += 1 + len(item[1])  # Prefijo + sufijo
        
        return bytes_sin_comprimir, bytes_comprimidos


# Ejemplo
terminos = [
    'algoritmo', 'algoritmos', 'algebraico', 'algebra',
    'buscar', 'busqueda', 'busquedas', 'bueno',
    'datos', 'dato', 'dataframe', 'database',
    'programar', 'programa', 'programacion', 'programador'
]

dic = DiccionarioComprimido()
dic.agregar_terminos(terminos, tamaño_bloque=4)

sin_comp, con_comp = dic.calcular_compresion(terminos)
print(f"Diccionario con {len(terminos)} términos:")
print(f"  Sin compresión: {sin_comp} bytes")
print(f"  Con front coding: {con_comp} bytes")
print(f"  Ratio: {sin_comp / con_comp:.2f}x")
print(f"  Ahorro: {100 * (1 - con_comp / sin_comp):.1f}%")
```

## Resumen

La compresión de índices es esencial para sistemas de recuperación de información a gran escala:

- **Gap encoding** reduce IDs a diferencias pequeñas
- **Variable Byte** ofrece buen balance compresión/velocidad
- **Gamma/Delta codes** son óptimos en bits pero más lentos
- **Front coding** comprime el diccionario eficientemente
- **Skip pointers** aceleran intersecciones de listas largas

La elección de técnicas depende de:
- Tamaño de la colección
- Patrones de consulta
- Balance CPU vs espacio
- Requisitos de velocidad

En sistemas reales como Lucene/Elasticsearch, se combinan múltiples técnicas para lograr compresión de 3-5x mientras mantienen excelente rendimiento de búsqueda.