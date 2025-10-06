# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    """Item para representar un libro extraído del sitio Books to Scrape"""
    title = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()