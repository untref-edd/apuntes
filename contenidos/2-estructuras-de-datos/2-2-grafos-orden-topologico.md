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

# Orden Topológico

El ordenamiento topológico de un grafo es un orden lineal de sus vértices tal que, para cada arista dirigida $(u, v)$, el vértice $u$ aparece antes que el vértice $v$ en el orden. Este concepto es aplicable únicamente a grafos dirigidos acíclicos (DAG). 

Se utiliza para resolver problemas de planificación y dependencia de tareas, donde es necesario determinar un orden en el que se deben realizar las tareas.

## Algoritmo de Kahn

Una forma de encontrar un ordenamiento topológico es mediante el algoritmo de Kahn ([Arthur Kahn](https://en.wikipedia.org/wiki/Arthur_Kahn){target=_blank}), que utiliza un enfoque basado en el grado de entrada de los vértices. Los pasos son los siguientes:

1. Calcular el grado de entrada (in-degree) de cada vértice.
2. Colocar todos los vértices con grado de entrada 0 en una cola.
3. Mientras la cola no esté vacía:
   1. Extraer un vértice de la cola y añadirlo al ordenamiento.
   2. Para cada vecino del vértice extraído, reducir su grado de entrada en 1. Si el grado de entrada de un vecino se convierte en 0, añadirlo a la cola.
4. Si se han procesado todos los vértices, el ordenamiento es válido. Si no, el grafo contiene ciclos.

## Implementación

A continuación se muestra una implementación del algoritmo de Kahn en Python:

```python
from collections import deque

def orden_topologico_kahn(grafo):
    in_degree = {u: 0 for u in grafo}
    for u in grafo:
        for v in grafo[u]:
            in_degree[v] += 1

    cola = deque([u for u in grafo if in_degree[u] == 0])
    orden = []

    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in grafo[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                cola.append(v)

    if len(orden) == len(grafo):
        return orden
    else:
        raise ValueError("El grafo contiene ciclos")

# Ejemplo de uso
grafo = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

print(orden_topologico_kahn(grafo))
```
4. Si se han procesado todos los vértices, el ordenamiento es válido. Si no, el grafo contiene ciclos.

## Implementación

A continuación se muestra una implementación del algoritmo de Kahn en Python:

```python
from collections import deque

def orden_topologico_kahn(grafo):
    in_degree = {u: 0 for u in grafo}
    for u in grafo:
        for v in grafo[u]:
            in_degree[v] += 1

    cola = deque([u for u in grafo if in_degree[u] == 0])
    orden = []

    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in grafo[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                cola.append(v)

    if len(orden) == len(grafo):
        return orden
    else:
        raise ValueError("El grafo contiene ciclos")

# Ejemplo de uso
grafo = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

print(orden_topologico_kahn(grafo))
```

## Conclusiones

El ordenamiento topológico es una herramienta poderosa para trabajar con grafos dirigidos acíclicos. 