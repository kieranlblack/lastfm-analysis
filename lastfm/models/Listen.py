from datetime import datetime, timezone
from lastfm.models.PrettyPrintable import PrettyPrintable
import lastfm.models.Song as Song


class Listen(PrettyPrintable):
    def __init__(self, song: Song.Song, timestamp: int):
        self.song = song
        self.time = datetime.fromtimestamp(timestamp, timezone.utc)

    def __eq__(self, other):
        if isinstance(other, Listen):
            return self.song == other.song and self.time == other.time
        return NotImplemented

    def __hash__(self):
        return hash((self.song, self.time))

    def dict_representation(self):
        return {
            "song": self.song,
            "time": self.time.isoformat(),
        }
