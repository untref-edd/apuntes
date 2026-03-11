# Directivas para Agentes de IA

Este documento contiene las directivas que deben seguir todos los agentes de inteligencia artificial que colaboren en este proyecto.

## 1. Información General del Proyecto

- **Tipo**: Apuntes universitarios para la materia "Estructuras de Datos" (UNTREF)
- **Idioma**: El idioma principal del proyecto es **español rioplatense**
- **Tono y Formalidad**: El tono del contenido debe ser moderadamente formal. Debe ser amigable pero serio, adecuado para material de estudio universitario.
- **Sintaxis**: Todo el contenido debe ser escrito utilizando la sintaxis de [MyST (Mark-up Your Structured Text)](https://mystmd.org/).
- **Estructura y Nomenclatura**: El contenido se organiza en la carpeta `contenidos/`. Los nuevos archivos deben seguir la convención de nomenclatura existente (ej: `X-Y-tema.md`) y ubicarse en la subcarpeta temática apropiada.
- **Dependencias de Código**: Todo código Python debe usar únicamente las librerías listadas en `requirements.txt`. Si se necesita una nueva, se debe proponer la modificación de dicho archivo.
- **Archivos Estáticos**: Las imágenes y otros recursos estáticos deben ser agregados a la carpeta `contenidos/_static/figures`.
- **Citas Bibliográficas**: Toda referencia bibliográfica debe ser añadida al archivo `contenidos/references.bib` y citada apropiadamente desde el texto utilizando la sintaxis de MyST.
- **Build system**: MyST (mystmd) - ver https://mystmd.org/
- **Licencia**: CC-BY-SA-4.0

______________________________________________________________________

## 2. Comandos de Build, Lint y Test

### Instalación de dependencias

```bash
make install
# Equivalente a: pip install --requirement requirements.txt
# o manualmente:
pip install -r requirements.txt
```

### Formateo de código

```bash
make fmt
# Formatea Markdown con mdformat y Python con black (line-length 120)
```

Comandos individuales:

- `mdformat --number contenidos/**/*.md` - Formatea archivos Markdown
- `mdformat --number .opencode/**/*.md` - Formatea comandos de OpenCode
- `black --line-length 120 .` - Formatea código Python

### Compilación del libro

```bash
make build      # Compila ejecutando las celdas
make pdf        # Genera PDF
make clean      # Limpia artifacts
make start      # Inicia servidor de desarrollo
```

Comandos individuales:

```bash
# MyST
cd contenidos && myst build --execute
cd contenidos && myst start --execute
cd contenidos && myst clean --all --yes

# Python
python -m black --line-length 120 .
python -m mdformat --number contenidos/**/*.md
```

### Tests

**No existe un framework de tests configurado actualmente.** Si necesitas agregar tests:

- Usa `pytest` como framework de testing
- Crea archivos de test en `contenidos/_static/code/tests/`
- Ejecuta tests con: `pytest contenidos/_static/code/tests/`
- Para un solo test: `pytest contenidos/_static/code/tests/test_file.py::test_function_name`

______________________________________________________________________

## 3. Estructura del Proyecto

```output
contenidos/                    # Contenido principal (MyST markdown)
├── _static/code/             # Código Python (paquetes instalables)
│   ├── grafos/               # Algoritmos de grafos
│   ├── ii/                   # Índices invertidos
│   └── ...
├── _static/figures/          # Imágenes y recursos estáticos
├── templates/                # Plantillas de exportación
├── references.bib           # Referencias bibliográficas
└── myst.yml                  # Configuración del proyecto
scripts/build_pdf.py          # Script de generación PDF
requirements.txt              # Dependencias Python
Makefile                      # Comandos de build
```

______________________________________________________________________

## 4. Convenciones de Código Python

### Estilo General

- **Line length**: 120 caracteres (configuración de Black)
- **Docstrings**: Usar formato Google-style con descripción detallada en español
- **Comentarios**: Evitar comentarios obvios; priorizar código autodocumentado
- **Encoding**: UTF-8 (default en Python 3)

### Imports

Orden recomendado (separar con líneas en blanco):

```python
# Estándar (stdlib)
import io
import json
import secrets
from heapq import heappush, heappop

# Terceros (third-party)
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import HTML, display

# Local modules
from stack_exception import StackException
```

### Tipos

- **Type hints**: Opcionales pero recomendados para funciones públicas
- Usar `typing` cuando sea necesario: `list[dict]`, `dict[str, Any]`, etc.

### Convenciones de Nombres

| Elemento                   | Convención                       | Ejemplo               |
| -------------------------- | -------------------------------- | --------------------- |
| Clases                     | PascalCase                       | `Stack`, `Graph`      |
| Funciones                  | snake_case                       | `dijkstra_trace_fine` |
| Variables                  | snake_case                       | `node_colors`         |
| Métodos privados           | snake_case con `_`               | `_items`              |
| Constantes                 | MAYÚSCULAS_SNAKE                 | `MAX_ITERATIONS`      |
| Excepciones personalizadas | PascalCase terminar en Exception | `StackException`      |

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

______________________________________________________________________

## 5. MyST y Contenido

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

______________________________________________________________________

## 6. Guías de Estilo de Contenido

### Markdown (MyST)

- **Numeración de líneas**: Habilitada (`mdformat --number`)
- **Frontmatter**: Incluir en cada archivo nuevo
- **Citas**: Usar sintaxis MyST `{cite}` y agregar a `references.bib`
- **Código**: Usar fenced blocks con lenguaje especificado

### Imágenes y Recursos

- Ubicación: `contenidos/_static/figures/`
- Nomenclatura: descriptiva, minúsculas, guiones si es necesario
- Incluir alt text cuando sea apropiado

### Convenciones de Contenido

- **Nomenclatura de archivos**: `X-Y-tema.md` (ej: `2-1-grafos-introduccion.md`)
- **Carpetas temáticas**:
  - `1-taller-de-python/`
  - `2-estructuras-de-datos/`
  - `3-representacion-datos/`
  - `4-recuperacion-informacion/`
  - `5-aplicaciones/`
  - `Anexos/`
- **Tono**: Moderadamente formal, amigable pero serio
- **Bibliografía**: Agregar a `references.bib` y citar con `{cite}`

______________________________________________________________________

## 7. Dependencias

Solo usar librerías listadas en `requirements.txt`. Para agregar nuevas:

1. Proponer modificación de `requirements.txt`
2. Verificar compatibilidad con Python 3.11+
3. Asegurar que sea de propósito general, no dependencia específica de un ejemplo

______________________________________________________________________

## 8. Errores Comunes a Evitar

- No hacer commit de archivos generados (`exports/*.pdf`, `_build/`, etc.)
- No modificar archivos en `contenidos/templates/` a menos que sea necesario
- No agregar imágenes fuera de `_static/figures/`
- No usar librerías no listadas en requirements.txt

______________________________________________________________________

## 9. Notas Adicionales

- El proyecto usa `myst-parser` y `mystmd` para construir la documentación
- Los archivos Python en `_static/code/` pueden ser ejecutados como scripts o importados
- Los paquetes locales (`grafos`, `ii`) están definidos en `pyproject.toml`
- Python >= 3.11 requerido (ver `pyproject.toml`)
