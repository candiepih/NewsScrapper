from datetime import datetime

class Tech:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

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
            #time
            date_time = datetime.today()
            #using strftime() to get the current time value
            current_time = date_time.strftime("%I:%M %p")
            #date now
            date_now = date_time.strftime("%b %d, %Y")
            articles.append({
                "source": "The Verge",
                "favicon": self.response.css('link[rel="icon"]::attr(href)').get(),
                "title": title.strip() if title is not None else None,
                "image": image,
                'genre': "Tech",
                "category": "Technology",
                "followUpLink": container.css(".c-entry-box--compact__title a::attr(href)").get(),
                "time": current_time,
                "date": date_now
            })

        Tech.__news.append({
            "publisher": "The Verge",
            "articles": articles
        })

    # def gamespot_news(self):
    #     containers = self.response.css(".medium-span7 .card-item")
    #     articles = []
    #     previous_titles = []

    #     for container in containers:
    #         title = container.css(".card-item__content h4::text").get()
    #         image = container.css(".card-item__img img::attr(src)").get()

    #         if title in previous_titles:
    #             continue
    #         else:
    #             previous_titles.append(title)
    #         if title is None or image is None:
    #             continue

    #         link = container.css(".card-item__content a::attr(href)").get()
    #         articles.append({
    #             "title": title.strip() if title is not None else None,
    #             "followUpLink": link if link[0] != "/" else "{}{}".format(self.url, link),
    #             "image": image,
    #             "source": "Game Spot",
    #             'genre': None,
    #             "published": {
    #                 "timestamp": None,
    #                 "date": None
    #             }
    #         })
    #     Tech.__news.append({
    #         "publisher": "Game Spot",
    #         "articles": articles
    #     })

    def aggregator(self):
        # if self.url == 'https://www.theverge.com':
        self.verge_news()
        # elif self.url == 'https://www.gamespot.com':
        #     self.gamespot_news()

    @property
    def news(self):
        data = {
            "category": "Technology",
            "category_id": 4,
            "news": Tech.__news,
        }
        return data

