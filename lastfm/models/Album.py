from typing import Set

import lastfm.models.Artist as Artist
import lastfm.models.Song as Song
from lastfm.models.PrettyPrintable import PrettyPrintable
from mongo.Cacheable import Cacheable


class Album(Cacheable, PrettyPrintable):
    _ALBUMS = dict()
    COLLECTION_NAME = "albums"

    def __new__(cls, album_name: str, artist_name: str):
        album_id = (album_name, artist_name)
        if album_id not in Album._ALBUMS:
            new_album = super(Album, cls).__new__(cls)
            new_album._init(album_name, artist_name)
            Album._ALBUMS[album_id] = new_album
        return Album._ALBUMS.get(album_id)

    def _init(self, album_name: str, artist_name: str):
        Cacheable._init(self, self.COLLECTION_NAME)
        self.name = album_name
        self.artist = Artist.Artist(artist_name)
        self.songs: Set[Song.Song] = set()

        self.artist.albums.add(self)
        self.save()
        self.artist.save()

    @property
    def num_listens(self):
        return sum([song.num_listens for song in self.songs])

    @property
    def unique_id(self):
        return (self.name, self.artist)

    def __eq__(self, other):
        if isinstance(other, Album):
            return self.name == other.name and self.artist == other.artist
        return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)

    @staticmethod
    def load(o: object):
        return Album(o["name"], o["artist"])

    def as_dict(self):
        return {
            "name": self.name,
            "artist": self.artist.name,
            "songs": list(self.songs)
        }
