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

# Web Scraping

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp"""
import os
import shutil

csv_path = os.path.join(os.getcwd(), '../_static/code/scraping/books_scraper/horror_books.csv')
tmp_dir = "/tmp"
os.chdir(tmp_dir)
for filename in os.listdir(tmp_dir):
    file_path = os.path.join(tmp_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"No se pudo borrar {file_path}: {e}")
```

Web scraping es el proceso de extraer información de sitios web de forma automatizada.

Mientras que las APIs proporcionan interfaces estructuradas para acceder a datos, el web scraping permite obtener información de sitios que no ofrecen APIs o cuando se necesita acceder a datos que no están disponibles a través de ellas.

Los artefactos que realizan web scraping se conocen comúnmente como ***"scrapers"***, ***"spiders"*** o ***"crawlers"***. Estos programas navegan por las páginas web, descargan su contenido HTML y extraen la información relevante.

Los buscadores web utilizan ***crawlers*** para indexar el contenido de la web y hacer que sea accesible a través de búsquedas. De alguna manera, los crawlers son la columna vertebral de los motores de búsqueda que permite a los buscadores descubrir y organizar la vasta cantidad de información disponible en Internet, almacenando en sus bases de datos no solo las URLs, sino también fragmentos de texto y metadatos asociados a cada página.

El siguiente diagrama ilustra la arquitectura básica de un ***crawler***:

```{mermaid}
---
name: crawler_diagram
---
flowchart TB
    %% Definición del flujo principal (de arriba a abajo para mejor alineación visual)
    subgraph Entrada[" "]
        A[URLs semilla] --> B[Frontera de URLs]
    end

    subgraph Descarga_y_Analisis[" "]
        B --> C[Obtenedor de HTML]
        C --> D[Analizador HTML]
        D --> E[Detección de duplicados]
    end

    subgraph Extraccion_y_Gestion[" "]
        E --> F[Extractor de URLs]
        F --> G[Filtro de URLs]
        G --> H[Cargador/Detector de URLs]
        H --> I[(Almacenamiento de URLs)]
        H --> B
    end

    %% Módulos auxiliares arriba del flujo principal
    subgraph Auxiliares[" "]
        direction LR
        J[Resolutor DNS] --> K[Cacheo] --> L[(Almacenamiento de datos)]
    end

    %% Conexiones auxiliares
    C --> J
    E --> K
    E --> L
    K --> L

    %% Colores principales
    style A fill:#b6e8b0,stroke:#2e8b57,stroke-width:2px,color:#000
    style B fill:#b6e8b0,stroke:#2e8b57,stroke-width:2px,color:#000

    style C fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000
    style D fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000
    style E fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000
    style F fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000
    style G fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000
    style H fill:#add8e6,stroke:#4682b4,stroke-width:2px,color:#000

    style J fill:#d8b0ff,stroke:#7b68ee,stroke-width:2px,color:#000
    style K fill:#d8b0ff,stroke:#7b68ee,stroke-width:2px,color:#000

    style I fill:#ffe599,stroke:#c9a602,stroke-width:2px,color:#000
    style L fill:#ffe599,stroke:#c9a602,stroke-width:2px,color:#000

    %% Fondo de grupos
    style Entrada fill:#fff9c4,stroke:#fff9c4
    style Descarga_y_Analisis fill:#fff9c4,stroke:#fff9c4
    style Extraccion_y_Gestion fill:#fff9c4,stroke:#fff9c4
    style Auxiliares fill:#fff9c4,stroke:#fff9c4
```

URLs semilla
: Puntos de partida para el crawler. Una serie de URLs iniciales desde donde comenzar la exploración.

Frontera de URLs
: Estructura de datos que almacena las URLs pendientes de visitar. Cada vez que el *crawler* visita una página, extrae nuevas URLs y las añade a esta frontera.

Obtenedor de HTML
: Componente que realiza solicitudes HTTP para descargar el contenido HTML de las páginas web.

Analizador HTML
: Procesa el HTML descargado para extraer información relevante, como texto, enlaces, imágenes, etc.

Detección de duplicados
: Módulo que verifica si una URL ya ha sido visitada para evitar procesarla nuevamente.

Extractor de URLs
: Extrae todas las URLs presentes en la página web analizada.

Filtro de URLs
: Aplica reglas para decidir qué URLs deben ser añadidas a la frontera (por ejemplo, solo URLs del mismo dominio).

Cargador/Detector de URLs
: Añade nuevas URLs a la frontera y marca las URLs visitadas.

Almacenamiento de URLs
: Base de datos o archivo donde se guardan las URLs visitadas y pendientes.

Resolutor DNS
: Convierte nombres de dominio en direcciones IP para realizar las solicitudes HTTP.

Cacheo
: Almacena temporalmente respuestas HTTP para mejorar la eficiencia y reducir la carga en los servidores web.

Almacenamiento de datos
: Base de datos o archivo donde se guardan los datos extraídos del contenido web.

El proceso de web scraping puede variar en complejidad dependiendo del sitio web objetivo y de los datos que se desean extraer. Algunos sitios pueden tener estructuras HTML simples, mientras que otros pueden utilizar JavaScript para cargar contenido dinámicamente, lo que requiere técnicas más avanzadas.

En general el proceso de búsqueda inicia con una lista de URLs semilla, que son las páginas iniciales que el crawler visitará. A partir de estas páginas, el crawler descarga el contenido HTML y lo analiza para extraer información relevante y nuevas URLs. Estas nuevas URLs se añaden a la frontera de URLs pendientes de visitar, y el proceso se repite hasta que se alcanzan ciertos límites, como un número máximo de páginas visitadas o una profundidad máxima de exploración.

Para gestionar la frontera de URLs, se pueden utilizar diferentes estructuras de datos como colas (FIFO) para una exploración en anchura o pilas (LIFO) para una exploración en profundidad. Además, es importante implementar mecanismos para evitar visitar la misma URL múltiples veces, lo que se puede lograr mediante el uso de conjuntos o bases de datos para rastrear las URLs ya visitadas.

También se pueden establecer reglas para filtrar las URLs que se añaden a la frontera, como limitar la exploración a un dominio específico o evitar ciertos tipos de contenido.

## Consideraciones Legales y Éticas

Antes de realizar una exploración de la web, es fundamental considerar aspectos legales y éticos. Algunos sitios web prohíben el scraping en sus términos de servicio, y es importante respetar estas políticas para evitar problemas legales.

También es crucial ser respetuoso con los servidores web, evitando sobrecargar el sitio con demasiadas solicitudes en poco tiempo.

Los servidores pueden tener mecanismos para detectar y bloquear actividades sospechosas, como un número excesivo de solicitudes en un corto período.

En general las políticas de acceso a un sitio web por parte de los scrapers se regulan mediante:

robots.txt
: Archivo en la raíz del sitio web que especifica qué partes pueden ser accedidas por robots automatizados.

```{code-cell} python
---
tags: hide-output
---
import requests

# Verificar el archivo robots.txt
url_robots = 'https://python.org/robots.txt'
response = requests.get(url_robots)

print("Contenido de robots.txt de python.org:")
print('\n'.join(response.text.split('\n')))
```

El formato típico de un archivo `robots.txt` incluye directivas como `User-agent`, `Disallow`, y `Allow` para controlar el acceso de diferentes tipos de bots a distintas partes del sitio web.

El protocolo Robots Exclusion Standard define cómo los bots deben interpretar estas directivas para respetar las políticas del sitio. Este protocolo se encuentra estandarizado a través de la [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html).

Términos de Servicio
: Muchos sitios web prohíben explícitamente el scraping en sus términos de uso.

Leyes de Protección de Datos
: Regulaciones como GDPR en Europa o leyes locales de protección de datos personales.

Propiedad Intelectual
: El contenido scrapeado puede estar protegido por derechos de autor.

Identificarse correctamente
: Usar un User-Agent descriptivo que permita al administrador del sitio contactarte.

Uso responsable de los datos
: No usar los datos scrapeados para propósitos no éticos o ilegales.

## Web Scraping Manual con Python

Python ofrece excelentes bibliotecas para web scraping. Las más populares son `requests` para realizar solicitudes HTTP y `BeautifulSoup` para parsear HTML.

### Instalación de Bibliotecas

```bash
pip install requests beautifulsoup4 lxml
```

`BeautifulSoup` es una biblioteca para parsear documentos HTML y XML, facilitando la navegación y búsqueda de elementos dentro del árbol del documento.

### Ejemplo Básico de un crawler

```{code-cell} python
---
tags: hide-output
---
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import time

def es_mismo_dominio(url, dominio_base):
    """Verifica si la URL pertenece al mismo dominio base."""
    return urlparse(url).netloc == dominio_base

def crawler_frontera(url_semilla, max_paginas=50, retraso=1, archivo_csv='enlaces.csv'):
    """
    Función para realizar crawling web utilizando una frontera de enlaces tipo
    FIFO (cola).
    Recorre páginas web comenzando desde una URL semilla, siguiendo enlaces encontrados
    hasta un máximo de páginas.

    Parámetros:
    - url_semilla (str): URL inicial desde donde comienza el crawling.
    - max_paginas (int, opcional): Número máximo de páginas a visitar (por defecto 50).
    - retraso (int o float, opcional): Tiempo de espera (en segundos) entre solicitudes
    para evitar sobrecargar el servidor (por defecto 1).
    - archivo_csv (str, opcional): Nombre del archivo CSV donde se guardarán los enlaces
    encontrados (por defecto 'enlaces.csv').
    """
    frontera = [url_semilla]
    visitadas = set()
    enlaces_extraidos = []

    dominio_base = urlparse(url_semilla).netloc

    while frontera and len(visitadas) < max_paginas:
        url_actual = frontera.pop(0)
        if url_actual in visitadas:
            continue

        print(f"Visitando: {url_actual}")
        try:
            response = requests.get(url_actual, timeout=10, headers={
                # Es recomendable configurar el encabezado 'User-Agent' con un valor descriptivo que
                # identifique el crawler y proporcione información de contacto.
                # Esto ayuda a los administradores de los sitios web a identificar el origen de las solicitudes
                # y contactar al responsable en caso necesario.
                # Además, usar un User-Agent personalizado demuestra buenas prácticas y respeto por las
                #  políticas del sitio.
                'User-Agent': 'MiCrawler/1.0 (contacto@ejemplo.com)'
            })
            response.raise_for_status()
        except Exception as e:
            print(f"  Error al acceder: {e}")
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        visitadas.add(url_actual)

        # Extraer y guardar enlaces
        for enlace in soup.find_all('a', href=True):
            # En una página html los enlaces están en etiquetas <a href="...">
            url_encontrada = urljoin(url_actual, enlace['href'])
            url_encontrada = url_encontrada.split('#')[0]  # Quitar fragmentos
            if es_mismo_dominio(url_encontrada, dominio_base):
                if url_encontrada not in visitadas and url_encontrada not in frontera:
                    frontera.append(url_encontrada)
                enlaces_extraidos.append({'pagina': url_actual, 'enlace': url_encontrada})

        time.sleep(retraso)  # Ser respetuoso con el servidor

    # Guardar enlaces en un archivo CSV
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['pagina', 'enlace'])
        writer.writeheader()
        writer.writerows(enlaces_extraidos)

    print(f"\nTotal de páginas visitadas: {len(visitadas)}")
    print(f"Enlaces guardados en: {archivo_csv}")

# Ejemplo de uso:
crawler_frontera('https://quotes.toscrape.com/', max_paginas=10, archivo_csv='enlaces_quotes.csv')
```

En el siguiente enlace se puede descargar el archivo .csv generado por el ***crawler***: [`enlaces_quotes.csv`](enlaces_quotes.csv)

## Scrapy

Scrapy es un *framework* de Python para web scraping a gran escala. Proporciona funcionalidades avanzadas como:

- Gestión automática de solicitudes concurrentes
- Manejo de robots.txt
- Extracción de datos con selectores CSS y XPath
- Exportación a múltiples formatos (JSON, CSV, XML)
- Middleware para personalizar el comportamiento

### Instalación de Scrapy

```bash
pip install scrapy
```

````{admonition} Anatomía de un Spider en Scrapy
Una *spider* en Scrapy es una clase que hereda de `scrapy.Spider` y define cómo navegar y extraer información de un sitio web. Los elementos clave que se deben configurar son:

- **name**: Identificador único de la spider dentro del proyecto.
- **allowed_domains**: Lista de dominios permitidos para evitar que la spider navegue fuera del sitio objetivo.
- **start_urls**: Lista de URLs iniciales desde donde comenzará el scraping.
- **custom_settings** *(opcional)*: Permite definir configuraciones específicas para esta spider, como el retraso entre descargas, el User-Agent, el respeto a robots.txt, número de solicitudes concurrentes, etc.
- **parse**: Método principal que procesa la respuesta de cada URL y define cómo extraer los datos o seguir enlaces adicionales.

Ejemplo básico:

```python
import scrapy

class MiSpider(scrapy.Spider):
    name = 'mi_spider'
    allowed_domains = ['ejemplo.com']
    start_urls = ['https://ejemplo.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Espera 1 segundo entre solicitudes
        'ROBOTSTXT_OBEY': True,  # Respeta robots.txt
        'USER_AGENT': 'MiSpider/1.0 (contacto@ejemplo.com)'
    }

    def parse(self, response):
        # Lógica de extracción de datos
        for elemento in response.css('div.item'):
            yield {
                'titulo': elemento.css('h2::text').get(),
                'enlace': elemento.css('a::attr(href)').get(),
            }
        # Seguir enlaces a otras páginas si es necesario
        siguiente = response.css('a.siguiente::attr(href)').get()
        if siguiente:
            yield response.follow(siguiente, self.parse)
```

**Resumen de configuración esencial:**
- Define el nombre y dominios permitidos.
- Especifica las URLs de inicio.
- Ajusta `custom_settings` para controlar el comportamiento de la spider.
- Implementa el método `parse` para extraer y procesar la información. En el ejemplo, se extraen títulos y enlaces de elementos con la clase `item`, y se sigue un enlace de paginación si está presente.

Para spiders más avanzados, se pueden sobrescribir otros métodos o definir múltiples funciones de parseo según la estructura del sitio.
````

## Proyecto Práctico: Spider de Libros con Scrapy

A continuación se presenta un tutorial paso a paso para crear un spider con **Scrapy** que visite el sitio [Books to Scrape](https://books.toscrape.com/) y genere un archivo CSV con títulos y precios de los libros de la categoría "Horror".

### Paso 1: Crear un Proyecto Scrapy

Crear un nuevo proyecto de Scrapy en el directorio actual:

Iniciar un nuevo proyecto y una spider:

```bash
scrapy startproject books_scraper
cd books_scraper
scrapy genspider books books.toscrape.com
```

### Paso 2: Estructura del Proyecto

El comando anterior crea la siguiente estructura de directorios:

```text
books_scraper/
    scrapy.cfg
    books_scraper/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            books.py
```

### Paso 3: Definir los Items

Editar el archivo `items.py` para definir la estructura de datos que queremos extraer:

```python
# books_scraper/items.py
import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
```

### Paso 4: Implementar el Spider

Editar el archivo `spiders/books.py` con la lógica de extracción:

```python
# books_scraper/spiders/books.py
import scrapy
from books_scraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        "https://books.toscrape.com/catalogue/category/books/horror_31/index.html"
    ]

    def parse(self, response):
        """Extrae información de libros de la página actual"""

        # Extraer todos los libros de la página
        books = response.xpath("//article[contains(@class,'product_pod')]")

        for book in books:
            item = BookItem()

            # Extraer título
            item["title"] = book.xpath(".//h3/a/@title").get().strip()

            # Extraer precio
            price_text = (
                book.xpath(".//p[contains(@class,'price_color')]/text()").get().strip()
            )
            item["price"] = price_text.replace("£", "") if price_text else None

            # Extraer disponibilidad
            availability = book.xpath(
                ".//p[contains(@class,'instock') and contains(@class,'availability')]/text()"
            ).getall()
            item["availability"] = (
                "".join(availability).strip() if availability else None
            )

            # Extraer calificación
            rating_class = book.xpath(
                ".//p[contains(@class,'star-rating')]/@class"
            ).get()
            if rating_class:
                rating = rating_class.split()[-1]
                item["rating"] = rating
            else:
                item["rating"] = None

            item["category"] = "Horror"

            yield item

        # Seguir a la siguiente página si existe
        next_page = response.xpath("//li[contains(@class,'next')]/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
```

### Paso 5: Configurar Pipeline para CSV

Crear un pipeline personalizado para exportar a CSV. Editar `pipelines.py`:

```python
# books_scraper/pipelines.py
import csv
import os


class CsvExportPipeline:
    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        """Se ejecuta cuando se abre el spider"""
        self.file = open("horror_books.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=["title", "price", "category", "availability", "rating"],
        )
        self.writer.writeheader()

    def close_spider(self, spider):
        """Se ejecuta cuando se cierra el spider"""
        if self.file:
            self.file.close()

    def process_item(self, item, spider):
        """Procesa cada item extraído"""
        self.writer.writerow(dict(item))
        return item
```

### Paso 6: Configurar Settings

Editar `settings.py` para activar el pipeline y configurar el comportamiento del spider:

```python
# books_scraper/settings.py
BOT_NAME = "books_scraper"

SPIDER_MODULES = ["books_scraper.spiders"]
NEWSPIDER_MODULE = "books_scraper.spiders"

# Respetar robots.txt
ROBOTSTXT_OBEY = True

# Configurar pipelines
ITEM_PIPELINES = {
    "books_scraper.pipelines.CsvExportPipeline": 300,
}

# Configurar delays para ser respetuosos con el servidor
DOWNLOAD_DELAY = 1  # Esperar 1 segundo entre requests
RANDOMIZE_DOWNLOAD_DELAY = 0.5  # Variar el delay ±50%

# User agent personalizado
USER_AGENT = "books_scraper (untref.edu.ar)"

# Configuración de logging
LOG_LEVEL = "INFO"
```

### Paso 7: Ejecutar el Spider

Para ejecutar el spider y generar el archivo CSV:

```bash
cd books_scraper
scrapy crawl books
# Esto generará un archivo 'horror_books.csv' con los resultados
```

### Paso 8: Análisis de Resultados (Opcional)

Podemos analizar los resultados usando pandas:

```{code-cell} python
---
tags: hide-output
---
import pandas as pd

# Cargar los datos
df = pd.read_csv(csv_path)

# Estadísticas básicas
print("Estadísticas de los libros de Horror:")
print(f"Total de libros: {len(df)}")
print(f"Precio promedio: £{df['price'].astype(float).mean():.2f}")
print(f"Precio mínimo: £{df['price'].astype(float).min():.2f}")
print(f"Precio máximo: £{df['price'].astype(float).max():.2f}")

# Distribución de calificaciones
print("\nDistribución de calificaciones:")
print(df['rating'].value_counts())
```

[Descargar código completo del Spider](https://github.com/untref-edd/apuntes/tree/main/contenidos/_static/code/scraping)

### Extensiones Posibles

- **Múltiples categorías**: Modificar `start_urls` para incluir más categorías
- **Imágenes**: Agregar extracción de URLs de imágenes de libros
- **Detalles adicionales**: Visitar páginas individuales de libros para más información
- **Base de datos**: Cambiar el pipeline para guardar en SQLite o PostgreSQL
- **Monitoreo**: Agregar logging y métricas de rendimiento

## Comparación: APIs vs Web Scraping

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

## Mejores Prácticas para Web Scraping

1. **Verificar legalidad**: Revisar términos de servicio y robots.txt
2. **Identificarse**: Usar un User-Agent descriptivo
3. **Ser respetuoso**: Limitar la frecuencia de solicitudes
4. **Manejar errores**: Anticipar cambios en la estructura del sitio
5. **Considerar alternativas**: Preferir APIs cuando estén disponibles
6. **Mantener el código**: Si los sitios cambian, el scraper debe actualizarse

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

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scrapy Documentation](https://docs.scrapy.org/)

### Libros y Referencias Académicas

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. Capítulo 20: Web Crawling and Indexes.{cite:p}`irbook`
- Ryan Mitchell, *Web Scraping with Python*, 3rd Edition, O'Reilly Media, 2024.{cite:p}`Mitchell2024`

### Sitios para Practicar Web Scraping

- [Quotes to Scrape](https://quotes.toscrape.com/) - Sitio diseñado para practicar scraping
- [Books to Scrape](https://books.toscrape.com/) - Tienda de libros ficticia para scraping
- [Scrape This Site](https://www.scrapethissite.com/) - Ejercicios de scraping

### Aspectos Legales

- [Can I scrape your website?](https://blog.apify.com/is-web-scraping-legal/)
- [Understanding robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
