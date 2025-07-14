---
file_format: mystnb
kernelspec:
  name: python3
---
# Introducción a Python

Python es un lenguaje de programación multipropósito, creado a fines de los 80 por <a href="https://es.wikipedia.org/wiki/Guido_van_Rossum" target="_blank">Guido van Rossum</a>.


> *Guido Van Rossum es el principal autor de Python, y su continuo rol central en decidir la dirección de Python es reconocido, refiriéndose a él como Benevolente Dictador Vitalicio (en inglés: Benevolent Dictator for Life, BDFL); sin embargo el 12 de julio de 2018 declinó de dicha situación de honor sin dejar un sucesor o sucesora y con una declaración altisonante:*
>
> > __*"Entonces, ¿qué van a hacer todos ustedes? ¿Crear una democracia? ¿Anarquía? ¿Una dictadura? ¿Una federación?"*__
> > 
> Fuente: <a href="https://es.wikipedia.org/wiki/Python" target="_blank">Wikipedia</a>

## Multiparadigma

Python es un lenguaje de programación **orientado a objetos, introspectivo y reflexivo, imperativo y funcional**. 

Permite usar diferentes estilos de programación según las necesidades del proyecto, incluso combinando varios estilos en un mismo proyecto.

Esta característica de Python lo hace muy versátil y adecuado para una amplia variedad de aplicaciones, desde desarrollo web hasta análisis de datos y aprendizaje automático.

Python actualmente se utiliza en una amplia gama de aplicaciones, incluyendo:

- Desarrollo web (con frameworks como Django y Flask)
- Análisis de datos y ciencia de datos (con bibliotecas como Pandas y NumPy)
- Aprendizaje automático e inteligencia artificial (con bibliotecas como TensorFlow y PyTorch)
- Automatización de tareas y scripts
- Desarrollo de aplicaciones de escritorio y móviles 

## Fuertemente tipado y dinámico

Python es un lenguaje **fuertemente tipado**, lo que significa que no se permite realizar operaciones entre tipos de datos incompatibles. Por ejemplo, no se puede sumar un número y una cadena de texto sin convertir explícitamente uno de los tipos.

Además, Python es un lenguaje **dinámico**, lo que significa que no es necesario declarar el tipo de una variable al momento de su creación. El tipo se determina en tiempo de ejecución, lo que permite una mayor flexibilidad en la programación.

No hay que confundir el tipado dinámico con el tipado débil, ya que se determine el tipo de una variable en tiempo de ejecución no implica que se puedan realizar operaciones entre tipos de datos incompatibles. En Python, si intentamos realizar una operación entre tipos incompatibles, obtendrás un error en tiempo de ejecución.

## Sintaxis clara y legible

Python se caracteriza por su sintaxis clara y legible, lo que facilita la escritura y comprensión del código. Algunas características de la sintaxis de Python son:

- Uso de indentación para definir bloques de código, en lugar de llaves o palabras clave.
- Uso de palabras clave en inglés para estructuras de control, como `if`, `for`, `while`, `def`, etc.
- Uso de comentarios con el símbolo `#` para agregar
- documentación y explicaciones en el código.
- Uso de convenciones de nomenclatura para variables y funciones, como `snake_case` para nombres de variables y `CamelCase` para nombres de clases.
- Uso de comillas simples o dobles para definir cadenas de texto, lo que permite mayor flexibilidad en la escritura de cadenas.
- Uso de espacios en blanco para mejorar la legibilidad del código, como separar operadores y operandos con espacios.
- Uso de funciones integradas y bibliotecas estándar para realizar tareas comunes, lo que reduce la necesidad de escribir código desde cero.
- Uso de excepciones para manejar errores y situaciones inesperadas, lo que permite un manejo más robusto de errores en el código.

## Interactivo y fácil de aprender

Python es un lenguaje interactivo, lo que significa que se puede ejecutar código línea por línea en un intérprete o consola. Esto facilita la experimentación y el aprendizaje, ya que se pueden probar fragmentos de código de forma rápida y sencilla.

```{code-cell} python
print("¡Hola, Mundo!")
```

## Zen de Python

El Zen de Python es una colección de principios que guían el diseño y la filosofía del lenguaje. Se puede acceder a él ejecutando el siguiente comando en un intérprete de Python:

```{code-cell} python
import this
``` 

## Instalación y primeros pasos

Para comenzar a trabajar con Python, es necesario instalarlo en tu sistema. Puedes descargar la última versión de Python desde su <a href="https://www.python.org/downloads/" target="_blank">sitio web oficial</a>.

Una vez instalado, puedes ejecutar Python desde la línea de comandos o utilizar un entorno de desarrollo integrado (IDE) como PyCharm, Visual Studio Code o Jupyter Notebook.

### Instalación en Windows

Para instalar Python en Windows, sigue estos pasos:

1. Descarga el instalador de Python desde el <a href="https://www.python.org/downloads/" target="_blank">sitio web oficial</a>.
2. Ejecuta el instalador y sigue las instrucciones en pantalla.
3. Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.
4. Una vez completada la instalación, abre una ventana de terminal (cmd) y escribe `python --version` para verificar que Python se haya instalado correctamente.

### Instalación en Linux
Para instalar Python en Linux, puedes utilizar el gestor de paquetes de tu distribución. Por ejemplo, en Ubuntu o Debian, puedes ejecutar los siguientes comandos:

```sh
sudo apt update
sudo apt install python3
```

### Instalación en macOS
Para instalar Python en macOS, puedes utilizar Homebrew, un gestor de paquetes para macOS. Si no tienes Homebrew instalado, puedes instalarlo siguiendo las instrucciones en su <a href="https://brew.sh/" target="_blank">sitio web oficial</a>.

```sh
brew install python
```

### Verificación de la instalación
Una vez que hayas instalado Python, puedes verificar la instalación abriendo una terminal y ejecutando el siguiente comando:
```sh
python --version
```
Esto debería mostrar la versión de Python instalada en tu sistema. 

## Recursos adicionales

- <a href="https://docs.python.org/3/" target="_blank">Documentación Oficial de Python</a>.
- <a href="https://docs.python.org/es/3.13/tutorial/index.html" target="_blank">Tutorial Oficial de Python</a>.