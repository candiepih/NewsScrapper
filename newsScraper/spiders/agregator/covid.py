class Covid:
    __news = []

    def __init__(self, response):
        self.response = response
        self.url = response.url
        self.aggregator()

    def citizen(self):
        container = self.response.xpath("//table/tr")[1]
        tds = container.css("td")
        articles = [
            {
                "location": tds[0].css("::text")[0].get(),
                "confirmed": tds[1].css("::text")[0].get(),
                "recovered": tds[2].css("::text")[0].get(),
                "deaths": tds[3].css("::text")[0].get()
            },
            {
                "location": "Global",
                "confirmed": tds[1].css("::text")[1].get().strip(),
                "recovered": tds[2].css("::text")[1].get().strip(),
                "deaths": tds[3].css("::text")[1].get().strip()
            }
        ]
        Covid.__news.append({
            "publisher": "Citizentv",
            "articles": articles
        })

    def aggregator(self):
        if self.url == "https://citizentv.co.ke/":
            self.citizen()

    @property
    def news(self):
        data = {
            "category": "Covid",
            "category_id": 13,
            "news": Covid.__news,
        }
        return data
