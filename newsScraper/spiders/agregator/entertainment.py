class Entertainment:
    __news = {
        "category": "Entertainment",
        "publisher": 'Ew',
        "category_id": 2,
    }

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.aggregator()

    def ew_news(self):
        containers = self.response.css(".category-page-item")
        top_containers = self.response.css(".categoryPageHeader__container-details .entityTout__details")
        all_articles = []

        previous_titles = []
        for topContainer in top_containers:
            title = topContainer.css("a.entityTout__link span::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            all_articles.append({
                "title": title.strip() if title is not None else None,
                "image": topContainer.css(".entityTout__image div.lazy-image::attr(data-src)").get(),
                "category": None,
                "followUpLink": topContainer.css("a.entityTout__link::attr(href)").get(),
                "published": None,
            })

        for container in containers:
            title = container.css(".category-page-item-content-wrapper a span::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            all_articles.append({
                "title": title.strip() if title is not None else None,
                "image": container.css(".category-page-item-image div.lazy-image::attr(data-src)").get(),
                "category": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(".category-page-item-category-label::text").get(),
                "followUpLink": container.css(".category-page-item-content-wrapper a::attr(href)").get(),
                "published": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(
                    ".category-page-item-timestamp::text").get(),
            })

        self.__news["articles"] = all_articles

    def trailer_addict_news(self):
        containers = self.response.css("#top_features ul li")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css("a h2::text").get()
            image = container.css("li::attr(style)").re_first(r'url\(([^\)]+)')

            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "followUpLink": container.css("a::attr(href)").get(),
                "publisher": "Trailer Addict",
                "published": None,
            })

        self.__news["videos"] = articles

    def aggregator(self):
        if self.url == 'https://www.traileraddict.com':
            self.trailer_addict_news()
        elif self.url == 'https://ew.com/':
            self.ew_news()

    @property
    def news(self):
        return Entertainment.__news



