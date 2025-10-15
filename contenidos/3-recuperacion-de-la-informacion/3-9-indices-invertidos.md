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

Los **índices invertidos** son la estructura de datos fundamental en los sistemas de recuperación de información modernos. Son utilizados por motores de búsqueda, sistemas de búsqueda en documentos, y cualquier aplicación que necesite encontrar documentos que contengan ciertos términos de manera eficiente.

La idea central es simple pero poderosa: en lugar de ir de documento a documento buscando términos (búsqueda secuencial), creamos una estructura que va de término a documentos. Es decir, para cada término del vocabulario, mantenemos una lista de los documentos donde aparece.

## Motivación

Imaginemos que tenemos una colección de documentos y queremos buscar aquellos que contienen la palabra "Python". Sin un índice, tendríamos que:

1. Leer cada documento completo
2. Buscar la palabra "Python" en cada uno
3. Guardar los documentos que la contengan

Este proceso es extremadamente ineficiente para colecciones grandes. Con un índice invertido, simplemente buscamos "python" en el diccionario y obtenemos directamente la lista de documentos que lo contienen.

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo: búsqueda sin índice (ineficiente)
documentos = {
    1: "Python es un lenguaje de programación",
    2: "Java es un lenguaje orientado a objetos",
    3: "Python y Java son lenguajes populares",
    4: "Machine learning con Python"
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

Como se puede ver, este método requiere examinar cada documento completo. Para colecciones con millones de documentos, esto es impracticable.

## Recuperación Booleana

La **recuperación booleana** es el modelo más simple de recuperación de información. En este modelo, las consultas se formulan como expresiones booleanas con operadores AND, OR y NOT.

Por ejemplo:
- `Python AND programación`: documentos que contienen ambos términos
- `Python OR Java`: documentos que contienen al menos uno de los términos
- `Python AND NOT Java`: documentos que contienen "Python" pero no "Java"

El modelo booleano es determinístico: un documento o bien coincide con la consulta o no. No hay noción de "cuán bien" coincide un documento.

### Ejemplo de Consultas Booleanas

```{code-cell} python
---
tags: [hide-output]
---
# Simulación de recuperación booleana básica
def buscar_and(termino1, termino2, documentos):
    """Busca documentos que contienen ambos términos"""
    docs1 = set(buscar_sin_indice(termino1, documentos))
    docs2 = set(buscar_sin_indice(termino2, documentos))
    return docs1 & docs2  # Intersección

def buscar_or(termino1, termino2, documentos):
    """Busca documentos que contienen al menos uno de los términos"""
    docs1 = set(buscar_sin_indice(termino1, documentos))
    docs2 = set(buscar_sin_indice(termino2, documentos))
    return docs1 | docs2  # Unión

def buscar_not(termino1, termino2, documentos):
    """Busca documentos que contienen termino1 pero no termino2"""
    docs1 = set(buscar_sin_indice(termino1, documentos))
    docs2 = set(buscar_sin_indice(termino2, documentos))
    return docs1 - docs2  # Diferencia

# Ejemplos
print(f"Python AND Java: {buscar_and('Python', 'Java', documentos)}")
print(f"Python OR Java: {buscar_or('Python', 'Java', documentos)}")
print(f"Python AND NOT Java: {buscar_not('Python', 'Java', documentos)}")
```

Aunque este enfoque funciona, sigue siendo ineficiente porque realiza búsquedas secuenciales. Los índices invertidos resuelven este problema.

## Estructura del Índice Invertido

Un índice invertido consta de dos componentes principales:

1. **Diccionario (o vocabulario)**: Contiene todos los términos únicos que aparecen en la colección
2. **Listas de postings**: Para cada término del diccionario, una lista de documentos donde aparece

```{code-cell} python
---
tags: [hide-output]
---
from collections import defaultdict

class IndiceInvertido:
    """Implementación simple de un índice invertido"""
    
    def __init__(self):
        # Diccionario: término -> conjunto de IDs de documentos
        self.indice = defaultdict(set)
        # Almacena los documentos originales
        self.documentos = {}
    
    def agregar_documento(self, doc_id, texto):
        """Agrega un documento al índice"""
        self.documentos[doc_id] = texto
        
        # Tokenizar el texto en palabras
        palabras = texto.lower().split()
        
        # Agregar cada palabra al índice
        for palabra in palabras:
            # Eliminar puntuación básica
            palabra = palabra.strip('.,;:!?')
            if palabra:  # Ignorar strings vacíos
                self.indice[palabra].add(doc_id)
    
    def buscar(self, termino):
        """Busca documentos que contienen el término"""
        return self.indice.get(termino.lower(), set())
    
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
        for termino in sorted(self.indice.keys()):
            docs = sorted(self.indice[termino])
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

### Búsquedas con el Índice

Ahora podemos realizar búsquedas muy eficientemente:

```{code-cell} python
---
tags: [hide-output]
---
# Búsquedas simples
print(f"\nDocumentos con 'python': {indice.buscar('python')}")
print(f"Documentos con 'lenguaje': {indice.buscar('lenguaje')}")

# Búsquedas booleanas
print(f"\nPython AND Java: {indice.buscar_and('python', 'java')}")
print(f"Python OR Machine: {indice.buscar_or('python', 'machine')}")
print(f"Python AND NOT Java: {indice.buscar_not('python', 'java')}")
```

La diferencia de eficiencia es dramática: en lugar de leer todos los documentos, solo consultamos el diccionario y obtenemos directamente las listas de postings relevantes.

## El Vocabulario y Procesamiento de Términos

En la práctica, el procesamiento de términos es más sofisticado que simplemente convertir a minúsculas y separar por espacios. Los sistemas reales realizan:

### Normalización

Convertir términos a una forma canónica para mejorar las coincidencias:

```{code-cell} python
---
tags: [hide-output]
---
import re

def normalizar_texto(texto):
    """Normaliza un texto para indexación"""
    # Convertir a minúsculas
    texto = texto.lower()
    # Remover puntuación (dejar solo letras, números y espacios)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

# Ejemplo
texto = "¡Python es GENIAL! ¿No lo crees?"
print(f"Original: {texto}")
print(f"Normalizado: {normalizar_texto(texto)}")
```

### Tokenización

Dividir el texto en unidades individuales (tokens):

```{code-cell} python
---
tags: [hide-output]
---
def tokenizar(texto):
    """Tokeniza un texto en palabras"""
    texto_normalizado = normalizar_texto(texto)
    tokens = texto_normalizado.split()
    return tokens

texto = "Python 3.9 es la versión más reciente"
tokens = tokenizar(texto)
print(f"Tokens: {tokens}")
```

### Eliminación de Stopwords

Las **stopwords** son palabras muy frecuentes que aportan poco valor semántico (como "el", "la", "de", "es", etc.). Eliminarlas reduce el tamaño del índice:

```{code-cell} python
---
tags: [hide-output]
---
# Lista básica de stopwords en español
STOPWORDS = {
    'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 
    'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener',
    'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir',
    'este', 'ir', 'otro', 'ese', 'si', 'me', 'ya', 'ver', 'porque',
    'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber', 'qué',
    'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta', 'año',
    'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande', 'eso',
    'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí', 'día', 'uno',
    'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa', 'tanto', 'hombre',
    'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte', 'después', 'vida',
    'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar', 'nada', 'cada',
    'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo', 'ante',
    'cual', 'ellos', 'esto', 'mí', 'antes', 'algunos', 'unos',
    'otras', 'otra', 'esa', 'estos', 'quienes',
    'muchos', 'sea', 'nosotros', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas',
    'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías',
    'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas',
    'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra',
    'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está',
    'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis',
    'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán',
    'es', 'son', 'somos', 'soy'
}

def eliminar_stopwords(tokens):
    """Elimina stopwords de una lista de tokens"""
    return [token for token in tokens if token not in STOPWORDS]

# Ejemplo
texto = "Python es un lenguaje de programación muy popular"
tokens = tokenizar(texto)
tokens_sin_stop = eliminar_stopwords(tokens)

print(f"Tokens originales: {tokens}")
print(f"Sin stopwords: {tokens_sin_stop}")
```

### Stemming y Lematización

El **stemming** reduce las palabras a su raíz o stem (por ejemplo, "programación", "programar", "programador" → "program"). La **lematización** es similar pero usa conocimiento lingüístico para reducir a la forma base (lema).

```{code-cell} python
---
tags: [hide-output]
---
# Stemming simple basado en reglas (muy básico)
def stem_simple(palabra):
    """Stemming muy básico para español"""
    sufijos = ['ación', 'ción', 'ador', 'adora', 'ando', 'iendo', 'ar', 'er', 'ir']
    for sufijo in sufijos:
        if palabra.endswith(sufijo) and len(palabra) > len(sufijo) + 2:
            return palabra[:-len(sufijo)]
    return palabra

# Ejemplos
palabras = ['programación', 'programar', 'programador', 'estudiante', 'estudiar']
for palabra in palabras:
    print(f"{palabra} → {stem_simple(palabra)}")
```

```{note}
Para aplicaciones reales en español, se recomienda usar librerías especializadas como **NLTK** o **spaCy** que implementan algoritmos más sofisticados como el stemmer de Snowball o lematización basada en diccionarios.
```

## Algoritmos de Construcción de Índices

Cuando trabajamos con colecciones grandes de documentos que no caben en memoria RAM, necesitamos algoritmos especializados para construir el índice invertido. Existen tres enfoques principales: BSBI, SPIMI, y construcción distribuida con MapReduce.

### BSBI (Blocked Sort-Based Indexing)

El algoritmo **BSBI** (Blocked Sort-Based Indexing) es una técnica que construye índices cuando la colección de documentos no cabe en memoria. Divide el procesamiento en dos fases:

**Fase 1: Generación de bloques ordenados**
1. Lee documentos en bloques que sí caben en memoria
2. Para cada bloque, extrae pares (término, doc_id)
3. Ordena los pares en memoria
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

```{mermaid}
---
name: mapreduce-indexing
title: Construcción de Índice Invertido con MapReduce
---
flowchart TB
    subgraph Input[Entrada]
        D1[Documento 1]
        D2[Documento 2]
        D3[Documento 3]
        D4[Documento N]
    end
    
    subgraph Map[Fase Map]
        M1[Mapper 1]
        M2[Mapper 2]
        M3[Mapper 3]
        M4[Mapper N]
    end
    
    subgraph Shuffle[Shuffle & Sort]
        S1[Agrupa por término]
        S2[Ordena postings]
    end
    
    subgraph Reduce[Fase Reduce]
        R1[Reducer 1<br/>términos a-f]
        R2[Reducer 2<br/>términos g-m]
        R3[Reducer 3<br/>términos n-z]
    end
    
    subgraph Output[Salida]
        I1[Índice parcial 1]
        I2[Índice parcial 2]
        I3[Índice parcial 3]
    end
    
    D1 --> M1
    D2 --> M2
    D3 --> M3
    D4 --> M4
    
    M1 -->|"(término, doc_id)"| S1
    M2 -->|"(término, doc_id)"| S1
    M3 -->|"(término, doc_id)"| S1
    M4 -->|"(término, doc_id)"| S1
    
    S1 --> S2
    
    S2 -->|término: a-f| R1
    S2 -->|término: g-m| R2
    S2 -->|término: n-z| R3
    
    R1 --> I1
    R2 --> I2
    R3 --> I3
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

| Característica | BSBI | SPIMI | MapReduce |
|----------------|------|-------|-----------|
| **Tamaño de colección** | Mediano (GB) | Mediano (GB) | Masivo (TB-PB) |
| **Requisito de memoria** | Bajo (tamaño de bloque) | Medio (diccionario dinámico) | Distribuido |
| **Complejidad implementación** | Baja | Media | Alta |
| **Velocidad (single machine)** | Media | Alta | N/A |
| **Escalabilidad** | Limitada | Limitada | Excelente |
| **Tolerancia a fallos** | Manual | Manual | Automática |
| **I/O en disco** | 2 pasadas (leer + escribir) | 2 pasadas | Red + disco |
| **Uso de CPU** | Alto (ordenamiento) | Medio | Distribuido |
| **Mejor caso de uso** | Colecciones medianas, recursos limitados | Colecciones medianas, más memoria | Colecciones masivas, cluster disponible |

### Consideraciones Prácticas

Al elegir un algoritmo de construcción de índices, considerar:

1. **Tamaño de la colección**:
   - < 1 GB: Construcción en memoria simple
   - 1-100 GB: BSBI o SPIMI
   - > 100 GB: MapReduce o sistemas especializados

2. **Recursos disponibles**:
   - RAM limitada: BSBI (menor uso de memoria)
   - RAM abundante: SPIMI (más rápido)
   - Cluster disponible: MapReduce

3. **Frecuencia de actualización**:
   - Actualizaciones frecuentes: Índices incrementales
   - Reconstrucción completa: Batch processing

4. **Requisitos de tiempo**:
   - Tiempo real: Índices incrementales
   - Batch: Cualquier algoritmo según tamaño

## Implementación con BSBI

Ahora veamos una implementación práctica usando el algoritmo BSBI con un corpus de documentos sobre las obras de Tolkien:

```{code-cell} python
---
tags: [hide-output]
---
import sys
sys.path.append('../_static/code/ii')

from ii import BSBI
from pathlib import Path

# Crear constructor BSBI con bloques pequeños
bsbi = BSBI(tamaño_bloque=50)

# Construir índice desde el corpus de Tolkien
corpus_path = Path('../_static/code/ii/corpus')
print(f"Construyendo índice desde: {corpus_path}\n")

indice = bsbi.construir_indice(corpus_path)

# Mostrar estadísticas
print(f"Índice construido exitosamente")
print(f"Términos únicos: {len(indice)}")
print(f"Total de postings: {sum(len(docs) for docs in indice.values())}")

# Mostrar algunos términos de ejemplo
print("\nEjemplos de términos y sus postings:")
terminos_ejemplo = ['frodo', 'ring', 'gandalf', 'hobbit', 'aragorn']
for termino in terminos_ejemplo:
    docs = bsbi.buscar(termino)
    if docs:
        print(f"  '{termino}': {docs}")
```

El algoritmo BSBI procesa los documentos en bloques, creando índices parciales ordenados que luego fusiona eficientemente. Esto permite manejar colecciones que no caben en memoria.

## Índice Invertido Completo

Para casos donde la colección sí cabe en memoria, podemos usar una implementación más simple:

```{code-cell} python
---
tags: [hide-output]
---
from collections import defaultdict
import re


class IndiceInvertidoCompleto:
    """Índice invertido con procesamiento de texto completo"""
    
    def __init__(self, usar_stopwords=True, usar_stemming=False):
        self.indice = defaultdict(set)
        self.documentos = {}
        self.usar_stopwords = usar_stopwords
        self.usar_stemming = usar_stemming
    
    def normalizar(self, texto):
        """Normaliza el texto"""
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto
    
    def tokenizar(self, texto):
        """Tokeniza y procesa el texto"""
        texto = self.normalizar(texto)
        tokens = texto.split()
        
        # Eliminar stopwords si está habilitado
        if self.usar_stopwords:
            tokens = [t for t in tokens if t not in STOPWORDS]
        
        # Aplicar stemming si está habilitado
        if self.usar_stemming:
            tokens = [stem_simple(t) for t in tokens]
        
        return tokens
    
    def agregar_documento(self, doc_id, texto):
        """Agrega un documento al índice"""
        self.documentos[doc_id] = texto
        tokens = self.tokenizar(texto)
        
        for token in tokens:
            if token:  # Ignorar strings vacíos
                self.indice[token].add(doc_id)
    
    def buscar(self, termino):
        """Busca un término en el índice"""
        # Procesar el término de búsqueda de la misma manera
        tokens = self.tokenizar(termino)
        if not tokens:
            return set()
        termino_procesado = tokens[0]
        return self.indice.get(termino_procesado, set())
    
    def buscar_and(self, *terminos):
        """Busca documentos que contienen todos los términos"""
        if not terminos:
            return set()
        resultado = self.buscar(terminos[0])
        for termino in terminos[1:]:
            resultado &= self.buscar(termino)
        return resultado
    
    def buscar_or(self, *terminos):
        """Busca documentos que contienen al menos uno de los términos"""
        resultado = set()
        for termino in terminos:
            resultado |= self.buscar(termino)
        return resultado
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del índice"""
        return {
            'num_terminos': len(self.indice),
            'num_documentos': len(self.documentos),
            'terminos_mas_frecuentes': sorted(
                [(t, len(docs)) for t, docs in self.indice.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


# Crear índice con diferentes configuraciones
print("=== Índice SIN procesamiento ===")
indice1 = IndiceInvertidoCompleto(usar_stopwords=False, usar_stemming=False)
indice1.agregar_documento(1, "La programación en Python es muy popular")
indice1.agregar_documento(2, "Programar en Python es divertido y educativo")
indice1.agregar_documento(3, "Los programadores de Python son muy demandados")
stats1 = indice1.obtener_estadisticas()
print(f"Términos en el índice: {stats1['num_terminos']}")

print("\n=== Índice CON stopwords removidas ===")
indice2 = IndiceInvertidoCompleto(usar_stopwords=True, usar_stemming=False)
indice2.agregar_documento(1, "La programación en Python es muy popular")
indice2.agregar_documento(2, "Programar en Python es divertido y educativo")
indice2.agregar_documento(3, "Los programadores de Python son muy demandados")
stats2 = indice2.obtener_estadisticas()
print(f"Términos en el índice: {stats2['num_terminos']}")

print("\n=== Índice CON stopwords y stemming ===")
indice3 = IndiceInvertidoCompleto(usar_stopwords=True, usar_stemming=True)
indice3.agregar_documento(1, "La programación en Python es muy popular")
indice3.agregar_documento(2, "Programar en Python es divertido y educativo")
indice3.agregar_documento(3, "Los programadores de Python son muy demandados")
stats3 = indice3.obtener_estadisticas()
print(f"Términos en el índice: {stats3['num_terminos']}")

# Comparar búsquedas
print("\n=== Comparación de búsquedas ===")
print(f"Búsqueda 'programación':")
print(f"  Sin procesamiento: {indice1.buscar('programación')}")
print(f"  Con stopwords: {indice2.buscar('programación')}")
print(f"  Con stemming: {indice3.buscar('programación')}")

print(f"\nBúsqueda 'programar':")
print(f"  Sin procesamiento: {indice1.buscar('programar')}")
print(f"  Con stopwords: {indice2.buscar('programar')}")
print(f"  Con stemming: {indice3.buscar('programar')}")  # Encuentra ambos!
```

Como podemos observar, el procesamiento reduce significativamente el tamaño del vocabulario y mejora la recuperación al agrupar variantes morfológicas de las mismas palabras.

## Construcción de Índices

La construcción de un índice invertido para una colección grande de documentos requiere consideraciones especiales:

### Construcción en Memoria

Para colecciones pequeñas que caben en memoria, el proceso es simple:

```{code-cell} python
---
tags: [hide-output]
---
def construir_indice_simple(documentos):
    """Construye un índice invertido en memoria"""
    indice = IndiceInvertidoCompleto(usar_stopwords=True, usar_stemming=True)
    
    for doc_id, texto in documentos.items():
        indice.agregar_documento(doc_id, texto)
    
    return indice


# Ejemplo con una colección de documentos
coleccion = {
    1: "Python es un lenguaje interpretado de alto nivel",
    2: "Java es un lenguaje compilado y tipado estáticamente",
    3: "Python y Java son lenguajes orientados a objetos",
    4: "Machine Learning se implementa frecuentemente en Python",
    5: "Los frameworks de Java incluyen Spring y Hibernate"
}

indice_final = construir_indice_simple(coleccion)
stats = indice_final.obtener_estadisticas()

print(f"Índice construido:")
print(f"  - Documentos: {stats['num_documentos']}")
print(f"  - Términos únicos: {stats['num_terminos']}")
print(f"\nTérminos más frecuentes:")
for termino, freq in stats['terminos_mas_frecuentes']:
    print(f"  {termino}: aparece en {freq} documento(s)")
```

### Complejidad

La construcción de un índice tiene complejidad:
- **Tiempo**: O(n × m) donde n es el número de documentos y m es el promedio de términos por documento
- **Espacio**: O(T) donde T es el número total de términos únicos en la colección

Para colecciones muy grandes que no caben en memoria, se utilizan técnicas como:
- **Construcción por bloques**: Dividir la colección en bloques, crear índices parciales y luego fusionarlos
- **Ordenamiento externo**: Usar algoritmos de ordenamiento que funcionen con datos en disco
- **Procesamiento distribuido**: Utilizar frameworks como MapReduce para procesar en paralelo

## Aplicaciones Prácticas

Los índices invertidos se utilizan en:

- **Motores de búsqueda web**: Google, Bing, etc.
- **Búsqueda en documentos**: Elasticsearch, Solr, Lucene
- **Búsqueda en código**: GitHub Code Search
- **Bases de datos full-text**: PostgreSQL, MongoDB con índices de texto
- **Sistemas de recomendación**: Para encontrar ítems similares
- **Detección de plagio**: Comparar documentos eficientemente

```{code-cell} python
---
tags: [hide-output]
---
# Ejemplo: Sistema simple de búsqueda de documentos
class SistemaBusqueda:
    """Sistema básico de búsqueda de documentos"""
    
    def __init__(self):
        self.indice = IndiceInvertidoCompleto(usar_stopwords=True, usar_stemming=True)
    
    def indexar_documentos(self, documentos):
        """Indexa una colección de documentos"""
        for doc_id, contenido in documentos.items():
            self.indice.agregar_documento(doc_id, contenido)
    
    def buscar_consulta(self, consulta):
        """Procesa una consulta y retorna documentos relevantes"""
        # Por simplicidad, asumimos consulta como términos separados por espacio (OR implícito)
        terminos = consulta.split()
        docs = self.indice.buscar_or(*terminos)
        
        # Retornar documentos con su contenido
        resultados = []
        for doc_id in docs:
            resultados.append({
                'id': doc_id,
                'contenido': self.indice.documentos[doc_id]
            })
        return resultados


# Crear sistema y buscar
sistema = SistemaBusqueda()
sistema.indexar_documentos(coleccion)

# Realizar búsqueda
consulta = "Machine Learning Python"
resultados = sistema.buscar_consulta(consulta)

print(f"Consulta: '{consulta}'")
print(f"Se encontraron {len(resultados)} documento(s):\n")
for res in resultados:
    print(f"[Doc {res['id']}] {res['contenido']}")
```

## Resumen

Los índices invertidos son esenciales para la recuperación eficiente de información:

- Permiten búsquedas rápidas al ir de término a documentos
- Consisten en un diccionario de términos y listas de postings
- El procesamiento de texto (normalización, tokenización, stopwords, stemming) mejora la efectividad
- Algoritmos como BSBI, SPIMI y MapReduce permiten construir índices para colecciones grandes
- Se utilizan en todos los motores de búsqueda modernos
- La construcción para colecciones grandes requiere técnicas especiales

En el siguiente capítulo veremos cómo comprimir estos índices para reducir el espacio que ocupan, lo cual es crucial cuando trabajamos con colecciones de millones de documentos.

## Referencias y Recursos Adicionales

### Bibliografía Principal

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). **Introduction to Information Retrieval**. Cambridge University Press.
  - Capítulo 1: Boolean retrieval
  - Capítulo 2: The term vocabulary and postings lists
  - Capítulo 4: Index construction
  - [Disponible online](https://nlp.stanford.edu/IR-book/){target="_blank"}

- Baeza-Yates, R., & Ribeiro-Neto, B. (2011). **Modern Information Retrieval: The Concepts and Technology behind Search** (2nd ed.). Addison-Wesley.

- Büttcher, S., Clarke, C. L., & Cormack, G. V. (2010). **Information Retrieval: Implementing and Evaluating Search Engines**. MIT Press.

### Recursos en Línea

- [Elasticsearch Guide - Inverted Index](https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html){target="_blank"}: Documentación sobre índices invertidos en Elasticsearch

- [Apache Lucene Documentation](https://lucene.apache.org/core/documentation.html){target="_blank"}: Motor de búsqueda open source que implementa índices invertidos

- [Whoosh Documentation](https://whoosh.readthedocs.io/){target="_blank"}: Librería Python de búsqueda full-text

- [Information Retrieval - Stanford CS276](https://web.stanford.edu/class/cs276/){target="_blank"}: Curso de Stanford sobre recuperación de información

### Herramientas y Librerías

- **Elasticsearch**: Motor de búsqueda distribuido basado en Lucene
  - [https://www.elastic.co/elasticsearch/](https://www.elastic.co/elasticsearch/){target="_blank"}

- **Apache Solr**: Plataforma de búsqueda empresarial basada en Lucene
  - [https://solr.apache.org/](https://solr.apache.org/){target="_blank"}

- **Whoosh**: Motor de búsqueda en Python puro
  - [https://whoosh.readthedocs.io/](https://whoosh.readthedocs.io/){target="_blank"}

- **NLTK (Natural Language Toolkit)**: Procesamiento de lenguaje natural en Python
  - [https://www.nltk.org/](https://www.nltk.org/){target="_blank"}

- **spaCy**: Librería avanzada de NLP
  - [https://spacy.io/](https://spacy.io/){target="_blank"}

### Artículos y Papers

- Cutting, D., & Pedersen, J. (1997). "Space Optimizations for Total Ranking". *Proceedings of RIAO*.

- Zobel, J., & Moffat, A. (2006). "Inverted files for text search engines". *ACM Computing Surveys*, 38(2).

- Dean, J., & Ghemawat, S. (2004). "MapReduce: Simplified Data Processing on Large Clusters". *OSDI*.

### Videos y Tutoriales

- [How Search Engines Work - Matt Cutts (Google)](https://www.youtube.com/results?search_query=how+search+engines+work){target="_blank"}

- [Building a Search Engine - MIT OpenCourseWare](https://ocw.mit.edu/){target="_blank"}

### Para Profundizar

- Estudiar implementaciones reales en Lucene (Java) o Whoosh (Python)
- Experimentar con Elasticsearch para ver índices invertidos en producción
- Implementar variantes como índices posicionales (para búsquedas de frases)
- Explorar técnicas de ranking como TF-IDF y BM25
- Investigar índices para búsqueda aproximada y corrección ortográfica
