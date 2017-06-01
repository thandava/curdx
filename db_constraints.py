import pymongo

client = pymongo.MongoClient()

db = client.service_registry

#set unique keys on id field for profiles, services and providers collection.

db.profiles.create_index([('id', pymongo.ASCENDING)], unique=True)
db.services.create_index([('id', pymongo.ASCENDING)], unique=True)
db.providers.create_index([('id', pymongo.ASCENDING)], unique=True)
