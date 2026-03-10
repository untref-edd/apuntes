# Directivas para Agentes de IA

Este documento contiene las directivas que deben seguir todos los agentes de inteligencia artificial que colaboren en este proyecto.

## Lineamientos Generales

1. **Idioma**: El idioma principal del proyecto es **español rioplatense**.
2. **Tono y Formalidad**: El tono del contenido debe ser moderadamente formal. Debe ser amigable pero serio, adecuado para material de estudio universitario para la materia de Estructuras de Datos.
3. **Sintaxis**: Todo el contenido debe ser escrito utilizando la sintaxis de [MyST (Mark-up Your Structured Text)](https://mystmd.org/).
4. **Estructura y Nomenclatura**: El contenido se organiza en la carpeta `contenidos/`. Los nuevos archivos deben seguir la convención de nomenclatura existente (ej: `X-Y-tema.md`) y ubicarse en la subcarpeta temática apropiada.
5. **Dependencias de Código**: Todo código Python debe usar únicamente las librerías listadas en `requirements.txt`. Si se necesita una nueva, se debe proponer la modificación de dicho archivo.
6. **Archivos Estáticos**: Las imágenes y otros recursos estáticos deben ser agregados a la carpeta `contenidos/_static/figures`.
7. **Citas Bibliográficas**: Toda referencia bibliográfica debe ser añadida al archivo `contenidos/references.bib` y citada apropiadamente desde el texto utilizando la sintaxis de MyST.

---

## Comandos de Build, Lint y Test

### Instalación de dependencias

```bash
make install
# Equivalente a: pip install --requirement requirements.txt
```

### Formateo de código

```bash
make fmt
# Formatea Markdown con mdformat y Python con black (line-length 120)
```

Comandos individuales:
- `mdformat --number contenidos/**/*.md` - Formatea archivos Markdown
- `black --line-length 120 .` - Formatea código Python

### Build del libro

```bash
make build    # Compila el libro ejecutando las celdas
make pdf     # Genera el PDF
make start   # Inicia el servidor de desarrollo
make clean   # Elimina archivos generados
```

### Tests

**No existe un framework de tests configurado actualmente.** Si necesitas agregar tests:
- Usa `pytest` como framework de testing
- Crea archivos de test en `contenidos/_static/code/tests/`
- Ejecuta tests con: `pytest contenidos/_static/code/tests/`
- Para un solo test: `pytest contenidos/_static/code/tests/test_file.py::test_function_name`

---

## Convenciones de Código Python

### Estilo General

- **Line length**: 120 caracteres (configuración de Black)
- **Docstrings**: Usar formato Google-style con descripción detallada en español
- **Comentarios**: Evitar comentarios obvios; priorizar código autodocumentado
- **Encoding**: UTF-8 (default en Python 3)

### Imports

Orden recomendado (separar con líneas en blanco):

```python
# 标准库 (stdlib)
import io
import json
import secrets
from heapq import heappush, heappop

# 第三方库 (third-party)
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import HTML, display

# 本地模块 (local modules)
from stack_exception import StackException
```

### Tipos

- **Type hints**: Opcionales pero recomendados para funciones públicas
- Usar `typing` cuando sea necesario: `list[dict]`, `dict[str, Any]`, etc.

### Convenciones de Nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Clases | PascalCase | `Stack`, `Graph` |
| Funciones | snake_case | `dijkstra_trace_fine` |
| Variables | snake_case | `node_colors` |
| Métodos privados | snake_case con `_` | `_items` |
| Constantes | MAYÚSCULAS_SNAKE | `MAX_ITERATIONS` |
| Excepciones personalizadas | PascalCase terminar en Exception | `StackException` |

### Manejo de Errores

- Usar excepciones personalizadas heredando de `Exception`
- Mensajes de error en español, claros y concisos
- Capturar excepciones específicas (`ValueError`, `StackException`) en lugar de `Exception`

```python
# Correcto
if self.is_empty():
    raise StackException("pop from empty stack")

# Incorrecto
if self.is_empty():
    raise Exception("Error")
```

### Métodos Mágicos (`__str__`, `__repr__`)

Incluir siempre `__repr__` para debugging y `__str__` cuando sea necesaria una representación legible.

```python
def __str__(self):
    return f"Stack: {self._items} (cima: {self._items[-1]})"

def __repr__(self):
    return f"Stack({self._items})"
```

### Estructura de Archivos de Código

1. Docstring del módulo (módulo level)
2. Imports
3. Constantes globales
4. Funciones auxiliares
5. Clases
6. Demo/main (opcional, envuelto en `if __name__ == "__main__":`)

---

## MyST y Contenido

### Frontmatter de capítulos

```yaml
---
file: ruta/al/archivo.md
---
```

### Citas Bibliográficas

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

### Ejecución de Celdas

Usar el tag `exercise` o `solution` de MyST para notebooks:

````markdown
```{exercise}
:label: ejercicio-1

Tu enunciado aquí.
```

```{solution}
:label: solucion-1

def respuesta():
    pass
```
````

---

## Notas Adicionales

- El proyecto usa `myst-parser` y `mystmd` para construir la documentación
- Los archivos Python en `_static/code/` pueden ser ejecutados como scripts o importados
- Los paquetes locales (`grafos`, `ii`) están definidos en `pyproject.toml`
- Python >= 3.11 requerido (ver `pyproject.toml`)
