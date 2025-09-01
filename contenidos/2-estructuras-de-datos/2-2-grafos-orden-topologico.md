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

Una forma de encontrar un ordenamiento topológico es mediante el algoritmo de Kahn ([Arthur Kahn](https://en.wikipedia.org/wiki/Arthur_Kahn){target="_blank"}), que utiliza un enfoque basado en el grado de entrada de los vértices. Los pasos son los siguientes:

```{code-block}
---
linenos:
---
ORDEN TOPOLÓGICO (G: DiGrafo)
    q <- Cola vacía

    PARA CADA v EN G.nodos:
        SI v.grado_entrada == 0:
            q.encolar(v)

    MIENTRAS NO q.esta_vacia:
        v = q.desencolar()

        VISITAR v

        PARA CADA w EN v.nodos_adyacentes:
            w.grado_entrada -= 1

            SI w.grado_entrada == 0:
                q.encolar(w)

    SI quedaron nodos sin imprimir:
        REPORTAR error: grafo con ciclos
```

Por ejemplo dado el siguiente grafo:

```{figure} ../assets/images/grafo_dag.png
---
name: grafo_dag2
width: 60%
---
Grafo Dirigido Acíclico
```

Un orden topológico posible es: $V_2, V_0, V_1, V_3, V_4, V_6, V_5$. Como se observa a continuación.

```{figure} ../assets/images/grafo_orden_topologico.png
---
name: orden_topologico
width: 60%
---
Ordenamiento Topológico
```

```{Important}
El orden topológico no es único. Pueden existir múltiples ordenamientos topológicos para un mismo grafo. El orden topológico depende de la forma en que se procesan los nodos en el algoritmo. Por ejemplo si se usa una pila en lugar de una cola se obtiene un ordenamiento diferente
```

### Complejidad

La complejidad del algoritmo de Kahn es $O(|V|+|E|)$. Esto se debe a que cada vértice y cada arista se procesan una sola vez.

```{note}
En los algoritmos de grafos se acostumbra a utilizar tanto la cantidad de vértices |V| como la cantidad de aristas |E| para analizar la complejidad temporal ya que si bien se puede acotar |E| en función de |V|, expresarlo en función de ambas variables brinda más información sobre el comportamiento del algoritmo en diferentes tipos de grafos.
```

## Cálculo del orden topológico con NetworkX

***NetworkX*** proporciona el método `topological_sort`{l=python} para calcular el orden topológico de un grafo dirigido acíclico (DAG).

```{code-cell}python
---
tags: [hide-output]
---
import networkx as nx

def orden_topologico_networkx(grafo):
    G = nx.DiGraph(grafo)
    return list(nx.topological_sort(G))

# Ejemplo de uso
grafo = {
    'V0': ['V1', 'V3'],
    'V1': ['V3', 'V4'],
    'V2': ['V0', 'V5'],
    'V3': ['V4', 'V5', 'V6'],
    'V4': ['V6'],
    'V5': [],
    'V6': ['V5']
}

print(orden_topologico_networkx(grafo))
```
