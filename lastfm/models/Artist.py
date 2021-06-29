from typing import Set

import lastfm.models.Album as Album
from lastfm.models.PrettyPrintable import PrettyPrintable
from mongo.Cacheable import Cacheable


class Artist(Cacheable, PrettyPrintable):
    _ARTISTS = dict()
    COLLECTION_NAME = "artists"

    def __new__(cls, artist_name: str):
        artist_id = artist_name
        if artist_id not in Artist._ARTISTS:
            new_artist = super(Artist, cls).__new__(cls)
            new_artist._init(artist_name)
            Artist._ARTISTS[artist_id] = new_artist
        return Artist._ARTISTS.get(artist_id)

    def _init(self, artist_name: str):
        Cacheable._init(self, self.COLLECTION_NAME)
        self.name = artist_name
        self.albums: Set[Album.Album] = set()
        self.save()

    @property
    def num_listens(self):
        return sum([album.num_listens for album in self.albums])

    @property
    def unique_id(self):
        return (self.name,)

    def __eq__(self, other):
        if isinstance(other, Artist):
            return self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)

    @staticmethod
    def load(o: object):
        return Artist(o["name"])

    def as_dict(self):
        return {
            "name": self.name,
            "albums": list(self.albums),
        }
