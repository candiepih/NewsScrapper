import scrapy
from ..items import NewsscraperItem
from .agregator.world import World
from .agregator.sport import Sport
from .agregator.entertainment import Entertainment
from .agregator.tech import Tech


class BusinessspiderSpider(scrapy.Spider):
    name = 'newsSpider'
    allowed_domains = [
        'africa.businessinsider.com',
        'ew.com',
        'skysports.com',
        'techcrunch.com',
        'forbes.com',
        'independent.co.uk',
        'foxnews.com',
        'bt.com',
        'imdb.com',
        'theverge.com',
        'gamespot.com',
        'soccerhighlights.net',
    ]

    start_urls = [
        'https://africa.businessinsider.com/',
        'https://ew.com/',
        'https://www.skysports.com/',
        'https://techcrunch.com/',
        'https://www.forbes.com/lifestyle/',
        'https://www.independent.co.uk/news/world',
        'https://www.foxnews.com/world',
        'https://www.bt.com/sport/football/videos',
        'https://www.imdb.com/trailers/',
        'https://www.theverge.com',
        'https://www.gamespot.com',
        'https://www.soccerhighlights.net/',
    ]
    tech_urls = [
        'https://techcrunch.com/',
        'https://www.theverge.com',
        'https://www.gamespot.com'
    ]
    world_urls = [
        'https://www.foxnews.com/world',
        'https://www.independent.co.uk/news/world'
    ]
    sport_urls = [
        'https://www.skysports.com/',
        'https://www.bt.com/sport/football/videos',
        'https://www.soccerhighlights.net/'
    ]
    entertainment_urls = [
        'https://ew.com/',
        'https://www.imdb.com/trailers/',
    ]

    count_urls = 0
    expected_urls = len(start_urls)
    items: NewsscraperItem = NewsscraperItem()

    # HANDLES BUSINESS NEWS
    def handlingBusinessNews(self, response):
        containers = response.css(".layout-item")
        allArticles = []
        previous_titles = []
        for container in containers:
            title = container.css("div.gradient-overlay a::attr(title)").get()
            subtitle = None
            # stripping title to prepare for filtering
            new_title = title.strip() if title is not None else None
            if new_title in previous_titles:
                continue
            else:
                previous_titles.append(new_title)

            allArticles.append({
                "title": title.strip() if title is not None else None,
                "subTitle": subtitle.strip() if subtitle is not None else None,
                "image": container.css("div.imageBlock picture source::attr(data-original)").get(),
                "followUpLink": container.css("div.gradient-overlay a::attr(href)").get(),
                "published": {
                    "timestamp": None,
                    "date": None,
                },
            })

        businessNews = {
            "category": "Business",
            "category_id": 1,
            "publisher": 'Business Insider',
            "articles": allArticles
        }
        return businessNews

    def handlingLifestyleNews(self, response):
        news = []
        previous_titles = []

        top_banner = response.css('.card--large')

        news.append({
            "title": top_banner.css("a.headlink::text").get(),
            "followUpLink": top_banner.css("a.headlink::attr(href)").get(),
            "image": top_banner.css(".preview__image::attr(background-image)").get(),
            "published": {
                "timestamp": None,
                "date": None
            }
        })

        bottom_articles = response.css('.et-promoblock-star-item')
        for bottom_article in bottom_articles:
            title = bottom_article.css(".stream-item__title").css("a::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            image = bottom_article.css(".stream-item__image::attr(style)").re_first(r'url\(([^\)]+)')
            image = image.strip('"') if image is not None else None
            image2 = bottom_article.css(".ratio16x9::attr(style)").re_first(r'url\(([^\)]+)')
            image2 = image2.strip('"') if image2 is not None else None

            news.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": bottom_article.css(".stream-item__title").css("a::attr(href)").get(),
                "image": image if image is not None else image2,
                "published": {
                    "timestamp": bottom_article.css(".stream-item__date::attr(data-date)").get(),
                    "date": None
                }
            })

        allNews = {
            "category": "Lifestyle",
            "category_id": 5,
            "publisher": 'Forbes',
            "articles": news
        }
        return allNews

    def parse(self, response):
        if response.url == 'https://africa.businessinsider.com/':
            BusinessspiderSpider.items["businessNews"] = self.handlingBusinessNews(response)
            self.count_urls += 1
        elif response.url in self.entertainment_urls:
            entertainment = Entertainment(response, response.url)
            BusinessspiderSpider.items["entertainmentNews"] = entertainment.news
            self.count_urls += 1
        elif response.url in self.sport_urls:
            sport = Sport(response, response.url)
            BusinessspiderSpider.items["sportNews"] = sport.news
            self.count_urls += 1
        elif response.url in self.tech_urls:
            tech = Tech(response, response.url)
            BusinessspiderSpider.items["techNews"] = tech.news
            self.count_urls += 1
        elif response.url == 'https://www.forbes.com/lifestyle/':
            BusinessspiderSpider.items["lifestyleNews"] = self.handlingLifestyleNews(response)
            self.count_urls += 1
        elif response.url in self.world_urls:
            world = World(response, response.url)
            BusinessspiderSpider.items["worldNews"] = world.news
            self.count_urls += 1

        if self.count_urls == self.expected_urls:
            yield BusinessspiderSpider.items

