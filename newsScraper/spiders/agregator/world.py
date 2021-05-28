class World:
    __news = {
        "category": "World",
        "category_id": 6,
        "publisher": 'Independent',
    }

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.aggregator()

    def independent_news(self):
        containers = self.response.css(".article-default")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".title::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            url = "https://www.independent.co.uk" + container.css(".title::attr(href)").get()
            articles.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": url,
                "image": container.css(".image-wrap amp-img::attr(src)").get(),
                "genre": container.css(".capsule::text").get(),
                "published": {
                    "timestamp": None,
                    "time": None
                },
            })
        World.__news["articles"] = articles

    def fox_news(self):
        containers = self.response.css(".article")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".title a::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            url = container.css(".title a::attr(href)").get()
            image = container.css(".m img::attr(src)").get()
            if url is None or image is None:
                continue

            articles.append({
                "title": title.strip() if title is not None else None,
                "followUpLink": "https://www.foxnews.com" + url,
                "image": image,
                "Genre": container.css(".eyebrow a::text").get(),
                "publisher": 'Fox news',
                "published": {
                    "timestamp": None,
                    "time": None
                },
            })
        World.__news["more_articles"] = articles

    def aggregator(self):
        if self.url == 'https://www.independent.co.uk/news/world':
            self.independent_news()
        elif self.url == 'https://www.foxnews.com/world':
            self.fox_news()

    @property
    def news(self):
        return World.__news
