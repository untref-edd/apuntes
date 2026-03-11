# Directivas para Agentes de IA

Este documento contiene las directivas para agentes que colaboren en este proyecto.

## Lineamientos Generales

1. **Idioma**: Español rioplatense
2. **Tono**: Moderadamente formal, amigable pero serio
3. **Sintaxis**: MyST (Mark-up Your Structured Text)
4. **Estructura**: Contenido en `contenidos/`, archivos con formato `X-Y-tema.md`
5. **Dependencias**: Solo librerías de `requirements.txt`
6. **Estáticos**: Imágenes en `contenidos/_static/figures`
7. **Citas**: Agregar a `contenidos/references.bib` y usar sintaxis MyST

---

## Comandos de Build, Lint y Test

### Instalación y formateo

```bash
make install          # pip install --requirement requirements.txt
make fmt              # formatea MD y Python (mdformat + black)
```

Comandos individuales:
- `mdformat --number contenidos/**/*.md` - Markdown
- `black --line-length 120 .` - Python

### Build y desarrollo

```bash
make build    # compila ejecutando celdas
make pdf      # genera PDF
make start    # servidor de desarrollo
make clean    # elimina archivos generados
```

### Tests (pytest no configurado aún)

Si agregas tests:
```bash
pytest contenidos/_static/code/tests/                    # todos los tests
pytest contenidos/_static/code/tests/test_file.py::test_name  # un test
```

---

## Convenciones de Código Python

### Estilo General

- **Line length**: 120 caracteres
- **Docstrings**: Google-style en español
- **Encoding**: UTF-8

### Imports (ordenar con líneas en blanco)

```python
# stdlib
import json
from heapq import heappush, heappop

# third-party
import networkx as nx
import matplotlib.pyplot as plt

# local modules
from stack_exception import StackException
```

### Tipos

- Type hints opcionales pero recomendados
- Usar `typing`: `list[dict]`, `dict[str, Any]`

### Convenciones de Nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Clases | PascalCase | `Stack`, `Graph` |
| Funciones | snake_case | `dijkstra_trace_fine` |
| Variables | snake_case | `node_colors` |
| Métodos privados | `_snake_case` | `_items` |
| Constantes | MAYÚSCULAS_SNAKE | `MAX_ITERATIONS` |
| Excepciones | PascalCase + Exception | `StackException` |

### Manejo de Errores

- Excepciones personalizadas heredando de `Exception`
- Mensajes en español, claros y concisos
- Capturar excepciones específicas (`ValueError`, `StackException`)

```python
# Correcto
if self.is_empty():
    raise StackException("pop from empty stack")
```

### Métodos Mágicos

Incluir siempre `__repr__` para debugging y `__str__` cuando sea necesaria una representación legible.

```python
def __repr__(self):
    return f"Stack({self._items})"
```

### Estructura de Archivos

1. Docstring del módulo
2. Imports
3. Constantes globales
4. Funciones auxiliares
5. Clases
6. Demo/main (opcional, en `if __name__ == "__main__":`)

---

## MyST y Contenido

### Frontmatter

```yaml
---
file: ruta/al/archivo.md
---
```

### Citas

```markdown
{cite}`python_tutorial_es`
```

### Bloques de Código

````markdown
```{code-block} python
:linenos:

def ejemplo():
    pass
```
````

### Ejercicios y Soluciones

````markdown
```{exercise}
:label: ejercicio-1

Enunciado aquí.
```

```{solution}
:label: solucion-1

def respuesta():
    pass
```
````

---

## Notas Adicionales

- Usa `myst-parser` y `mystmd` para construir la documentación
- Paquetes locales (`grafos`, `ii`) en `pyproject.toml`
- Python >= 3.11 requerido