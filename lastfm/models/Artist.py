from typing import Set

from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Album as Album


class Artist(PrettyPrintable):
    _ARTISTS = dict()

    def __new__(cls, artist_name: str):
        artist_id = artist_name
        if artist_id not in Artist._ARTISTS:
            new_artist = super(Artist, cls).__new__(cls)
            new_artist.init(artist_name)
            Artist._ARTISTS[artist_id] = new_artist
        return Artist._ARTISTS.get(artist_id)

    def init(self, artist_name: str):
        self.name = artist_name
        self.albums: Set[Album.Album] = set()

    @property
    def num_listens(self):
        return sum([album.num_listens for album in self.albums])

    def __eq__(self, other):
        if isinstance(other, Artist):
            return self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash(self.name)

    @property
    def dict_representation(self):
        return {
            "name": self.name,
            "albums": self.albums,
        }
