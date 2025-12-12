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
description: Introducción a la teoría de grafos, definiciones básicas, tipos de grafos y representación en Python.
---

# Grafos

Un grafo es un modelo matemático que permite representar relaciones entre objetos. Un grafo está compuesto por nodos (o vértices) y aristas (o enlaces) que conectan pares de nodos.

Formalmente un grafo se define como

$$
G = (V, E)
$$

donde:

**$V$**: Conjunto de vértices

**$E$**: Conjunto de aristas. Las aristas conectan pares de vértices.

Además se cumple que $E \subseteq V \times V$. Esto quiere decir que cada arista une un par de vértices.

**$|V|$**: Cardinal de V (denota la cantidad de vértices del grafo).

**$|E|$**: Cardinal de E (denota la cantidad de aristas).

Entre un par cualquiera de vértices sólo puede haber una arista. Por lo tanto siempre se cumple que:

$$
|E| ≤ |V|^2
$$

```{figure} ../_static/figures/grafo_ejemplo_light.svg
---
class: only-light-mode
width: 60%
---
Ejemplo de un grafo
```

```{figure} ../_static/figures/grafo_ejemplo_dark.svg
---
class: only-dark-mode
width: 60%
---
Ejemplo de un grafo
```

Si entre cada par de vértices se puede tener más de una arista, entonces se trata de un **multigrafo**. En esta materia no vamos a estudiar **multigrafos**.

[Ver más sobre multigrafos](https://es.wikipedia.org/wiki/Multigrafo)

## Grafos dirigidos y no dirigidos

Los grafos se pueden clasificar en dirigidos y no dirigidos. En un grafo dirigido, las aristas tienen una dirección y conectan un vértice de origen con un vértice de destino. En cambio, en un grafo no dirigido, las aristas no tienen dirección y simplemente conectan dos vértices.

Por ejemplo, en la siguiente imagen se observa las relaciones de amistad en una red social, donde las relaciones son simétricas, es decir, si A es amigo de B, entonces B es amigo de A. Estas relaciones se pueden representar con un grafo no dirigido.

```{figure} ../_static/figures/grafo_red_light.svg
---
class: only-light-mode
width: 70%
---
Grafo de amistades en una red social
```

```{figure} ../_static/figures/grafo_red_dark.svg
---
class: only-dark-mode
width: 70%
---
Grafo de amistades en una red social
```

Los grafos dirigidos permiten representar relaciones asimétricas entre dos nodos, por ejemplo en la red social X (anteriormente Twitter), si A sigue a B, las publicaciones de B aparecerán en el *feed* de A, pero si B no sigue a A, las publicaciones de A no aparecerán en el *feed* de B.

El plan de estudios de una carrera es otro ejemplo que se puede modelar con un grafo dirigido, donde las materias son los nodos y las aristas indican las correlativas que se deben aprobar antes de cursar una materia.

```{figure} ../_static/figures/grafo_carrera_light.svg
---
class: only-light-mode
---
Grafo de correlativas en un plan de estudios
```

```{figure} ../_static/figures/grafo_carrera_dark.svg
---
class: only-dark-mode
---
Grafo de correlativas en un plan de estudios
```

Los **grafos dirigidos** también se denominan **digrafos**.

Como se observa en la última figura hay vértices que no están conectados a otros vértices. Un grafo puede tener vértices _"desconectados"_.

## Grafos conexos

Un grafo no dirigido se dice **conexo** si existe un camino entre cada par de vértices, es decir, para cualquier par de vértices, se puede llegar de uno al otro siguiendo las aristas del grafo. Para grafos conexos no dirigidos se cumple que:

$$
V - 1 \leq |E| \leq \frac{V \times (V - 1)}{2}
$$

```{figure} ../_static/figures/grafos_conexos_light.svg
---
class: only-light-mode
---
Grafos conexos no dirigidos
```

```{figure} ../_static/figures/grafos_conexos_dark.svg
---
class: only-dark-mode
---
Grafos conexos no dirigidos
```

En grafos dirigidos como las aristas tiene un sentido, se puede distinguir entre grafos dirigidos **fuertemente conexos** o **debilmente conexos**

Un grafo dirigido es **fuertemente conexo** si, para cualquier par de vértices elegidos al azar ($u$ y $v$), existe:

1. Un camino dirigido que va desde $u$ hasta $v$.
2. Un camino dirigido que va desde $v$ hasta $u$.

Mientras se considera que un grafo dirigido es **debilmente conexo** si el **grafo subyacente** es conexo.

```{admonition} Definición
---
class: hint
---
El **grafo subyacente** de un grafo dirigido es el grafo no dirigido que se obtiene al eliminar las direcciones de las aristas del grafo dirigido.
```

```{figure} ../_static/figures/grafos_conexos_dirigidos_light.svg
---
class: only-light-mode
---
Grafos conexos dirigidos
```

```{figure} ../_static/figures/grafos_conexos_dirigidos_dark.svg
---
class: only-dark-mode
---
Grafos conexos dirigidos
```

## Grafos ponderados y no ponderados

Un grafo se dice que es **ponderado** si cada arista tiene un peso o costo asociado. Este peso puede representar diferentes cosas, como la distancia entre dos nodos o el tiempo necesario para recorrer una arista. Por otro lado, un grafo es **no ponderado** si sus aristas no tienen pesos.

```{figure} ../_static/figures/grafo_con_pesos_light.svg
---
class: only-light-mode
width: 60%
---
Grafo ponderado con costos en las aristas
```

```{figure} ../_static/figures/grafo_con_pesos_dark.svg
---
class: only-dark-mode
width: 60%
---
Grafo ponderado con costos en las aristas
```

## Definiciones

### Camino

Un camino en un grafo (dirigido o no dirigido) es una secuencia de vértices en la que cada par de vértices adyacentes está conectado por una arista. Un camino puede ser **simple** (sin vértices repetidos) o tener **ciclos** (vértices repetidos). En general cuando se habla sólo de camino se refiere a un **camino simple** sin ciclos.

```{figure} ../_static/figures/grafo_camino_light.svg
---
class: only-light-mode
---
Caminos en grafos
```

```{figure} ../_static/figures/grafo_camino_dark.svg
---
class: only-dark-mode
---
Caminos en grafos
```

#### Costo de un camino

El costo de un camino en un grafo ponderado es la suma de los pesos de las aristas que lo componen. En un grafo no ponderado, se puede considerar que todas las aristas tienen el mismo costo (costo de 1) y el costo del camino representa la cantidad de aristas que lo componen.

En la figura anterior el costo del camino $A-E$ en el grafo no dirgido es:

$$
\begin{equation*}
4 + 2 + 4 + 3 = 13
\end{equation*}
$$

mientras que el costo del ciclo en el grafo dirigido es:

$$
\begin{equation*}
4 + 2 + 5 = 11
\end{equation*}
$$

### Grafo Dirigido Acíclico

Es un grafo cuyas aristas son dirigidas y no presenta ciclos, también conocidos como _**DAG**_ por su sigla en inglés (_Directed Acyclic Graph_). Los _**DAG**_ son un tipo de grafo con amplias aplicaciones y se utilizan en diversas áreas como la informática, la biología, etc.

Visto de otra forma si partimos de un vértice cualquiera del grafo no existe ningún camino que permita regresar al mismo vértice.

```{figure} ../_static/figures/grafo_dag_light.svg
---
class: only-light-mode
width: 60%
---
Grafo Dirigido Acíclico
```

```{figure} ../_static/figures/grafo_dag_dark.svg
---
class: only-dark-mode
width: 60%
---
Grafo Dirigido Acíclico
```

### Grado de entrada

El grado de entrada de un vértice en un grafo dirigido es el número de aristas que llegan a ese vértice. En otras palabras, es la cantidad de aristas entrantes que tiene un vértice.

Por ejemplo en el grafo anterior el grado de entrada del vértice $V_5$ es 3

### Grado de salida

El grado de salida de un vértice en un grafo dirigido es el número de aristas que salen de ese vértice. En otras palabras, es la cantidad de aristas salientes que tiene un vértice.

Por ejemplo en el grafo anterior el grado de salida del vértice $V_5$ es 0

#### Fuente

Es un vértice cuyo grado de entrada es 0

#### Sumidero

Es un vértice cuyo grado de salida es 0

```{important} Importante
Un ***DAG*** siempre tiene al menos un vértice ***fuente*** y un vértice ***sumidero***.

En el grafo de la figura anterior, el vértice $V_2$ es una fuente y el vértice $V_5$ es un sumidero.
```

## Representación de grafos

En estructuras de datos hay al menos dos formas de representar un grafo. Usando una **lista de adyacencia** o una **matriz de adyacencia**.

### Matriz de adyacencia

Dado el siguiente grafo $G=(V, A)$

donde

$$
\begin{equation*}
V=\{V_0, V_1, V_2, V_3, V_4, V_5, V_6\}
\end{equation*}
$$

$$
\begin{equation*}
\begin{aligned}
A=\{(V_0, V_1, 2), (V_0, V_3, 1), (V_1, V_3, 3), (V_1, V_4, 10), (V_2, V_0, 4), (V_2, V_5, 5),\\
   (V_3, V_2, 2), (V_3, V_4, 2), (V_3, V_5, 8), (V_3, V_6, 4), (V_4, V_6, 5), (V_6, V_5, 1)\}
\end{aligned}
\end{equation*}
$$

```{figure} ../_static/figures/grafo_dirigido_light.svg
---
class: only-light-mode
---
Grafo dirigido
```

```{figure} ../_static/figures/grafo_dirigido_dark.svg
---
class: only-dark-mode
---
Grafo dirigido
```

Se numeran los vértices del grafo desde $0$ hasta $n-1$ y se genera una matriz de adyacencia $M$ de tamaño $n \times n$ donde $M[i][j]$ representa el peso de la arista que conecta el vértice $V_i$ con el vértice $V_j$. Si no hay arista entre $V_i$ y $V_j$, se puede representar con un valor especial, como $\infty$ o $-$.

```{table}
---
align: center
---
|           | **$V_0$** | **$V_1$** | **$V_2$** | **$V_3$** | **$V_4$** | **$V_5$** | **$V_6$** |
| :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| **$V_0$** |     -     |     2     |     -     |     1     |     -     |     -     |     -     |
| **$V_1$** |     -     |     -     |     -     |     3     |    10     |     -     |     -     |
| **$V_2$** |     4     |     -     |     -     |     -     |     -     |     5     |     -     |
| **$V_3$** |     -     |     -     |     2     |     -     |     2     |     8     |     4     |
| **$V_4$** |     -     |     -     |     -     |     -     |     -     |     -     |     5     |
| **$V_5$** |     -     |     -     |     -     |     -     |     -     |     -     |     -     |
| **$V_6$** |     -     |     -     |     -     |     -     |     -     |     1     |     -     |
```

La matriz de adyacencia es una representación eficiente para grafos densos, donde el número de aristas es cercano al número máximo posible ($|V|^2$). Sin embargo, puede ser ineficiente en términos de espacio para grafos dispersos, donde el número de aristas es mucho menor que el número máximo posible. En la matriz de ejemplo solo unos pocos elementos son diferentes de '-'.

Una ventaja de esta representación es que permite verificar rápidamente si existe una arista entre dos vértices, simplemente consultando el valor en la matriz.

Para representar grafos no ponderados se acostumbra poner un 1 donde hay una arista y 0 en el resto de la matriz.

Si el grafo es no dirigido, la matriz de adyacencia será simétrica, por ejemplo la matriz de adyacencia para el siguiente grafo:

```{figure} ../_static/figures/grafo_no_dirigido_light.svg
---
class: only-light-mode
width: 60%
---
Grafo no dirigido
```

```{figure} ../_static/figures/grafo_no_dirigido_dark.svg
---
class: only-dark-mode
width: 60%
---
Grafo no dirigido
```

```{table}
---
align: center
---
|         | **$A$** | **$B$** | **$C$** | **$D$** | **$E$** |
| :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| **$A$** |    -    |    4    |    5    |    -    |    1    |
| **$B$** |    4    |    -    |    2    |    -    |    -    |
| **$C$** |    5    |    2    |    -    |    4    |    -    |
| **$D$** |    -    |    -    |    4    |    -    |    3    |
| **$E$** |    1    |    -    |    -    |    3    |    -    |
```

### Listas de adyacencias

La lista de adyacencia es otra forma de representar un grafo. En lugar de usar una matriz, se utiliza una lista de listas (o un diccionario) donde cada vértice tiene una lista de sus vecinos adyacentes y el peso de la arista que los conecta.

Para el grafo dirigido anterior la lista de adyacencia sería:

```{figure} ../_static/figures/grafo_dirigido_lista_light.svg
---
class: only-light-mode
width: 80%
---
Lista de adyacencia del grafo dirigido
```

```{figure} ../_static/figures/grafo_dirigido_lista_dark.svg
---
class: only-dark-mode
width: 80%
---
Lista de adyacencia del grafo dirigido
```

En cada nodo de la lista se almacena el par $(vecino, peso)$ que representa la arista que conecta el vértice con su vecino.

A continuación la lista de adyacencia para el grafo no dirigido del punto anterior:

```{figure} ../_static/figures/grafo_no_dirigido_lista_light.svg
---
class: only-light-mode
width: 80%
---
Lista de adyacencia del grafo no dirigido
```

```{figure} ../_static/figures/grafo_no_dirigido_lista_dark.svg
---
class: only-dark-mode
width: 80%
---
Lista de adyacencia del grafo no dirigido
```

## Grafos en Python

En Python existen varias bibliotecas que facilitan la representación y manipulación de grafos. Vamos a usar **NetworkX** para representar grafos y **Matplotlib** para visualizarlos.

**NetworkX** proporciona estructuras de datos y algoritmos eficientes para trabajar con grafos, lo que facilita tareas como la búsqueda de caminos, la detección de ciclos y el análisis de redes.

Ambas bibliotecas se deben instalar previamente.

```console
pip install networkx matplotlib
```

Los vértices deben ser de tipos _hashables_, es decir, cualquier tipo que pueda ser clave de un diccionario. Los tipos inmutables como cadenas, números o tuplas suelen ser una buena elección para usarlos como identificadores de nodos.

### Crear grafos

Existen varias formas de crear un grafo. A continuación algunas de las más usuales:

`Graph()`
: Para crear un grafo simple, vacío y no dirigido.

`DiGraph()`
: Para crear un grafo dirigido incialmente vacío.

Para agregar aristas se puede usar:

`add_edge(u, v, weight=w)`
: Para agregar una arista desde el nodo `u` al nodo `v` con un peso `w`.
Si el grafo es no dirigido, también se agregará la arista en la dirección opuesta.
Si los nodos `u` y `v` no existen en el grafo, se agregarán automáticamente.

`add_weighted_edges_from(iterable)`
: Para agregar múltiples aristas de una sola vez desde un `iterable` de tuplas `(u, v, w)`. Si se omite el peso, se asumirá un peso de 1.

`add_edges_from(iterable)`
: Para agregar múltiples aristas de una sola vez desde `iterable` de tuplas `(u, v, d)`. El último parámetro, opcional, puede ser un diccionario con atributos de la arista.

También se pueden agregar nodos individuales

`add_node(n)`
: Para agregar un nodo `n` al grafo.

`add_nodes_from(iterable)`
: Para agregar múltiples nodos desde un `iterable`. Cada elemento puede ser un nodo o una tupla de la forma `(n, d)`, donde `n` es el nodo y `d` es un diccionario con los atributos opcionales.

### Graficar grafos

**Networkx** incluye interfaces para la visualización de grafos en **Matplotlib** y **Graphviz**.

La interfaz `networkx.drawing.nx_pylab` provee funciones que permiten crear y usar figuras con ejes de **Matplotlib**.

```{code-cell} python
---
tags: hide-output
---
import networkx as nx
import matplotlib.pyplot as plt  # permite crear figuras, mostrarlas, etc.

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos y aristas
G.add_weighted_edges_from([(0, 1, 4), (0, 2, 5), (1, 2, 2), (2, 3, 4), (3, 4, 3)])

# Dibujar el grafo
# pos = nx.spring_layout(G) # posiciones para todos los nodos
pos = nx.circular_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.kamada_kawai_layout(G)
nx.draw(
    G,
    pos,
    with_labels=True,  # etiquetar nodos
    node_size=800,  # tamaño de los nodos
    node_color="#e1f5ff",  # color de los nodos (azul claro)
    edgecolors="#4682b4",  # color del borde de los nodos (azul acero)
    linewidths=2,  # grosor del borde de los nodos
    font_size=12,  # tamaño de la fuente
    font_color="#333333",  # color de la fuente
    edge_color="#333333",  # color de las aristas
    width=2,  # grosor de las aristas
)
edge_labels = nx.get_edge_attributes(G, "weight")  # Obtener los pesos de las aristas
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color="#333333"
)  # Dibujar las etiquetas de las aristas
plt.title("Grafo Dirigido")  # Título de la figura
plt.show()  # Mostrar la figura
```

Un _**layout**_ es un diccionario {nodo: (x, y)} con la posición de cada vértice. **NetworkX** incluye varios algoritmos para calcular layouts.

`spring_layout`
: Posiciona nodos con un modelo de fuerzas.

`circular_layout`
: Posiciona nodos en un círculo.

`shell_layout`
: Posiciona nodos en capas concéntricas.

`kamada_kawai_layout`
: Posiciona nodos minimizando la energía de un sistema de resortes.

### Ejemplo: Grafo de una red de transporte

```{code-cell} python
---
tags: hide-input
---
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Crear grafo dirigido (direcciones de rutas posibles)
G = nx.DiGraph()

# 1) Agregar estaciones (nodos) con atributos
G.add_node("Central", tipo="Terminal", linea="Roja")
G.add_node("Parque", tipo="Normal", linea="Roja")
G.add_node("Puerto", tipo="Normal", linea="Roja")
G.add_node("Museo", tipo="Normal", linea="Verde")
G.add_node("Plaza", tipo="Terminal", linea="Verde")
G.add_node("Estadio", tipo="Normal", linea="Verde")

# 2) Agregar conexiones (aristas) con atributos
G.add_edge("Central", "Parque", distancia=2.5, tipo="normal")
G.add_edge("Parque", "Puerto", distancia=3.0, tipo="express")
G.add_edge("Puerto", "Museo", distancia=4.0, tipo="normal")
G.add_edge("Museo", "Plaza", distancia=2.0, tipo="normal")
G.add_edge("Plaza", "Estadio", distancia=3.5, tipo="express")
G.add_edge("Parque", "Museo", distancia=5.0, tipo="normal")

# 3) Dibujar grafo
# Definimos posiciones manualmente para mejorar la visualización y cumplir requerimientos
pos = {
    "Puerto": (0, 0),
    "Parque": (5, 0),
    "Museo": (2, 2.5),
    "Plaza": (0, 5),
    "Central": (6, 5),
    "Estadio": (-2, 7),
}

# Colores de nodos según línea
colores_lineas = {"Roja": "#ffcdd2", "Verde": "#c8e6c9"}
node_colors = [colores_lineas[G.nodes[n]["linea"]] for n in G.nodes()]

# Grosor y estilo de aristas según tipo de vía
edge_widths = [2 if G[u][v]["tipo"] == "express" else 1 for u, v in G.edges()]
edge_styles = [
    "dashed" if G[u][v]["tipo"] == "express" else "solid" for u, v in G.edges()
]

# Dibujar nodos
nx.draw_networkx_nodes(
    G, pos, node_color=node_colors, node_size=1200, edgecolors="#333333"
)

# Dibujar aristas
for i, (u, v) in enumerate(G.edges()):
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v)],
        width=edge_widths[i],
        style=edge_styles[i],
        arrows=True,
        edge_color="#333333",
    )

# Etiquetas de nodos
nx.draw_networkx_labels(G, pos, font_size=9)

# Etiquetas de aristas (distancia)
edge_labels = {(u, v): f'{G[u][v]["distancia"]}' for u, v in G.edges()}
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color="#333333", font_size=8
)

# Leyenda
legend_elements = [
    Line2D(
        [0],
        [0],
        color="#ffcdd2",
        marker="o",
        linestyle="None",
        markersize=12,
        label="Línea Roja",
        markeredgecolor="#333333",
    ),
    Line2D(
        [0],
        [0],
        color="#c8e6c9",
        marker="o",
        linestyle="None",
        markersize=12,
        label="Línea Verde",
        markeredgecolor="#333333",
    ),
    Line2D([0], [0], color="gray", linewidth=2, linestyle="solid", label="Vía normal"),
    Line2D(
        [0], [0], color="gray", linewidth=2, linestyle="dashed", label="Vía express"
    ),
]
plt.legend(handles=legend_elements, loc="upper right", fontsize=10)

plt.title("Mini-Red de Transporte Urbano", fontsize=14)
plt.axis("off")
plt.margins(0.2)  # Márgenes para evitar recortes
plt.show()
```

## Recursos para profundizar

- [Documentación de NetworkX](https://networkx.org/documentation/stable/index.html)
- [Tutorial de Matplotlib](https://matplotlib.org/stable/tutorials/index.html)
- [Introducción a grafos y redes con Python](https://cienciadedatos.net/documentos/pygml01-introduccion-grafos-redes-python)
- [NetworkX Tutorial](https://www.kaggle.com/code/alireza151/networkx-tutorial)
