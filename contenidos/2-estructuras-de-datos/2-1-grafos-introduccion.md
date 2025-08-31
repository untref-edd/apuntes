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

```{note}
Si entre cada par de vértices se puede tener más de una arista, entonces se trata de un **multigrafo** o **grafo multivariado**. En esta materia no vamos a estudiar **multigrafos**.

[Ver más sobre multigrafos](https://es.wikipedia.org/wiki/Multigrafo){target="_blank"}
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
width: 80%
---
Grafo de correlativas en un plan de estudios
```

Los **grafos dirigidos** también se denominan **digrafos**.

Como se observa en la última figura hay vértices que no están conectados a otros vértices. Un grafo puede tener vértices *"desconectados"*. Si todos los vértices de un grafo están conectados entre sí, se dice que el grafo es **conexo** y se cumple que $|V| - 1 ≤ |E| ≤ |V|^2$.

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

|  Arista  | Peso |
| :------: | :--: |
| $(A, B)$ |  4   |
| $(B, C)$ |  2   |
| $(C, D)$ |  4   |
| $(D, E)$ |  3   |

</div>

por lo tanto el costo del camino $A-E$ es:

$$4 + 2 + 4 + 3 = 13$$

Grafo Dirigido Acíclico
: Es un grafo cuyas aristas son dirigidas y no presenta ciclos, también conocidos como ***DAG*** por su sigla en inglés (**D**irected **A**cyclic **G**raph). Los ***DAG*** son un tipo de grafo con amplias aplicaciones y se utilizan en diversas áreas como la informática, la biología, etc.

Visto de otra forma si partimos de un vértice cualquiera del grafo no existe ningún camino que permita regresar al mismo vértice.

```{figure} ../assets/images/grafo_dag.png
---
name: grafo_dag
width: 60%
---
Grafo dirigido acíclico
```

Grado de entrada
: El grado de entrada de un vértice en un grafo dirigido es el número de aristas que llegan a ese vértice. En otras palabras, es la cantidad de aristas entrantes que tiene un vértice.
: Por ejemplo en el grafo anterior el grado de entrada del vértice $V_5$ es 3

Grado de salida
: El grado de salida de un vértice en un grafo dirigido es el número de aristas que salen de ese vértice. En otras palabras, es la cantidad de aristas salientes que tiene un vértice.
: Por ejemplo en el grafo anterior el grado de salida del vértice $V_5$ es 0

Fuente
: Es un vértice que cuyo grado de entrada es 0

Sumidero
: Es un vértice cuyo grado de salida es 0

```{Important}
Un ***DAG*** siempre tiene al menos un vértice ***fuente*** y un vértice ***sumidero***.
En el grafo de la figura anterior, el vértice $V_0$ es una fuente y el vértice $V_5$ es un sumidero.
```

## Representación de Grafos

En una computadora hay al menos dos formas de representar un grafo. Usando una **lista de adyacencia** o una **matriz de adyacencia**.

### Matriz de adyacencia

Dado el siguiente grafo $G=(V, A)$

donde

$$
V=\{V_0, V_1, V_2, V_3, V_4, V_5, V_6\}
$$

$$
\begin{aligned}
A=\{(V_0, V_1, 2), (V_0, V_3, 1), (V_1, V_3, 3), (V_1, V_4, 10), (V_3, V_4, 2), (V_3, V_6, 4),\\
   (V_3, V_5, 8), (V_3, V_2, 2), (V_2, V_0, 4), (V_2, V_5, 5), (V_4, V_6, 6), (V_6, V_5, 1)\}
\end{aligned}
$$

```{figure} ../assets/images/grafo_dirigido.png
---
name: grafo_dirigido
width: 60%
---
Grafo dirigido
```

Se numeran los vértices del grafo desde $0$ hasta $n-1$ y se genera una matriz de adyacencia $M$ de tamaño $n \times n$ donde $M[i][j]$ representa el peso de la arista que conecta el vértice $V_i$ con el vértice $V_j$. Si no hay arista entre $V_i$ y $V_j$, se puede representar con un valor especial, como $\infty$ o $-$.

|           | **$V_0$** | **$V_1$** | **$V_2$** | **$V_3$** | **$V_4$** | **$V_5$** | **$V_6$** |
| --------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **$V_0$** |     -     |     2     |     1     |     -     |     -     |     -     |     -     |
| **$V_1$** |     -     |     -     |     3     |    10     |     -     |     -     |     -     |
| **$V_2$** |     4     |     -     |     -     |     -     |     5     |     -     |     -     |
| **$V_3$** |     -     |     2     |     -     |     2     |     8     |     4     |     -     |
| **$V_4$** |     -     |     -     |     -     |     -     |     -     |     5     |     -     |
| **$V_5$** |     -     |     -     |     -     |     -     |     -     |     -     |     -     |
| **$V_6$** |     -     |     -     |     -     |     -     |     -     |     -     |     1     |

La matriz de adyacencia es una representación eficiente para grafos densos, donde el número de aristas es cercano al número máximo posible ($|V|^2$). Sin embargo, puede ser ineficiente en términos de espacio para grafos dispersos, donde el número de aristas es mucho menor que el número máximo posible. En la matriz de ejemplo solo unos pocos elementos son diferentes de '-'.

Una ventaja de esta representación es que permite verificar rápidamente si existe una arista entre dos vértices, simplemente consultando el valor en la matriz.

Para representar grafos no ponderados se acostumbra poner un 1 donde hay una arista y 0 en el resto de la matriz.

Si el grafo es no dirigido, la matriz de adyacencia será simétrica, por ejemplo la matriz de adyacencia para el siguiente grafo:

```{figure} ../assets/images/grafo_con_pesos.png
---
name: grafo_no_dirigido
width: 60%
---
Grafo no dirigido
```

|         | **$A$** | **$B$** | **$C$** | **$D$** | **$E$** |
| ------: | :-----: | :-----: | :-----: | :-----: | :-----: |
| **$A$** |    -    |    4    |    5    |    -    |    1    |
| **$B$** |    4    |    -    |    2    |    -    |    -    |
| **$C$** |    5    |    2    |    -    |    4    |    -    |
| **$D$** |    -    |    -    |    4    |    -    |    3    |
| **$E$** |    1    |    -    |    -    |    3    |    -    |

### Listas de adyacencias

La lista de adyacencia es otra forma de representar un grafo. En lugar de usar una matriz, se utiliza una lista de listas (o un diccionario) donde cada vértice tiene una lista de sus vecinos adyacentes y el peso de la arista que los conecta.

Para el grafo dirigido anterior la lista de adyacencia sería:

```{figure} ../assets/images/grafo_dirigido_lista.svg
---
name: grafo_dirigido_lista
width: 80%
---
Lista de adyacencia del grafo dirigido
```

En cada nodo de la lista se almacena el par $(vecino, peso)$ que representa la arista que conecta el vértice con su vecino.

A continuación la lista de adyacencia para el grafo no dirigido del punto anterior:

```{figure} ../assets/images/grafo_no_dirigido_lista.svg
---
name: grafo_no_dirigido_lista
width: 80%
---
Lista de adyacencia del grafo no dirigido
```

## Grafos en Python

En Python existen varias bibliotecas que facilitan la representación y manipulación de grafos. Vamos a usar **NetworkX** para representar grafos y **Matplotlib** para visualizarlos.

**Networkx** estructuras de datos y algoritmos eficientes para trabajar con grafos, lo que facilita tareas como la búsqueda de caminos, la detección de ciclos y el análisis de redes.

Ambas bibliotecas se deben instalar previamente.

```console
pip install networkx matplotlib
```

Los vértices deben ser de tipos inmutables de datos. Es decir, cualquier tipo que pueda ser clave de un diccionario.

### Crear grafos

Existen varias formas de crear un grafo. A continuación algunas de las que más usaremos:

`Graph()`{l=python}
: Para crear un grafo simple, vacío y no dirigido.

`DiGraph()`{l=python}
: Para crear un grafo dirigido incialmente vacío.

Para agregar aristas se puede usar:

`add_edge(u, v, weight=w)`{l=python}
: Para agregar una arista desde el nodo `u`{l=python} al nodo `v`{l=python} con un peso `w`{l=python}.
Si el grafo es no dirigido, también se agregará la arista en la dirección opuesta.
Si los nodos `u`{l=python} y `v`{l=python} no existen en el grafo, se agregarán automáticamente.

`add_weighted_edges_from(iterable)`{l=python}
: Para agregar múltiples aristas de una sola vez desde un `iterable`{l=python} de tuplas `(u, v, w)`{l=python}. Si se omite el peso, se asumirá un peso de 1.

`add_edges_from(iterable)`{l=python}
: Para agregar múltiples aristas de una sola vez desde `iterable`{l=python} de tuplas `(u, v, d)`{l=python}. El último parámetro, opcional, puede ser un diccionario con atributos de la arista.

También se pueden agregar nodos individuales

`add_node(n)`{l=python}
: Para agregar un nodo `n`{l=python} al grafo.

`add_node_from(iterable)`{l=python}
: Para agregar múltiples nodos desde un `iterable`{l=python}, de tuplas de la forma `(n, d)`{l=python}, donde `n`{l=python} es el nodo y `d`{l=python} es un diccionario con los atributos opcionales.

### Graficar grafos

**Networkx** incluye interfaces para la visualización de grafos en **Matplotlib** y **Graphviz**.

La interfaz `networkx.drawing.nx_pylab` provee funciones que permiten crear y usar figuras con ejes de **Matplotlib**.

```{code-cell} python
---
tags: [hide-output]
---
import networkx as nx 
import matplotlib.pyplot as plt # permite crear figuras, mostrarlas, etc.

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos y aristas
G.add_weighted_edges_from([
    (0, 1, 4),
    (0, 2, 5),
    (1, 2, 2),
    (2, 3, 4),
    (3, 4, 3)
])

# Dibujar el grafo
# pos = nx.spring_layout(G) # posiciones para todos los nodos
pos = nx.circular_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.kamada_kawai_layout(G)
nx.draw(
  G, pos,
  with_labels = True, # etiquetar nodos
  node_size = 700, # tamaño de los nodos
  node_color = 'lightblue', # color de los nodos
  font_size = 12, # tamaño de la fuente
  edge_color = 'gray', # color de las aristas
  width = 2 # grosor de las aristas
)
edge_labels = nx.get_edge_attributes(G, 'weight') # Obtener los pesos de las aristas
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Dibujar las etiquetas de las aristas
plt.title("Grafo Dirigido") # Título de la figura
plt.show() # Mostrar la figura
```

Un ***layout*** es un diccionario {nodo: (x, y)} con la posición de cada vértice. **NetworkX** incluye varios algoritmos para calcular layouts.

`spring_layout`{l=python}
: Posiciona nodos con un modelo de fuerzas.

`circular_layout`{l=python}
: Posiciona nodos en un círculo.

`shell_layout`{l=python}
: Posiciona nodos en capas concéntricas.

`kamada_kawai_layout`{l=python}
: Posiciona nodos minimizando la energía de un sistema de resortes.

### Ejemplo: Grafo de una red de transporte

```{code-cell} python
---
tags: [hide-input]
---
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Crear grafo dirigido (direcciones de rutas posibles)
G = nx.DiGraph()

# 1) Agregar estaciones (nodos) con atributos
G.add_node("Central", tipo="Terminal", linea="Roja")
G.add_node("Parque", tipo="Normal", linea="Roja")
G.add_node("Universidad", tipo="Normal", linea="Roja")
G.add_node("Museo", tipo="Normal", linea="Verde")
G.add_node("Plaza", tipo="Terminal", linea="Verde")
G.add_node("Estadio", tipo="Normal", linea="Verde")

# 2) Agregar conexiones (aristas) con atributos
G.add_edge("Central", "Parque", distancia=2.5, tipo="normal")
G.add_edge("Parque", "Universidad", distancia=3.0, tipo="express")
G.add_edge("Universidad", "Museo", distancia=4.0, tipo="normal")
G.add_edge("Museo", "Plaza", distancia=2.0, tipo="normal")
G.add_edge("Plaza", "Estadio", distancia=3.5, tipo="express")
G.add_edge("Parque", "Museo", distancia=5.0, tipo="normal")

# 3) Dibujar grafo
pos = nx.spring_layout(G, seed=42)

# Colores de nodos según línea
colores_lineas = {"Roja": "red", "Verde": "green"}
node_colors = [
  colores_lineas[G.nodes[n]["linea"]]
  for n in G.nodes()
]

# Grosor y estilo de aristas según tipo de vía
edge_widths = [
  2 if G[u][v]["tipo"] == "express" else 1
  for u, v in G.edges()
]
edge_styles = [
  "dashed" if G[u][v]["tipo"] == "express" else "solid"
  for u, v in G.edges()
]

# Dibujar nodos
nx.draw_networkx_nodes(
  G, pos, node_color=node_colors, node_size=1200
)

# Dibujar aristas
for i, (u, v) in enumerate(G.edges()):
  nx.draw_networkx_edges(
    G, pos, edgelist=[(u, v)],
    width=edge_widths[i], style=edge_styles[i], arrows=True
  )

# Etiquetas de nodos
nx.draw_networkx_labels(G, pos, font_size=9)

# Etiquetas de aristas (distancia)
edge_labels = {
  (u, v): f'{G[u][v]["distancia"]} km'
  for u, v in G.edges()
}
nx.draw_networkx_edge_labels(
  G, pos, edge_labels=edge_labels, font_color="blue"
)

# Leyenda
legend_elements = [
  Line2D([0], [0], color='red', marker='o', linestyle='None', markersize=12, label='Línea Roja'),
  Line2D([0], [0], color='green', marker='o', linestyle='None', markersize=12, label='Línea Verde'),
  Line2D([0], [0], color='gray', linewidth=2, linestyle='solid', label='Vía normal'),
  Line2D([0], [0], color='gray', linewidth=2, linestyle='dashed', label='Vía express')
]
plt.legend(handles=legend_elements, loc='lower left', fontsize=10)

plt.title("Mini-Red de Transporte Urbano", fontsize=14)
plt.axis("off")
plt.show()
```

## Recursos para profundizar

- [Documentación de NetworkX](https://networkx.org/documentation/stable/index.html){target="\_blank"}
- [Tutorial de Matplotlib](https://matplotlib.org/stable/tutorials/index.html){target="\_blank"}
- [Introducción a grafos y redes con Python](https://cienciadedatos.net/documentos/pygml01-introduccion-grafos-redes-python){target="\_blank"}
- [NetworkX Tutorial](https://www.kaggle.com/code/alireza151/networkx-tutorial){target="\_blank"}
