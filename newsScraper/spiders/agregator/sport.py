from .videos import Videos


class Sport:
    __news = []

    def __init__(self, response, videos_list):
        self.response = response
        self.url = response.url
        self.videos = []
        self.aggregator(videos_list)
        Videos.videos = self.videos

    def sky_news(self, videos_list):
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
                "genre": category.strip() if category is not None else None,
                "source": "Sky sports",
                "followUpLink": self.response.url + link[1:] if link[0][:1] == "/" else link,
                "published": {
                    "timestamp": None,
                    "date": None
                }
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
                    "genre": None,
                    "followUpLink": self.response.url + link[1:] if link[0][:1] == "/" else link,
                    "published": {
                        "timestamp": None,
                        "date": None
                    }
            })

        Sport.__news.append({
            "publisher": "Sky Sports",
            "articles": articles
        })
        videos_list.append({
            "publisher": "Sky Sports",
            "articles": videos
        })

    def soccer_highlights(self, videos_list):
        parent = self.response.css("div.td-pb-span8")
        containers = parent.css(".td_module_wrap")
        videos = []
        previous_titles = []

        for container in containers:
            title = container.css("h3.td-module-title a::text").get()
            image = container.css(".td-image-wrap img::attr(src)").get()
            url = container.css("h3.td-module-title a::attr(href)").get()
            Genre = container.css("a.td-post-category::text").get()

            if title in previous_titles or title is None or image is None or url is None:
                continue
            else:
                previous_titles.append(title)

            videos.append({
                "title": title.strip(),
                "image": image.strip("'"),
                "source": "Soccer Highlights",
                "genre": Genre,
                "followUpLink": url,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })
        videos_list.append({
            "publisher": "Soccer Highlights",
            "articles": videos
        })

    def the_star(self):
        containers = self.response.css(".col-lg-9 .section-article")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css(".article-card-title::text").get()
            image = container.css(".image-loader-image::attr(data-background-image)").get()
            url = container.css(".article-body a::attr(href)").get()

            if title in previous_titles or title is None or image is None or url is None:
                continue
            else:
                previous_titles.append(title)

            articles.append({
                "title": title.strip(),
                "image": image.strip("'"),
                "source": "The Star",
                "genre": None,
                "followUpLink": 'https://www.the-star.co.ke' + url,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })

        Sport.__news.append({
            "publisher": "The Star",
            "articles": articles
        })

    def aggregator(self, videos_list):
        if self.url == 'https://www.skysports.com/':
            self.sky_news(videos_list)
        elif self.url == "https://www.soccerhighlights.net/":
            self.soccer_highlights(videos_list)
        elif self.url == "https://www.the-star.co.ke/sports/":
            self.the_star()

    @property
    def news(self):
        data = {
            "category": "Sports",
            "category_id": 3,
            "news": Sport.__news,
        }
        return data


