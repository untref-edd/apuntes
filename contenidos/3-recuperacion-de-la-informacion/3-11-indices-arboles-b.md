---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: pythoF
---

# Árboles B - Índices Ordenados

Con los índices invertidos hemos visto cómo organizar la información para acelerar las búsquedas por términos. Sin embargo, en muchos casos es necesario realizar búsquedas con comodines o rangos, como por ejemplo:

- Buscar todos los documentos que contengan términos que empiecen con "comput*".
- Buscar documentos con fechas entre "2020-01-01" y "2020-12-31".
- Buscar productos con precios entre 100 y 500.
- Buscar nombres de usuarios que contengan la cadena "admin".

Para estos casos, los índices invertidos no son la mejor opción, ya que están optimizados para búsquedas exactas de términos. En su lugar, se utilizan **índices ordenados** basados en estructuras de datos como los **árboles B**.

## ¿Qué es un Árbol B?

Un árbol B es una estructura de datos autoequilibrada que mantiene los datos ordenados y permite búsquedas, inserciones y eliminaciones en tiempo logarítmico. Los árboles B son especialmente útiles para sistemas de bases de datos y sistemas de archivos debido a su capacidad para manejar grandes cantidades de datos y minimizar las operaciones de lectura/escritura en disco.

Un árbol-B de orden $M$ (el máximo número de hijos que puede tener cada nodo) es un árbol que satisface las siguientes propiedades:

- Cada nodo tiene como máximo $M$ hijos.
- Cada nodo (excepto la raíz) tiene como mínimo $⌈M/2⌉$ claves.
- Si la raíz no es una hoja, entonces debe tener al menos 2 hijos.
- Todos los nodos hoja aparecen al mismo nivel.
- Un nodo no hoja con k hijos contiene k-1 elementos o claves almacenados.
- Los hijos de un nodo con claves (k1, ···, km) tienen que cumplir ciertas condiciones:
  - El primer hijo tiene valores menores que k1.
  - El segundo tiene valores mayores o igual a k1 y menores que k2, etc.
  - El último hijo tiene valores mayores que km.
  
Para construir índices usaremos árboles B+, una variante de los árboles B en la que:

- Todos los valores se almacenan en las hojas.
- Los nodos internos solo almacenan claves para guiar la búsqueda.
- Las hojas están enlazadas entre sí para facilitar recorridos secuenciales.

## Ejemplo de Árbol B+
Consideremos un árbol B+ de orden 3 (cada nodo puede tener hasta 3 hijos) que almacena las siguientes palabras:"PACO", "POCO", "PECA", "PICO", "PALA", "POLO", "PIEL" y "PIPA". El árbol se vería así:

```{figure} ../assets/images/bplus1.png
---
name: bplus1
---
Árbol B+ de orden 3.

```

## Ejercicio Interactivo

En la siguiente simulación presionar en que nodo insertar el nuevo valor y observar cómo se reestructura el árbol B cuando es necesario. Al finalizar con el botón grade se puede observar los puntos obtenidos.

<iframe src="https://opendsa-server.cs.vt.edu/embed/bPlusTreeInsertPRO" height="600" width="100%" scrolling="no"></iframe>