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
description: La web como fuente de información, APIs,
---

# La Web y las APIs

La Web es una de las fuentes de información más grandes y diversas disponibles en la actualidad. Contiene datos estructurados, semiestructurados y no estructurados que pueden ser aprovechados para múltiples propósitos: análisis de datos, investigación, monitoreo de precios, agregación de noticias, entre otros. En este capítulo exploraremos el funcionamiento de la Web y cómo acceder a información a través de APIs.

## Introducción al Funcionamiento de la Web

### Arquitectura Cliente-Servidor

La World Wide Web funciona bajo un modelo cliente-servidor. El siguiente diagrama ilustra cómo interactúan estos componentes:

```{figure} ../_static/figures/arquitectura_cliente_servidor_light.svg
---
class: only-light-mode
---
Arquitectura Cliente-Servidor
```

```{figure} ../_static/figures/arquitectura_cliente_servidor_dark.svg
---
class: only-dark-mode
---
Arquitectura Cliente-Servidor
```

Los componentes principales son:

**Cliente (Navegador)**
: Programa que solicita recursos web (páginas HTML, imágenes, videos, etc.). Los navegadores más comunes son Chrome, Firefox, Safari y Edge.

**Servidor Web**
: Aplicación que responde a las solicitudes de los clientes, enviando los recursos solicitados. Ejemplos incluyen Apache, Nginx, y servidores de aplicaciones como Node.js o Python con frameworks como Django o FastAPI.

**DNS (Domain Name System)**
: Sistema que traduce nombres de dominio legibles (como `www.untref.edu.ar`) a direcciones IP numéricas que los computadores pueden entender.

En primer lugar el cliente o browser realiza una consulta DNS para obtener la dirección IP del servidor web asociado al dominio. Luego, el cliente envía una solicitud HTTP al servidor, que procesa la solicitud y devuelve una respuesta con el recurso solicitado.

Hoy en día a través de la web no solo se puede obtener páginas HTML, sino también se pueden ejecutar aplicaciones web completas, donde el servidor puede enviar datos y código (generalmente JavaScript) que se ejecuta en el navegador del cliente, permitiendo interfaces interactivas y dinámicas.

### El Protocolo HTTP

HTTP (*HyperText Transfer Protocol*) es el protocolo de comunicación que permite la transferencia de información en la Web. Define cómo los clientes y servidores intercambian mensajes.

HTTP fue diseñado para ser simple y flexible, permitiendo la transferencia de diferentes tipos de datos (HTML, JSON, imágenes, etc.) a través de una estructura de mensajes estándar.

El protocolo HTTP sigue un modelo de solicitud-respuesta (*request-response*), donde el cliente envía una solicitud al servidor y este responde con el recurso solicitado o un mensaje de error.

En el siguiente diagrama de secuencia se muestra una interacción típica entre un cliente y un servidor utilizando HTTP:

```{figure} ../_static/figures/secuencia_http_light.svg
---
class: only-light-mode
---
Interacción HTTP Cliente-Servidor
```

```{figure} ../_static/figures/secuencia_http_dark.svg
---
class: only-dark-mode
---
Interacción HTTP Cliente-Servidor
```

**Petición enviada:**

```text
GET /contact HTTP/1.1
Host: example.com
User-Agent: curl/8.6.0
Accept: */*
```

La petición HTTP consta de varias líneas, donde la primera línea indica el método HTTP (`GET`), el recurso solicitado (`/contact`) y la versión del protocolo (`HTTP/1.1`). Las líneas siguientes son las cabeceras (*headers*) que proporcionan información adicional sobre la solicitud. En este caso, se especifica el host, el agente de usuario (navegador) y los tipos de contenido aceptados.

**Respuesta recibida:**

```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Date: Fri, 21 Jun 2024 14:18:33 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Content-Length: 1234

<!doctype html>
<!-- HTML content follows -->
```

La respuesta HTTP también consta de varias líneas, donde la primera línea indica el protocolo que usa el servidor y el código de estado (`200 OK`), seguido de las cabeceras de respuesta y finalmente el cuerpo del mensaje que contiene el HTML de la página.

#### Características de HTTP

Sin estado (stateless)
: Cada solicitud es independiente, el servidor no mantiene información sobre solicitudes anteriores (algunos servidores implementan algunos mecanismos para manejar sesiones, pero esto no es parte del protocolo HTTP en sí).

Basado en texto
: Los mensajes son legibles por humanos

Extensible
: Permite agregar nuevos métodos y cabeceras

Cliente-Servidor
: Modelo de comunicación request-response

#### Métodos HTTP Principales

Los métodos HTTP definen las peticiones que se puede solicitar al servidor sobre un recurso específico:

`GET`
: Solicita un recurso específico. Es el método más común para solicitar un recurso al servidor. Si no se especifica un recurso en particular, el servidor generalmente devuelve la página principal, normalmente `index.html`.

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

En Python, la biblioteca `requests` facilita la realización de solicitudes HTTP. Aquí hay un ejemplo básico de cómo hacer una solicitud GET:

```{code-cell} python
---
tags: hide-output
---
import requests

try:
    # Realizar una solicitud GET
    response = requests.get("https://untref.edu.ar/", timeout=30)

    print(f"Código de estado: {response.status_code}")
    for k, v in response.headers.items():
        print(f"{k}: {v}")
    print(f"\nPrimeros 200 caracteres del contenido (página html):")
    print(f"{response.text[:200]}")
except requests.exceptions.RequestException as e:
    print(f"No se pudo conectar a untref.edu.ar: {e}")
```

El intercambio entre cliente y servidor puede verse en *"crudo"* utilizando herramientas como `curl` en la línea de comandos. Aquí hay un ejemplo de cómo se vería una solicitud y respuesta HTTP:

```bash
curl -v https://untref.edu.ar/
```

```{note} Nota
cURL es una herramienta de línea de comandos, gratuita y de código abierto, para transferir datos usando diversas URLs y protocolos, comúnmente utilizada para interactuar con APIs, descargar archivos y probar recursos web. Es compatible con una amplia gama de protocolos como HTTP, HTTPS, FTP y SMB. cURL está disponible de forma nativa en sistemas operativos basados en Unix, incluyendo Linux y macOS, y está preinstalado en las versiones modernas de Windows.
```

**Petición enviada:**

```text
GET / HTTP/1.1
Host: www.untref.edu.ar
User-Agent: curl/8.12.1
Accept: */*
```

**Respuesta recibida:**

```text
HTTP/1.1 200 OK
Date: Mon, 06 Oct 2025 15:06:59 GMT
Server: Apache
Cache-Control: no-cache
Set-Cookie: XSRF-TOKEN=eyJpdiI6IkhZbnpaYmpEV0ZaM1ZaRVwvYUQzbDZRPT0iLCJ2YWx1ZSI6ImtcL240ZFRjS1BhYWZmZWNcL0t3a1FtNFwvVWRhY0Q5Wm5qakF4M09UekM0T3hvbW0zb2FDTkZ3ZGxPTExQUGpCNXY1WUZvRW1oODhrQ2pEWlV4OCtkT3RnPT0iLCJtYWMiOiIzZjM3OTcyYTU4YmVlZmZmNGVhODIwOWI1Y2U5MWQ2YjNkZjBiMmFhZGQ3MjU2OWYzZTExYTQzZTA4NDVlY2JhIn0%3D; expires=Mon, 06-Oct-2025 17:07:00 GMT; Max-Age=7200; path=/
Set-Cookie: laravel_session=eyJpdiI6IkxIeHIyRElDdm82bFV1WDdrRTRickE9PSIsInZhbHVlIjoiYTRMZklQZDk2RTgwMjdLMXlFQ2ltVjJoWjhsdzB1a2ZhSmVYYlo1amc4a1FwYU9EQUQrWUo2b2QweEVxQThPcTJnWTlTbklMMkNUYjdJVUtGYWsyOXc9PSIsIm1hYyI6ImExOTNmMGNhN2NjMGJlN2I2ZDAwZTIwNWMyMDg2ZTU3NTdlNjYwNTRmYTc4NTYyODU4NjBmMTI0YWQ4Y2JhNWYifQ%3D%3D; expires=Mon, 06-Oct-2025 17:07:00 GMT; Max-Age=7200; path=/; HttpOnly
Transfer-Encoding: chunked
Content-Type: text/html; charset=UTF-8
<!DOCTYPE html>
<html lang="es">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <title>UNTREF</title>
...

```

### HTTPS: HTTP Seguro

HTTPS (HTTP Secure) es la versión segura de HTTP que utiliza encriptación TLS/SSL para proteger la comunicación entre cliente y servidor. Es fundamental para:

- Proteger datos sensibles (contraseñas, información financiera)
- Verificar la identidad del servidor
- Prevenir ataques de intermediarios (man-in-the-middle)
- Mejorar el posicionamiento en motores de búsqueda

## APIs: Interfaces de Programación de Aplicaciones

Las APIs (*Application Programming Interfaces*) son interfaces que permiten que diferentes aplicaciones se comuniquen entre sí de manera programática. En el contexto web, las APIs proporcionan puntos de acceso (*endpoints*) que los desarrolladores pueden usar para acceder a datos y funcionalidades de un servicio.

```{figure} ../_static/figures/arquitectura_api_light.svg
---
class: only-light-mode
---
Arquitectura de una API REST
```

```{figure} ../_static/figures/arquitectura_api_dark.svg
---
class: only-dark-mode
---
Arquitectura de una API REST
```

Una aplicación cliente (por ejemplo una aplicación web o móvil) realiza solicitudes HTTP a una API REST, que procesa la solicitud, interactúa con bases de datos u otros servicios, y devuelve los datos en formatos como JSON o XML.

El protocolo base es HTTP, y los recursos se acceden a través de URLs específicas. Por ejemplo una URL típica de una API REST podría ser:

```html
https://api.ejemplo.com/v1/usuarios/123
```

Donde:

- `https://api.ejemplo.com` es el dominio de la API. Es decir el servidor donde está alojada la API.
- `/v1` indica la versión de la API. Un servidor puede tener múltiples versiones de una API para mantener compatibilidad con clientes antiguos.
- `/usuarios/123` es el recurso específico (usuario con ID 123).

Ante esta solicitud, la API podría devolver un JSON con los datos del usuario:

```json
{
  "id": 123,
  "nombre": "Juan Pérez",
  "email": "juan.perez@ejemplo.com"
}
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

Vamos a consumir una API pública para consultar resultados electorales de Argentina, disponible en [https://resultados.mininterior.gob.ar](https://resultados.mininterior.gob.ar).

```{code-cell} python
---
tags: hide-output
---
import requests
import json

try:
    # Realizar una solicitud GET a la API del Ministerio del Interior
    response = requests.get(
        "https://resultados.mininterior.gob.ar/api/resultados/getResultados?"
        "anioEleccion=2019&tipoRecuento=1&tipoEleccion=2&categoriaId=1&"
        "distritoId=2&seccionProvincialId=1&seccionId=118",
        timeout=30
    )
    if response.status_code == 200:
        datos = response.json()
        print(json.dumps(datos, indent=2, ensure_ascii=False))
    else:
        print(f"Error al acceder a la API: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except requests.exceptions.RequestException as e:
    print(f"No se pudo conectar a resultados.mininterior.gob.ar: {e}")
```

En la solicitud anterior, se puede ver que se utilizan varios parámetros en la URL para especificar los datos que se quieren consultar

| Parámetro               | Valor | Significado                    |
| ----------------------- | ----- | ------------------------------ |
| `anioEleccion=2019`     | 2019  | Año de la elección consultada. |
| `tipoRecuento=1`        | 1     | 1 = Recuento Provisional       |
| `tipoEleccion=2`        | 2     | 2 = Elecciones Generales       |
| `categoriaId=1`         | 1     | 1 = Presidente de la Nación.   |
| `distritoId=2`          | 2     | 2 = Provincia de Buenos Aires. |
| `seccionProvincialId=1` | 1     | 1 = Primera Sección Electoral. |
| `seccionId=118`         | 118   | 118 = Tres de Febrero.         |

La documentación de la API se puede [descargar](https://www.argentina.gob.ar/sites/default/files/2017/08/api-publicacion-resultados-electorales.zip) desde el sitio oficial del Ministerio del Interior.

La respuesta de la API es un JSON con los resultados detallados para Tres de Febrero.

#### Ejemplo: API de Información Geográfica

Muchas APIs REST proporcionan datos estructurados útiles. Vamos a consultar OpenStreetMap (OSM) que ofrece datos geográficos.

```{note} Nota
 [OpenStreetMap](https://www.openstreetmap.org/about) es un proyecto colaborativo para crear un mapa libre y editable del mundo. Los datos son aportados por voluntarios y están disponibles bajo la licencia [Open Database License (ODbL)](https://es.wikipedia.org/wiki/Licencia_Abierta_de_Bases_de_Datos).
```

```{code-cell} python
---
tags: hide-output
---
import requests
from lxml import etree as ET

try:
    # Realizar una solicitud GET a la API de Open Maps
    # Way Id = 1275831310 (Sede Caseros I de la UNTREF)
    response = requests.get(
        "https://api.openstreetmap.org/api/0.6/way/1275831310", timeout=30
    )
    if response.status_code == 200:
        # Parsear la respuesta XML
        root = ET.fromstring(response.content)
        # Recorrer el XML de OpenStreetMap

        # Buscar el elemento <way>
        way = root.find("way")
        if way is not None:
            print(f"ID del way: {way.get('id')}")
            print("Etiquetas asociadas:")
            for tag in way.findall("tag"):
                clave = tag.get("k")
                valor = tag.get("v")
                print(f"  {clave}: {valor}")
        else:
            print("No se encontró el elemento <way> en la respuesta.")
    else:
        print(f"Error al acceder a la API: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"No se pudo conectar a api.openstreetmap.org: {e}")
```

La documentación de la API de OpenStreetMap está disponible en [https://wiki.openstreetmap.org/wiki/API_v0.6](https://wiki.openstreetmap.org/wiki/API_v0.6).

Con el way ID `1275831310` también se puede obtener el mapa correspondiente a través del servicio Overpass API, que permite consultas más complejas. Aquí hay un ejemplo de cómo obtener la geometría del way en formato GeoJSON y visualizarlo en un mapa interactivo usando la librería `folium`:

```python
import requests
import folium


def obtener_geojson_way(osm_way_id):
    # Consulta Overpass para el way específico
    url = "https://overpass-api.de/api/interpreter"
    # Query Overpass: way + nodos + metadata
    query = f"""
    [out:json];
    way({osm_way_id});
    out body;
    >;
    out meta;
    """
    response = requests.get(url, params={"data": query}, timeout=30)
    response.raise_for_status()
    return response.json()


def construir_mapa(geojson_data):
    # Extraer nodos del way y sus coordenadas
    # Overpass pone los nodos como elementos tipo "node" en el array "elements"
    nodes = {}
    for el in geojson_data.get("elements", []):
        if el["type"] == "node":
            nodes[el["id"]] = (el["lat"], el["lon"])
    # Construir lista ordenada de coordenadas del way
    coords = []
    for el in geojson_data.get("elements", []):
        if el["type"] == "way":
            for nid in el["nodes"]:
                if nid in nodes:
                    coords.append(nodes[nid])
    # Centrar el mapa en la primera coordenada
    if not coords:
        raise RuntimeError("No se hallaron coordenadas del way")
    centro = coords[0]
    mapa = folium.Map(location=centro, zoom_start=18)
    # Añadir polígono (o línea) al mapa
    folium.PolyLine(locations=coords, color="blue", weight=3).add_to(mapa)
    # También podrías usar folium.Polygon si es cerrado
    return mapa
    # Visualizar el mapa en el notebook


def main():
    osm_way_id = 1275831310  # el way de la Sede Caseros I
    try:
        geojson = obtener_geojson_way(osm_way_id)
        mapa = construir_mapa(geojson)
        # Mostrar el mapa en el notebook
        display(mapa)
    except requests.exceptions.RequestException as e:
        print(f"No se pudo obtener datos de Overpass API: {e}")
    except RuntimeError as e:
        print(f"Error al construir el mapa: {e}")


if __name__ == "__main__":
    main()
```

El fragmento de código anterior realiza los siguientes pasos:

1. Extraer coordenadas de los nodos que forman el "way" desde un objeto GeoJSON.
2. Centrar el mapa en la primera coordenada encontrada.
3. Dibujar la línea (o polígono) sobre el mapa usando folium.PolyLine.
4. Mostrar el mapa en un entorno interactivo (como Jupyter Notebook) usando display(mapa).

La función principal (main) obtiene el GeoJSON de un "way" específico, en este caso la Sede Caseros I, construye el mapa y lo muestra.

overpass-api.de es un servicio web que permite consultar y extraer datos de OpenStreetMap mediante un lenguaje de consultas específico (Overpass QL). Se usa para obtener información geográfica detallada, como nodos, caminos y relaciones, de la base de datos de OSM.

```{note} Nota
[GeoJSON](https://es.wikipedia.org/wiki/GeoJSON) es un formato basado en JSON para representar datos geográficos. Define varias estructuras como Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon y GeometryCollection para describir diferentes tipos de geometrías espaciales.
```

Los servicios que ofrece OpenStreetMap se pueden consultar en su [wiki](https://wiki.openstreetmap.org/wiki/Main_Page).

#### Autenticación en APIs REST

Las APIs frecuentemente requieren autenticación, sobre todo cuando se trata de servicios **privados**. Los métodos más comunes son:

API Keys
: Una clave secreta que se envía en la URL o en las cabeceras.

OAuth 2.0
: Protocolo de autorización más complejo pero seguro, usado por servicios como Google, Facebook, Twitter.

Bearer Tokens
: Tokens de acceso que se envían en el header de autorización.

En general, antes de poder consultar una API, es necesario registrarse y obtener las credenciales necesarias.

## Mejores Prácticas para Usar APIs

1. **Leer la documentación**: Entender límites de velocidad, autenticación y términos de uso
2. **Manejar errores**: Implementar reintentos con backoff exponencial
3. **Cachear respuestas**: Evitar solicitudes repetidas
4. **Monitorear cuotas**: Estar atento a los límites de uso
5. **Versionar**: Usar versiones específicas de APIs para evitar cambios inesperados

## Referencias y Recursos Adicionales

### Documentación Oficial

- [Requests Documentation](https://requests.readthedocs.io/)
- [HTTP Documentation (MDN)](https://developer.mozilla.org/es/docs/Web/HTTP)
- [REST API Tutorial](https://restfulapi.net/)

### APIs Públicas para Practicar

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - API REST falsa para testing
- [REST Countries](https://restcountries.com/) - Información sobre países
- [OpenWeatherMap](https://openweathermap.org/api) - Datos meteorológicos
- [The Star Wars API](https://swapi.dev/) - Datos de Star Wars
- [PokéAPI](https://pokeapi.co/) - Información sobre Pokémon

### Libros y Referencias Académicas

- En el capítulo 19: Web Search Basics del libro {cite:p}`irbook` se presenta la estructura de la Web y los protocolos HTTP. Este libro se encuentra gratis en formato PDF y html en el sitio web de la Universidad de Stanford.
