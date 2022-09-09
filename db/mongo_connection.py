"""
Handle creation of database pymongo connections
"""
import pymongo
from config.env import env


class PymongoDBConnection:

    def __init__(self, database=None):
        self.uri = env('MONGODB_URI') or 'mongodb://localhost:27017'
        self.database = database or 'news'
        self.client = self.get_client()

    def get_client(self):
        """
        Gets the client from the current connection
        """
        return pymongo.MongoClient(self.uri)

    def get_collection(self):
        """
        Retrieves the current db object from client
        """
        return self.client[self.database]
