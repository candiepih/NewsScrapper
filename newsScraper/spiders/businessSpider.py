import scrapy
from ..items import NewsscraperItem
import hashlib


class BusinessspiderSpider(scrapy.Spider):
    name = 'newsSpider'
    allowed_domains = ['africa.businessinsider.com', 'ew.com', 'skysports.com', 'techcrunch.com', 'elle.com', 'newsnow.co.uk']
    start_urls = [
        'https://africa.businessinsider.com/',
        'https://ew.com/',
        'https://www.skysports.com/',
        'https://techcrunch.com/',
        'https://www.elle.com/fashion/',
        'https://www.newsnow.co.uk/h/World+News'
    ]
    items: NewsscraperItem = NewsscraperItem()

    def hashing(self, value):
        m = hashlib.md5()
        m.update(value.encode('utf8'))
        hashedVar = m.hexdigest()
        return hashedVar

    # HANDLES BUSINESS NEWS
    def handlingBusinessNews(self, response):
        containers = response.css(".col-xs-12")
        allArticles = []
        for container in containers:
            title = container.css(".itemTitle::text").get()
            subtitle = container.css(".itemLead::text").get()
            allArticles.append({
                "title": title.strip() if title is not None else None,
                "subTitle": subtitle.strip() if subtitle is not None else None,
                "image": container.css("div.itemImage source img::attr(data-original)").get(),
                "followUpLink": container.css("a.itemWrapper::attr(href)").get(),
                "published": {
                    "timestamp": None,
                    "date": container.css("span.itemDate::text").get(),
                },
            })
        allArticles.pop(0)
        allArticles.pop(1)
        businessNews = {
            "category": "Business",
            "category_id": 1,
            "publisher": 'Businessinsider',
            "articles": allArticles
        }

        return businessNews

    # HANDLING ENTERTAINMENT NEWS
    def handlingEntertainmentNews(self, response):
        containers = response.css(".category-page-item")
        allArticles = []
        for container in containers:
            allArticles.append({
                "title": container.css(".category-page-item-content-wrapper a span::text").get().strip(),
                "image": container.css(".category-page-item-image div.lazy-image::attr(data-src)").get(),
                "category": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(".category-page-item-category-label::text").get(),
                "followUpLink": container.css(".category-page-item-content-wrapper a::attr(href)").get(),
                "published": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(
                    ".category-page-item-timestamp::text").get(),
            })

        entertainmentNews = {
            "category": "Entertainment",
            "publisher": 'Ew',
            "category_id": 2,
            "articles": allArticles
        }

        return entertainmentNews

    def handlingSportNews(self, response):
        containers = response.css(".sdc-site-tile--has-link")

        allSports = []
        trendingNews = []

        for container in containers:
            category = container.css("a.sdc-site-tile__tag-link::text").get()
            link = container.css("h3.sdc-site-tile__headline a.sdc-site-tile__headline-link::attr(href)").get()
            allSports.append({
                "title": container.css(".sdc-site-tile__headline-link span.sdc-site-tile__headline-text::text").get(),
                "image": container.css(".sdc-site-tile__image-wrap source img::attr(src)").get(),
                "category": category.strip() if category is not None else None,
                "followUpLink": response.url + link[1:] if link[0][:1] == "/" else link
            })

        containers = response.css(".sdc-site-trending__link")
        for container in containers:
            link = container.css("a.sdc-site-trending__link::attr(href)").get()
            trendingNews.append({
                "title": container.css("a.sdc-site-trending__link span.sdc-site-trending__link-text::text").get(),
                "followUpLink": response.url + link[1:] if link[0][:1] == "/" else link
            })

        sportNews = {
            "category": "Sport",
            "category_id": 3,
            "publisher": 'Sky Sports',
            "articles": {
                "all": allSports,
                "trending": trendingNews
            }
        }

        return sportNews

    def handlingTechNews(self, response):
        containers = response.css(".post-block--unread")
        news = []
        for container in containers:
            date = container.css("header.post-block__header div.post-block__meta time::text").get()
            title = container.css(
                "header.post-block__header h2.post-block__title a.post-block__title__link::text").get()
            subtitle = container.css(".post-block__content::text").get()
            news.append({
                "title": title.strip() if title is not None else title,
                "subTitle": subtitle.strip() if subtitle is not None else subtitle,
                "followUpLink": container.css(
                    "header.post-block__header h2.post-block__title a.post-block__title__link::attr(href)").get(),
                "published": {
                    "timestamp": container.css(
                        "header.post-block__header div.post-block__meta time::attr(datetime)").get(),
                    "date": date.strip() if date is not None else date
                },
                "image": container.css("footer.post-block__footer img::attr(src)").get()
            })
        allNews = {
            "category": "Technology",
            "category_id": 4,
            "publisher": 'Techcrunch',
            "articles": news
        }

        return allNews

    def handlingFashionNews(self, response):
        containers = response.css('.custom-item-inner')
        news = []
        for container in containers:
            link = "https://www.elle.com"+container.css(".item-title::attr(href)").get()
            news.append({
                "title": container.css(".item-title::text").get(),
                "followUpLink": link,
                "image": container.css(".custom-item-image img::attr(data-src)").get(),
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })
        allNews = {
            "category": "Fashion",
            "category_id": 5,
            "publisher": 'Elle',
            "articles": news
        }
        return allNews

    def handlingWorldNews(self, response):
        containers = response.css(".js-maincontent").css(".newsfeed")
        news = []
        for container in containers:
            news.append({
                "title": container.css(".hll::text").get(),
                "followUpLink": container.css(".hll::attr(href)").get(),
                "source": container.css(".src-part::text").get(),
                "published": {
                    "timestamp": container.css("span.time::attr(data-time)").get(),
                    "time": container.css("span.time::text").get()
                },
            })
        news = {
            "category": "World",
            "category_id": 6,
            "publisher": 'Newsnow',
            "articles": news
        }

        return news

    def parse(self, response):

        if response.url == 'https://africa.businessinsider.com/':
            BusinessspiderSpider.items["businessNews"] = self.handlingBusinessNews(response)
        elif response.url == 'https://ew.com/':
            BusinessspiderSpider.items["entertainmentNews"] = self.handlingEntertainmentNews(response)
        elif response.url == 'https://www.skysports.com/':
            BusinessspiderSpider.items["sportNews"] = self.handlingSportNews(response)
        elif response.url == 'https://techcrunch.com/':
            BusinessspiderSpider.items["techNews"] = self.handlingTechNews(response)
        elif response.url == 'https://www.elle.com/fashion/':
            BusinessspiderSpider.items["fashionNews"] = self.handlingFashionNews(response)
        elif response.url == 'https://www.newsnow.co.uk/h/World+News':
            BusinessspiderSpider.items["worldNews"] = self.handlingWorldNews(response)

        countAllUrls = 0

        for url in BusinessspiderSpider.start_urls:
            countAllUrls += 1

        if len(BusinessspiderSpider.items) == countAllUrls:
            yield BusinessspiderSpider.items








