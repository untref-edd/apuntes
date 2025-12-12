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
description: Recorridos de grafos, BFS, DFS
---

# Recorridos

En esta sección veremos algoritmos para recorrer grafos. Basicamente hay dos formas de recorrer un grafo: a lo ancho y en profundidad.

Recorrer un grafo significa visitar todos sus vértices y aristas de una manera sistemática y ordenada. 

Los recorridos de grafos son fundamentales en muchas aplicaciones, como la búsqueda de caminos, la detección de ciclos, la planificación de tareas y la optimización de redes.

## Recorrido a lo ancho: _Breadth First Search_ (BFS)

El recorrido a lo ancho, o BFS, es un algoritmo que explora los nodos de un grafo en capas, visitando primero todos los nodos a una distancia dada antes de pasar a los nodos a una mayor distancia. Esto se logra utilizando una cola para llevar un registro de los nodos por visitar.

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

### Complejidad del algoritmo BFS

$$
O(|V| + |A|)
$$

El tiempo de ejecución del algoritmo BFS es $O(|V| + |A|)$ cuando el grafo se representa mediante **listas de adyacencia**.

Esto se debe a que:

1.  Cada vértice se encola y desencola a lo sumo una vez. Las operaciones en la cola toman tiempo constante $O(1)$, por lo que el tiempo total dedicado a estas operaciones es $O(|V|)$.
2.  Al procesar un vértice $u$, el algoritmo recorre su lista de adyacencia. Como cada arista $(u, v)$ se considera una vez si el grafo es dirigido o dos veces si el grafo es no dirigido, el tiempo total dedicado a recorrer las listas de adyacencia es proporcional al número total de aristas, es decir $O(|A|)$. Esto es importante porque hace que obtener los vértices adyacentes tome tiempo proporcional al número de aristas incidentes en el vértice y no al número total de vértices.

Por lo tanto, la complejidad total es la suma de los tiempos para procesar vértices y aristas: $O(|V| + |A|)$.

```{admonition} Importante
:class: important
Si el grafo se representa mediante una **matriz de adyacencia**, para encontrar los vértices adyacentes a $u$ debemos recorrer toda la fila correspondiente en la matriz, lo cual toma tiempo $O(|V|)$. Como esto se hace para cada uno de los $|V|$ vértices, la complejidad total se convierte en **$O(|V|^2)$**. Por lo tanto, el algoritmo BFS es $O(|V|^2)$ cuando el grafo se representa mediante una matriz de adyacencia.
```

### Aplicaciones del recorrido BFS

#### Caminos Mínimos en grafos no ponderados

Supongamos que queremos calcular el camino mínimo (menor costo) desde un vértice $s$ a cualquier otro vértice alcanzable desde $s$. Si el grafo es no ponderado, podemos considerar que todas las aristas tienen peso 1, el algoritmo BFS es el más apropiado para resolver este problema. En este caso el camino mínimo entre dos vértices coincide con el camino más corto.

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

La ventaja de este algoritmo es que encuentra el camino más corto (mínimo número de aristas) desde el vértice `s` a cualquier otro vértice alcanzable desde `s` en $O(|V| + |A|)$.

### Grafo Bipartito

Grafo Bipartito
: Un grafo **no dirigido** es bipartito si los vértices se pueden dividir en dos grupos, de modo tal que las aristas vayan siempre de un vértice de un grupo a un vértice del otro grupo.

```{figure} ../_static/figures/grafo_bipartito_light.svg
---
class: only-light-mode
width: 60%
---
Grafo Bipartito
```

```{figure} ../_static/figures/grafo_bipartito_dark.svg
---
class: only-dark-mode
width: 60%
---
Grafo Bipartito
```

Reordenando los vértices de un grafo bipartito se puede ver claramente la división en dos grupos, donde las aristas van siempre de un grupo a otro y no hay aristas entre vértices del mismo grupo. En la imagen no hay aristas entre vértices azules ni tampoco entre vértices rojos.

```{figure} ../_static/figures/grafo_bipartito_ordenado_light.svg
---
class: only-light-mode
width: 60%
---
Grafo Bipartito Ordenado
```

```{figure} ../_static/figures/grafo_bipartito_ordenado_dark.svg
---
class: only-dark-mode
width: 60%
---
Grafo Bipartito Ordenado
```

El algoritmo para verificar si un grafo es bipartito, se puede implementar usando los valores `True` y `False` para *pintar* los vértices y verificar que no haya aristas entre vértices del mismo color. El recorrido a lo ancho es ideal para este problema ya que va visitando los vértices por capas, es decir, va visitando los vértices que están a una distancia 1, luego los vértices que están a una distancia 2, y así sucesivamente.

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
: Bot que utilizan los motores de búsqueda para descubrir páginas siguiendo los enlaces que hay en ella. Más adelante veremos cómo implementar un web crawler en el capítulo de {doc}`../3-representacion-datos/3-6-web-scraping`.

Sistemas de navegación GPS
: Para encontrar caminos entre dos puntos en un mapa ponderando distancias, tiempos, etc.

## Recorrido en profundidad: _Depth First Search_ DFS

El recorrido en profundidad, o DFS, es un algoritmo que explora los nodos profundizando lo más posible en cada rama antes de retroceder. Esto se logra utilizando una pila (o la pila de llamadas del sistema si se usa recursión) para llevar un registro de los nodos que deben ser visitados. (En forma análoga a la técnica de backtracking que intenta profundizar una solución hasta que encuentra una solución válida o hasta que se queda sin opciones)

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

#### Detección de ciclos

El recorrido en profundidad (DFS) es muy útil para detectar si un grafo contiene ciclos.

En un grafo dirigido, existe un ciclo si durante el DFS encontramos una arista que va hacia un vértice que está siendo visitado actualmente (es decir, que está en la pila de recursión). Esto se conoce como una **arista de retroceso** (*back edge*).

```text
TIENE_CICLO(G):
    visitado = Conjunto()
    en_recursion = Conjunto()

    PARA CADA v EN G.vertices:
        SI detecta_ciclo(v, visitado, en_recursion):
            DEVOLVER Verdadero
    
    DEVOLVER Falso

detecta_ciclo(v, visitado, en_recursion):
    visitado.agregar(v)
    en_recursion.agregar(v)

    PARA CADA vecino EN v.adyacentes:
        SI vecino EN en_recursion:
            DEVOLVER Verdadero  # Ciclo encontrado
        
        SI vecino NO EN visitado:
            SI detecta_ciclo(vecino, visitado, en_recursion):
                DEVOLVER Verdadero

    en_recursion.remover(v)
    DEVOLVER Falso
```

### Otras aplicaciones

Resolución de dependencias
: Herramientas de construcción como Make o gestores de paquetes como npm utilizan DFS (mediante ordenamiento topológico) para determinar el orden correcto de compilación o instalación.

Inteligencia Artificial en juegos
: Algoritmos como Minimax utilizan DFS para explorar el árbol de decisiones en juegos como el ajedrez o las damas.

Generación y resolución de laberintos
: DFS se usa comúnmente para generar laberintos perfectos (con un único camino entre dos puntos) y para encontrar la salida.

Análisis de código
: Los compiladores recorren el Árbol de Sintaxis Abstracta (AST) usando DFS para analizar y optimizar el código fuente.
