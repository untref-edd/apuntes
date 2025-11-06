# Registrarse como Desarrollador de Meta (Facebook)

Este instructivo detalla el proceso completo para registrarse como desarrollador de Meta (Facebook), crear una aplicación y generar el Token de Acceso de Usuario necesario para realizar análisis de datos de redes sociales, explorar grafos de amistades y acceder a información pública usando Python.

## Como obtener un ***"Access Token"*** de Facebook para Análisis de Datos

El primer paso es crear una cuenta de desarrollador en la plataforma Meta.

1. Ir al Portal de Desarrolladores

   - Abrir un navegador web y acceder al portal oficial: [https://developers.facebook.com/](https://developers.facebook.com/){target="\_blank"}.

2. Iniciar Sesión

   - Hacer clic en el botón **"Empezar"** en la esquina superior derecha e iniciar sesión con una cuenta personal de Facebook.

   ```{note}
   **Requisito importante**: Necesitas tener una cuenta de Facebook activa y verificada para poder solicitar acceso como desarrollador.
   ```

3. Verificar la Cuenta

   - Seguir las instrucciones para completar el registro. Esto incluye:

     - Aceptar las **Condiciones de la plataforma** y las **Políticas para desarrolladores**.

     - Verificar la identidad proporcionando un número de teléfono o correo electrónico para recibir un código de confirmación.

     - Completar el perfil de desarrollador con información sobre el propósito de uso.

4. Proceso de Verificación

   - Meta puede solicitar información adicional sobre el uso previsto de la API.

   - La verificación puede ser inmediata o tomar hasta 24-48 horas.

   - Algunos casos de uso requieren verificación empresarial adicional.

## Crear una Nueva Aplicación de Consumidor

Una vez aprobada tu cuenta de desarrollador, puedes crear aplicaciones para acceder a la Graph API.

1. Crear una Nueva Aplicación

   - Desde el panel de desarrolladores, hacer clic en el botón verde **"Crear aplicación"**.

2. Seleccionar el Tipo de Aplicación

   - Elegir la opción **"Otro"** para casos de uso personalizados.

   - En la pantalla siguiente, seleccionar **"Ninguno"**. Esto proporciona un **"lienzo en blanco"**, ideal para trabajar directamente con la API sin configuraciones predefinidas.

   - Alternativamente, puedes seleccionar:

     - **"Consumidor"**: Para aplicaciones que consumen datos de Facebook.

     - **"Empresa"**: Para herramientas internas de empresa.

     - **"Gaming"**: Para aplicaciones de juegos.

3. Configurar Detalles de la Aplicación

   - En el campo **"Nombre de la aplicación"**, escribir un nombre descriptivo (ej: "Analizador de Grafos Académico").

   - **Propósito de la aplicación**: Describir claramente el caso de uso (ej: "Análisis académico de redes sociales").

   - **Correo de contacto**: Verificar que el correo de contacto sea correcto.

   - **Categoría de la aplicación**: Seleccionar la categoría más apropiada.

4. Crear y Configurar

   - Hacer clic en **"Crear aplicación"**. Se podría solicitar la contraseña de Facebook por seguridad.

   - Una vez creada, se abrirá el panel de control de la aplicación.

## Generar y Configurar el Token de Acceso de Usuario

Este es el paso más importante: obtener la ***"llave"*** para acceder a los datos de la Graph API.

1. Abrir el Explorador de la ***API Graph***

   - En el menú lateral izquierdo del panel de la aplicación, navegar a **Herramientas** > **Explorador de la API Graph**.

2. Configurar la Solicitud del Token

   - En la parte superior derecha de la pantalla, verificar los siguientes campos:

     - **Aplicación de Meta**: Asegurarse de que esté seleccionada la aplicación recién creada.

     - **Usuario o página**: Confirmar que esté elegida la opción **"Identificador de usuario"**.

     - **Versión de API**: Seleccionar la versión más reciente (ej: v18.0 o superior).

3. Configurar Permisos Necesarios

   - Hacer clic en la pestaña **"Permisos"**.

   - Se desplegará una lista de categorías de permisos:

     **Permisos básicos recomendados:**

     - `user_likes`: Para leer páginas que le han gustado al usuario.
     - `user_posts`: Para acceder a las publicaciones del usuario.
     - `user_friends`: Para obtener la lista de amigos (limitado).
     - `email`: Para obtener el correo electrónico del usuario.

4. Generar el Token de Acceso

   - Hacer clic en el botón azul **"Generate Access Token"**.

   - Aparecerá una ventana emergente de Facebook solicitando confirmar los permisos. **Aceptar** para continuar.

   - El sistema generará un **Token de Acceso de Usuario** de corta duración (1-2 horas).

5. Copiar y Extender el Token

   - El campo **"Identificador de acceso"** contendrá una larga cadena de caracteres.

   - **Copiar inmediatamente** el token haciendo clic en el icono de copiar.

   ```{warning}
   Los tokens de usuario tienen duración limitada. Para uso prolongado, considera generar tokens de larga duración o implementar renovación automática.
   ```

## Explorar la Graph API con Consultas Útiles

El Explorador de Graph API permite probar diferentes consultas antes de implementarlas en código.

### Consultas Básicas de Usuario

1. **Información del Usuario Actual**

   ```text
   /me?fields=id,name,email,birthday,location
   ```

2. **Páginas que le Gustan al Usuario**

   ```text
   /me/likes?fields=name,category,fan_count,website
   ```

3. **Publicaciones del Usuario**

   ```text
   /me/posts?fields=message,created_time,likes.summary(true),comments.summary(true)
   ```

### Consultas para Análisis de Redes

1. **Lista de Amigos (limitada)**

   ```text
   /me/friends?fields=name,id
   ```

   ```{note}
   Solo devuelve amigos que también usan la aplicación debido a restricciones de privacidad.
   ```

2. **Información de una Página Específica**

   ```text
   /{page-id}?fields=name,fan_count,category,website,about,location
   ```

3. **Publicaciones de una Página Pública**

   ```text
   /{page-id}/posts?fields=message,created_time,likes.summary(true),shares.summary(true)
   ```

### Consultas Avanzadas para Investigación

1. **Eventos Públicos**

   ```text
   /search?type=event&q=tecnología&fields=name,description,start_time,place
   ```

2. **Lugares Cercanos**

   ```text
   /search?type=place&center=lat,lng&distance=1000&fields=name,location,checkins
   ```

3. **Análisis de Engagement**

   ```text
   /{post-id}?fields=reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0),shares.summary(total_count).limit(0)
   ```

## Configurar Permisos Avanzados y Revisión de Aplicación

Para acceder a datos más sensibles, Meta requiere un proceso de revisión.

1. **Permisos que Requieren Revisión**

   - `user_posts`: Publicaciones del usuario
   - `user_photos`: Fotos del usuario
   - `manage_pages`: Gestión de páginas
   - `publish_pages`: Publicar en páginas

2. **Proceso de Revisión de Aplicación**

   - Ir a **Revisión de aplicación** en el panel lateral.

   - Seleccionar los permisos necesarios y proporcionar:

     - **Justificación detallada** del uso.
     - **Capturas de pantalla** de la funcionalidad.
     - **Video demostración** de cómo se usan los datos.

3. **Configurar Webhook (Opcional)**

   - Para recibir actualizaciones en tiempo real:

     - Ir a **Productos** > **Webhooks**.

     - Configurar URL de endpoint y eventos de interés.

## Tipos de Tokens y Gestión de Autenticación

Meta maneja diferentes tipos de tokens según el caso de uso:

### Token de Acceso de Usuario

- **Duración**: 1-2 horas por defecto
- **Uso**: Acceso a datos del usuario autenticado
- **Extensión**: Puede extenderse a 60 días

### Token de Acceso de Página

- **Duración**: No expira (mientras la aplicación tenga permisos)
- **Uso**: Gestión y publicación en páginas
- **Obtención**: A través del token de usuario con permisos `manage_pages`

### Token de Aplicación

- **Duración**: No expira
- **Uso**: Acceso a datos públicos y gestión de aplicación
- **Formato**: `{app-id}|{app-secret}`

### Extender la Duración del Token

```bash
# Extender token de usuario (60 días)
curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-token}"
```

## Probar las Credenciales y Conectividad

Una vez obtenido el token, es importante verificar que funciona correctamente.

1. **Verificar Token con curl**

   ```bash
   # Verificar información del usuario
   curl -i -X GET "https://graph.facebook.com/me?access_token={your-token}"

   # Verificar páginas que le gustan
   curl -i -X GET "https://graph.facebook.com/me/likes?access_token={your-token}"
   ```

2. **Usar el Debugger de Tokens**

   - Ir a [Facebook Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
   - Pegar el token para verificar:
     - **Validez y expiración**
     - **Permisos otorgados**
     - **ID de aplicación y usuario**

3. **Verificar con Python**

   ```python
   import requests

   token = "YOUR_ACCESS_TOKEN"
   response = requests.get(f"https://graph.facebook.com/me?access_token={token}")

   if response.status_code == 200:
       print("✓ Token válido:", response.json())
   else:
       print("✗ Error:", response.text)
   ```

## Limitaciones y Restricciones Actuales

Es crucial entender las limitaciones de la Graph API tras los cambios de privacidad.

### Restricciones de Datos de Usuario

- **Solo datos propios**: Acceso limitado a datos del usuario autenticado
- **Amigos limitados**: Solo amigos que también usan la aplicación
- **Revisión obligatoria**: Muchos permisos requieren proceso de revisión
- **Rate limiting**: Límites estrictos en número de llamadas por hora

### Datos Públicos Disponibles

- **Páginas públicas**: Información básica y publicaciones públicas
- **Eventos públicos**: Eventos marcados como públicos
- **Lugares**: Información de ubicaciones y check-ins públicos
- **Grupos públicos**: Contenido de grupos públicos (limitado)

### Rate Limits y Cuotas

- **200 llamadas por hora** por usuario para aplicaciones en desarrollo
- **Límites más altos** para aplicaciones verificadas
- **Throttling automático** cuando se exceden los límites

## Consideraciones de Seguridad

### Protección de Credenciales

1. **Nunca hardcodear** tokens en el código fuente
2. **Usar variables de entorno** para almacenar credenciales
3. **Implementar renovación automática** de tokens
4. **Monitorear el uso** de tokens en el panel de desarrollador

### Ejemplo de Configuración Segura

```python
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales de forma segura
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

# Verificar que las credenciales están disponibles
if not all([FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET]):
    raise ValueError("Faltan credenciales de Facebook en variables de entorno")
```

### Archivo .env (ejemplo)

```bash
# Credenciales de Facebook
FACEBOOK_ACCESS_TOKEN=your_user_access_token_here
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here

# Configuración adicional
FACEBOOK_API_VERSION=v18.0
FACEBOOK_RATE_LIMIT_DELAY=1
```

### Mejores Prácticas de Seguridad

1. **Rotación de tokens**: Renovar tokens periódicamente
2. **Monitoreo de uso**: Revisar logs de API en el panel de desarrollador
3. **Principio de menor privilegio**: Solo solicitar permisos necesarios
4. **Validación de entrada**: Sanitizar datos recibidos de la API
5. **HTTPS obligatorio**: Usar siempre conexiones seguras

## Documentación y Recursos Útiles

### Documentación Oficial

- [Meta for Developers - Getting Started](https://developers.facebook.com/docs/development/create-an-app/){target="\_blank"}
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/){target="\_blank"}
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/){target="\_blank"}
- [Facebook SDK for Python](https://facebook-sdk.readthedocs.io/){target="\_blank"}

### Librerías de Python Recomendadas

- [**facebook-sdk**](https://facebook-sdk.readthedocs.io/){target="\_blank"}: SDK de terceros/comunidad para interactuar con Graph API en Python
- [**requests**](https://requests.readthedocs.io/){target="\_blank"}: Para llamadas HTTP directas (recomendado para máxima compatibilidad)
- [**python-facebook-api**](https://github.com/sns-sdks/python-facebook){target="\_blank"}: Alternativa moderna mantenida por la comunidad

### Herramientas de Desarrollo

- [**Graph API Explorer**](https://developers.facebook.com/tools/explorer/): Probar consultas interactivamente
- [**Access Token Debugger**](https://developers.facebook.com/tools/debug/accesstoken/): Verificar tokens
- [**Sharing Debugger**](https://developers.facebook.com/tools/debug/): Probar compartir contenido

### Ejemplos de Endpoints Útiles

- **Usuario actual**: `/me`
- **Páginas favoritas**: `/me/likes`
- **Publicaciones**: `/me/posts`
- **Información de página**: `/{page-id}`
- **Publicaciones de página**: `/{page-id}/posts`
- **Eventos**: `/me/events`

```{important}
**Nota sobre privacidad y cambios recientes**: La API de Facebook Graph ha limitado significativamente el acceso a datos de usuarios desde el escándalo de [Cambridge Analytica en 2018](https://es.wikipedia.org/wiki/Cambridge_Analytica){target="_blank"}. Actualmente, solo se puede acceder a datos del propio usuario autenticado y datos públicos. Muchas funcionalidades que antes estaban disponibles ahora requieren revisión de aplicación y justificación detallada del caso de uso.
```
