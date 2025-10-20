# Registrarse como Desarrollador de X (Twitter)

Este instructivo detalla el proceso completo para registrarse como desarrollador de X (anteriormente Twitter), crear una aplicación y generar las credenciales necesarias (Bearer Token y Access Token) para realizar análisis de datos y acceder tanto a tweets históricos como a streams en tiempo real usando Python.

## Como obtener un ***"Bearer Token"*** y ***"Access Token"*** de X (Twitter) para Análisis de Datos

El primer paso es crear una cuenta de desarrollador en la plataforma X.

1. Ir al Portal de Desarrolladores

   - Abrir un navegador web y acceder al portal oficial: [https://developer.twitter.com/](https://developer.twitter.com/){target="\_blank"}.

1. Iniciar Sesión

   - Hacer clic en el botón **"Sign up"** en la esquina superior derecha e iniciar sesión con una cuenta personal de X (Twitter).

   ```{note}
   **Requisito importante**: Necesitas tener una cuenta de X/Twitter verificada con un número de teléfono válido para poder solicitar acceso como desarrollador.
   ```

1. Solicitar Acceso como Desarrollador

   - Hacer clic en **"Apply for a developer account"**.

   - Completar el formulario de solicitud:

     - **Propósito de uso**: Seleccionar entre Académico/Investigación, Comercial, Personal, o Estudiante.

     - **Descripción detallada**: Explicar específicamente cómo planeas usar la API (ej: "Análisis académico de tendencias en redes sociales para curso de Estructuras de Datos").

     - **Casos de uso específicos**: Indicar si vas a analizar tweets, hacer streaming, publicar contenido, etc.

1. Verificar la Solicitud

   - Revisar toda la información y enviar la solicitud.

   - Aceptar las **Condiciones de Servicio para Desarrolladores** y la **Política de Uso de la API**.

   - La aprobación puede tomar desde minutos hasta 1-2 días hábiles.

## Crear una Nueva Aplicación (App)

Una vez aprobada tu cuenta de desarrollador, puedes crear aplicaciones para acceder a la API.

1. Acceder al Panel de Desarrollador

   - Desde el Developer Portal, hacer clic en **"Projects & Apps"** en el menú lateral.

1. Crear un Nuevo Proyecto

   - Hacer clic en el botón **"+ Create Project"**.

   - Asignar un nombre descriptivo al proyecto (ej: "Analizador de Redes Sociales Académico").

   - Seleccionar el caso de uso más apropiado:

     - **"Exploring the API"**: Para aprendizaje y experimentación.

     - **"Making a bot"**: Para crear bots automatizados.

     - **"Doing academic research"**: Para investigación académica.

     - **"Building internal tools"**: Para herramientas empresariales.

1. Crear una Aplicación dentro del Proyecto

   - Después de crear el proyecto, X te pedirá crear una aplicación.

   - Asignar un nombre único a la aplicación (ej: "TwitterDataAnalyzer2024").

   - Proporcionar una descripción clara del propósito de la aplicación.

## Obtener las Credenciales de Autenticación

Este es el paso más importante: generar las ***"llaves"*** para acceder a los datos de X.

1. Configurar Niveles de Acceso

   - En el panel de tu aplicación, ir a la pestaña **"Settings"**.

   - En **"App permissions"**, configurar los permisos necesarios:

     - **Read**: Para leer tweets, perfiles, y datos públicos.

     - **Write**: Para publicar tweets (opcional para análisis de datos).

     - **Direct Messages**: Para acceder a mensajes directos (raramente necesario).

   ```{important}
   Para análisis de datos, generalmente solo necesitas permisos de **"Read"**.
   ```

1. Generar el Bearer Token (API v2)

   - Ir a la pestaña **"Keys and Tokens"**.

   - En la sección **"Bearer Token"**, hacer clic en **"Generate"**.

   - **Copiar y guardar** inmediatamente el Bearer Token en un lugar seguro.

   ```{warning}
   El Bearer Token se muestra solo una vez. Si lo pierdes, deberás regenerar uno nuevo.
   ```

1. Generar Consumer Keys (API v1.1)

   - En la sección **"Consumer Keys"**, hacer clic en **"Generate"**.

   - Se generarán automáticamente:

     - **API Key** (Consumer Key)

     - **API Secret Key** (Consumer Secret)

   - **Copiar y guardar** ambas credenciales de forma segura.

1. Generar Access Token y Access Token Secret

   - En la sección **"Access Token and Secret"**, hacer clic en **"Generate"**.

   - Se generarán:

     - **Access Token**

     - **Access Token Secret**

   - **Copiar y guardar** ambas credenciales.

## Configurar Permisos para Streaming y Búsqueda

Para acceder a diferentes funcionalidades de la API, necesitas configurar permisos específicos.

1. Configurar Permisos de la Aplicación

   - En **"App permissions"**, seleccionar el nivel apropiado:

     - **Read**: Suficiente para leer tweets históricos y hacer streaming.

     - **Read and Write**: Si planeas publicar tweets desde tu aplicación.

   - Guardar los cambios.

1. Verificar Nivel de Acceso a la API

   - X ofrece diferentes niveles de acceso:

     - **Free**: 500,000 tweets por mes, acceso básico a API v2.

     - **Basic** (\$100/mes): 10 millones de tweets por mes, acceso completo a API v2.

     - **Pro** (\$5,000/mes): 50 millones de tweets por mes, acceso a datos históricos completos.

     - **Enterprise**: Acceso personalizado y soporte premium.

1. Configurar Webhook URLs (Opcional)

   - Si planeas usar webhooks para recibir datos en tiempo real:

     - Ir a **"Settings"** > **"Webhook URLs"**.

     - Agregar la URL de tu servidor que recibirá los datos.

## Probar las Credenciales

Una vez obtenidas las credenciales, es importante verificar que funcionan correctamente.

1. Verificar Bearer Token

   - Usar el **Postman** o **curl** para hacer una petición de prueba:

   ```bash
   curl -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
        "https://api.twitter.com/2/tweets/search/recent?query=python"
   ```

1. Verificar Access Tokens

   - Para OAuth 1.0a, las credenciales se usan en conjunto para firmar las peticiones.

   - La librería `tweepy` de Python maneja automáticamente la autenticación.

## Niveles de Acceso y Limitaciones

Es importante entender las limitaciones de cada nivel de acceso:

### Free Tier (Gratuito)

- **500,000 tweets** por mes
- **1 aplicación** por proyecto
- **Acceso a API v2** básica
- **Search Recent** (últimos 7 días)
- **Filtered Stream** básico
- **Sin acceso a datos históricos** completos

### Basic Tier (\$100/mes)

- **10 millones de tweets** por mes
- **3 aplicaciones** por proyecto
- **Acceso completo a API v2**
- **Search Recent y Archive** (histórico completo)
- **Filtered Stream** avanzado
- **Soporte estándar**

### Pro Tier (\$5,000/mes)

- **50 millones de tweets** por mes
- **Aplicaciones ilimitadas**
- **Acceso a Full Archive Search**
- **Datos históricos** desde 2006
- **Analytics y métricas** avanzadas
- **Soporte prioritario**

## Documentación y Recursos Útiles

### Documentación Oficial

- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api){target="\_blank"}
- [API v2 Quick Start Guide](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api){target="\_blank"}
- [Authentication Guide](https://developer.twitter.com/en/docs/authentication/overview){target="\_blank"}
- [Rate Limits and Pricing](https://developer.twitter.com/en/docs/twitter-api/rate-limits){target="\_blank"}

### Librerías de Python Recomendadas

- [**Tweepy**](https://docs.tweepy.org/){target="\_blank"}: Librería de terceros (muy popular) para Python
- [**Python-Twitter**](https://python-twitter.readthedocs.io/){target="\_blank"}: Alternativa robusta
- [**TwitterAPI**](https://github.com/geduldig/TwitterAPI){target="\_blank"}: Acceso directo a endpoints

### Ejemplos de Endpoints Útiles

- **Search Recent Tweets**: `/2/tweets/search/recent`
- **Search Historical**: `/2/tweets/search/all` (requiere Academic Research o Basic+)
- **User Timeline**: `/2/users/:id/tweets`
- **Filtered Stream**: `/2/tweets/search/stream`
- **Sample Stream**: `/2/tweets/sample/stream`

## Consideraciones de Seguridad

### Protección de Credenciales

1. **Nunca hardcodear** las credenciales en el código fuente.
1. **Usar variables de entorno** o archivos de configuración privados.
1. **Agregar archivos de credenciales** al `.gitignore`.
1. **Regenerar tokens** periódicamente por seguridad.

### Ejemplo de Configuración Segura

```python
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales de forma segura
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
```

```{important}
**Nota sobre cambios recientes**: Desde la adquisición por Elon Musk en 2022, X ha modificado significativamente sus políticas de API. El acceso gratuito está más limitado y muchas funcionalidades requieren suscripciones pagadas. Siempre verificar la documentación oficial para conocer las limitaciones actuales.
```
