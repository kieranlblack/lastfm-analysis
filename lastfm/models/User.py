from typing import List

from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Song as Song


class User(PrettyPrintable):
    def __init__(self, username: str):
        self.username = username
        self.songs: List[Song.Song] = None

    @property
    def dict_representation(self):
        return {
            "username": self.username,
            "songs": self.songs,
        }
