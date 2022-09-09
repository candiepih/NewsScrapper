# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from db import db


class NewsscraperPipeline:
    def __init__(self):
        self.entertainmentCollection = db["entertainment"]
        self.sportCollection = db["sports"] if db["sports"] is not None else db.create_collection('sports')
        self.techCollection = db["technology"] if db["sports"] is not None else db.create_collection('technology')
        self.worldCollection = db["worldnews"] if db["sports"] is not None else db.create_collection('worldnews')
        self.topBuzzCollection = db["top_buzz"] if db["sports"] is not None else db.create_collection('top_buzz')
        self.politicsCollection = db["politics"] if db["sports"] is not None else db.create_collection('politics')
        self.existing_titles = self.retrieve_existing_title()

    def retrieve_existing_title(self) -> dict:
        """
        Retrieve existing titles
        """
        existing_titles = {}
        collections = [self.politicsCollection, self.techCollection, self.worldCollection,
                       self.topBuzzCollection, self.entertainmentCollection, self.sportCollection]
        for collection in collections:
            cursor = list(collection.find({}))
            if not cursor:
                continue
            category = cursor[0].get('category')
            if category not in existing_titles:
                existing_titles[category] = []
            publishers = cursor[0].get('news')
            for publisher in publishers:
                articles = publisher.get('articles')
                for article in articles:
                    title = article.get('title')
                    if title in existing_titles:
                        continue
                    existing_titles[category].append(title)
        return existing_titles

    def update_data(self, collection, item):
        publishers = item.get('news')
        existing_titles: list = self.existing_titles.get(item.get('category'))
        for publisher in publishers:
            articles = publisher.get('articles')
            for article in articles:
                if article.get('title') in existing_titles:
                    continue
                query = {'category_id': item['category_id']}
                operation = {'$push': {'news.$[].articles': {'$each': [article],
                                                             '$position': 0}}}
                collection.update_one(query, operation)

    def handle_collections(self, collection, item, item_name, category):
        if category not in db.list_collection_names():
            collection.insert_one(dict(item[item_name]))
        else:
            self.update_data(collection, item[item_name])

    def process_item(self, item, spider):
        if bool(item):
            self.handle_collections(self.entertainmentCollection, item, "entertainmentNews", "entertainment")
            self.handle_collections(self.sportCollection, item, "sportNews", "sports")
            self.handle_collections(self.techCollection, item, "techNews", "technology")
            self.handle_collections(self.worldCollection, item, "worldNews", "worldnews")
            self.handle_collections(self.topBuzzCollection, item, "topBuzzNews", "top_buzz")
            self.handle_collections(self.politicsCollection, item, "politicsNews", "politics")

        return item
