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
description: grafos, ordenamiento topológico, Khan
---

# Orden Topológico

El ordenamiento topológico de un grafo es un orden lineal de sus vértices tal que, para cada arista dirigida $(u, v)$, el vértice $u$ aparece antes que el vértice $v$ en el orden. Este concepto es aplicable únicamente a grafos dirigidos acíclicos (DAG).

Se utiliza para resolver problemas de planificación y dependencia de tareas, donde es necesario determinar un orden en el que se deben realizar las tareas.

## Algoritmo de Kahn

Una forma de encontrar un ordenamiento topológico es mediante el algoritmo de Kahn ([Arthur Kahn](https://en.wikipedia.org/wiki/Arthur_Kahn)), que utiliza un enfoque basado en el grado de entrada de los vértices. Los pasos son los siguientes:

```{code-block}
---
linenos: true
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

    SI quedaron nodos sin procesar:
        REPORTAR error: grafo con ciclos
```

Por ejemplo dado el siguiente grafo:

```{figure} ../_static/figures/grafo_dag_light.svg
---
class: only-light-mode
---
Grafo Dirigido Acíclico
```

```{figure} ../_static/figures/grafo_dag_dark.svg
---
class: only-dark-mode
---
Grafo Dirigido Acíclico
```

Un orden topológico posible es: $V_2$, $V_0$, $V_1$, $V_3$, $V_4$, $V_6$, $V_5$. Como se observa a continuación.

```{figure} ../_static/figures/grafo_orden_topologico_light.svg
---
class: only-light-mode
---
Ordenamiento Topológico
```

```{figure} ../_static/figures/grafo_orden_topologico_dark.svg
---
class: only-dark-mode
---
Ordenamiento Topológico
```

```{admonition} El orden topológico no es único
---
class: important
---
Pueden existir múltiples ordenamientos topológicos para un mismo grafo. El orden topológico depende de la forma en que se procesan los nodos en el algoritmo. Por ejemplo si se usa una pila en lugar de una cola se obtiene un ordenamiento diferente.
```

### Complejidad

La complejidad del algoritmo de Kahn es $O(|V|+|E|)$. Esto se debe a que cada vértice y cada arista se procesan una sola vez.

```{note} Nota
En los algoritmos de grafos se acostumbra a utilizar tanto la cantidad de vértices $|V|$ como la cantidad de aristas $|E|$ para analizar la complejidad temporal ya que si bien se puede acotar $|E|$ en función de $|V|$, expresarlo en función de ambas variables brinda más información sobre el comportamiento del algoritmo en diferentes tipos de grafos.
```

## Cálculo del orden topológico con NetworkX

**_NetworkX_** proporciona el método `topological_sort` para calcular el orden topológico de un grafo dirigido acíclico (DAG).

```{code-cell} python
---
tags: hide-output
---
import networkx as nx

grafo = {
    "V0": ["V1", "V3"],
    "V1": ["V3", "V4"],
    "V2": ["V0", "V5"],
    "V3": ["V4", "V5", "V6"],
    "V4": ["V6"],
    "V5": [],
    "V6": ["V5"],
}

G = nx.DiGraph(grafo)

list(nx.topological_sort(G))
```
