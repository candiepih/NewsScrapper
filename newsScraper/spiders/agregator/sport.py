class Sport:
    __news = {
        "category": "Sport",
        "category_id": 3,
        "publisher": 'Sky Sports',
    }

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.aggregator()

    def sky_news(self):
        containers = self.response.css(".sdc-site-tile--has-link")
        articles = []
        previous_titles = []
        videos = []

        for container in containers:
            title = container.css(".sdc-site-tile__headline-link span.sdc-site-tile__headline-text::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)
            category = container.css("a.sdc-site-tile__tag-link::text").get()
            link = container.css("h3.sdc-site-tile__headline a.sdc-site-tile__headline-link::attr(href)").get()
            articles.append({
                "title": title.strip() if title is not None else None,
                "image": container.css(".sdc-site-tile__image-wrap source img::attr(src)").get(),
                "category": category.strip() if category is not None else None,
                "followUpLink": self.response.url + link[1:] if link[0][:1] == "/" else link
            })
        container = self.response.css("ul.sdc-site-carousel__rail")
        containers = container.css(".sdc-site-carousel__rail-item")
        for item in containers:
            title = item.css(".sdc-site-carousel__headline span::text").get()
            if title in previous_titles:
                continue
            else:
                previous_titles.append(title)

            link = item.css(".sdc-site-carousel__headline a::attr(href)").get()
            image = item.css(".sdc-site-carousel__rail-image-wrap picture")
            videos.append({
                    "title": title.strip() if title is not None else None,
                    "image": image.css("img::attr(src)").get(),
                    "source": "Sky sports",
                    "category": None,
                    "followUpLink": self.response.url + link[1:] if link[0][:1] == "/" else link
            })

        Sport.__news["articles"] = articles
        if "videos" in Sport.__news.keys():
            [Sport.__news["videos"].append(v) for v in videos]
        else:
            Sport.__news["videos"] = videos

    def bt_news(self):
        containers = self.response.css(".col-xs-6")
        videos = []
        previous_titles = []

        for container in containers:
            title = container.css(".content").css(".content-title p").css("a::text").get()
            if title in previous_titles or title is None:
                continue
            else:
                previous_titles.append(title)

            lock = container.css(".image-container").css(".tile-icons img.lock-icon::attr(src)").get()
            if lock is not None:
                continue
            link = container.css(".content").css(".content-title p").css("a::attr(href)").get()
            image = container.css(".image-container v-lazy-image::attr(src)").get()

            videos.append({
                    "title": title.strip() if title is not None else None,
                    "image": image,
                    "source": "BT Sport",
                    "category": None,
                    "followUpLink": link
            })
        if "videos" in Sport.__news.keys():
            [Sport.__news["videos"].append(v) for v in videos]
        else:
            Sport.__news["videos"] = videos

    def highlights_football(self):
        parent = self.response.css("div.td_with_ajax_pagination")
        containers = parent.css(".td-module-container")
        videos = []
        previous_titles = []

        for container in containers:
            title = container.css("h3.entry-title a::text").get()
            image = container.css(".td-image-container a span::attr(style)").re_first(r'url\(([^\)]+)')
            url = container.css("h3.entry-title a::attr(href)").get()
            Genre = container.css("a.td-post-category::text").get()

            if title in previous_titles or title is None or image is None or url is None:
                continue
            else:
                previous_titles.append(title)

            videos.append({
                "title": title.strip(),
                "image": image.strip("'"),
                "source": "Highlights Football",
                "Genre": Genre,
                "category": None,
                "followUpLink": url,
                "published": {
                    "timestamp": container.css("time.entry-date::attr(datetime)").get(),
                    "date": None
                }
            })
        if "videos" in Sport.__news.keys():
            [Sport.__news["videos"].append(v) for v in videos]
        else:
            Sport.__news["videos"] = videos

    def aggregator(self):
        if self.url == 'https://www.skysports.com/':
            self.sky_news()
        elif self.url == 'https://www.bt.com/sport/football/videos':
            self.bt_news()
        elif self.url == "https://highlightsfootball.net/":
            self.highlights_football()

    @property
    def news(self):
        return Sport.__news

