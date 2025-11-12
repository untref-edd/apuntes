# Apuntes de Estructuras de Datos

## Instalación y configuración del entorno

Si deseas desarrollar y/o compilar el apunte de Estructuras de Datos, debes:

> [!TIP]
> Para esta guía se asume que tienes Python instalado.
>
> Se recomienda crear un entorno virtual de Python para trabajar con este proyecto.

> [!NOTE]
> Este proyecto utiliza **Jupyter Book 2**, que es una reescritura completa basada en el motor MyST Document Engine.

1. Clonar este repositorio

2. Instalar las dependencias del proyecto.

   ```sh
   pip install -r requirements.txt
   ```

3. (Opcional) Edita los archivos fuente del libro ubicados en el directorio `contenidos`

4. Para compilar el libro ejecutar:

   ```sh
   cd contenidos
   jupyter-book build
   ```

   Una versión HTML completamente renderizada del libro se construirá en `contenidos/_build/site/public`.

5. (Opcional) Se puede servir este HTML utilizando el siguiente comando de Python:

   ```sh
   python -m http.server --directory contenidos/_build/site/public
   ```

### Ejecutando comando con `make`

`make` es una herramienta de automatización de tareas muy útil. En este proyecto se utiliza para instalar las dependencias, compilar el libro y servirlo en un servidor web local.

En el apartado anterior hemos explicado como se instalan las dependencies de este proyecto y como "construir" el libro. A continuación se detallan los comandos que se pueden ejecutar con `make`.

Primero debemos asegurarnos de que tenemos `make` disponible en nuestro sistema. En sistemas Unix (como Linux o MacOS) es probable que ya lo tengamos instalado. En Windows, se puede instalar con [`winget`](https://docs.microsoft.com/en-us/windows/package-manager/winget/).

```sh
winget install -e --id GnuWin32.Make
```

Una vez que tenemos `make` disponible, podemos ejecutar los siguientes comandos:

- `make install`: Instala las dependencias del proyecto.
- `make build`: Compila el libro.
- `make clean`: Elimina los archivos generados por la compilación.
- `make server`: Sirve el libro en un servidor web local.

Esto simplifica el proceso de desarrollo y permite que cualquier persona pueda compilar y servir el libro sin tener que recordar los comandos de Python o Jupyter Book.

## Notas sobre Jupyter Book 2

Esta versión del libro utiliza **Jupyter Book 2**, que es una reescritura completa basada en el motor MyST Document Engine. Los principales cambios incluyen:

- **Configuración unificada**: Toda la configuración ahora está en `contenidos/myst.yml` (en lugar de `_config.yml` y `_toc.yml`)
- **Nuevo directorio de salida**: Los archivos compilados se generan en `contenidos/_build/site/` (en lugar de `contenidos/_build/html/`)
- **Arquitectura moderna**: JB2 genera contenido JSON que se renderiza con una aplicación web moderna

### Migración desde Jupyter Book 1

Si tienes una versión anterior de este proyecto (JB1), los archivos de backup de la configuración antigua están guardados como `._config.yml.bak` y `._toc.yml.bak`.
