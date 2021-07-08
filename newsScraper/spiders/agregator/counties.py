class Counties:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def nation_africa(self):
        containers = self.response.css(".teasers-row")
        articles = []
        previous_titles = []

        for container in containers:
            county_name = container.css(".section-label a::text").get()
            minor_containers = container.css("li")
            for m_container in minor_containers:
                title = m_container.css(".teaser-image-large_title::text").get()
                if title in previous_titles or title is None:
                    continue
                else:
                    previous_titles.append(title)

                link = m_container.css("a::attr(href)").get()
                date = m_container.css(".date::text").get()
                image = m_container.css("figure img::attr(data-src)").get()
                articles.append({
                        "title": title.strip() if title is not None else None,
                        "image": "https://nation.africa" + image,
                        "source": "Nation Africa",
                        "county": county_name,
                        "genre": m_container.css(".article-topic::text").get(),
                        "followUpLink": "https://nation.africa/kenya" + link,
                        "published": {
                            "timestamp": None,
                            "date": date.strip() if date is not None else None,
                        }
                })
        Counties.__news.append({
            "publisher": "Nation Africa",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://nation.africa/kenya/counties":
            self.nation_africa()

    @property
    def news(self):
        data = {
            "category": "Counties",
            "category_id": 10,
            "news": Counties.__news,
        }
        return data
