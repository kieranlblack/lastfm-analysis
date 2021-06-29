import lastfm.models.Album as Album
import lastfm.models.Artist as Artist
from lastfm.models.PrettyPrintable import PrettyPrintable
from mongo.Cacheable import Cacheable


class Song(Cacheable, PrettyPrintable):
    _SONGS = dict()
    COLLECTION_NAME = "songs"

    def __new__(cls, song_name: str, album_name: str, artist_name: str):
        song_id = (song_name, album_name, artist_name)
        if song_id not in Song._SONGS:
            new_song = super(Song, cls).__new__(cls)
            new_song._init(song_name, album_name, artist_name)
            Song._SONGS[song_id] = new_song
        song = Song._SONGS.get(song_id)
        song.num_listens += 1
        return song

    def _init(self, song_name: str, album_name: str, artist_name: str):
        Cacheable._init(self, self.COLLECTION_NAME)
        self.name = song_name
        self.album = Album.Album(album_name, artist_name)
        self.artist = Artist.Artist(artist_name)
        self.num_listens = 0
        self._fully_loaded = False
        self._duration = None

        self.album.songs.add(self)
        self.save()
        self.album.save()

    def _resolve_full_song(self):
        # self._track_methods.get_info(self)
        pass

    @property
    def duration(self):
        if not self._fully_loaded:
            self._resolve_full_song()
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def unique_id(self):
        return (self.name, self.album, self.artist)

    def __eq__(self, other):
        if isinstance(other, Song):
            return self.name == other.name and self.album == other.album and self.artist == other.artist
        return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)

    @staticmethod
    def load(o: object):
        return Song(o["name"], o["album"], o["artist"])

    def as_dict(self):
        return {
            "name": self.name,
            "artist": self.artist.name,
            "album": self.album.name,
            "duration": self._duration,
        }
