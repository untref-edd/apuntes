# EDD Code - Estructuras de Datos

Este paquete contiene implementaciones de estructuras de datos y algoritmos utilizados en el curso de Estructuras de Datos de la Universidad Nacional de Tres de Febrero (UNTreF).

## Paquetes incluidos

### `grafos`
Implementaciones de algoritmos de grafos:
- Caminos mínimos (Dijkstra, Bellman-Ford)
- Recorridos (BFS, DFS)
- Ordenamiento topológico

### `ii` (Inverted Index)
Implementaciones de índices invertidos:
- BSBI (Blocked Sort-Based Indexing)
- Construcción y fusión de índices
- Compresión de índices

## Instalación

Este paquete se instala automáticamente como parte del proyecto de apuntes:

```bash
pip install -e .
```

## Uso

```python
# Importar paquete de grafos
from grafos import caminos_minimos

# Importar paquete de índices invertidos
from ii import BSBI

# Crear índice invertido
bsbi = BSBI(tamaño_bloque=1000)
```

## Desarrollo

Para contribuir al desarrollo de estos paquetes, asegúrate de instalar en modo editable:

```bash
pip install -e contenidos/_static/code
```
