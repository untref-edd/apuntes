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

# Grafos

Un grafo es un modelo matemático que permite representar relaciones entre objetos. Un grafo está compuesto por nodos (o vértices) y aristas (o enlaces) que conectan pares de nodos.

Formalmente un grafo se define como

```{math}
G = (V, E)
```

donde:

$V$: Conjunto de vértices

$E ⊆ V × V$: Conjunto de aristas. Las aristas conectan pares de vértices.

$|V|$: Cardinal de V (denota la cantidad de vértices del grafo).

$|E|$: Cardinal de E (denota la cantidad de aristas).

Entre un par cualquiera de vértices sólo puede haber una arista. Por lo tanto siempre se cumple que:

$$|E| ≤ |V|^2$$

```{figure} ../assets/images/grafo_ejemplo.png
---
name: grafo_ejemplo
width: 60%
---
Ejemplo de un grafo
```

## Grafos Dirigidos y No Dirigidos

Los grafos se pueden clasificar en dirigidos y no dirigidos. En un grafo dirigido, las aristas tienen una dirección y conectan un vértice de origen con un vértice de destino. En cambio, en un grafo no dirigido, las aristas no tienen dirección y simplemente conectan dos vértices.

Por ejemplo en la siguiente imagen se observa las relaciones de amistad en una red social, donde las relaciones son simétricas, es decir, si A es amigo de B, entonces B es amigo de A. Estas relaciones se pueden representar con un grafo no dirigido. 

```{figure} ../assets/images/grafo_red.png
---
name: grafo_red
width: 60%
---
Grafo de amistades en una red social
```

Los grafos dirigidos permiten representar relaciones asimétricas entre dos nodos. Por ejemplo el plan de estudios de una carrera se puede modelar con un grafo dirigido, donde las materias son los nodos y las aristas indican las correlativas que se deben aprobar antes de cursar una materia.

```{figure} ../assets/images/grafo_carrera.png
---
name: grafo_carrera
width: 60%
---
Grafo de correlativas en un plan de estudios
```

Los **grafos dirigidos** también se denominan **digrafos**.

## Grafos ponderados y no ponderados

Un grafo se dice que es **ponderado** si cada arista tiene un peso o costo asociado. Este peso puede representar diferentes cosas, como la distancia entre dos nodos o el tiempo necesario para recorrer una arista. Por otro lado, un grafo es **no ponderado** si sus aristas no tienen pesos.

```{figure} ../assets/images/grafo_con_pesos.png
---
name: grafo_con_pesos
width: 60%
---
Grafo ponderado con costos en las aristas
```

## Definiciones

Camino
: Un camino en un grafo es una secuencia de vértices en la que cada par de vértices adyacentes está conectado por una arista. Un camino puede ser **simple** (sin vértices repetidos) o tener **ciclos** (vértices repetidos). En general cuando se habla sólo de camino se refiere a un **camino simple** sin ciclos.

```{figure} ../assets/images/grafo_camino.png
---
name: grafo_camino
width: 60%
---
Grafo que representa un camino simple. El camino conecta los vértices A, B, C, D y E. Se observa que no hay ningún camino entre los vértices A y G por ejemplo.
```

Costo de un camino
: El costo de un camino en un grafo ponderado es la suma de los pesos de las aristas que lo componen. En un grafo no ponderado, se puede considerar que todas las aristas tienen el mismo costo (costo de 1) y el costo del camino representa la cantidad de aristas que lo componen.

Por ejemplo, en la siguiente tabla se observa el peso de las aristas que componen el camino $A-E$:

<div align="center" style="width: 40%; margin: auto;">

|  Arista  | Peso  |
| :------: | :---: |
| $(A, B)$ |   4   |
| $(B, C)$ |   2   |
| $(C, D)$ |   4   |
| $(D, E)$ |   3   |

</div>

por lo tanto el costo del camino $A-E$ es:

$$4 + 2 + 4 + 3 = 13$$

Grafo Dirigido Acíclico
: Es un grafo cuyas aristas son dirigidas y no presenta ciclos, también conocidos como ***DAG*** por su sigla en inglés. Los DAG son un tipo de grafo con amplias aplicaciones y se utilizan en diversas áreas como la informática, la biología, etc.

Visto de otra forma si partimos de un vértice cualquiera del grafo no existe ningún camino que permita regresar al mismo vértice.

```{figure} ../assets/images/grafo_dag.png
---
name: grafo_dag
width: 60%
---
Grafo dirigido acíclico
```

## Representación de Grafos
