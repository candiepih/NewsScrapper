import scrapy
from ..items import NewsscraperItem
from .agregator.world import World
from .agregator.sport import Sport
from .agregator.entertainment import Entertainment
from .agregator.tech import Tech
from .agregator.politics import Politics
from .agregator.counties import Counties
from .agregator.education import Education
from .agregator.lifestyle import Lifestyle
from .agregator.business import Business
from .agregator.topbuzz import TopBuzz
from .agregator.eastafrica import EastAfrica


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
        'the-star.co.ke',
        'standardmedia.co.ke',
        'nation.africa',
        'mpasho.co.ke',
        'ghafla.com',
        'tuko.co.ke'
        'businessdailyafrica.com',
        'kenyanwallstreet.com',
        'kenyans.co.ke',
        'theeastafrican.co.ke'
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
        'https://www.the-star.co.ke/sports/',
        'https://www.standardmedia.co.ke/category/3/politics',
        'https://nation.africa/kenya/news/politics',
        'https://nation.africa/kenya/counties',
        'https://www.standardmedia.co.ke/category/56/education',
        'https://mpasho.co.ke/lifestyle/',
        'https://mpasho.co.ke/entertainment/',
        'http://www.ghafla.com/ke/tag/ghafla-entertainment-news/',
        'https://www.tuko.co.ke/entertainment/',
        'https://www.businessdailyafrica.com/',
        'https://kenyanwallstreet.com/category/kenyan-news/',
        'https://www.kenyans.co.ke/news',
        'https://www.tuko.co.ke/latest/',
        'https://www.theeastafrican.co.ke/'
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
        'https://www.soccerhighlights.net/',
        'https://www.the-star.co.ke/sports/'
    ]
    entertainment_urls = [
        'https://ew.com/',
        'https://www.imdb.com/trailers/',
        'https://mpasho.co.ke/entertainment/',
        'http://www.ghafla.com/ke/tag/ghafla-entertainment-news/',
        'https://www.tuko.co.ke/entertainment/'
    ]
    politics_urls = [
        'https://www.standardmedia.co.ke/category/3/politics',
        'https://nation.africa/kenya/news/politics'
    ]
    counties_urls = [
        'https://nation.africa/kenya/counties'
    ]
    lifestyle_urls = [
        'https://www.forbes.com/lifestyle/',
        'https://mpasho.co.ke/lifestyle/'
    ]
    business_urls = [
        'https://africa.businessinsider.com/',
        'https://www.businessdailyafrica.com/',
        'https://kenyanwallstreet.com/category/kenyan-news/'
    ]
    top_buzz_urls = [
        "https://www.kenyans.co.ke/news",
        "https://www.tuko.co.ke/latest/"
    ]
    east_africa = [
        'https://www.theeastafrican.co.ke/'
    ]

    videos_dict = {
        "category": "Videos",
        "category_id": 9,
        "news": [],
    }
    count_urls = 0
    expected_urls = (len(start_urls) - 1)
    news_containers = {}
    items: NewsscraperItem = NewsscraperItem()

    @staticmethod
    def organise_data(category_id, category_name, news_data):
        data = {
            "category": category_name,
            "category_id": category_id,
            "news": news_data,
        }
        return data

    def parse(self, response):
        if response.url in self.business_urls:
            business = Business(response)
            self.news_containers["businessNews"] = business
            # self.count_urls += 1
        elif response.url in self.entertainment_urls:
            entertainment = Entertainment(response, self.videos_dict["news"])
            self.news_containers["entertainmentNews"] = entertainment
            # self.count_urls += 1
        elif response.url in self.sport_urls:
            sport = Sport(response, self.videos_dict["news"])
            self.news_containers["sportNews"] = sport
            # self.count_urls += 1
        elif response.url in self.tech_urls:
            tech = Tech(response)
            self.news_containers["techNews"] = tech
            # self.count_urls += 1
        elif response.url in self.lifestyle_urls:
            lifestyle = Lifestyle(response)
            self.news_containers["lifestyleNews"] = lifestyle
            # self.count_urls += 1
        elif response.url in self.world_urls:
            world = World(response)
            self.news_containers["worldNews"] = world
            # self.count_urls += 1
        elif response.url in self.top_buzz_urls:
            top_buzz = TopBuzz(response)
            self.news_containers["topBuzzNews"] = top_buzz
            # self.count_urls += 1
        elif response.url in self.east_africa:
            east_africa = EastAfrica(response)
            self.news_containers["eastAfricaNews"] = east_africa
            # self.count_urls += 1
        elif response.url in self.politics_urls:
            politics = Politics(response)
            self.news_containers["politicsNews"] = politics
            # self.count_urls += 1
        elif response.url in self.counties_urls:
            counties = Counties(response)
            self.news_containers["countiesNews"] = counties
            # self.count_urls += 1
        elif response.url == 'https://www.standardmedia.co.ke/category/56/education':
            education = Education(response)
            self.news_containers["educationNews"] = education
            # self.count_urls += 1

        self.count_urls += 1
        if self.count_urls == self.expected_urls:
            BusinessspiderSpider.items["videos"] = self.videos_dict
            for k, v in self.news_containers.items():
                BusinessspiderSpider.items[k] = v.news
            yield BusinessspiderSpider.items
