from typing import Set

from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Artist as Artist
import lastfm.models.Song as Song


class Album(PrettyPrintable):
    _ALBUMS = dict()

    def __new__(cls, album_name: str, artist_name: str):
        album_id = (album_name, artist_name)
        if album_id not in Album._ALBUMS:
            new_album = super(Album, cls).__new__(cls)
            new_album.init(album_name, artist_name)
            Album._ALBUMS[album_id] = new_album
        return Album._ALBUMS.get(album_id)

    def init(self, album_name: str, artist_name: str):
        self.name = album_name
        self.artist = Artist.Artist(artist_name)
        self.songs: Set[Song.Song] = set()

        self.artist.albums.add(self)

    @property
    def num_listens(self):
        return sum([song.num_listens for song in self.songs])

    def __eq__(self, other):
        if isinstance(other, Album):
            return self.name == other.name and self.artist == other.artist
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.artist))

    @property
    def dict_representation(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "songs": self.songs
        }
