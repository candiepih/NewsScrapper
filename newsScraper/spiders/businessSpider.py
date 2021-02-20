import scrapy
from ..items import NewsscraperItem
import hashlib


class BusinessspiderSpider(scrapy.Spider):
    name = 'newsSpider'
    allowed_domains = ['africa.businessinsider.com', 'ew.com', 'skysports.com', 'techcrunch.com', 'forbes.com', 'independent.co.uk']
    start_urls = [
        'https://africa.businessinsider.com/',
        'https://ew.com/',
        'https://www.skysports.com/',
        'https://techcrunch.com/',
        'https://www.forbes.com/lifestyle/',
        'https://www.independent.co.uk/news/world'
    ]

    items: NewsscraperItem = NewsscraperItem()

    # HANDLES BUSINESS NEWS
    def handlingBusinessNews(self, response):
        containers = response.css(".col-xs-12")
        allArticles = []
        previous_title = ""
        for container in containers:
            title = container.css(".itemTitle::text").get()
            subtitle = container.css(".itemLead::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            allArticles.append({
                "title": title,
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
            "publisher": 'Business Insider',
            "articles": allArticles
        }

        return businessNews

    # HANDLING ENTERTAINMENT NEWS
    def handlingEntertainmentNews(self, response):
        containers = response.css(".category-page-item")
        topContainers = response.css(".categoryPageHeader__container-details .entityTout__details")
        allArticles = []

        previous_title = ""
        for topContainer in topContainers:
            title = topContainer.css("a.entityTout__link span::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            allArticles.append({
                "title": stripped_title,
                "image": topContainer.css(".entityTout__image div.lazy-image::attr(data-src)").get(),
                "category": None,
                "followUpLink": topContainer.css("a.entityTout__link::attr(href)").get(),
                "published": None,
            })

        for container in containers:
            title = container.css(".category-page-item-content-wrapper a span::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            allArticles.append({
                "title": stripped_title,
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
        articles = []
        previous_title = ""

        for container in containers:
            title = container.css(".sdc-site-tile__headline-link span.sdc-site-tile__headline-text::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title
            category = container.css("a.sdc-site-tile__tag-link::text").get()
            link = container.css("h3.sdc-site-tile__headline a.sdc-site-tile__headline-link::attr(href)").get()
            articles.append({
                "title": stripped_title,
                "image": container.css(".sdc-site-tile__image-wrap source img::attr(src)").get(),
                "category": category.strip() if category is not None else None,
                "followUpLink": response.url + link[1:] if link[0][:1] == "/" else link
            })

        containers = response.css(".sdc-site-trending__link")
        for container in containers:
            title = container.css("a.sdc-site-trending__link span.sdc-site-trending__link-text::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title
            link = container.css("a.sdc-site-trending__link::attr(href)").get()
            articles.append({
                "title": stripped_title,
                "followUpLink": response.url + link[1:] if link[0][:1] == "/" else link
            })

        sportNews = {
            "category": "Sport",
            "category_id": 3,
            "publisher": 'Sky Sports',
            "articles": articles
        }

        return sportNews

    def handlingTechNews(self, response):
        containers = response.css(".post-block--unread")
        news = []
        previous_title = ""

        for container in containers:
            date = container.css("header.post-block__header div.post-block__meta time::text").get()
            title = container.css(
                "header.post-block__header h2.post-block__title a.post-block__title__link::text").get()
            subtitle = container.css(".post-block__content::text").get()

            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            news.append({
                "title": stripped_title,
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

    def handlingLifestyleNews(self, response):
        news = []

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

        top_articles = response.css('.card--blog')
        previous_title = ""

        for top_article in top_articles:
            title = top_article.css(".chansec-special-feature__nonpaid--title::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title
            image = top_article.css(".stream-item__image::attr(style)").re_first(r'url\(([^\)]+)')
            image.strip('"') if image is not None else None
            image2 = top_article.css(".ratio16x9::attr(style)").re_first(r'url\(([^\)]+)')
            image2.strip('"') if image2 is not None else None
            news.append({
                "title": stripped_title,
                "followUpLink": top_article.css(".chansec-special-feature__title-wrapper").css("a::attr(href)").get(),
                "image": image2 if image2 is not None else image,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })

        bottom_articles = response.css('.et-promoblock-star-item')
        for bottom_article in bottom_articles:
            title = bottom_article.css(".stream-item__title").css("a::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            image = bottom_article.css(".stream-item__image::attr(style)").re_first(r'url\(([^\)]+)')
            image.strip('"') if image is not None else None
            image2 = bottom_article.css(".ratio16x9::attr(style)").re_first(r'url\(([^\)]+)')
            image2.strip('"') if image2 is not None else None
            news.append({
                "title": stripped_title,
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

    def handlingWorldNews(self, response):
        containers = response.css(".article-default")

        articles = []
        previous_title = ""

        for container in containers:
            title = container.css(".title::text").get()
            stripped_title = title.strip() if title is not None else None,
            if stripped_title == previous_title:
                continue
            else:
                previous_title = stripped_title

            url = "https://www.independent.co.uk" + container.css(".title::attr(href)").get()
            articles.append({
                "title": stripped_title,
                "followUpLink": url,
                "image": container.css(".image-wrap amp-img::attr(src)").get(),
                "genre": container.css(".capsule::text").get(),
                "published": {
                    "timestamp": None,
                    "time": None
                },
            })
        news = {
            "category": "World",
            "category_id": 6,
            "publisher": 'Independent',
            "articles": articles
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
        elif response.url == 'https://www.forbes.com/lifestyle/':
            BusinessspiderSpider.items["lifestyleNews"] = self.handlingLifestyleNews(response)
        elif response.url == 'https://www.independent.co.uk/news/world':
            BusinessspiderSpider.items["worldNews"] = self.handlingWorldNews(response)

        countAllUrls = 0

        for url in BusinessspiderSpider.start_urls:
            countAllUrls += 1

        if len(BusinessspiderSpider.items) == countAllUrls:
            yield BusinessspiderSpider.items








