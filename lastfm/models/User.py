from typing import Set

import lastfm.models.Listen as Listen
from lastfm.models.PrettyPrintable import PrettyPrintable
from mongo.Cacheable import Cacheable

class User(Cacheable, PrettyPrintable):
    COLLECTION_NAME = "users"

    def __init__(self, username: str):
        Cacheable._init(self, self.COLLECTION_NAME)
        self.username = username
        self.listens: Set[Listen.Listen] = set()

    @property
    def unique_songs(self):
        return {listen.song for listen in self.listens}

    @property
    def num_listens(self):
        return len(self.listens)

    @property
    def num_unique_listens(self):
        return len(self.unique_songs)

    @property
    def unique_id(self):
        return (self.username,)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.username == other.username
        return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)

    def save(self):
        for listen in self.listens:
            listen.save()
        Cacheable.save(self)

    @staticmethod
    def load(o: object):
        user = User(o["username"])
        new_listens = []
        for raw_listen in o["listens"]:
            raw_listen["user"] = user
            new_listens.append(Listen.Listen.load(raw_listen))
        user.listens = new_listens
        return user

    def as_dict(self):
        return {
            "username": self.username,
            "listens": list(self.listens),
        }
