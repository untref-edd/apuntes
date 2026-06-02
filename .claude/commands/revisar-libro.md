---
description: Revisa el libro completo en busca de errores gramaticales y explicaciones ambiguas. Pasá el número de unidad ("1", "2", "3", "4") para revisar solo esa sección.
---

Revisá los apuntes universitarios de Estructuras de Datos (UNTREF) buscando errores de gramática en español rioplatense y explicaciones ambiguas o poco claras.

$ARGUMENTS

## Archivos por unidad

Todos los archivos están en `contenidos/`. Excluir todo lo que esté dentro de `_build/`.

- **Unidad 1** — Taller de Python: `1-taller-de-python/*.md`
- **Unidad 2** — Estructuras de Datos: `2-estructuras-de-datos/*.md`
- **Unidad 3** — Representación de Datos: `3-representacion-datos/*.md`
- **Unidad 4** — Recuperación de Información: `4-recuperacion-informacion/*.md`
- **Otros** — Introducción y Anexos: `introduccion.md`, `5-aplicaciones/*.md`, `Anexos/*.md`

## Workflow

Lanzá 4 agentes en paralelo, uno por unidad temática. Cada agente debe:

1. Leer todos los archivos de su unidad
2. Revisar **solo el texto narrativo** — ignorar: código Python, outputs de celdas, tablas de datos, nombres de variables e imports
3. Reportar hallazgos en el formato indicado abajo

### Criterios — Gramática

- Concordancia de género y número (artículo/sustantivo/adjetivo)
- Tildes correctas, incluidas las diacríticas (más/mas, sí/si, él/el, etc.)
- Ausencia de signos de apertura en preguntas (¿) o exclamaciones (¡)
- Gerundios usados como predicados principales cuando no corresponde
- Uso de mayúsculas después de dos puntos cuando no corresponde

### Criterios — Claridad

- Términos técnicos usados sin definición previa dentro del capítulo
- Ejemplos que no ilustran lo que dicen ilustrar
- Frases con más de una interpretación posible
- Referencias a conceptos aún no introducidos sin advertencia explícita

## Formato de cada hallazgo

```
**Archivo**: `ruta/archivo.md`
**Sección**: nombre aproximado
**Tipo**: Gramática | Claridad
**Problema**: descripción breve del error o ambigüedad
**Sugerencia**: corrección propuesta
```

## Output final

Cuando todos los agentes terminen, presentá los resultados agrupados por archivo en orden de capítulo. Al final, incluí un resumen con el total de hallazgos por tipo (Gramática / Claridad) y por unidad.
