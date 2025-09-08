"""
Algoritmos de caminos mínimos en grafos: Dijkstra y Bellman-Ford.
Incluye funciones para trazar paso a paso y visualización interactiva.
"""

import io
import base64
import json
import secrets
from heapq import heappush, heappop

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import HTML, display


def dijkstra_trace_fine(graph, source):
    """
    Ejecuta Dijkstra paso a paso y guarda cada estado para visualización.

    Args:
        graph (nx.Graph): Grafo dirigido y ponderado.
        source: Nodo origen.

    Returns:
        list[dict]: Lista de estados del algoritmo.
    """
    dist = {v: float("inf") for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    visited = {v: False for v in graph.nodes()}
    pq = []
    dist[source] = 0
    heappush(pq, (0, source))

    steps = []
    step = 1

    while pq:
        _, v = heappop(pq)
        if visited[v]:
            steps.append(
                dict(
                    step=step,
                    action=(f"{v} desencolado, ya fue visitado por lo tanto no se procesa"),
                    current=v,
                    dist=dict(dist),
                    prev=dict(prev),
                    visited=dict(visited),
                    pq=list(pq),
                )
            )
            step += 1
            continue

        visited[v] = True
        steps.append(
            dict(
                step=step,
                action=f"{v} desencolado, se marca como visitado",
                current=v,
                dist=dict(dist),
                prev=dict(prev),
                visited=dict(visited),
                pq=list(pq),
            )
        )
        step += 1

        for w, edata in graph[v].items():
            if not visited[w]:
                updated = False
                if dist[v] + edata["weight"] < dist[w]:
                    dist[w] = dist[v] + edata["weight"]
                    prev[w] = v
                    heappush(pq, (dist[w], w))
                    updated = True
                steps.append(
                    dict(
                        step=step,
                        action=(f"Procesar adyacente {w} " f"({'actualiza y encola' if updated else 'sin cambio'})"),
                        current=v,
                        dist=dict(dist),
                        prev=dict(prev),
                        visited=dict(visited),
                        pq=list(pq),
                    )
                )
            else:
                steps.append(
                    dict(
                        step=step,
                        action=(f"Procesar adyacente {w} (ya visitado, se ignora)"),
                        current=v,
                        dist=dict(dist),
                        prev=dict(prev),
                        visited=dict(visited),
                        pq=list(pq),
                    )
                )
            step += 1
    return steps


def render_frame_dijkstra(graph, step, pos=None):
    """
    Renderiza un paso del algoritmo de Dijkstra como imagen y tabla.

    Args:
        graph (nx.Graph): Grafo.
        step (dict): Estado del algoritmo.
        pos (dict, opcional): Posiciones de los nodos.

    Returns:
        dict: Imagen codificada, tabla HTML y cola de prioridad HTML.
    """
    current = step["current"]
    visited = step["visited"]
    dist = step["dist"]
    prev = step["prev"]

    if pos is None:
        pos = nx.spring_layout(graph, seed=7)

    node_colors = []
    for n in graph.nodes():
        if visited[n]:
            node_colors.append("#34a853")
        else:
            node_colors.append("#dddddd")

    tree_edges = set()
    for v, p in prev.items():
        if p is not None:
            tree_edges.add((p, v))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#cccccc", width=1.5)
    if tree_edges:
        nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=list(tree_edges), edge_color="#222222", width=2.5)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=650, edgecolors="#333", linewidths=1.2)
    nx.draw_networkx_labels(graph, pos, font_color="white", font_weight="bold")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"), font_size=9)
    ax.set_title(f"{step['action']} (paso {step['step']})")
    ax.axis("off")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    def fmt(x):
        return "∞" if np.isinf(x) else int(x)

    df = pd.DataFrame(
        {
            "Nodo": list(graph.nodes()),
            "Distancia": [fmt(dist[n]) for n in graph.nodes()],
            "Previo": [prev[n] if prev[n] else "—" for n in graph.nodes()],
            "Visitado": ["Sí" if visited[n] else "No" for n in graph.nodes()],
        }
    )
    styled = df.style.hide(axis="index").set_table_attributes('class="dij-table"')

    pq_df = pd.DataFrame(step["pq"], columns=["Distancia", "Nodo"]).sort_values("Distancia")
    pq_html = pq_df.to_html(index=False, classes="pq-table")

    return {
        "img": f"data:image/png;base64,{img_b64}",
        "table": styled.to_html(),
        "pq": pq_html,
    }


def show_dijkstra_step_by_step(graph, source):
    """
    Muestra la ejecución paso a paso del algoritmo de Dijkstra.

    Args:
        graph (nx.Graph): Grafo dirigido y ponderado.
        source: Nodo origen.
    """
    steps = dijkstra_trace_fine(graph, source)
    pos = nx.spring_layout(graph, seed=7)
    frames = [render_frame_dijkstra(graph, s, pos) for s in steps]

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


def bellman_ford_trace(graph, source):
    """
    Ejecuta Bellman-Ford paso a paso y guarda cada estado para visualización.

    Args:
        graph (nx.Graph): Grafo dirigido y ponderado.
        source: Nodo origen.

    Returns:
        list[dict]: Lista de estados del algoritmo.
    """
    dist = {v: float("inf") for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    dist[source] = 0

    steps = []
    step = 1

    num_nodes = len(graph.nodes())
    edges = [(u, v, edata["weight"]) for u, v, edata in graph.edges(data=True)]

    # |V|-1 iteraciones
    for i in range(num_nodes - 1):
        dist_old = dict(dist)
        for u, v, w in edges:
            action = f"Iteración {i+1}, relajar arista {u}->{v} (peso {w})"
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                action += " → se actualiza"
            else:
                action += " → sin cambio"

            steps.append(
                dict(
                    step=step,
                    action=action,
                    current=u,
                    dist=dict(dist),
                    prev=dict(prev),
                    prev_dist=dict(dist_old),
                    pq=[],
                )
            )
            step += 1

    # iteración extra: detectar ciclos negativos
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            steps.append(
                dict(
                    step=step,
                    action=f"Se detecta ciclo negativo usando arista {u}->{v}",
                    current=u,
                    dist=dict(dist),
                    prev=dict(prev),
                    prev_dist=dict(dist),
                    pq=[],
                )
            )
            step += 1
            break

    return steps


def render_frame_bellman_ford(graph, step, pos=None, source=None):
    """
    Renderiza un paso del algoritmo de Bellman-Ford como imagen y tabla.

    Args:
        graph (nx.Graph): Grafo.
        step (dict): Estado del algoritmo.
        pos (dict, opcional): Posiciones de los nodos.
        source: Nodo origen.

    Returns:
        dict: Imagen codificada, tabla HTML y detalle HTML.
    """
    current = step["current"]
    dist = step["dist"]
    prev = step["prev"]
    prev_dist = step.get("prev_dist", {n: float("inf") for n in graph.nodes()})

    if pos is None:
        pos = nx.spring_layout(graph, seed=7)

    # Colorear nodos:
    node_colors = []
    for n in graph.nodes():
        if n == source:
            node_colors.append("#34a853")  # origen siempre verde
        elif step["step"] == 1:
            node_colors.append("#dddddd")  # primer paso → todos grises excepto origen
        else:
            if dist[n] == prev_dist.get(n, float("inf")):
                node_colors.append("#34a853")  # verde si no cambió
            else:
                node_colors.append("#dddddd")  # gris si cambió

    # Aristas del árbol de predecesores
    tree_edges = set()
    for v, p in prev.items():
        if p is not None:
            tree_edges.add((p, v))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#cccccc", width=1.5)
    if tree_edges:
        nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=list(tree_edges), edge_color="#222222", width=2.5)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=650, edgecolors="#333", linewidths=1.2)
    nx.draw_networkx_labels(graph, pos, font_color="white", font_weight="bold")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"), font_size=9)
    ax.set_title(f"{step['action']} (paso {step['step']})")
    ax.axis("off")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    def fmt(x):
        return "∞" if np.isinf(x) else int(x)

    df = pd.DataFrame(
        {
            "Nodo": list(graph.nodes()),
            "Distancia": [fmt(dist[n]) for n in graph.nodes()],
            "Previo": [prev[n] if prev[n] else "—" for n in graph.nodes()],
        }
    )
    styled = df.style.hide(axis="index").set_table_attributes('class="bf-table"')

    return {
        "img": f"data:image/png;base64,{img_b64}",
        "table": styled.to_html(),
        "pq": f"<p>{step['action']}</p>",
    }


def show_bellman_ford_step_by_step(graph, source):
    """
    Muestra la ejecución paso a paso del algoritmo de Bellman-Ford.

    Args:
        graph (nx.Graph): Grafo dirigido y ponderado.
        source: Nodo origen.
    """
    steps = bellman_ford_trace(graph, source)
    pos = nx.spring_layout(graph, seed=7)
    frames = [render_frame_bellman_ford(graph, s, pos) for s in steps]

    uid = secrets.token_hex(3)
    root_id = f"bf-{uid}"
    html = f"""
  <div id="{root_id}" class="bf-widget">
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
    <h4>Detalle</h4>
    <div class="pq"></div>
    </div>
    </div>
    <script type="application/json" class="data">{json.dumps(frames)}</script>
    <style>
    .bf-widget .view {{ display:grid; grid-template-columns: 1fr 1fr; gap:1rem; }}
    .bf-widget img {{ width:100%; border:1px solid #ddd; border-radius:.5rem; }}
    .pq-table, .bf-table {{ border-collapse: collapse; width:100%; margin-top:.5rem; }}
    .pq-table th, .pq-table td, .bf-table th, .bf-table td {{ border:1px solid #ddd; padding:.3rem; text-align:center; }}
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
