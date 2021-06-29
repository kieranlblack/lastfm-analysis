from typing import Optional

import lastfm.models.Song as Song
import lastfm.models.User as User
from lastfm.api.Methods import Methods


class TrackMethods(Methods):
    def get_info(self, song: Song.Song, user: Optional[User.User]=None):
        params = {
            "track": song.name,
            "artist": song.artist.name,
            "username": user.username if user is not None else None,
        }
        res = self._get_request("track.getInfo", params)
        song.duration = res["track"]["duration"] * (10 ** -3)
        song.listeners = res["track"]["listeners"]
        song.playcount = res["track"]["playcount"]
        return song
