"""
Spider para extraer información de libros de horror del sitio Books to Scrape.

Este spider navega por la categoría de Horror en books.toscrape.com y extrae:
- Título del libro
- Precio
- Disponibilidad
- Calificación (rating)
- URL del libro

El spider maneja automáticamente la paginación y respeta los delays
configurados para ser respetuoso con el servidor.
"""

import scrapy
from books_scraper.items import BookItem


class BooksSpider(scrapy.Spider):
    """Spider principal para extraer libros de horror"""

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/horror_31/index.html"]

    custom_settings = {
        "FEEDS": {
            "books_export.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "indent": 2,
            },
        },
    }

    def parse(self, response):
        """
        Extrae información de libros de la página actual y maneja paginación.

        Args:
            response: Respuesta HTTP de la página

        Yields:
            BookItem: Items con información de los libros
            scrapy.Request: Requests para páginas siguientes
        """
        self.logger.info(f"Procesando página: {response.url}")

        # Extraer todos los libros de la página
        books = response.xpath("//article[contains(@class,'product_pod')]")
        self.logger.info(f"Encontrados {len(books)} libros en esta página")

        for book in books:
            item = self.extract_book_data(book, response)
            if item:
                yield item

        # Seguir a la siguiente página si existe
        next_page = response.xpath("//li[contains(@class,'next')]/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Siguiendo a siguiente página: {next_page_url}")
            yield scrapy.Request(
                next_page_url, callback=self.parse, meta={"page_number": response.meta.get("page_number", 1) + 1}
            )
        else:
            self.logger.info("No hay más páginas para procesar")

    def extract_book_data(self, book_selector, response):
        """
        Extrae datos de un libro individual.

        Args:
            book_selector: Selector CSS del libro
            response: Respuesta HTTP actual

        Returns:
            BookItem: Item con datos del libro o None si hay error
        """
        try:
            item = BookItem()

            # Extraer título
            title = book_selector.xpath(".//h3/a/@title").get()
            if not title:
                title = book_selector.xpath(".//h3/a/text()").get()
            item["title"] = title.strip() if title else None

            # Extraer precio
            price_text = book_selector.xpath(".//p[contains(@class,'price_color')]/text()").get()
            if price_text:
                # Remover el símbolo de libra y espacios
                price_clean = price_text.replace("£", "").strip()
                item["price"] = price_clean
            else:
                item["price"] = None

            # Extraer disponibilidad
            availability = book_selector.xpath(
                ".//p[contains(@class,'instock') and contains(@class,'availability')]/text()"
            ).getall()
            if availability:
                # Unir todos los textos y limpiar espacios
                availability_text = "".join(availability).strip()
                item["availability"] = availability_text
            else:
                item["availability"] = "Unknown"

            # Extraer calificación
            rating_class = book_selector.xpath(".//p[contains(@class,'star-rating')]/@class").get()
            if rating_class:
                # La clase contiene algo como "star-rating Three"
                rating_parts = rating_class.split()
                if len(rating_parts) >= 2:
                    rating = rating_parts[-1]  # Última palabra (One, Two, Three, etc.)
                    item["rating"] = rating
                else:
                    item["rating"] = "Unknown"
            else:
                item["rating"] = "Unknown"

            # Extraer URL relativa del libro
            book_url = book_selector.xpath(".//h3/a/@href").get()
            if book_url:
                # Convertir URL relativa a absoluta
                item["url"] = response.urljoin(book_url)
            else:
                item["url"] = response.url

            # Asignar categoría
            item["category"] = "Horror"

            # Log del libro extraído
            self.logger.debug(f'Libro extraído: {item["title"]} - £{item["price"]}')

            return item

        except Exception as e:
            self.logger.error(f"Error extrayendo datos del libro: {e}")
            return None

    def parse_book_detail(self, response):
        """
        Parser opcional para extraer información detallada de cada libro.

        Este método puede ser usado si se desea extraer información adicional
        de la página individual de cada libro.

        Args:
            response: Respuesta HTTP de la página del libro

        Yields:
            BookItem: Item con información detallada del libro
        """
        book_item = response.meta.get("book_item")

        # Extraer información adicional de la página del libro
        description = response.xpath("//*[@id='product_description']/following-sibling::p[1]/text()").get()
        if description:
            book_item["description"] = description.strip()

        # Extraer información de la tabla de producto
        product_info = {}
        rows = response.xpath("//table[contains(@class,'table-striped')]//tr")
        for row in rows:
            key = row.xpath(".//td[1]//text()").get()
            value = row.xpath(".//td[last()]//text()").get()
            if key and value:
                product_info[key.strip()] = value.strip()

        book_item["product_info"] = product_info

        yield book_item
