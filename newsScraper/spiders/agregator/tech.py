class Tech:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def techcrunch_news(self):
        containers = self.response.css(".post-block--unread")
        articles = []
        previous_titles = []

        for container in containers:
            date = container.css("header.post-block__header div.post-block__meta time::text").get()
            title = container.css(
                "header.post-block__header h2.post-block__title a.post-block__title__link::text").get()
            subtitle = container.css(".post-block__content::text").get()

            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            link = container.css("header.post-block__header h2.post-block__title a.post-block__title__link::attr(href)").get()
            timestamp = container.css(
                        "header.post-block__header div.post-block__meta time::attr(datetime)").get()
            image = container.css("footer.post-block__footer img::attr(src)").get()
            articles.append({
                "title": title.strip() if title is not None else None,
                "subTitle": subtitle.strip() if subtitle is not None else subtitle,
                "source": "Techcrunch",
                "genre": None,
                "followUpLink": link,
                "image": image,
                "published": {
                    "timestamp": timestamp,
                    "date": date.strip() if date is not None else date
                },
            })

        Tech.__news.append({
            "publisher": "Techcrunch",
            "articles": articles
        })

    def verge_news(self):
        containers = self.response.css(".c-entry-box--compact--article")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".c-entry-box--compact__title a::text").get()
            image = container.css(".c-entry-box--compact__image noscript img::attr(src)").get()

            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)
            if title is None or image is None:
                continue

            articles.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": container.css(".c-entry-box--compact__title a::attr(href)").get(),
                "image": image,
                'genre': None,
                "source": "The Verge",
                "published": {
                    "timestamp": container.css(".c-byline .c-byline__item time::attr(datetime)").get(),
                    "date": None
                }
            })

        Tech.__news.append({
            "publisher": "The Verge",
            "articles": articles
        })

    def gamespot_news(self):
        containers = self.response.css(".medium-span7 .card-item")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".card-item__content h4::text").get()
            image = container.css(".card-item__img img::attr(src)").get()

            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)
            if title is None or image is None:
                continue

            link = container.css(".card-item__content a::attr(href)").get()
            articles.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": link if link[0] != "/" else "{}{}".format(self.url, link),
                "image": image,
                "source": "Game Spot",
                'genre': None,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })
        Tech.__news.append({
            "publisher": "Game Spot",
            "articles": articles
        })

    def aggregator(self):
        if self.url == 'https://www.theverge.com':
            self.verge_news()
        elif self.url == 'https://techcrunch.com/':
            self.techcrunch_news()
        elif self.url == 'https://www.gamespot.com':
            self.gamespot_news()

    @property
    def news(self):
        data = {
            "category": "Technology",
            "category_id": 4,
            "news": Tech.__news,
        }
        return data

