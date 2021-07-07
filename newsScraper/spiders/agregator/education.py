class Education:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def standard_media(self):
        containers = self.response.css(".links")
        articles = []
        previous_titles = []

        for container in containers:
            current_containers = container.css(".card")
            if current_containers.css("i.fa-key").get() is not None:
                continue
            title = current_containers.css(".card-title::text").get()
            link = container.css("::attr(href)").get()
            image = current_containers.css("img::attr(data-src)").get()
            if title in previous_titles or image is None:
                continue
            else:
                previous_titles.append(title)
            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "source": "Standard Media",
                "Genre": None,
                "followUpLink": link,
                "published": {
                    "timestamp": None,
                    "date": current_containers.css(".text-right::text").get()
                }
            })
        Education.__news.append({
            "publisher": "Standard Media",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://www.standardmedia.co.ke/category/56/education":
            self.standard_media()

    @property
    def news(self):
        data = {
            "category": "Education",
            "category_id": 9,
            "news": Education.__news,
        }
        return data
