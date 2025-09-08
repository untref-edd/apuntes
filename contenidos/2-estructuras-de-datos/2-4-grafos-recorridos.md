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

# Recorridos

En esta sección veremos dos algoritmos para recorrer grafos. Basicamente hay dos formas de recorrer un grafo: a lo ancho y en profundidad.

Recorrer un grafo significa visitar todos sus vértices y aristas de una manera sistemática y ordenada. Los recorridos de grafos son fundamentales en muchas aplicaciones, como la búsqueda de caminos, la detección de ciclos, la planificación de tareas y la optimización de redes.

## Recorrido a lo ancho: _Breadth First Search_ (BFS)

El recorrido a lo ancho, o BFS, es un algoritmo que explora los nodos de un grafo en capas, visitando primero todos los nodos a una distancia dada antes de pasar a los nodos a una mayor distancia. Esto se logra utilizando una cola para llevar un registro de los nodos que deben ser visitados. Un ejemplo de aplicación de este recorrido lo vimos cuando estudiamos orden topológico.

```text
BFS (s: Vertice):
    q <- Cola()

    q.encolar(s)
    visitado[s] = True

    MIENTRAS NO q.esta_vacia()
        v = q.desencolar()

        PARA CADA w EN v.adyacentes:
            SI NO visitado[w]:
                visitado[w] = True
                q.encolar(w)
```

## Complejidad del algoritmo BFS

$$
O(|V| + |A|)
$$

## Aplicaciones del recorrido BFS

### Camino Mínimo en grafos sin pesos

```text
CAMINO_MINIMO_BFS (s: Vertice)
    q <- Cola()

    distancia[s] = 0
    previo[s] = None

    q.encolar(s)
    visitado[s] = True

    MIENTRAS NO q.esta_vacia()
        v = q.desencolar()

        PARA CADA w EN v.adyacentes:
            SI NO visitado[w]:
                visitado[w] = True
                distancia[w] = distancia[v] + 1
                previo[w] = v
                q.encolar(w)
```

La ventaja de este algoritmo es que encuentra el camino más corto (mínimo número de aristas) desde el vértice `s`{l=python} a cualquier otro vértice alcanzable desde `s`{l=python} en $O(|V| + |A|)$.

### Grafo Bipartito

Grafo Bipartito
: Un grafo **no dirigido** es bipartito si los vértices se pueden dividir en dos grupos, de modo tal que las aristas vayan siempre de un vértice de un grupo a un vértice del otro grupo.

```{figure} ../assets/images/grafo-bipartito.png
---
name: grafo-bipartito
align: center
width: 60%
---
Grafo Bipartito
```

Reordenando los vértices de un grafo bipartito se puede ver claramente la división en dos grupos, donde las aristas van siempre de un grupo a otro y no hay aristas entre vértices del mismo grupo.

```{figure} ../assets/images/grafo-bipartito-ordenado.png
---
name: grafo-bipartito-ordenado
align: center
width: 60%
---
Grafo Bipartito Ordenado
```

```text
ES_BIPARTITO (s: Vertice):
    q <- Cola()

    color[s] = True

    q.encolar(s)
    visitado[s] = True

    MIENTRAS NO q.esta_vacia()
        v = q.desencolar()

        PARA CADA w EN v.adyacentes:
            SI NO visitado[w]:
                visitado[w] = True
                color[w] = NOT color[v]
                q.encolar(w)
            SINO:
                SI color[w] == color[v]:
                    DEVOLVER False

    DEVOLVER True
```

### Otras Aplicaciones

Web Crawler
: Bot que utilizan los motores de búsqueda para descubrir páginas siguiendo los enlaces que hay en ella.

Sistemas de navegación GPS
: Para encontrar localizaciones vecinas.

## Recorrido en profundidad: _Depth First Search_ DFS

El recorrido en profundidad, o DFS, es un algoritmo que explora los nodos de un grafo adentrándose lo más posible en cada rama antes de retroceder. Esto se logra utilizando una pila (o la pila de llamadas del sistema si se usa recursión) para llevar un registro de los nodos que deben ser visitados.

```text
DFS (v, visitado = {}, contador = 0):
    visitado[v] = True
    contador += 1

    PARA CADA w EN v.adyacentes:
        SI NO visitado[w]:
            DFS(w, visitado, contador)

    DEVOLVER contador
```

### Complejidad

$$
O(|V| + |A|)
$$

### Aplicaciones

#### Componentes conexas

Grafo conexo
: Un grafo no dirigido es conexo si para todo par de vértices $u$ y $v$ de $G$, hay un camino que los une.

Componentes conexas
: Dado un grafo no dirigido $G$, una componentes conexa es un conjunto de vértices tal que empezando en uno de ellos cualquiera podemos acceder al resto recorriendo las aristas.

Componentes fuertemente conexas
: Dado un grafo dirigido $G$, una componentes fuertemente conexa es un conjunto de vértices tal que empezando en uno de ellos cualquiera podemos acceder al resto recorriendo las aristas en el sentido que indican.

```text
COMPONENTES_CONEXAS (G: Grafo):
    PARA CADA v EN G.vertices:
        visitado[v] = -1

    contador = 0

    PARA CADA v EN G.vertices:
        SI visitado[v] == -1
            DFS(v, visitado, contador)
            contador += 1


DFS (v, visitado, contador):
    visitado[v] = contador
    PARA CADA w EN v.adyacentes:
        SI visitado[w] == -1:
            DFS(w, visitado, contador)
```

### Otras aplicaciones

- Detección de ciclos en un grafo dirigido o no dirigido.
- Encontrar caminos en un laberinto.
- Encontrar componentes fuertemente connexas en un grafo dirigido (usando el algoritmo de Kosaraju o Tarjan).
