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
width: 50%
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

A continuación se muestra la aplicación del algoritmo al grafo de la figura anterior, desde que se desencola el vértice inicial a distancia 0 y se lo marca como visitado. Es decir en la primera iteración del ciclo MIENTRAS, luego de desencolar el vértice inicial.

```{code-cell}python
:tags: [remove-input]
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io, base64, json, secrets
from heapq import heappush, heappop
from IPython.display import HTML, display

# Grafo dirigido
G = nx.DiGraph()
edges = [
    ("A","B",4), ("A","C",1),
    ("B","E",3), 
    ("C","B",2), ("C","D",2),
    ("D","E",3)
]
G.add_weighted_edges_from(edges)
SOURCE = "A"

# -------- Dijkstra con subpasos --------
def dijkstra_trace_fine(G, s):
    dist = {v: float("inf") for v in G.nodes()}
    prev = {v: None for v in G.nodes()}
    visited = {v: False for v in G.nodes()}
    pq = []
    dist[s] = 0
    heappush(pq, (0, s))

    steps = []
    step = 1

    while pq:
        d, v = heappop(pq)
        if visited[v]:
            continue

        # Subpaso: desencolamos v
        visited[v] = True
        steps.append(dict(
            step=step, action=f"Desencolar {v}", current=v,
            dist=dict(dist), prev=dict(prev),
            visited=dict(visited), pq=list(pq)
        ))
        step += 1

        # Subpasos: procesar adyacentes
        for w, edata in G[v].items():
            if not visited[w]:
                # mostramos antes de comparar
                updated = False
                if dist[v] + edata["weight"] < dist[w]:
                    dist[w] = dist[v] + edata["weight"]
                    prev[w] = v
                    heappush(pq, (dist[w], w))
                    updated = True
                steps.append(dict(
                    step=step,
                    action=(f"Procesar adyacente {w} "
                            f"({'actualiza y encola' if updated else 'sin cambio'})"),
                    current=v,
                    dist=dict(dist), prev=dict(prev),
                    visited=dict(visited), pq=list(pq)
                ))
                step += 1
    return steps

steps = dijkstra_trace_fine(G, SOURCE)

# -------- Renderizado --------
pos = nx.spring_layout(G, seed=7)

def render_frame(step):
    current = step["current"]
    visited = step["visited"]
    dist = step["dist"]
    prev = step["prev"]

    # Colores de nodos
    node_colors = []
    for n in G.nodes():
        if n == current:
            node_colors.append("#f4b400")  # actual (ámbar)
        elif visited[n]:
            node_colors.append("#34a853")  # visitado
        else:
            node_colors.append("#dddddd")  # no visitado

    # árbol de predecesores
    tree_edges = set()
    for v, p in prev.items():
        if p is not None:
            tree_edges.add((p, v))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc", width=1.5)
    if tree_edges:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=list(tree_edges),
                               edge_color="#222222", width=2.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=650, edgecolors="#333", linewidths=1.2)
    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"), font_size=9)
    ax.set_title(f"{step['action']} (paso {step['step']})")
    ax.axis("off")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    # Tabla distancias
    def fmt(x): return "∞" if np.isinf(x) else int(x)
    df = pd.DataFrame({
        "Nodo": list(G.nodes()),
        "Distancia": [fmt(dist[n]) for n in G.nodes()],
        "Previo": [prev[n] if prev[n] else "—" for n in G.nodes()],
        "Visitado": ["Sí" if visited[n] else "No" for n in G.nodes()]
    })
    styled = df.style.hide(axis="index").set_table_attributes('class="dij-table"')

    # Cola de prioridad
    pq_df = pd.DataFrame(step["pq"], columns=["Distancia", "Nodo"]).sort_values("Distancia")
    pq_html = pq_df.to_html(index=False, classes="pq-table")

    return {
        "img": f"data:image/png;base64,{img_b64}",
        "table": styled.to_html(),
        "pq": pq_html
    }

frames = [render_frame(s) for s in steps]

# -------- UI HTML+JS --------
uid = secrets.token_hex(3)
root_id = f"dij-{uid}"
html = f"""
<div id="{root_id}" class="dij-widget">
  <div class="controls">
    <button data-act="prev">◀</button>
    <input class="slider" type="range" min="0" max="{len(frames)-1}" step="1" value="0"/>
    <button data-act="next">▶</button>
    <span class="label"></span>
  </div>
  <div class="view">
    <div class="left"><img class="img" /></div>
    <div class="right">
      <h4>Tabla de distancias</h4>
      <div class="tbl"></div>
      <h4>Cola de prioridad</h4>
      <div class="pq"></div>
    </div>
  </div>
  <script type="application/json" class="data">{json.dumps(frames)}</script>
  <style>
    .dij-widget .view {{ display:grid; grid-template-columns: 1fr 1fr; gap:1rem; }}
    .dij-widget img {{ width:100%; border:1px solid #ddd; border-radius:.5rem; }}
    .pq-table, .dij-table {{ border-collapse: collapse; width:100%; margin-top:.5rem; }}
    .pq-table th, .pq-table td, .dij-table th, .dij-table td {{ border:1px solid #ddd; padding:.3rem; text-align:center; }}
  </style>
  <script>
  (function(root){{
    const data = JSON.parse(root.querySelector(".data").textContent);
    const img = root.querySelector(".img");
    const tbl = root.querySelector(".tbl");
    const pq = root.querySelector(".pq");
    const slider = root.querySelector(".slider");
    const label = root.querySelector(".label");
    const btnPrev = root.querySelector('[data-act="prev"]');
    const btnNext = root.querySelector('[data-act="next"]');

    function show(i){{
      const f = data[i];
      img.src = f.img;
      tbl.innerHTML = f.table;
      pq.innerHTML = f.pq;
      label.textContent = `Paso ${{i+1}} / {len(frames)}`;
      slider.value = i;
    }}
    btnPrev.onclick = () => show(Math.max(0, Number(slider.value)-1));
    btnNext.onclick = () => show(Math.min(data.length-1, Number(slider.value)+1));
    slider.oninput = e => show(Number(e.target.value));
    show(0);
  }})(document.getElementById("{root_id}"));
  </script>
</div>
"""

display(HTML(html))

```


