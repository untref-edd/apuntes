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

# Recuperación de la Información de la Web

La Web es una de las fuentes de información más grandes y diversas disponibles en la actualidad. Contiene datos estructurados, semiestructurados y no estructurados que pueden ser aprovechados para múltiples propósitos: análisis de datos, investigación, monitoreo de precios, agregación de noticias, entre otros. En este capítulo exploraremos las diferentes técnicas y tecnologías para acceder y extraer información de la Web.

## Introducción al Funcionamiento de la Web

### Arquitectura Cliente-Servidor

La World Wide Web funciona bajo un modelo cliente-servidor donde:

**Cliente (Navegador)**
: Programa que solicita recursos web (páginas HTML, imágenes, videos, etc.). Los navegadores más comunes son Chrome, Firefox, Safari y Edge.

**Servidor Web**
: Aplicación que responde a las solicitudes de los clientes, enviando los recursos solicitados. Ejemplos incluyen Apache, Nginx, y servidores de aplicaciones como Node.js o Python con frameworks como Django o FastAPI.

**DNS (Domain Name System)**
: Sistema que traduce nombres de dominio legibles (como `www.google.com`) a direcciones IP numéricas que los computadores pueden entender.

### El Protocolo HTTP

HTTP (*HyperText Transfer Protocol*) es el protocolo de comunicación que permite la transferencia de información en la Web. Define cómo los clientes y servidores intercambian mensajes.

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

### GraphQL

GraphQL es un lenguaje de consulta para APIs desarrollado por Facebook en 2012 y liberado como código abierto en 2015. A diferencia de REST, donde cada endpoint devuelve una estructura fija de datos, GraphQL permite al cliente especificar exactamente qué datos necesita.

#### Ventajas de GraphQL sobre REST

**Una sola solicitud para múltiples recursos**
: En REST, obtener datos relacionados puede requerir múltiples solicitudes a diferentes endpoints. GraphQL permite obtener todos los datos necesarios en una sola consulta.

**Sin over-fetching ni under-fetching**
: El cliente solicita exactamente los campos que necesita, ni más ni menos.

**Tipado fuerte**
: El esquema define claramente los tipos de datos disponibles.

**Introspección**
: Es posible consultar el esquema de la API para descubrir qué datos y operaciones están disponibles.

**Versionado no necesario**
: Los campos se pueden agregar o depreciar sin romper clientes existentes.

#### Ejemplo de Consulta GraphQL

```{code-cell} python
import requests
import json

# Ejemplo usando la API pública de GraphQL de Countries
url = 'https://countries.trevorblades.com/'

# Consulta GraphQL para obtener información de países de América del Sur
query = """
{
  continents(filter: {code: {eq: "SA"}}) {
    name
    countries {
      name
      capital
      currency
      languages {
        name
      }
    }
  }
}
"""

response = requests.post(url, json={'query': query})
data = response.json()

print("Países de América del Sur:\n")
paises_sa = data['data']['continents'][0]['countries']

for pais in paises_sa[:5]:  # Mostrar solo los primeros 5
    print(f"\n{pais['name']}")
    print(f"  Capital: {pais.get('capital', 'N/A')}")
    print(f"  Moneda: {pais.get('currency', 'N/A')}")
    
    idiomas = pais.get('languages', [])
    if idiomas:
        nombres_idiomas = [lang['name'] for lang in idiomas]
        print(f"  Idiomas: {', '.join(nombres_idiomas)}")
```

#### Mutaciones en GraphQL

Además de consultas (queries), GraphQL soporta mutaciones para modificar datos:

```{code-cell} python
# Ejemplo conceptual de una mutación GraphQL
import requests
import json

# Mutación para crear un nuevo usuario (ejemplo ilustrativo)
mutation = """
mutation CrearUsuario($nombre: String!, $email: String!) {
  crearUsuario(input: {nombre: $nombre, email: $email}) {
    id
    nombre
    email
    creadoEn
  }
}
"""

variables = {
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com"
}

# En un caso real, esto se enviaría a un endpoint GraphQL
payload = {
    'query': mutation,
    'variables': variables
}

print("Ejemplo de mutación GraphQL:")
print(json.dumps(payload, indent=2))
```

#### Comparación REST vs GraphQL

```{list-table}
---
header-rows: 1
---
* - Característica
  - REST
  - GraphQL
* - Endpoints
  - Múltiples endpoints (uno por recurso)
  - Un único endpoint
* - Estructura de datos
  - Fija (definida por el servidor)
  - Flexible (definida por el cliente)
* - Over-fetching
  - Común
  - No ocurre
* - Under-fetching
  - Requiere múltiples solicitudes
  - Una consulta obtiene todo
* - Versionado
  - Necesario (v1, v2, etc.)
  - No necesario
* - Caché
  - Más fácil con HTTP
  - Requiere implementación especial
* - Curva de aprendizaje
  - Más simple
  - Más compleja
```

## Web Scraping

Web scraping es el proceso de extraer información de sitios web de forma automatizada. Mientras que las APIs proporcionan interfaces estructuradas para acceder a datos, el web scraping permite obtener información de sitios que no ofrecen APIs o cuando se necesita acceder a datos que no están disponibles a través de ellas.

### Consideraciones Legales y Éticas

Antes de realizar web scraping, es fundamental considerar:

#### Aspectos Legales

**Archivo robots.txt**
: Archivo en la raíz del sitio web que especifica qué partes pueden ser accedidas por robots automatizados.

```{code-cell} python
import requests

# Verificar el archivo robots.txt
url_robots = 'https://www.python.org/robots.txt'
response = requests.get(url_robots)

print("Contenido de robots.txt de python.org (primeras líneas):")
print('\n'.join(response.text.split('\n')[:20]))
```

**Términos de Servicio**
: Muchos sitios web prohíben explícitamente el scraping en sus términos de uso.

**Leyes de Protección de Datos**
: Regulaciones como GDPR en Europa o leyes locales de protección de datos personales.

**Propiedad Intelectual**
: El contenido scrapeado puede estar protegido por derechos de autor.

#### Buenas Prácticas Éticas

**Respetar robots.txt**
: Siempre verificar y respetar las directivas del archivo robots.txt.

**Limitar la frecuencia de solicitudes**
: No sobrecargar los servidores con demasiadas solicitudes simultáneas.

```{code-cell} python
import time
import requests

def scraping_respetuoso(urls, delay=1):
    """
    Realiza solicitudes con un delay entre cada una.
    
    Args:
        urls: Lista de URLs a consultar
        delay: Segundos de espera entre solicitudes
    """
    resultados = []
    
    for url in urls:
        print(f"Consultando: {url}")
        response = requests.get(url)
        resultados.append(response)
        
        # Esperar antes de la siguiente solicitud
        time.sleep(delay)
    
    return resultados

# Ejemplo de uso
urls_ejemplo = [
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/1'
]

print("Realizando solicitudes con delay de 2 segundos...")
# resultados = scraping_respetuoso(urls_ejemplo, delay=2)
print("Scraping respetuoso completado")
```

**Identificarse correctamente**
: Usar un User-Agent descriptivo que permita al administrador del sitio contactarte.

**Uso responsable de los datos**
: No usar los datos scrapeados para propósitos no éticos o ilegales.

### Web Scraping Manual con Python

Python ofrece excelentes bibliotecas para web scraping. Las más populares son `requests` para realizar solicitudes HTTP y `BeautifulSoup` para parsear HTML.

#### Instalación de Bibliotecas

```bash
pip install requests beautifulsoup4 lxml
```

#### Ejemplo Básico: Extraer Información de una Página

```{code-cell} python
import requests
from bs4 import BeautifulSoup

# Obtener una página web
url = 'https://quotes.toscrape.com/'
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar todas las citas
    citas = soup.find_all('div', class_='quote')
    
    print(f"Se encontraron {len(citas)} citas:\n")
    
    for cita in citas[:3]:  # Mostrar solo las primeras 3
        texto = cita.find('span', class_='text').get_text()
        autor = cita.find('small', class_='author').get_text()
        
        # Tags
        tags = cita.find_all('a', class_='tag')
        tags_texto = [tag.get_text() for tag in tags]
        
        print(f"Cita: {texto}")
        print(f"Autor: {autor}")
        print(f"Tags: {', '.join(tags_texto)}")
        print("-" * 60)
else:
    print(f"Error al acceder a la página: {response.status_code}")
```

#### Selectores CSS

BeautifulSoup también permite usar selectores CSS, que son muy potentes y flexibles:

```{code-cell} python
import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Usar selectores CSS
# Seleccionar todas las citas usando select()
citas = soup.select('div.quote')

print(f"Total de citas encontradas: {len(citas)}\n")

# Seleccionar elementos específicos dentro de cada cita
for cita in citas[:2]:
    # El texto de la cita
    texto = cita.select_one('span.text').get_text()
    
    # El autor
    autor = cita.select_one('small.author').get_text()
    
    # Todos los tags
    tags = [tag.get_text() for tag in cita.select('a.tag')]
    
    print(f"'{texto}'")
    print(f"  — {autor}")
    print(f"  Tags: {', '.join(tags)}\n")
```

#### Navegación y Extracción de Enlaces

```{code-cell} python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todos los enlaces
enlaces = soup.find_all('a')

print("Algunos enlaces encontrados:\n")

enlaces_unicos = set()
for enlace in enlaces[:10]:
    href = enlace.get('href')
    texto = enlace.get_text().strip()
    
    if href:
        # Convertir enlaces relativos a absolutos
        url_completa = urljoin(url, href)
        
        if url_completa not in enlaces_unicos:
            enlaces_unicos.add(url_completa)
            print(f"{texto:30} -> {url_completa}")
```

#### Manejo de Tablas HTML

```{code-cell} python
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Ejemplo con una tabla HTML simple
html_tabla = """
<table>
    <tr>
        <th>País</th>
        <th>Capital</th>
        <th>Población (millones)</th>
    </tr>
    <tr>
        <td>Argentina</td>
        <td>Buenos Aires</td>
        <td>45.4</td>
    </tr>
    <tr>
        <td>Brasil</td>
        <td>Brasilia</td>
        <td>214.3</td>
    </tr>
    <tr>
        <td>Chile</td>
        <td>Santiago</td>
        <td>19.5</td>
    </tr>
</table>
"""

soup = BeautifulSoup(html_tabla, 'html.parser')
tabla = soup.find('table')

# Extraer encabezados
encabezados = [th.get_text() for th in tabla.find_all('th')]

# Extraer filas
filas = []
for tr in tabla.find_all('tr')[1:]:  # Saltar la fila de encabezados
    fila = [td.get_text() for td in tr.find_all('td')]
    filas.append(fila)

# Crear DataFrame
df = pd.DataFrame(filas, columns=encabezados)
print(df)
```

#### Manejo de Errores y Timeouts

```{code-cell} python
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, HTTPError

def scrape_con_manejo_errores(url, timeout=10):
    """
    Realiza web scraping con manejo robusto de errores.
    
    Args:
        url: URL a scrapear
        timeout: Tiempo máximo de espera en segundos
    """
    try:
        # Realizar la solicitud con timeout
        response = requests.get(url, timeout=timeout)
        
        # Verificar el código de estado
        response.raise_for_status()
        
        # Parsear el contenido
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return soup
        
    except Timeout:
        print(f"Error: Tiempo de espera agotado para {url}")
    except HTTPError as e:
        print(f"Error HTTP {e.response.status_code}: {url}")
    except RequestException as e:
        print(f"Error en la solicitud: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    return None

# Ejemplo de uso
soup = scrape_con_manejo_errores('https://quotes.toscrape.com/')
if soup:
    titulo = soup.find('title')
    print(f"Título de la página: {titulo.get_text() if titulo else 'No encontrado'}")
```

### Web Scraping con Scrapy

Scrapy es un framework de Python para web scraping a gran escala. Proporciona funcionalidades avanzadas como:

- Gestión automática de solicitudes concurrentes
- Manejo de robots.txt
- Extracción de datos con selectores CSS y XPath
- Exportación a múltiples formatos (JSON, CSV, XML)
- Middleware para personalizar el comportamiento

#### Instalación de Scrapy

```bash
pip install scrapy
```

#### Anatomía de una Spider de Scrapy

Una spider es una clase que define cómo scrapear un sitio:

```{code-cell} python
# Este código es ilustrativo de cómo se vería una spider de Scrapy
# En la práctica, se ejecuta desde la línea de comandos

ejemplo_spider = """
import scrapy

class CitasSpider(scrapy.Spider):
    name = 'citas'
    start_urls = ['https://quotes.toscrape.com/']
    
    # Configuración para ser respetuoso
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Esperar 1 segundo entre solicitudes
        'ROBOTSTXT_OBEY': True,  # Respetar robots.txt
        'USER_AGENT': 'MiScraper/1.0 (contacto@ejemplo.com)'
    }
    
    def parse(self, response):
        # Extraer todas las citas de la página
        for cita in response.css('div.quote'):
            yield {
                'texto': cita.css('span.text::text').get(),
                'autor': cita.css('small.author::text').get(),
                'tags': cita.css('a.tag::text').getall(),
            }
        
        # Seguir al siguiente enlace de paginación
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
"""

print("Ejemplo de Spider de Scrapy:")
print(ejemplo_spider)
```

#### Crear un Proyecto Scrapy

```{code-cell} python
# Comandos para crear y ejecutar un proyecto Scrapy
comandos_scrapy = """
# 1. Crear un nuevo proyecto
scrapy startproject mi_proyecto

# 2. Navegar al directorio del proyecto
cd mi_proyecto

# 3. Crear una nueva spider
scrapy genspider nombre_spider dominio.com

# 4. Ejecutar la spider
scrapy crawl nombre_spider

# 5. Exportar a JSON
scrapy crawl nombre_spider -o resultados.json

# 6. Exportar a CSV
scrapy crawl nombre_spider -o resultados.csv
"""

print("Comandos básicos de Scrapy:")
print(comandos_scrapy)
```

#### Ejemplo Completo: Spider para Extraer Noticias

```{code-cell} python
# Ejemplo ilustrativo de una spider más completa
ejemplo_spider_noticias = """
import scrapy
from datetime import datetime

class NoticiasSpider(scrapy.Spider):
    name = 'noticias'
    allowed_domains = ['example-news.com']
    start_urls = ['https://example-news.com/']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'NewsBot/1.0 (contacto@ejemplo.com)'
    }
    
    def parse(self, response):
        # Extraer enlaces a artículos
        articulos = response.css('article.noticia')
        
        for articulo in articulos:
            enlace = articulo.css('a.titulo::attr(href)').get()
            
            if enlace:
                # Seguir cada enlace y parsear el artículo completo
                yield response.follow(enlace, self.parse_articulo)
        
        # Paginación
        siguiente = response.css('a.siguiente::attr(href)').get()
        if siguiente:
            yield response.follow(siguiente, self.parse)
    
    def parse_articulo(self, response):
        # Extraer información del artículo
        yield {
            'url': response.url,
            'titulo': response.css('h1.titulo::text').get(),
            'fecha': response.css('time::attr(datetime)').get(),
            'autor': response.css('span.autor::text').get(),
            'categoria': response.css('span.categoria::text').get(),
            'contenido': ' '.join(response.css('div.contenido p::text').getall()),
            'tags': response.css('a.tag::text').getall(),
            'scrapeado_en': datetime.now().isoformat(),
        }
"""

print("Ejemplo de Spider para extraer noticias:")
print(ejemplo_spider_noticias)
```

#### Selectores XPath vs CSS en Scrapy

Scrapy soporta tanto selectores CSS como XPath:

```{code-cell} python
comparacion_selectores = """
# Selectores CSS
response.css('div.quote span.text::text').get()
response.css('a::attr(href)').getall()
response.css('div.quote').getall()

# Selectores XPath (más potentes pero más complejos)
response.xpath('//div[@class="quote"]/span[@class="text"]/text()').get()
response.xpath('//a/@href').getall()
response.xpath('//div[@class="quote"]').getall()

# XPath permite operaciones más complejas:
# Seleccionar elementos que contienen cierto texto
response.xpath('//div[contains(@class, "quote")]')

# Seleccionar el elemento padre
response.xpath('//span[@class="text"]/parent::div')

# Condiciones complejas
response.xpath('//div[@class="quote" and @id="primera"]')
"""

print("Comparación de selectores en Scrapy:")
print(comparacion_selectores)
```

#### Middleware y Pipelines en Scrapy

**Middleware**
: Componentes que procesan requests y responses.

**Pipelines**
: Procesan los items extraídos (limpieza, validación, almacenamiento).

```{code-cell} python
ejemplo_pipeline = """
# pipelines.py - Procesar items scrapeados

class LimpiezaPipeline:
    def process_item(self, item, spider):
        # Limpiar espacios en blanco
        if 'texto' in item:
            item['texto'] = item['texto'].strip()
        
        if 'autor' in item:
            item['autor'] = item['autor'].strip()
        
        return item

class ValidacionPipeline:
    def process_item(self, item, spider):
        # Validar que los campos requeridos estén presentes
        campos_requeridos = ['texto', 'autor']
        
        for campo in campos_requeridos:
            if campo not in item or not item[campo]:
                raise DropItem(f'Falta campo requerido: {campo}')
        
        return item

class AlmacenamientoPipeline:
    def open_spider(self, spider):
        self.archivo = open('resultados.json', 'w', encoding='utf-8')
        self.archivo.write('[\\n')
    
    def close_spider(self, spider):
        self.archivo.write('\\n]')
        self.archivo.close()
    
    def process_item(self, item, spider):
        import json
        linea = json.dumps(dict(item), ensure_ascii=False, indent=2)
        self.archivo.write(linea + ',\\n')
        return item

# En settings.py, activar los pipelines:
ITEM_PIPELINES = {
    'mi_proyecto.pipelines.LimpiezaPipeline': 100,
    'mi_proyecto.pipelines.ValidacionPipeline': 200,
    'mi_proyecto.pipelines.AlmacenamientoPipeline': 300,
}
"""

print("Ejemplo de Pipelines en Scrapy:")
print(ejemplo_pipeline)
```

### Scraping de Sitios Dinámicos (JavaScript)

Muchos sitios web modernos generan contenido dinámicamente con JavaScript. Para estos casos, herramientas como `requests` y `BeautifulSoup` no son suficientes porque solo obtienen el HTML inicial. Se necesitan herramientas que ejecuten JavaScript:

#### Selenium

```{code-cell} python
ejemplo_selenium = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar el driver (Chrome, Firefox, etc.)
driver = webdriver.Chrome()

try:
    # Navegar a la página
    driver.get('https://ejemplo-dinamico.com')
    
    # Esperar a que un elemento específico esté presente
    wait = WebDriverWait(driver, 10)
    elemento = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'contenido-dinamico'))
    )
    
    # Interactuar con la página
    boton = driver.find_element(By.ID, 'cargar-mas')
    boton.click()
    
    # Extraer datos
    items = driver.find_elements(By.CLASS_NAME, 'item')
    
    for item in items:
        titulo = item.find_element(By.TAG_NAME, 'h2').text
        descripcion = item.find_element(By.CLASS_NAME, 'descripcion').text
        print(f'{titulo}: {descripcion}')

finally:
    driver.quit()
"""

print("Ejemplo de Selenium para sitios dinámicos:")
print(ejemplo_selenium)
```

#### Playwright

Una alternativa moderna a Selenium:

```{code-cell} python
ejemplo_playwright = """
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Lanzar navegador
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Navegar a la página
    page.goto('https://ejemplo-dinamico.com')
    
    # Esperar a que el contenido se cargue
    page.wait_for_selector('.contenido-dinamico')
    
    # Hacer clic en un botón
    page.click('#cargar-mas')
    
    # Extraer datos
    items = page.query_selector_all('.item')
    
    for item in items:
        titulo = item.query_selector('h2').inner_text()
        descripcion = item.query_selector('.descripcion').inner_text()
        print(f'{titulo}: {descripcion}')
    
    browser.close()
"""

print("Ejemplo de Playwright para sitios dinámicos:")
print(ejemplo_playwright)
```

### Caso Práctico: Scraping Completo

Veamos un ejemplo completo que integra varios conceptos:

```{code-cell} python
import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urljoin

def verificar_robots_txt(base_url):
    """Verifica si el scraping está permitido según robots.txt"""
    robots_url = urljoin(base_url, '/robots.txt')
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            print(f"Robots.txt encontrado. Revisa las reglas antes de continuar.")
            print(response.text[:200] + "...")
            return True
    except:
        print("No se pudo acceder a robots.txt")
    return False

def scrape_quotes_con_paginacion(max_paginas=2):
    """
    Scrapea citas con paginación de manera ética y estructurada.
    """
    base_url = 'https://quotes.toscrape.com'
    
    # Verificar robots.txt
    verificar_robots_txt(base_url)
    
    todas_las_citas = []
    pagina_actual = 1
    
    while pagina_actual <= max_paginas:
        url = f'{base_url}/page/{pagina_actual}/'
        
        print(f"\nScrapeando página {pagina_actual}: {url}")
        
        try:
            # Headers para identificarnos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Educational Bot; contact@ejemplo.com)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer citas
            citas = soup.find_all('div', class_='quote')
            
            if not citas:
                print("No se encontraron más citas. Finalizando.")
                break
            
            for cita in citas:
                datos_cita = {
                    'texto': cita.find('span', class_='text').get_text(),
                    'autor': cita.find('small', class_='author').get_text(),
                    'tags': [tag.get_text() for tag in cita.find_all('a', class_='tag')],
                    'pagina': pagina_actual
                }
                todas_las_citas.append(datos_cita)
            
            print(f"  Extraídas {len(citas)} citas")
            
            # Respetar el servidor: esperar entre solicitudes
            time.sleep(1)
            
            pagina_actual += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            break
    
    return todas_las_citas

# Ejecutar el scraping
print("Iniciando scraping ético y estructurado...")
citas = scrape_quotes_con_paginacion(max_paginas=2)

print(f"\n{'='*60}")
print(f"Total de citas extraídas: {len(citas)}")
print(f"{'='*60}\n")

# Mostrar algunas estadísticas
if citas:
    print("Primeras 2 citas:")
    for i, cita in enumerate(citas[:2], 1):
        print(f"\n{i}. {cita['texto']}")
        print(f"   — {cita['autor']}")
        print(f"   Tags: {', '.join(cita['tags'])}")
```

## Comparación de Enfoques

```{list-table}
---
header-rows: 1
---
* - Aspecto
  - APIs
  - Web Scraping
* - Acceso a datos
  - Estructurado y oficial
  - No estructurado, extraído del HTML
* - Estabilidad
  - Alta (con versionado)
  - Baja (cambios en el HTML rompen el código)
* - Legalidad
  - Generalmente legal con términos claros
  - Zona gris, depende del sitio
* - Límites de velocidad
  - Explícitos y documentados
  - Implícitos, basados en el comportamiento del servidor
* - Facilidad de uso
  - Diseñado para ser consumido
  - Requiere ingeniería inversa del HTML
* - Cobertura de datos
  - Solo lo que la API expone
  - Potencialmente todo lo visible en el sitio
* - Mantenimiento
  - Bajo (cambios notificados)
  - Alto (cambios no notificados)
```

## Recomendaciones y Mejores Prácticas

### Para APIs

1. **Leer la documentación**: Entender límites de velocidad, autenticación y términos de uso
2. **Manejar errores**: Implementar reintentos con backoff exponencial
3. **Cachear respuestas**: Evitar solicitudes repetidas
4. **Monitorear cuotas**: Estar atento a los límites de uso
5. **Versionar**: Usar versiones específicas de APIs para evitar cambios inesperados

### Para Web Scraping

1. **Verificar legalidad**: Revisar términos de servicio y robots.txt
2. **Identificarse**: Usar un User-Agent descriptivo
3. **Ser respetuoso**: Limitar la frecuencia de solicitudes
4. **Manejar errores**: Anticipar cambios en la estructura del sitio
5. **Considerar alternativas**: Preferir APIs cuando estén disponibles
6. **Mantener el código**: Los sitios cambian, el scraper debe actualizarse

### Consideraciones de Rendimiento

```{code-cell} python
import requests
from concurrent.futures import ThreadPoolExecutor
import time

def scraping_secuencial(urls):
    """Scraping tradicional, una URL a la vez"""
    inicio = time.time()
    resultados = []
    
    for url in urls:
        response = requests.get(url)
        resultados.append(len(response.content))
    
    duracion = time.time() - inicio
    return resultados, duracion

def scraping_concurrente(urls, max_workers=5):
    """Scraping concurrente usando ThreadPoolExecutor"""
    inicio = time.time()
    
    def fetch(url):
        response = requests.get(url)
        return len(response.content)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        resultados = list(executor.map(fetch, urls))
    
    duracion = time.time() - inicio
    return resultados, duracion

# Ejemplo conceptual (no ejecutar en producción sin limitaciones)
urls_ejemplo = [f'https://httpbin.org/delay/1' for _ in range(3)]

print("Comparación de enfoques de scraping:")
print("\nSecuencial:")
print("  - Ventajas: Simple, fácil de controlar")
print("  - Desventajas: Lento para muchas URLs")
print("\nConcurrente:")
print("  - Ventajas: Mucho más rápido")
print("  - Desventajas: Puede sobrecargar el servidor si no se controla")
```

## Herramientas y Bibliotecas Adicionales

### Parseo y Análisis

- **lxml**: Parser XML/HTML muy rápido
- **html5lib**: Parser que simula el comportamiento de navegadores
- **parsel**: Librería de extracción usada por Scrapy

### Automatización de Navegadores

- **Selenium**: Control de navegadores web para automatización
- **Playwright**: Alternativa moderna a Selenium
- **Puppeteer**: Control de Chrome/Chromium (Node.js)

### Gestión de Solicitudes

- **httpx**: Cliente HTTP asíncrono moderno
- **aiohttp**: Cliente HTTP asíncrono
- **requests-html**: Requests con soporte para JavaScript

### Almacenamiento y Procesamiento

- **pandas**: Análisis y manipulación de datos
- **SQLAlchemy**: ORM para bases de datos
- **MongoDB**: Base de datos NoSQL para datos no estructurados

## Referencias y Recursos Adicionales

### Documentación Oficial

- [Requests Documentation](https://requests.readthedocs.io/){target="_blank"}
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/){target="_blank"}
- [Scrapy Documentation](https://docs.scrapy.org/){target="_blank"}
- [GraphQL Documentation](https://graphql.org/learn/){target="_blank"}

### Libros y Referencias Académicas

- Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, *Introduction to Information Retrieval*, Cambridge University Press, 2008. Capítulos 19 y 20.
- Ryan Mitchell, *Web Scraping with Python*, 2nd Edition, O'Reilly Media, 2018.

### APIs Públicas para Practicar

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/){target="_blank"} - API REST falsa para testing
- [REST Countries](https://restcountries.com/){target="_blank"} - Información sobre países
- [OpenWeatherMap](https://openweathermap.org/api){target="_blank"} - Datos meteorológicos
- [The Star Wars API](https://swapi.dev/){target="_blank"} - Datos de Star Wars
- [PokéAPI](https://pokeapi.co/){target="_blank"} - Información sobre Pokémon

### Sitios para Practicar Web Scraping

- [Quotes to Scrape](https://quotes.toscrape.com/){target="_blank"} - Sitio diseñado para practicar scraping
- [Books to Scrape](https://books.toscrape.com/){target="_blank"} - Tienda de libros ficticia para scraping
- [Scrape This Site](https://www.scrapethissite.com/){target="_blank"} - Ejercicios de scraping

### Recursos en Español

- [Tutorial de Requests en Español](https://docs.python-requests.org/es/latest/){target="_blank"}
- [Comunidad Python Argentina](https://python.org.ar/){target="_blank"}

### Aspectos Legales

- [Can I scrape your website?](https://blog.apify.com/is-web-scraping-legal/){target="_blank"}
- [Understanding robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro){target="_blank"}
