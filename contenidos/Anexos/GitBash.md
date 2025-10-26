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

# Activación automática de entorno virtual en Git Bash

Para esta guía se asume que el sistema Windows cuenta con Python y Git Bash instalados.

## Crear un entorno virtual

Parados sobre la carpeta donde queremos crear el entorno virtual, podemos hacer:

```console
python -m venv 3 .venv
```

Donde `3` es la versión de Python a utilizar (podemos ser más específicos en la numeración como `3.13`, o `3.13.1`). `.venv` es el nombre del entorno virtual que vamos a crear, eso puede ser cualquier cosa que consideremos apropiado (también será el nombre de la carpeta que se creará donde ejecutamos `venv`).

## Activar el entorno virtual

Para activar el entorno virtual, debemos usar los _scripts_ que se crearon en la carpeta `.venv`.

```console
source .venv/Scripts/activate
```

Si todo salió relativamente bien, es posible que en nuestro _prompt_ aparezca el nombre del entorno virtual... por ejemplo el mió se ve así:

```output
(.venv)
~/Projects/untref-edd/edd
$
```

_(si, esas 3 líneas son todo el prompt)_

## Desactivar el entorno virtual

Simplemente ejecutando:

```console
deactivate
```

## Borrar el entorno virutal

Se debe borrar la carpeta que se había creado:

```console
rm -r .venv
```

## Activar el entorno virtual cuando entramos al directorio del "proyecto"

Primero debemos instalar una ayudita en nuestro archivo `~/.bashrc`:

```bash
# Helpers for `venv`
function set_local_venv {
    echo $1 > .python-version
}

function activate_venv {
    [ ! -f .python-version ] && return

    env_name=`cat .python-version`
    activate_script=$env_name/Scripts/activate

    [ ! -f $activate_script ] && return

    source $activate_script
}

# This will simulate chpwd hook effect on this bash context
export PROMPT_COMMAND=activate_venv
```

Tanto copiar esas líneas manualmente, como ejecutar el siguiente comando en Git Bash, habilita estas funciones.

```console
echo -e "\n\n# Helpers for \`venv\`\nfunction set_local_venv {\n    echo \$1 > .python-version\n}\n\nfunction activate_venv {\n    [ ! -f .python-version ] && return\n\n    env_name=\`cat .python-version\`\n    activate_script=\$env_name/Scripts/activate\n\n    [ ! -f \$activate_script ] && return\n\n    source \$activate_script\n}\n\n# This will simulate chpwd hook effect on this bash context\nexport PROMPT_COMMAND=activate_venv\n" >> $HOME/.bashrc
```

Cerramos todas las terminales y las volvemos a abrir.

### Cómo usar la activación automática

Primero es necesario decirle a nuestro programita "qué entorno queremos activar", para eso usamos un archivo oculto llamado `.python-version` (este es un nombre con convención que se usan en varias herramientas como `pyenv`). Una de las funciones creamos fue `set_local_venv`, que es utilidad que vamos a usar para "activar la activación automática en un determinado entorno virtual".

Siguiengo con nuestro ejemplo, para prender el entorno `.venv`, nos paramos en la carpeta del entorno y desde ahí ejecutamos:

```console
set_local_venv .venv
```

Y simplemente el entorno virtual `.vevn` se activará cada vez que entremos en esa carpeta.

Importante: los entornos virtuales no se desactivaran automáticamente.
