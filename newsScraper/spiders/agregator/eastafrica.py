import json


class EastAfrica:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def east_african(self):
        containers = self.response.css(".row .column")
        articles = []
        previous_titles = []
        for container in containers:
            title = container.css("h3 a::text").get()
            if title is None:
                title = container.css("h5 a::text").get()
            link = container.css("h3 a::attr(href)").get()
            if link is None:
                link = container.css("h5 a::attr(href)").get()
            if title in previous_titles or title is None or link is None:
                continue
            else:
                previous_titles.append(title)
            link = "https://www.theeastafrican.co.ke" + link
            image = container.css("img::attr(data-cm-responsive-media)").get()
            if image is not None:
                deserialized_image_data = json.loads(image)
                image = deserialized_image_data[0]["linksForWidth"]["400"]
                image = "https://www.businessdailyafrica.com" + image
            articles.append({
                "title": title.strip() if title is not None else None,
                "image": image,
                "source": "The EastAfrican",
                "Genre": None,
                "followUpLink": link,
                "published": {
                    "timestamp": None,
                    "date": None
                }
            })

        EastAfrica.__news.append({
            "publisher": "The EastAfrican",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://www.theeastafrican.co.ke/":
            self.east_african()

    @property
    def news(self):
        data = {
            "category": "East Africa",
            "category_id": 8,
            "news": EastAfrica.__news,
        }
        return data


