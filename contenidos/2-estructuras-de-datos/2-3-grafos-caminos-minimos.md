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
---
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

El algoritmo de Dijkstra fue propuesto por [Edsger W. Dijkstra](https://es.wikipedia.org/wiki/Edsger_Dijkstra){target="_blank"} en 1956 y publicado en 1959. Es un algoritmo ávido o *greedy* que encuentra todos los caminos mínimos desde un nodo inicial a todos los demás nodos en un grafo ponderado.

Sigue una estrategia de exploración de los nodos más cercanos al origen, actualizando las distancias mínimas a medida que avanza. 

La inicialización del algoritmo consiste a marcar a todos los vértices con distancia infinita, excepto el vértice de origen que se marca con distancia 0 y se encola en una **cola de prioridad de mínimos**.

En cada ciclo se extrae el vértice con la distancia más corta desde el origen, se lo marca como visitado y se exploran sus vecinos. Si se encuentra un vecino ya visitado, se ignora, ya que no se puede mejorar su distancia. A cada vecino se le actualiza su distancia si se encuentra un camino más corto y se encola.

El paso *greedy* del algoritmo consiste en seleccionar el vértice no visitado con la distancia más corta y marcarlo como visitado. Es decir el algoritmo considera que esa distancia no se podrá mejorar por ningún otro camino alternativo.

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

