# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from itemadapter import ItemAdapter


class CsvExportPipeline:
    """Pipeline para exportar items a un archivo CSV"""
    
    def __init__(self):
        self.file = None
        self.writer = None
    
    def open_spider(self, spider):
        """Se ejecuta cuando se abre el spider"""
        # Crear el archivo CSV en el directorio actual
        self.file = open('horror_books.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(
            self.file, 
            fieldnames=['title', 'price', 'category', 'availability', 'rating', 'url']
        )
        self.writer.writeheader()
        spider.logger.info("Archivo CSV creado: horror_books.csv")
    
    def close_spider(self, spider):
        """Se ejecuta cuando se cierra el spider"""
        if self.file:
            self.file.close()
            spider.logger.info("Archivo CSV cerrado correctamente")
    
    def process_item(self, item, spider):
        """Procesa cada item extraído"""
        # Convertir el item a diccionario y escribirlo al CSV
        adapter = ItemAdapter(item)
        self.writer.writerow(adapter.asdict())
        return item


class ValidationPipeline:
    """Pipeline para validar los datos extraídos"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Validar que el título no esté vacío
        if not adapter.get('title'):
            spider.logger.warning(f"Item sin título descartado: {item}")
            return None
            
        # Validar que el precio sea un número válido
        price = adapter.get('price')
        if price:
            try:
                float(price)
            except (ValueError, TypeError):
                spider.logger.warning(f"Precio inválido para {adapter.get('title')}: {price}")
                adapter['price'] = None
        
        return item


class CleanDataPipeline:
    """Pipeline para limpiar y formatear los datos"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Limpiar el título
        title = adapter.get('title')
        if title:
            adapter['title'] = title.strip()
        
        # Formatear el precio
        price = adapter.get('price')
        if price:
            # Remover caracteres no numéricos excepto punto decimal
            clean_price = ''.join(c for c in str(price) if c.isdigit() or c == '.')
            adapter['price'] = clean_price
        
        # Limpiar disponibilidad
        availability = adapter.get('availability')
        if availability:
            adapter['availability'] = ' '.join(availability.split())
        
        return item