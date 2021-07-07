# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    businessNews = scrapy.Field()
    entertainmentNews = scrapy.Field()
    sportNews = scrapy.Field()
    techNews = scrapy.Field()
    lifestyleNews = scrapy.Field()
    worldNews = scrapy.Field()
    topBuzzNews = scrapy.Field()
    eastAfricaNews = scrapy.Field()
    politicsNews = scrapy.Field()
    countiesNews = scrapy.Field()
    educationNews = scrapy.Field()
    videos = scrapy.Field()
