# Books Scraper

Un spider de Scrapy para extraer información de libros de horror del sitio [Books to Scrape](https://books.toscrape.com/).

## Descripción

Este proyecto utiliza Scrapy para extraer automáticamente información de libros de la categoría "Horror" del sitio Books to Scrape, incluyendo:

- Título del libro
- Precio
- Disponibilidad
- Calificación (rating)
- URL del libro
- Categoría

## Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala Scrapy:

```bash
pip install scrapy
```

## Uso

### Ejecutar el spider básico

```bash
# Desde el directorio del proyecto
cd books_scraper
scrapy crawl books
```

### Opciones avanzadas

```bash
# Ejecutar con logging detallado
scrapy crawl books -L DEBUG

# Ejecutar y guardar en archivo específico
scrapy crawl books -o books_output.csv

# Ejecutar con configuración personalizada
scrapy crawl books -s DOWNLOAD_DELAY=2
```

## Archivos de salida

El spider genera los siguientes archivos:

- `horror_books.csv`: Archivo CSV con todos los libros extraídos
- `books_export.json`: Archivo JSON con los mismos datos
- `scrapy.log`: Log detallado de la ejecución

## Estructura del proyecto

```
books_scraper/
├── scrapy.cfg              # Configuración del proyecto
├── books_scraper/
│   ├── __init__.py
│   ├── items.py            # Definición de items
│   ├── middlewares.py      # Middlewares personalizados
│   ├── pipelines.py        # Pipelines de procesamiento
│   ├── settings.py         # Configuración del spider
│   └── spiders/
│       ├── __init__.py
│       └── books.py        # Spider principal
```

## Configuración

El spider está configurado con las siguientes características:

- **Respeta robots.txt**: Se adhiere a las reglas del sitio
- **Delay entre requests**: 1 segundo por defecto para ser respetuoso
- **AutoThrottle**: Ajusta automáticamente la velocidad según la respuesta del servidor
- **Retry automático**: Reintenta requests fallidos
- **Logging detallado**: Registra toda la actividad

## Pipelines

El proyecto incluye tres pipelines:

1. **ValidationPipeline**: Valida que los datos extraídos sean correctos
2. **CleanDataPipeline**: Limpia y formatea los datos
3. **CsvExportPipeline**: Exporta los datos a CSV

## Personalización

### Cambiar la categoría

Para extraer libros de otra categoría, modifica la URL en `start_urls` en `spiders/books.py`:

```python
start_urls = [
    'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
]
```

### Añadir más campos

1. Agrega el campo en `items.py`
2. Modifica el método `extract_book_data` en `spiders/books.py`
3. Actualiza los pipelines si es necesario

## Aspectos legales

Este spider está diseñado para fines educativos y respeta:

- El archivo robots.txt del sitio
- Delays apropiados entre requests
- Límites de concurrencia razonables

Siempre verifica los términos de uso del sitio web antes de hacer scraping.

## Solución de problemas

### Error de conexión

Si obtienes errores de conexión, verifica:

1. Tu conexión a internet
2. Que el sitio esté disponible
3. Aumenta el `DOWNLOAD_DELAY` en settings.py

### Datos incompletos

Si faltan datos:

1. Verifica que los selectores CSS sean correctos
2. Revisa los logs para ver errores específicos
3. Ejecuta con `-L DEBUG` para más información

## Contribuir

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Agrega tests si es necesario
4. Envía un pull request