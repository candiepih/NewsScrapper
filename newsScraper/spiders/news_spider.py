from typing import Generator, Any

import scrapy
from ..items import NewsscraperItem
from .agregator.world import World
from .agregator.sport import Sport
from .agregator.entertainment import Entertainment
from .agregator.tech import Tech
from .agregator.politics import Politics
from .agregator.topbuzz import TopBuzz


class BusinessspiderSpider(scrapy.Spider):
    name = 'newsSpider'
    allowed_domains = [
        'theverge.com',
        'foxnews.com',
        'skysports.com',
        'mpasho.co.ke',
        'standardmedia.co.ke',
        'kenyans.co.ke'
    ]

    start_urls = [
        'https://www.theverge.com',
        'https://www.foxnews.com/world',
        'https://www.skysports.com/',
        'https://mpasho.co.ke/entertainment/',
        'https://www.standardmedia.co.ke/category/3/politics',
        'https://www.kenyans.co.ke/news'
    ]
    tech_urls = [
        'https://www.theverge.com',
    ]
    world_urls = [
        'https://www.foxnews.com/world',
    ]
    sport_urls = [
        'https://www.skysports.com/',
    ]
    entertainment_urls = [
        'https://mpasho.co.ke/entertainment/',
    ]
    politics_urls = [
        'https://www.standardmedia.co.ke/category/3/politics',
    ]
    
    
    top_buzz_urls = [
        "https://www.kenyans.co.ke/news"
    ]
    
    count_urls = 0
    expected_urls = len(start_urls)
    news_containers = {}
    items: NewsscraperItem = NewsscraperItem()

    def parse(self, response) -> Generator[NewsscraperItem, Any, None]:
        if response.url in self.entertainment_urls:
            entertainment = Entertainment(response)
            self.news_containers["entertainmentNews"] = entertainment
        elif response.url in self.sport_urls:
            sport = Sport(response)
            self.news_containers["sportNews"] = sport
        elif response.url in self.tech_urls:
            tech = Tech(response)
            self.news_containers["techNews"] = tech
        elif response.url in self.world_urls:
            world = World(response)
            self.news_containers["worldNews"] = world
        elif response.url in self.top_buzz_urls:
            top_buzz = TopBuzz(response)
            self.news_containers["topBuzzNews"] = top_buzz
        elif response.url in self.politics_urls:
            politics = Politics(response)
            self.news_containers["politicsNews"] = politics

        self.count_urls += 1
        if self.count_urls == self.expected_urls:
            for k, v in self.news_containers.items():
                BusinessspiderSpider.items[k] = v.news
            yield BusinessspiderSpider.items
