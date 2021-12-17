from datetime import datetime

class TopBuzz:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def kenyans(self):
        parent = self.response.css(".item-list")
        containers = parent.css("li")
        articles = []
        previous_titles = []
        for container in containers:
            title = container.css(".news-title a::text").get()
            link = container.css(".news-title a::attr(href)").get()
            if title in previous_titles or title is None or link is None:
                continue
            else:
                previous_titles.append(title)
            link = "https://www.kenyans.co.ke" + link
            image = container.css(".news-image img::attr(data-src)").get()
            image = "https://www.kenyans.co.ke" + image if image is not None else image
            #time
            date_time = datetime.today()
            #using strftime() to get the current time value
            current_time = date_time.strftime("%I:%M %p")
            #date now
            date_now = date_time.strftime("%b %d, %Y")
            articles.append({
                "source": "Kenyans",
                "favicon": "https://www.kenyans.co.ke" + self.response.css('link[rel="shortcut icon"]::attr(href)').get(),
                "title": title.strip() if title is not None else None,
                "image": image,
                "genre": container.css(".news-secondary a::text").get(),
                "category": 'Top Buzz',
                "followUpLink": link,
                "time": current_time,
                "date": date_now
            })

        TopBuzz.__news.append({
            "publisher": "Kenyans",
            "articles": articles
        })

    # def tuko(self):
    #     parent = self.response.css(".l-taxonomy-page-hero")
    #     containers = parent.css("article")
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

    #     TopBuzz.__news.append({
    #         "publisher": "Tuko",
    #         "articles": articles
    #     })

    def aggregator(self):
        if self.url == "https://www.kenyans.co.ke/news":
            self.kenyans()

    @property
    def news(self):
        data = {
            "category": "Top Buzz",
            "category_id": 7,
            "news": TopBuzz.__news,
        }
        return data


