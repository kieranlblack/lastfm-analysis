from datetime import datetime
from mongo.Cacheable import Cacheable

import lastfm.models.Song as Song
import lastfm.models.User as User
from lastfm.models.PrettyPrintable import PrettyPrintable


class Listen(Cacheable, PrettyPrintable):
    COLLECTION_NAME = "listens"

    def __init__(self, user: "User.User", song: Song.Song, time: datetime):
        Cacheable._init(self, self.COLLECTION_NAME)
        self.user = user
        self.song = song
        self.time = time

    @property
    def unique_id(self):
        return (self.user, self.song, self.time.isoformat())

    def __eq__(self, other):
        if isinstance(other, Listen):
            return self.song == other.song and self.time == other.time
        return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)

    @staticmethod
    def load(o: object):
        song = Song.Song.load(o["song"])
        return Listen(o["user"], song, datetime.fromisoformat(o["time"]))

    def as_dict(self):
        return {
            "user": self.user.username,
            "song": self.song,
            "time": self.time.isoformat(),
        }
