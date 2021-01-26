# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class NewsscraperPipeline:
    def __init__(self):
        password = "mutheeal.am."
        client = pymongo.MongoClient(
        "mongodb+srv://candiepih:" + password + "@cluster0.1fcmf.mongodb.net/news?retryWrites=true&w=majority")

        with client:
            self.db = client.news
            self.businessCollection = self.db["business"]
            self.entertainmentCollection = self.db["entertainment"]
            self.sportCollection = self.db["sport"]
            self.techCollection = self.db["technology"]
            self.fashionCollection = self.db["fashion"]
            self.worldCollection = self.db["world"]

    def update_data(self, collection, item):
        query = {"category_id": item['category_id']}
        new_data = {"$set": {"articles": item["articles"]}}
        collection.update_many(query, new_data)

    def process_item(self, item, spider):
        self.businessCollection.insert(dict(item['businessNews'])) if "business" not in self.db.list_collection_names() else self.update_data(self.businessCollection, item['businessNews'])
        self.entertainmentCollection.insert(dict(item['entertainmentNews'])) if "entertainment" not in self.db.list_collection_names() else self.update_data(self.entertainmentCollection, item['entertainmentNews'])
        self.sportCollection.insert(dict(item['sportNews'])) if "sport" not in self.db.list_collection_names() else self.update_data(self.sportCollection, item['sportNews'])
        self.techCollection.insert(dict(item['techNews'])) if "technology" not in self.db.list_collection_names() else self.update_data(self.techCollection, item['techNews'])
        self.fashionCollection.insert(dict(item['fashionNews'])) if "fashion" not in self.db.list_collection_names() else self.update_data(self.fashionCollection, item['fashionNews'])
        self.worldCollection.insert(dict(item['worldNews'])) if "world" not in self.db.list_collection_names() else self.update_data(self.worldCollection, item['worldNews'])

        return item
