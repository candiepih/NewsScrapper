from datetime import datetime


class Entertainment:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    # def ew_news(self):
    #     containers = self.response.css(".category-page-item")
    #     top_containers = self.response.css(".categoryPageHeader__container-details .entityTout__details")
    #     all_articles = []

    #     previous_titles = []
    #     for topContainer in top_containers:
    #         title = topContainer.css("a.entityTout__link span::text").get()
    #         if title in previous_titles:
    #             continue
    #         else:
    #             previous_titles.append(title)

    #         all_articles.append({
    #             "title": title.strip() if title is not None else None,
    #             "image": topContainer.css(".entityTout__image div.lazy-image::attr(data-src)").get(),
    #             "genre": None,
    #             "source": "EW",
    #             "followUpLink": topContainer.css("a.entityTout__link::attr(href)").get(),
    #             "published": {
    #                 "timestamp": None,
    #                 "date": None
    #             }
    #         })

    #     for container in containers:
    #         title = container.css(".category-page-item-content-wrapper a span::text").get()
    #         if title in previous_titles:
    #             continue
    #         else:
    #             previous_titles.append(title)

    #         all_articles.append({
    #             "title": title.strip() if title is not None else None,
    #             "image": container.css(".category-page-item-image div.lazy-image::attr(data-src)").get(),
    #             "genre": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(".category-page-item-category-label::text").get(),
    #             "followUpLink": container.css(".category-page-item-content-wrapper a::attr(href)").get(),
    #             "source": "EW",
    #             "published": {
    #                 "timestamp": container.css(".category-page-item-content-wrapper").css(".categoryPageItemInfo").css(
    #                     ".category-page-item-timestamp::text").get(),
    #                 "date": None
    #             }
    #         })

    #     Entertainment.__news.append({
    #         "publisher": "EW",
    #         "articles": all_articles
    #     })

    # def imdb_trailers(self, videos_list):
    #     containers = self.response.css(".ipc-poster-card")
    #     videos = []
    #     previous_titles = []
    #     for container in containers:
    #         title = container.css("a.ipc-poster-card__title::text").get()
    #         image = container.css("div.ipc-media__img img::attr(src)").get()
    #         url = container.css("a.ipc-lockup-overlay::attr(href)").get()

    #         if title in previous_titles or url is None or image is None:
    #             continue
    #         else:
    #             previous_titles.append(title)

    #         videos.append({
    #             "title": title.strip() if title is not None else None,
    #             "image": image,
    #             "followUpLink": "https://www.imdb.com{}".format(url),
    #             "genre": container.css(".ipc-poster-card__top::text").get(),
    #             "source": "Imdb",
    #             "published": {
    #                 "timestamp": None,
    #                 "date": None
    #             }
    #         })

    #     videos_list.append({
    #         "publisher": "Imdb",
    #         "articles": videos
    #     })

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
            #time
            date_time = datetime.today()
            #using strftime() to get the current time value
            current_time = date_time.strftime("%I:%M %p")
            #date now
            date_now = date_time.strftime("%b %d, %Y")
            articles.append({
                "source": "Mpasho",
                "favicon": "https://mpasho.co.ke" + self.response.css('link[rel="icon"]::attr(href)').get(),
                "title": title.strip() if title is not None else None,
                "image": "https:{}".format(image),
                "genre": genre,
                "category": "Entertainment",
                "followUpLink": link,
                "time": current_time,
                "date": date_now
            })
        Entertainment.__news.append({
            "publisher": "Mpasho",
            "articles": articles
        })

    # def ghafla(self):
    #     parent = self.response.css(".col-md-9")
    #     containers = parent.css("article")
    #     articles = []
    #     previous_titles = []
    #
    #     for container in containers:
    #         title = container.css(".omega h3 a::text").get()
    #         link = container.css(".omega h3 a::attr(href)").get()
    #         image = container.css(".alpha img::attr(src)").get()
    #         if title in previous_titles or title is None:
    #             continue
    #         else:
    #             previous_titles.append(title)
    #         articles.append({
    #             "title": title.strip() if title is not None else None,
    #             "image": image,
    #             "source": "Ghafla",
    #             "genre": None,
    #             "followUpLink": link,
    #             "published": {
    #                 "timestamp": None,
    #                 "date": container.css(".blog-date a::text").get()
    #             }
    #         })
    #     Entertainment.__news.append({
    #         "publisher": "Ghafla",
    #         "articles": articles
    #     })

    # def tuko(self):
    #     containers = self.response.css("article")
    #     articles = []
    #     previous_titles = []

    #     for container in containers:
    #         title = container.css("span::text").get()
    #         link = container.css("a::attr(href)").get()
    #         image = container.css(".thumbnail-picture__img::attr(src)").get()
    #         date = container.css(".c-article-info__time--clock::text").get()
    #         if title in previous_titles or title is None:
    #             continue
    #         else:
    #             previous_titles.append(title)
    #         articles.append({
    #             "title": title.strip() if title is not None else None,
    #             "image": image,
    #             "source": "Tuko",
    #             "genre": None,
    #             "followUpLink": link,
    #             "published": {
    #                 "timestamp": container.css(".c-article-info__time--clock::attr(datetime)").get(),
    #                 "date": date.strip() if date is not None else date
    #             }
    #         })
    #     Entertainment.__news.append({
    #         "publisher": "Tuko",
    #         "articles": articles
    #     })

    def aggregator(self):
        # if self.url == 'https://www.imdb.com/trailers/':
        #     self.imdb_trailers(videos_list)
        # elif self.url == 'https://ew.com/':
        #     self.ew_news()
        # elif self.url == 'https://mpasho.co.ke/entertainment/':
        self.mpasho()
        # elif self.url == "http://www.ghafla.com/ke/tag/ghafla-entertainment-news/":
        #     self.ghafla()
        # elif self.url == "https://www.tuko.co.ke/entertainment/":
        #     self.tuko()

    @property
    def news(self):
        data = {
            "category": "Entertainment",
            "category_id": 2,
            "news": Entertainment.__news,
        }
        return data




