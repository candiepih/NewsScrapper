# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class NewsscraperPipeline:
    def __init__(self):
        # password = "mutheeal.am."
        # self.client = pymongo.MongoClient(
        #         "mongodb+srv://candiepih:" + password + "@cluster0.1fcmf.mongodb.net/news?retryWrites=true&w=majority")
        self.client = pymongo.MongoClient("localhost", 27017)
        with self.client:
            self.db = self.client.news
            self.businessCollection = self.db["business"]
            self.entertainmentCollection = self.db["entertainment"]
            self.sportCollection = self.db["sport"]
            self.techCollection = self.db["technology"]
            self.fashionCollection = self.db["lifestyle"]
            self.worldCollection = self.db["world"]

            self.topBuzzCollection = self.db["top_buzz"]
            self.eastAfricaCollection = self.db["east_africa"]
            self.politicsCollection = self.db["politics"]
            self.countiesCollection = self.db["counties"]
            self.educationCollection = self.db["education"]
            self.videosCollection = self.db["videos"]

    @staticmethod
    def update_data(collection, item):
        query = {"category_id": item['category_id']}
        # collection.find_and_modify(query=query, update={"$set": {"articles": item["articles"]}})
        if "news" in item.keys():
            collection.find_and_modify(query=query, update={"$set": {"news": item["news"]}})
        # if "videos" in item.keys():
        #     collection.find_and_modify(query=query, update={"$set": {"videos": item["videos"]}})

    def handle_collections(self, collection, item, item_name, category):
        if category not in self.db.list_collection_names():
            collection.insert(dict(item[item_name]))
        else:
            self.update_data(collection, item[item_name])

    def process_item(self, item, spider):
        if bool(item):
            self.handle_collections(self.businessCollection, item, "businessNews", "business")
            self.handle_collections(self.entertainmentCollection, item, "entertainmentNews", "entertainment")
            self.handle_collections(self.sportCollection, item, "sportNews", "sport")
            self.handle_collections(self.techCollection, item, "techNews", "technology")
            self.handle_collections(self.fashionCollection, item, "lifestyleNews", "lifestyle")
            self.handle_collections(self.worldCollection, item, "worldNews", "world")

            self.handle_collections(self.topBuzzCollection, item, "topBuzzNews", "top_buzz")
            self.handle_collections(self.eastAfricaCollection, item, "eastAfricaNews", "east_africa")
            self.handle_collections(self.politicsCollection, item, "politicsNews", "politics")
            self.handle_collections(self.countiesCollection, item, "countiesNews", "counties")
            self.handle_collections(self.educationCollection, item, "educationNews", "education")
            self.handle_collections(self.videosCollection, item, "videos", "videos")

        return item
