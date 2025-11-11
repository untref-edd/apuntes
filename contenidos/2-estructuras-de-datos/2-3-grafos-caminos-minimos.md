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

# Caminos Mínimos

Un camino mínimo en un grafo es una secuencia de aristas que conecta dos vértices con el menor peso total posible. Este concepto es fundamental en diversas aplicaciones, como la navegación, la planificación de rutas y la optimización de redes.

Por ejemplo dado el siguiente grafo:

```{figure} ../assets/images/grafo_dijkstra.png
---
name: grafo_dijkstra
width: 60%
---
```

En la siguiente tabla encontramos los caminos mínimos desde el vértice $A$ a los demás vértices:

```{table}
---
align: center
---
| Vértice | Camino Mínimo | Costo |
| :-----: | :-----------: | :---: |
|   $A$   |       -       |   0   |
|   $B$   |    $A-C-B$    |   3   |
|   $C$   |     $A-C$     |   1   |
|   $D$   |    $A-C-D$    |   3   |
|   $E$   |  $A-C-D-E$    |   6   |
```

## Algoritmos para Encontrar Caminos Mínimos

Existen varios algoritmos para encontrar caminos mínimos en grafos, entre los más conocidos se encuentran:

Dijkstra
: Este algoritmo es eficiente para grafos ponderados con aristas de peso no negativo. Utiliza una cola de prioridad para explorar los vértices más cercanos al origen.

Bellman-Ford
: Este algoritmo puede manejar grafos con aristas de peso negativo y es útil para detectar ciclos negativos. Funciona relajando las aristas repetidamente.

Ambos algoritmos funcionan en grafos dirigidos y no dirigidos.

Cuando se trata de algoritmos sin pesos en las aristas, se acostumbra definir el camino mínimo como el que tiene la menor cantidad de aristas, lo que se logra asigando un costo de 1 a cada arista.

## Algoritmo de Dijkstra

El ***algoritmo de Dijkstra*** fue propuesto por [Edsger W. Dijkstra](https://es.wikipedia.org/wiki/Edsger_Dijkstra) en 1956 y publicado en 1959. Es un algoritmo ávido o ***greedy*** que encuentra todos los caminos mínimos desde un nodo inicial a todos los demás nodos en un grafo ponderado.

Sigue una estrategia de exploración de los nodos más cercanos al origen, actualizando las distancias mínimas a medida que avanza.

La inicialización del algoritmo consiste a marcar a todos los vértices con distancia infinita, excepto el vértice de origen que se marca con distancia 0 y se encola en una **cola de prioridad de mínimos**.

En cada ciclo se extrae el vértice con la distancia más corta desde el origen, se lo marca como visitado y se exploran sus vecinos. Si se encuentra un vecino ya visitado, se ignora, ya que no se puede mejorar su distancia. A cada vecino se le actualiza su distancia si se encuentra un camino más corto y se encola.

El paso ***greedy*** del algoritmo consiste en seleccionar el vértice no visitado con la distancia más corta y **marcarlo como visitado**. Es decir el algoritmo considera que esa distancia no se podrá mejorar por ningún otro camino alternativo.

```{code-block}
---
linenos:
---
DIJKSTRA (G: DiGrafo, s: Vertice)
    pq = ColaDePrioridad()

    PARA CADA v EN G.vertices
        distancia[v] = ∞
        previo[v] = None
        visitado[v] = False

    distancia[s] = 0
    pq.encolar(s, 0)

    MIENTRAS NO pq.esta_vacia():
        v = pq.desencolar_minimo()

        visitado[v] = True

        PARA CADA w EN v.adyacentes:
            SI w no está visitado:
                SI distancia[v] + peso(v, w) < distancia[w]:
                    distancia[w] = distancia[v] + peso(v, w)
                    previo[w] = v
                    pq.encolar(w, distancia[w])
```

A continuación se muestra la aplicación del algoritmo al grafo de la figura anterior.

```{code-cell} python
import networkx as nx
from grafos import caminos_minimos

# Definición del grafo dirigido (puedes modificarlo y ejecutar para ver el paso a paso)
G = nx.DiGraph()
edges = [
    ("A", "B", 4),
    ("A", "C", 1),
    ("B", "E", 3),
    ("C", "B", 2),
    ("C", "D", 2),
    ("D", "E", 3),
]
G.add_weighted_edges_from(edges)
SOURCE = "A"

caminos_minimos.show_dijkstra_step_by_step(G, SOURCE)
```

### Aristas negativas

Como el ***algoritmo de Dijkstra*** se basa en extraer de la cola de prioridad el vértice con la menor distancia provisional desde el origen y marcarlo como **visitado** —suponiendo que esa distancia ya no podrá mejorarse—, surge un problema cuando existen aristas con peso negativo ya que podría aparecer más adelante un camino más corto hacia un vértice que ya fue marcado como **visitado**, lo que rompe el supuesto fundamental del algoritmo.

Si hay alguna arista negativa ***Dijkstra*** puede fallar o no según el vértice que se considere como origen y la topología del grafo, por lo tanto para asegurar que el algoritmo funciona siempre:

```{important}
El algoritmo de ***Dijkstra*** no admite grafos con aristas con pesos negativos para poder asegurar su correcto funcionamiento
```

A continuación se muestra un ejemplo con una arista negativa donde el algoritmo de ***Dijkstra*** falla:

```{code-cell} python
import networkx as nx
from grafos import caminos_minimos

# Definición del grafo dirigido (puedes modificarlo y ejecutar para ver el paso a paso)
G = nx.DiGraph()
edges = [
    ("A", "B", 1),
    ("A", "C", 2),
    ("B", "E", 3),
    ("C", "B", -2),
    ("C", "D", 2),
    ("D", "E", 3),
]
G.add_weighted_edges_from(edges)
SOURCE = "A"

caminos_minimos.show_dijkstra_step_by_step(G, SOURCE)
```

El primer vértice que extrae de la cola de prioridad (paso 4) y marca como visitado es el vértice $B$. Luego al procesar $C$ se encuentra un camino más corto hasta $B$ con un costo total de 0, pero no puede actualizar su distancia ya que ya fue marcado como visitado (paso 7).

Si la arista $(A, B)$ fuera la única arista negativa del grafo entonces el algoritmo no fallaría y encontaría correctamente los costos mínimos hacia todos los vértices.

### Complejidad del algoritmo de Dijkstra

Si el grafo se representa mediante **listas de adyacencia**, recorrer todas las aristas del grafo tiene un costo de $O(|V|+|A|)$, que se simplifica a $O(|A|)$ cuando el grafo es conexo y $|A| \ge |V|$.

El algoritmo utiliza además una **cola de prioridad** (implementada típicamente con un **montículo binario**) donde se almacenan los vértices junto con su distancia mínima tentativa. Las operaciones críticas son:

- **`extract-min`** (extraer el vértice con menor distancia): costo $O(\log|V|)$, ejecutada a lo sumo $|V|$ veces para los vértices cuyo valor mínimo definitivo se extrae.
- Cada **relajación que mejora la distancia** del vértice objetivo simplemente **vuelve a encolarlo** con la nueva distancia, también con un costo de $O(\log|V|)$.

En total, cada arista se procesa a lo sumo una vez por iteración de extracción del vértice origen, y puede generar como máximo una inserción en la cola por relajación efectiva. Por tanto, el costo total del algoritmo es:

$$
T(n) = O(|V|\log|V|) + O(|A|\log|V|).
$$

Como en la mayoría de los grafos de interés se cumple $|A| \ge |V|$, el primer término de la suma queda dominado por el segundo y se obtiene la cota habitual:

$$
T(n) = O(|A|\log|V|).
$$

Otra manera de verlo: en cada iteración del bucle *MIENTRAS*, se procesan únicamente los adyacentes del vértice extraído, y a lo largo de todo el algoritmo cada arista ((u,v)) se examina una sola vez. Formalmente:

$$
\sum_{v \in V} \deg(v) = 2|A| \quad \Rightarrow \quad O(|A|)\ \text{relajaciones}.
$$

Cada relajación puede provocar la inserción de un nuevo elemento en la cola de prioridad, lo que explica la complejidad final de $O(|A|\log|V|)$.

## Algoritmo de Bellman-Ford

El ***algoritmo de Bellman-Ford*** fue desarrollado de manera independiente por dos investigadores en la década de 1950: [Richard Bellman](https://es.wikipedia.org/wiki/Richard_Bellman), quien lo publicó en 1958 en el marco de su trabajo sobre programación dinámica, y [Lester R. Ford Jr.](https://en.wikipedia.org/wiki/L._R._Ford_Jr.), que lo había presentado unos años antes (1956).

Este algoritmo es una alternativa y complemento al ya conocido algoritmo de ***Dijkstra*** (1956) que ofrece una solución eficiente al problema de caminos mínimos desde un origen pero con la restricción de no tener aristas con pesos negativos.

En muchos problemas reales pueden aparecer aristas con pesos negativos, por ejemplo, en modelos económicos (pérdidas y ganancias), en análisis de redes de flujo o incluso en ciertas métricas de ingeniería de software o logística. En estos casos, ***Bellman-Ford*** ofrece una solución más general:

- Permite calcular los caminos mínimos desde un nodo origen a todos los demás, incluso con pesos negativos.

- Informa si existe un **ciclo negativo**, es decir, un ciclo en el que la suma de los pesos es menor que cero, lo que implicaría que no existe una solución bien definida para el problema de caminos mínimos (porque siempre se puede “dar una vuelta más” al ciclo y disminuir la distancia indefinidamente).

Ciclo Negativo
: Un ciclo negativo en un grafo dirigido y ponderado es una secuencia de aristas que comienza y termina en el mismo vértice, y cuya suma de pesos es negativa.

Formalmente $C=V_0 \to V_1 \to V_2 \to ... \to V_k \to V_0$ es un ciclo negativo si:

$$
\sum_{i=0}^{k-1} w(v_i, v_{i+1}) < 0
$$

donde $w(u, v)$ es el peso de la arista $u \to w$

***Bellman-Ford*** se basa en la técnica de programación dinámica y en el principio de relajación de aristas:

La idea central es que, en un grafo sin ciclos negativos, el camino más corto entre dos vértices tiene a lo sumo $|V|−1$ aristas.

El algoritmo realiza sucesivas iteraciones en las que intenta mejorar (*relajar*) las distancias conocidas, comparando si pasar por una nueva arista ofrece un camino más corto.

Supuesto clave
: Después de realizar $∣V∣−1$ iteraciones, todas las distancias mínimas posibles estarán correctamente calculadas.

- Cada iteración (relajación) asegura que se encuentra la distancia mínima, al menos, a un vértice del grafo. En cada una de estas iteraciones se revisan todas las aristas del grafo, recalculando el costo mínimo de todos los vértices.

- En $|V|-1$ iteraciones se habrán explorado todas las posiblidades y por lo tanto se finaliza el cálculo.

- Una iteración adiciónal a las $|V|-1$ iteraciones anteriores, permite detectar ciclos negativos, ya que si la distancia de un vértice se mejora es porque hay al menos un ciclo negativo en el grafo.

```{code-block}
---
linenos:
---
BELLMAN_FORD (G: DiGrafo, s: Vertice)

    PARA CADA v EN G.nodos
        distancia[v] = ∞
        previo[v] = None

    distancia[s] = 0

    REPETIR len(G.nodos) - 1 VECES:
        PARA CADA (v, w, peso) EN G.aristas:
            SI distancia[v] + peso < distancia[w]
                distancia[w] = distancia[v] + peso
                previo[w] = v

    PARA CADA (v, w, peso) EN G.aristas:
        SI distancia[v] + peso < distancia[w]
            REPORTAR error: grafo con ciclos negativos
```

A continuación se muestra un ejemplo con una arista negativa donde el algoritmo de ***Dijkstra*** falla:

```{code-cell} python
import networkx as nx
from grafos import caminos_minimos

# Definición del grafo dirigido (puedes modificarlo y ejecutar para ver el paso a paso)
G = nx.DiGraph()
edges = [
    ("A", "B", 1),
    ("A", "C", 2),
    ("B", "E", 3),
    ("C", "B", -2),
    ("C", "D", 2),
    ("D", "E", 3),
]
G.add_weighted_edges_from(edges)
SOURCE = "A"

caminos_minimos.show_bellman_ford_step_by_step(G, SOURCE)
```

### Complejidad del algoritmo de Bellman-Ford

La complejidad temporal del ***algoritmo de Bellman-Ford*** está determinada por los dos ciclos anidados de las líneas 9 y 10. El bucle *REPETIR* se ejecuta $|V| - 1$ veces y el ciclo *PARA* se ejecuta $|A|$ veces y como adentro de los ciclos todas las operaciones son $O(1)$ queda:

$$
T(n)=O(|V|\times|A|)
$$

## Recursos para profundizar

- [Algoritmo de Dijkstra (Wikipiedia)](https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra)
- [Agloritmo de Bellman-Ford (Wikipedia)](https://es.wikipedia.org/wiki/Algoritmo_de_Bellman-Ford)
- [Algoritmo de Dijkstra en DSA](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)
- [Algoritmo de Bellman-Ford en DSA](https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php)
