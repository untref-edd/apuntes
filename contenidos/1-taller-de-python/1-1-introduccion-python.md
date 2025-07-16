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
# Introducción a Python

Python es un lenguaje de programación multipropósito, creado a fines de los años 80 por <a href="https://es.wikipedia.org/wiki/Guido_van_Rossum" target="_blank">Guido van Rossum</a>.

```{figure} ../assets/images/python-logo-generic.svg
:alt: Logo de Python
:width: 200px
:align: center

Logo oficial de Python
```

## Historia y filosofía

> *Guido Van Rossum es el principal autor de Python, y su continuo rol central en decidir la dirección de Python es reconocido, refiriéndose a él como Benevolente Dictador Vitalicio (en inglés: Benevolent Dictator for Life, BDFL); sin embargo el 12 de julio de 2018 declinó de dicha situación de honor sin dejar un sucesor o sucesora y con una declaración altisonante:*
>
> > ***"Entonces, ¿qué van a hacer todos ustedes? ¿Crear una democracia? ¿Anarquía? ¿Una dictadura? ¿Una federación?"***
> 
> Fuente: <a href="https://es.wikipedia.org/wiki/Python" target="_blank">Wikipedia</a>

### El Zen de Python

El Zen de Python es una colección de principios que guían el diseño y la filosofía del lenguaje:

```{code-cell}
import this
```

Estos principios enfatizan la importancia de escribir código claro, legible y elegante.

## Características principales

### Multiparadigma

Python es un lenguaje de programación **orientado a objetos, introspectivo y reflexivo, imperativo y funcional**. 

Permite usar diferentes estilos de programación según las necesidades del proyecto, incluso combinando varios estilos en un mismo proyecto.

La programación imperativa se basa en la ejecución secuencial de instrucciones. Para realizar una tarea se debe programar paso a paso especificando _**como**_ se debe hacer.

```{code-cell}
# Programación imperativa
def factorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

print(f"Factorial de 5: {factorial(5)}")
```

La programación funcional se basa en el uso de funciones puras y evita el estado mutable. Se enfoca en _**que**_ se debe hacer, utilizando funciones de orden superior y evitando efectos secundarios. En el capítulo de funciones profundizaremos un poco más en este paradigma.

```{code-cell}
# Quicksort en una línea (programación funcional)
qs = lambda lst: lst if len(lst) <= 1 else qs([x for x in lst[1:] if x < lst[0]]) + \
                                  [lst[0]] + qs([x for x in lst[1:] if x >= lst[0]])

lista = [3, 6, 8, 10, 1, 2, 1]
print(f"Lista ordenada: {qs(lista)}")
```

### Fuertemente tipado y dinámico

Python es un lenguaje **fuertemente tipado**, lo que significa que no se permite realizar operaciones entre tipos de datos incompatibles sin conversión explícita.

```{code-cell}
---
tags: [raises-exception]
---
# Ejemplo de tipado fuerte
resultado = "5" + 3  # Esto generará un error
```

```{code-cell}
# Conversión explícita necesaria
resultado_correcto = int("5") + 3
print(f"Resultado correcto: {resultado_correcto}")
```

```{code-cell}
# Tipado dinámico - las variables pueden cambiar de tipo
variable = 42        # int
print(f"Tipo: {type(variable)}, Valor: {variable}")

variable = "Python"  # str
print(f"Tipo: {type(variable)}, Valor: {variable}")

variable = [1, 2, 3] # list
print(f"Tipo: {type(variable)}, Valor: {variable}")
```

En este fragmento el mismo identificador `variable` se liga a diferentes tipos de datos a lo largo del tiempo, demostrando el tipado dinámico de Python. No hace falta declarar el tipo de la variable al momento de su creación, Python lo infiere automáticamente.

### Sintaxis clara y legible

Python se caracteriza por su sintaxis clara y legible:

```{code-cell}
---
mystnb:
  number_source_lines: true
---

def es_numero_primo(n):
    """
    Determina si un número es primo.
    
    Args:
        n (int): El número a evaluar
        
    Returns:
        bool: True si es primo, False en caso contrario
    """
    if n < 2:
        return False
    
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    
    return True

# Filtra una lista de números quedándose solo con los primos
numeros = [2, 3, 4, 5, 17, 25, 29]
primos = [num for num in numeros if es_numero_primo(num)]
print(f"Números primos: {primos}")
```

Los bloques de código se delimitan por indentación, lo que mejora la legibilidad y evita errores comunes de sintaxis.

En la línea 1 se define una función `es_numero_primo` que recibe un número entero `n` y devuelve `True` si es primo, o `False` en caso contrario. La definición de una función se realiza con la palabra clave `def`, seguida del nombre de la función, los parámetros entre paréntesis y dos puntos (`:`). Los dos puntos indican el inicio de un bloque de código que debe estar indentado, en este caso el cuerpo de la función.

El cuerpo de la función se extiende hasta la línea 18 a partir de la cual el código vuelve a estar alineado a la izquierda, indicando que ya no forma parte del bloque de la función.

Entre las líneas 2 y 10 encontramos la documentación de la función, que explica su propósito, los argumentos que recibe y el valor que devuelve. Esta documentación se escribe entre comillas triples (`"""`) y es accesible a través de la función `help(es_numero_primo)`. `help` es una función de Python que muestra la documentación de un objeto.

```{code-cell}
help(es_numero_primo)
```

Esta forma de documentar el código junto con el código mismo es una buena práctica que facilita la comprensión y el mantenimiento del código.

La forma de identar los bloques de código es fundamental en Python. A diferencia de otros lenguajes que utilizan llaves `{}` o palabras clave como `begin` y `end`, Python utiliza la indentación para definir el alcance de los bloques de código. Esto significa que todos los bloques deben estar correctamente indentados para evitar errores de sintaxis. Por ejemplo la identación puede ser de 4 espacios, que es la convención más común en Python.

## Aplicaciones de Python

Python se utiliza en una amplia gama de aplicaciones, gracias a su versatilidad y a la gran cantidad de bibliotecas y frameworks disponibles. Algunas de las áreas más comunes son:

```{list-table}
:header-rows: 1

* - Área
  - Frameworks/Bibliotecas
  - Ejemplos de uso
* - Desarrollo web
  - Django, Flask, FastAPI
  - Sitios web, APIs REST, aplicaciones web
* - Ciencia de datos
  - Pandas, NumPy, Matplotlib
  - Análisis de datos, visualización
* - Machine Learning
  - TensorFlow, PyTorch, Scikit-learn
  - Modelos predictivos, IA
* - Automatización
  - Selenium, Requests, Beautiful Soup
  - Web scraping, automatización de tareas
* - Desarrollo de juegos
  - Pygame, Panda3D
  - Juegos 2D y 3D
```

## Instalación y configuración

### Verificación de la instalación

Primero, verifica si Python ya está instalado:

```{code-cell}
import sys
print(f"Versión de Python: {sys.version}")
print(f"Plataforma: {sys.platform}")
```

### Instalación por sistema operativo

`````{tab-set}
````{tab-item} Windows
1. Descarga el instalador desde <a href="https://www.python.org/downloads/" target="_blank">python.org</a>
2. Ejecuta el instalador
3. **Importante**: Marca "Add Python to PATH"
4. Verifica la instalación:
   ```
   python --version
   pip --version
   ```
````
````{tab-item} Linux (Ubuntu/Debian)
```bash
# Actualizar repositorios
sudo apt update

# Instalar Python 3 y pip
sudo apt install python3 python3-pip

# Verificar instalación
python3 --version
pip3 --version
```
````
````{tab-item} macOS
```bash
# Usando Homebrew (recomendado)
brew install python

# O usando el instalador oficial desde python.org

# Verificar instalación
python3 --version
pip3 --version
```
````
`````


## Recursos adicionales

Para profundizar en el aprendizaje de Python, se recomienda consultar la documentación oficial, especialmente {cite}`python_tutorial_es`, que proporciona una introducción completa y detallada al lenguaje.

```{important}
**Documentación esencial:**
- <a href="https://docs.python.org/3/" target="_blank">Documentación oficial de Python</a>
- <a href="https://docs.python.org/es/3.13/tutorial/index.html" target="_blank">Tutorial oficial en español</a>
- <a href="https://peps.python.org/pep-0008/" target="_blank">PEP 8 - Guía de estilo</a>
```

```{seealso}
**Recursos para aprender:**
- <a href="https://realpython.com/" target="_blank">Real Python</a> - Tutoriales avanzados
- <a href="https://wiki.python.org/moin/BeginnersGuide" target="_blank">Python.org Beginner's Guide</a>
- <a href="https://automatetheboringstuff.com/" target="_blank">Automate the Boring Stuff</a> - Libro gratuito
```
````

