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

# La Web y las APIs

La Web es una de las fuentes de información más grandes y diversas disponibles en la actualidad. Contiene datos estructurados, semiestructurados y no estructurados que pueden ser aprovechados para múltiples propósitos: análisis de datos, investigación, monitoreo de precios, agregación de noticias, entre otros. En este capítulo exploraremos el funcionamiento de la Web y cómo acceder a información a través de APIs.

## Introducción al Funcionamiento de la Web

### Arquitectura Cliente-Servidor

La World Wide Web funciona bajo un modelo cliente-servidor. El siguiente diagrama ilustra cómo interactúan estos componentes:

```{mermaid}
flowchart LR
    A[Cliente<br/>Navegador] -->|1. Solicitud HTTP| B[Servidor Web]
    B -->|2. Respuesta HTTP| A
    A -->|3. Consulta DNS| C[Servidor DNS]
    C -->|4. Dirección IP| A
    
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style C fill:#e1ffe1
```

Los componentes principales son:

**Cliente (Navegador)**
: Programa que solicita recursos web (páginas HTML, imágenes, videos, etc.). Los navegadores más comunes son Chrome, Firefox, Safari y Edge.

**Servidor Web**
: Aplicación que responde a las solicitudes de los clientes, enviando los recursos solicitados. Ejemplos incluyen Apache, Nginx, y servidores de aplicaciones como Node.js o Python con frameworks como Django o FastAPI.

**DNS (Domain Name System)**
: Sistema que traduce nombres de dominio legibles (como `www.google.com`) a direcciones IP numéricas que los computadores pueden entender.

### El Protocolo HTTP

HTTP (*HyperText Transfer Protocol*) es el protocolo de comunicación que permite la transferencia de información en la Web. Define cómo los clientes y servidores intercambian mensajes.

```{mermaid}
sequenceDiagram
    participant C as Cliente
    participant S as Servidor
    
    C->>S: GET /index.html HTTP/1.1
    Note over C,S: Solicitud HTTP
    S->>C: HTTP/1.1 200 OK
    Note over C,S: Respuesta HTTP con contenido
```

#### Características de HTTP

- **Sin estado (stateless)**: Cada solicitud es independiente, el servidor no mantiene información sobre solicitudes anteriores
- **Basado en texto**: Los mensajes son legibles por humanos
- **Extensible**: Permite agregar nuevos métodos y cabeceras
- **Cliente-Servidor**: Modelo de comunicación request-response

#### Métodos HTTP Principales

Los métodos HTTP más comunes son:

`GET`
: Solicita un recurso específico. Es el método más común y solo debe recuperar datos sin modificarlos.

`POST`
: Envía datos al servidor para crear un nuevo recurso. Comúnmente usado en formularios.

`PUT`
: Actualiza un recurso existente con datos nuevos.

`DELETE`
: Elimina un recurso específico.

`HEAD`
: Similar a GET, pero solo solicita las cabeceras de la respuesta, sin el cuerpo.

`PATCH`
: Aplica modificaciones parciales a un recurso.

#### Códigos de Estado HTTP

Las respuestas HTTP incluyen un código de estado que indica el resultado de la solicitud:

**2xx (Éxito)**
: - `200 OK`: Solicitud exitosa
: - `201 Created`: Recurso creado exitosamente
: - `204 No Content`: Éxito pero sin contenido para devolver

**3xx (Redirección)**
: - `301 Moved Permanently`: El recurso se ha movido permanentemente
: - `302 Found`: Redirección temporal
: - `304 Not Modified`: El recurso no ha sido modificado desde la última solicitud

**4xx (Error del Cliente)**
: - `400 Bad Request`: Solicitud mal formada
: - `401 Unauthorized`: Autenticación requerida
: - `403 Forbidden`: Acceso denegado
: - `404 Not Found`: Recurso no encontrado
: - `429 Too Many Requests`: Límite de velocidad excedido

**5xx (Error del Servidor)**
: - `500 Internal Server Error`: Error genérico del servidor
: - `502 Bad Gateway`: El servidor actuó como gateway y recibió una respuesta inválida
: - `503 Service Unavailable`: Servidor no disponible temporalmente

#### Ejemplo de Solicitud HTTP con Python

```{code-cell} python
import requests

# Realizar una solicitud GET
response = requests.get('https://httpbin.org/get')

print(f"Código de estado: {response.status_code}")
print(f"Cabeceras de respuesta:\n{response.headers}")
print(f"\nContenido (primeros 200 caracteres):\n{response.text[:200]}")
```

### HTTPS: HTTP Seguro

HTTPS (HTTP Secure) es la versión segura de HTTP que utiliza encriptación TLS/SSL para proteger la comunicación entre cliente y servidor. Es fundamental para:

- Proteger datos sensibles (contraseñas, información financiera)
- Verificar la identidad del servidor
- Prevenir ataques de intermediarios (man-in-the-middle)
- Mejorar el posicionamiento en motores de búsqueda

## APIs: Interfaces de Programación de Aplicaciones

Las APIs (*Application Programming Interfaces*) son interfaces que permiten que diferentes aplicaciones se comuniquen entre sí de manera programática. En el contexto web, las APIs proporcionan endpoints (puntos de acceso) que los desarrolladores pueden usar para acceder a datos y funcionalidades de un servicio.

```{mermaid}
flowchart TB
    A[Aplicación Cliente] -->|Solicitud HTTP| B[API REST]
    B -->|JSON/XML| A
    B --> C[Base de Datos]
    B --> D[Servicios Externos]
    B --> E[Lógica de Negocio]
    
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style C fill:#fff4e1
    style D fill:#e1ffe1
    style E fill:#f5e1ff
```

### API REST (Representational State Transfer)

REST es un estilo arquitectónico para diseñar servicios web que se basa en los principios de HTTP. Una API REST expone recursos a través de URLs y utiliza los métodos HTTP estándar para operaciones CRUD (Create, Read, Update, Delete).

#### Principios de REST

**Arquitectura Cliente-Servidor**
: Separación de responsabilidades entre interfaz de usuario y almacenamiento de datos.

**Sin Estado**
: Cada solicitud contiene toda la información necesaria; el servidor no mantiene sesiones.

**Cacheable**
: Las respuestas deben indicar si pueden ser almacenadas en caché.

**Interfaz Uniforme**
: Uso consistente de URLs y métodos HTTP.

**Sistema en Capas**
: La arquitectura puede tener múltiples capas intermedias.

#### Ejemplo: Consumir una API REST Pública

Vamos a consumir la API pública de JSONPlaceholder, que simula un servicio REST:

```{code-cell} python
import requests
import json

# Obtener una lista de posts
response = requests.get('https://jsonplaceholder.typicode.com/posts')
posts = response.json()

print(f"Total de posts: {len(posts)}")
print(f"\nPrimer post:")
print(json.dumps(posts[0], indent=2))

# Obtener un post específico
post_id = 1
response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
post = response.json()
print(f"\nPost con ID {post_id}:")
print(f"Título: {post['title']}")
print(f"Cuerpo: {post['body'][:100]}...")

# Crear un nuevo post (simulado)
nuevo_post = {
    'title': 'Mi nuevo post',
    'body': 'Este es el contenido de mi post',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=nuevo_post
)

print(f"\nCódigo de respuesta al crear post: {response.status_code}")
print(f"Post creado (simulado):")
print(json.dumps(response.json(), indent=2))
```

#### Ejemplo: API de Información Geográfica

Muchas APIs REST proporcionan datos estructurados útiles. Veamos un ejemplo con una API de información de países:

```{code-cell} python
import requests
import json

# Obtener información sobre Argentina
response = requests.get('https://restcountries.com/v3.1/name/argentina')
paises = response.json()

if paises:
    argentina = paises[0]
    print(f"Nombre oficial: {argentina.get('name', {}).get('official', 'N/A')}")
    print(f"Capital: {argentina.get('capital', ['N/A'])[0]}")
    print(f"Región: {argentina.get('region', 'N/A')}")
    print(f"Población: {argentina.get('population', 'N/A'):,}")
    print(f"Área: {argentina.get('area', 'N/A'):,} km²")
    
    # Idiomas
    idiomas = argentina.get('languages', {})
    print(f"Idiomas: {', '.join(idiomas.values())}")
    
    # Monedas
    monedas = argentina.get('currencies', {})
    for codigo, info in monedas.items():
        print(f"Moneda: {info.get('name')} ({codigo})")
```

#### Ejemplo: API del Clima (OpenWeatherMap)

```{code-cell} python
import requests

# Nota: En un caso real, necesitarías registrarte y obtener una API key gratuita
# Este es solo un ejemplo ilustrativo de cómo funcionaría

def obtener_clima(ciudad, api_key):
    """
    Obtiene información del clima para una ciudad específica.
    
    Args:
        ciudad: Nombre de la ciudad
        api_key: Clave de API de OpenWeatherMap
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    parametros = {
        'q': ciudad,
        'appid': api_key,
        'units': 'metric',  # Para obtener temperatura en Celsius
        'lang': 'es'
    }
    
    try:
        response = requests.get(base_url, params=parametros)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        datos = response.json()
        
        print(f"Clima en {datos['name']}, {datos['sys']['country']}")
        print(f"Temperatura: {datos['main']['temp']}°C")
        print(f"Sensación térmica: {datos['main']['feels_like']}°C")
        print(f"Descripción: {datos['weather'][0]['description']}")
        print(f"Humedad: {datos['main']['humidity']}%")
        print(f"Velocidad del viento: {datos['wind']['speed']} m/s")
        
        return datos
        
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except KeyError as e:
        print(f"Error procesando la respuesta: {e}")

# Ejemplo de uso (requiere API key válida)
# obtener_clima("Buenos Aires", "TU_API_KEY_AQUI")
print("Para usar esta función, registrate en https://openweathermap.org/api")
```

#### Autenticación en APIs REST

Las APIs frecuentemente requieren autenticación. Los métodos más comunes son:

**API Keys**
: Una clave secreta que se envía en la URL o en las cabeceras.

```{code-cell} python
# Ejemplo conceptual con API key
import requests

# Opción 1: En la URL como parámetro
response = requests.get(
    'https://api.ejemplo.com/datos',
    params={'api_key': 'tu_clave_secreta'}
)

# Opción 2: En las cabeceras
headers = {'X-API-Key': 'tu_clave_secreta'}
response = requests.get('https://api.ejemplo.com/datos', headers=headers)

print(f"Método de autenticación configurado")
```

**OAuth 2.0**
: Protocolo de autorización más complejo pero seguro, usado por servicios como Google, Facebook, Twitter.

**Bearer Tokens**
: Tokens de acceso que se envían en el header de autorización.

```{code-cell} python
# Ejemplo conceptual con Bearer Token
import requests

headers = {
    'Authorization': 'Bearer tu_token_de_acceso_aqui'
}

response = requests.get('https://api.ejemplo.com/datos', headers=headers)
print(f"Autenticación con Bearer Token configurada")
```

## Mejores Prácticas para Usar APIs

### Recomendaciones Generales

1. **Leer la documentación**: Entender límites de velocidad, autenticación y términos de uso
2. **Manejar errores**: Implementar reintentos con backoff exponencial
3. **Cachear respuestas**: Evitar solicitudes repetidas
4. **Monitorear cuotas**: Estar atento a los límites de uso
5. **Versionar**: Usar versiones específicas de APIs para evitar cambios inesperados

### Manejo de Errores y Reintentos

```{code-cell} python
import requests
import time

def consumir_api_con_reintentos(url, max_intentos=3, delay=1):
    """
    Realiza una solicitud con reintentos en caso de error.
    
    Args:
        url: URL de la API
        max_intentos: Número máximo de reintentos
        delay: Tiempo de espera entre reintentos (en segundos)
    """
    for intento in range(max_intentos):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Intento {intento + 1} falló: {e}")
            if intento < max_intentos - 1:
                time.sleep(delay * (2 ** intento))  # Backoff exponencial
            else:
                print("Todos los intentos fallaron")
                raise
    
    return None

# Ejemplo de uso
# datos = consumir_api_con_reintentos('https://api.ejemplo.com/datos')
print("Función de reintentos definida")
```

## Referencias y Recursos Adicionales

### Documentación Oficial

- [Requests Documentation](https://requests.readthedocs.io/){target="_blank"}
- [HTTP Documentation (MDN)](https://developer.mozilla.org/es/docs/Web/HTTP){target="_blank"}
- [REST API Tutorial](https://restfulapi.net/){target="_blank"}

### Libros y Referencias Académicas

- Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, *Introduction to Information Retrieval*, Cambridge University Press, 2008. Capítulo 19: Web Search Basics.

### APIs Públicas para Practicar

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/){target="_blank"} - API REST falsa para testing
- [REST Countries](https://restcountries.com/){target="_blank"} - Información sobre países
- [OpenWeatherMap](https://openweathermap.org/api){target="_blank"} - Datos meteorológicos
- [The Star Wars API](https://swapi.dev/){target="_blank"} - Datos de Star Wars
- [PokéAPI](https://pokeapi.co/){target="_blank"} - Información sobre Pokémon

### Recursos en Español

- [Tutorial de Requests en Español](https://docs.python-requests.org/es/latest/){target="_blank"}
- [Comunidad Python Argentina](https://python.org.ar/){target="_blank"}
