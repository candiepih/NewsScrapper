from db.mongo_connection import PymongoDBConnection

conn = PymongoDBConnection()
client = conn.client
db = conn.get_collection()
