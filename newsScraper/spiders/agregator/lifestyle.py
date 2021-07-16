class Lifestyle:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def forbes(self):
        articles = []
        previous_titles = []

        top_banner = self.response.css('.card--large')
        articles.append({
            "title": top_banner.css("a.headlink::text").get(),
            "followUpLink": top_banner.css("a.headlink::attr(href)").get(),
            "image": top_banner.css(".preview__image::attr(background-image)").get(),
            "source": "Forbes",
            "genre": None,
            "published": {
                "timestamp": None,
                "date": None
            }
        })

        bottom_articles = self.response.css('.et-promoblock-star-item')
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

            articles.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": bottom_article.css(".stream-item__title").css("a::attr(href)").get(),
                "image": image if image is not None else image2,
                "source": "Forbes",
                "genre": None,
                "published": {
                    "timestamp": bottom_article.css(".stream-item__date::attr(data-date)").get(),
                    "date": None
                }
            })

        Lifestyle.__news.append({
            "publisher": "Forbes",
            "articles": articles
        })

    def mpasho(self):
        containers = self.response.css(".col-md-12")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".article-title::text").get()
            link = container.css(".article-body a::attr(href)").get()
            image = container.css(".image span::attr(data-background-image)").get()
            if title in previous_titles or title is None:
                continue
            else:
                previous_titles.append(title)
            link = "https://mpasho.co.ke" + link
            genre = container.css(".article-section a::text").get()
            genre = genre.replace("· ", "") if genre is not None else None
            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "source": "Mpasho",
                "genre": genre,
                "followUpLink": link,
                "published": {
                    "timestamp": None,
                    "date": container.css(".article-pub-date::text").get()
                }
            })
        Lifestyle.__news.append({
            "publisher": "Mpasho",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://www.forbes.com/lifestyle/":
            self.forbes()
        elif self.url == "https://mpasho.co.ke/lifestyle/":
            self.mpasho()

    @property
    def news(self):
        data = {
            "category": "Lifestyle",
            "category_id": 5,
            "news": Lifestyle.__news,
        }
        return data
