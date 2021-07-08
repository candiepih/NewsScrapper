class Politics:
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
                "genre": None,
                "followUpLink": link,
                "published": {
                    "timestamp": None,
                    "date": current_containers.css(".text-right::text").get()
                }
            })

        Politics.__news.append({
            "publisher": "Standard Media",
            "articles": articles
        })

    def nation_africa(self):
        containers = self.response.css(".teasers-row")
        articles = []
        previous_titles = []
        filtered_container = list(filter(lambda c: c.css("a::attr(name)").get() == "politics", containers))
        containers = filtered_container[0].css(".grid-container li")

        # first big article
        title = filtered_container[0].css("section a.teaser-image-large .teaser-image-large_title::text").get()
        image = filtered_container[0].css("section a.teaser-image-large figure img::attr(data-src)").get()
        url = filtered_container[0].css("section a.teaser-image-large::attr(href)").get()
        date = filtered_container[0].css(".date::text").get()
        articles.append({
            "title": title.strip() if title is not None else None,
            "image": "https://nation.africa" + image,
            "source": "Nation Africa",
            "genre": filtered_container[0].css(".article-topic::text").get(),
            "followUpLink": "https://nation.africa" + url,
            "published": {
                "timestamp": None,
                "date": date.strip() if date is not None else None,
            }
        })

        # Handle other articles
        for container in containers:
            title = container.css(".title-extra-small::text").get()
            if title in previous_titles or title is None:
                continue
            else:
                previous_titles.append(title)

            link = container.css("a::attr(href)").get()
            date = container.css(".date::text").get()
            articles.append({
                    "title": title.strip() if title is not None else None,
                    "image": None,
                    "source": "Nation Africa",
                    "genre": container.css(".article-topic::text").get(),
                    "followUpLink": "https://nation.africa/kenya" + link,
                    "published": {
                        "timestamp": None,
                        "date": date.strip() if date is not None else None,
                    }
            })
        Politics.__news.append({
            "publisher": "Nation Africa",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://www.standardmedia.co.ke/category/3/politics":
            self.standard_media()
        elif self.url == "https://nation.africa/kenya/news/politics":
            self.nation_africa()

    @property
    def news(self):
        data = {
            "category": "Politics",
            "category_id": 9,
            "news": Politics.__news,
        }
        return data


