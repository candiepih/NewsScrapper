# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    entertainmentNews = scrapy.Field()
    sportNews = scrapy.Field()
    techNews = scrapy.Field()
    worldNews = scrapy.Field()
    topBuzzNews = scrapy.Field()
    politicsNews = scrapy.Field()
