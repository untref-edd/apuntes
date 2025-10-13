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

# Como obtener un ***"Access Token"*** de Facebook para Análisis de Datos

Este instructivo detalla el proceso para registrarse como desarrollador de Meta, crear una aplicación de tipo Consumidor y generar el Token de Acceso de Usuario necesario para realizar análisis de datos con Python.

## Registrarse como Desarrollador de Meta

El primer paso es crear una cuenta de desarrollador.

1. Ir al Portal de Desarrolladores

    - Abrir un navegador web y acceder al portal oficial: [https://developers.facebook.com/](https://developers.facebook.com/){target="_blank"}.

2. Iniciar Sesión

    - Hacer clic en el botón **"Empezar"** en la esquina superior derecha e iniciar sesión con una cuenta personal de Facebook.

3. Verificar la Cuenta

    - Seguir las instrucciones para completar el registro. Esto incluye:

      - Aceptar las Condiciones de la plataforma y las Políticas para desarrolladores.

      - Verificar la identidad proporcionando un número de teléfono o correo electrónico para recibir un código de confirmación.

## Crear una Nueva Aplicación de Consumidor

Ahora, es momento de crear el proyecto que contendrá la lógica y los permisos.

1. Crear una Nueva Aplicación

    - Desde el panel de desarrolladores, hacer clic en el botón verde **"Crear aplicación"**.

2. Seleccionar el Tipo de Aplicación

    - Elegir la opción **"Otro"**.

    - En la pantalla siguiente, seleccionar **"Ninguno"**. Esto proporciona un **"lienzo en blanco"**, ideal para trabajar directamente con la API sin configuraciones predefinidas.

3. Asignar un Nombre y Crear

    - En el campo **"Nombre de la aplicación"**, escribir un nombre descriptivo (ej: "Analizador de Grafos Académico").

    - Verificar que el correo de contacto sea correcto.

    - Hacer clic en **"Crear aplicación"**. Se podría solicitar la contraseña de Facebook por seguridad.

## Generar y Copiar el Token de Acceso de Usuario

Este es el paso final y más importante: obtener la ***"llave"*** para acceder a los datos.

1. Abrir el Explorador de la ***API Graph***

    - En el menú lateral izquierdo del panel de la aplicación, navegar a Herramientas > Explorador de la API Graph.

2. Configurar la Solicitud del Token

    - A la derecha de la pantalla, verificar los siguientes campos:

        - Aplicación de Meta: Asegurarse de que esté seleccionada la aplicación recién creada.

        - Usuario o página: Confirmar que esté elegida la opción **"Identificador de usuario"**.

3. Añadir el Permiso `user_likes`

    - Hacer clic en la pestaña "Permisos".

    - Se desplegará una lista de categorías. Dentro de `User Data Permissions`, buscar y marcar la casilla del permiso `user_likes`. Este permiso es el que autoriza a la aplicación para leer la lista de páginas que le han gustado al usuario.

4. Generar el Token de Acceso

    - Hacer clic en el botón azul **"Generate Access Token".**

    - Aparecerá una ventana emergente de Facebook solicitando confirmar el permiso para acceder a los "Me gusta". Aceptar para continuar.

5. Copiar el Token Generado

    - El campo **"Identificador de acceso"** ahora contendrá una larga cadena de caracteres. Este es tu Token de Acceso de Usuario.

    - Hacer clic en el icono de copiar al lado del campo para guardarlo en el portapapeles.

Este token es la credencial que se deberá pegar en el script de Python para autenticar las solicitudes a la API de Facebook.

## Documentación oficial

- [Meta for Developers - Getting Started](https://developers.facebook.com/docs/development/create-an-app/){target="_blank"}
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/){target="_blank"}

```{important}
**Nota sobre privacidad**: La API de Facebook Graph ha limitado significativamente el acceso a datos de usuarios desde 2018 por razones de privacidad. Actualmente, solo se puede acceder a datos del propio usuario autenticado y amigos que hayan autorizado la aplicación. 
```