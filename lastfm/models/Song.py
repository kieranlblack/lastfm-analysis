from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Album as Album
import lastfm.models.Artist as Artist


class Song(PrettyPrintable):
    _SONGS = dict()

    def __new__(cls, song_name: str, album_name: str, artist_name: str):
        song_id = (song_name, album_name, artist_name)
        if song_id not in Song._SONGS:
            new_song = super(Song, cls).__new__(cls)
            new_song.init(song_name, album_name, artist_name)
            Song._SONGS[song_id] = new_song
        song = Song._SONGS.get(song_id)
        song.num_listens += 1
        return song

    def init(self, song_name: str, album_name: str, artist_name: str):
        self.name = song_name
        self.album = Album.Album(album_name, artist_name)
        self.artist = Artist.Artist(artist_name)
        self.num_listens = 0
        self._fully_loaded = False
        self._duration = None

        self.album.songs.add(self)

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

    def __eq__(self, other):
        if isinstance(other, Song):
            return self.name == other.name and self.album == other.album and self.artist == other.artist
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.album, self.artist))

    @property
    def dict_representation(self):
        return {
            "name": self.name,
            "artist": self.artist.name,
            "album": self.album.name,
            "duration": self._duration,
        }
