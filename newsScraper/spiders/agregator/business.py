import json


class Business:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def business_insider(self):
        containers = self.response.css(".layout-item")
        articles = []
        previous_titles = []
        for container in containers:
            title = container.css("div.gradient-overlay a::attr(title)").get()
            subtitle = None
            # stripping title to prepare for filtering
            new_title = title.strip() if title is not None else None
            if new_title in previous_titles:
                continue
            else:
                previous_titles.append(new_title)

            articles.append({
                "title": title.strip() if title is not None else None,
                "subTitle": subtitle.strip() if subtitle is not None else None,
                "image": container.css("div.imageBlock picture source::attr(data-original)").get(),
                "followUpLink": container.css("div.gradient-overlay a::attr(href)").get(),
                "published": {
                    "timestamp": None,
                    "date": None,
                },
            })
        Business.__news.append({
            "publisher": "Business Insider",
            "articles": articles
        })

    def business_daily(self):
        containers = self.response.css("article")
        articles = []
        previous_titles = []

        for container in containers:
            title = container.css("header .article-list-featured-title::text").get()
            if title is None:
                title = container.css("header .article-list-small-title::text").get()
                if title is None:
                    other_title = container.css("header h2::text").get()
                    title = other_title if other_title is not None else container.css("header h3::text").get()
            link = container.css("header a::attr(href)").get()
            if title in previous_titles or title is None or link is None:
                continue
            else:
                previous_titles.append(title)
            link = "https://www.businessdailyafrica.com" + link
            image = container.css("img::attr(data-cm-responsive-media)").get()
            if image is not None:
                deserialized_image_data = json.loads(image)
                image = deserialized_image_data[0]["linksForWidth"]["400"]
                image = "https://www.businessdailyafrica.com" + image
            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "source": "Business Daily",
                "Genre": container.css(".article-list-small-title span::text").get(),
                "followUpLink": link,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })

        Business.__news.append({
            "publisher": "Business Daily",
            "articles": articles
        })

    def kenya_wall_street(self):
        parent = self.response.css(".jeg_inner_content")
        containers = parent.css("article")
        articles = []
        previous_titles = []
        for container in containers:
            title = container.css(".jeg_post_title a::text").get()
            link = container.css(".jeg_post_title a::attr(href)").get()
            image = container.css("img::attr(src)").get()
            date = container.css(".jeg_meta_date a::text").get()

            new_title = title.strip() if title is not None else None
            if new_title in previous_titles:
                continue
            else:
                previous_titles.append(new_title)

            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "followUpLink": link,
                "source": "Kenyan Wall Street",
                "Genre": container.css(".jeg_post_category a::text").get(),
                "published": {
                    "timestamp": None,
                    "date": date.strip() if date is not None else date,
                },
            })
        Business.__news.append({
            "publisher": "Kenyan Wall Street",
            "articles": articles
        })

    def aggregator(self):
        if self.url == 'https://africa.businessinsider.com/':
            self.business_insider()
        elif self.url == 'https://www.businessdailyafrica.com/':
            self.business_daily()
        elif self.url == 'https://kenyanwallstreet.com/category/kenyan-news/':
            self.kenya_wall_street()

    @property
    def news(self):
        data = {
            "category": "Business",
            "category_id": 1,
            "news": Business.__news,
        }
        return data
