import json
import hashlib
from abc import ABC, abstractmethod
from typing import Tuple


from pymongo.results import InsertOneResult

from mongo.Mongo import Mongo


class Cacheable(ABC):
    def _init(self, collection: str):
        self._collection = collection

    @abstractmethod
    def as_dict(self):
        pass

    @property
    @abstractmethod
    def unique_id(self) -> Tuple[str]:
        pass

    @staticmethod
    @abstractmethod
    def load(self, o: object):
        pass

    @property
    @staticmethod
    @abstractmethod
    def COLLECTION_NAME(self):
        pass

    def save(self) -> InsertOneResult:
        def recurse_hash(o, base_hash=None):
            if not base_hash:
                base_hash = hashlib.md5()
            new_hash = base_hash.copy()
            for element in o:
                try:
                    new_hash.update(element.encode())
                except AttributeError:
                    new_hash = recurse_hash(element.unique_id, new_hash)
            return new_hash
        def default_to_as_dict(o):
            try:
                return o.as_dict()
            except AttributeError:
                raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
        me = json.loads(json.dumps(self.as_dict(), ensure_ascii=False, default=default_to_as_dict))
        me["unique_hash"] = recurse_hash(self.unique_id).hexdigest()
        return Mongo.instance.upsert(self._collection, me)
