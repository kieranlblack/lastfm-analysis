from typing import Any, List, Optional

import pymongo
from pymongo.results import InsertOneResult, UpdateResult


class Mongo():
    instance: Optional["Mongo"] = None

    def __new__(cls, url: str, database_name: str, username: str, password: str):
        if Mongo.instance is None:
            new_instance = super(Mongo, cls).__new__(cls)
            new_instance._init(url, database_name, username, password)
            Mongo.instance = new_instance
        return Mongo.instance

    def _init(self, url: str, database_name: str, username: str, password: str):
        self.database_name = database_name
        self._client = pymongo.MongoClient(url, username=username, password=password)
        self._database = self._client[self.database_name]

    def find(self, collection: str, filter_: str):
        return self._database[collection].find_one(filter_)

    def find_all(self, collection: str) -> List[Any]:
        all_items = []
        for document in self._database[collection].find(cursor_type=pymongo.CursorType.EXHAUST).sort([("$natural", 1)]):
            all_items.append(document)
        return all_items

    def insert(self, collection: str, o: object) -> InsertOneResult:
        return self._database[collection].insert_one(o)

    def upsert(self, collection: str, o: object) -> UpdateResult:
        return self._database[collection].replace_one({"unique_hash": o["unique_hash"]}, o, upsert=True)
