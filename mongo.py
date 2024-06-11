import pymongo

class Mongo:
    def __init__(self, db_name: str, collection_name: str):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, data: dict):
        self.collection.insert_one(data)

    def insert_many(self, data: list[dict]):
        self.collection.insert_many(data)

    def find_one(self, query: dict):
        return self.collection.find_one(query)

    def find(self, query: dict):
        return self.collection.find(query)

    def update_one(self, query: dict, data: dict):
        return self.collection.update_one(query, data)

    def update_many(self, query: dict, data: dict):
        return self.collection.update_many(query, data)

    def delete_one(self, query: dict):
        return self.collection.delete_one(query)

    def delete_many(self, query: dict):
        return self.collection.delete_many(query)

    def drop(self):
        self.collection.drop()

    def count(self):
        return self.collection.count_documents({})

    def __str__(self):
        return f"Database: {self.db.name}, Collection: {self.collection.name}"

    def __repr__(self):
        return f"Database: {self.db.name}, Collection: {self.collection.name}"
