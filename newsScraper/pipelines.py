# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class NewsscraperPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        with self.client:
            self.db = self.client.news
            self.entertainmentCollection = self.db["entertainment"]
            self.sportCollection = self.db["sports"]
            self.techCollection = self.db["technology"]
            self.worldCollection = self.db["worldnews"]
            self.topBuzzCollection = self.db["top_buzz"]
            self.politicsCollection = self.db["politics"]

    @staticmethod
    def update_data(collection, item):
        # query = {"category_id": item['category_id']}
        # collection.find_and_modify(query=query, update={"$set": {"articles": item["articles"]}})
        if "news" in item.keys():
            for allarticles in item["news"]:
                for article in allarticles['articles']:
                    # print(collection.count_documents({}))
                    if collection.find({'news.articles.title': article['title']}).limit(1).count() > 0:
                        # print("it is there")
                        continue
                    else:
                        # print(article)
                        collection.update({'category_id': item['category_id']}, {'$push': {'news.$[].articles': {'$each': [article], '$position': 0} }})
        # if "videos" in item.keys():
        #     collection.find_and_modify(query=query, update={"$set": {"videos": item["videos"]}})

    def handle_collections(self, collection, item, item_name, category):
        if category not in self.db.list_collection_names():
            collection.insert(dict(item[item_name]))
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
