from typing import Set

from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Listen as Listen


class User(PrettyPrintable):
    def __init__(self, username: str):
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
    def dict_representation(self):
        return {
            "username": self.username,
            "listens": self.listens,
        }
