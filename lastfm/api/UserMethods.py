from datetime import datetime
from functools import partial
from operator import is_not
from typing import List, Optional

import requests

from lastfm.api.Methods import Methods
from lastfm.models.User import User
from lastfm.models.Song import Song


class UserMethods(Methods):
    def _get_recent_tracks(self, user: User, limit: Optional[int]=200, page: Optional[int]=None,
                          from_: Optional[datetime]=None, to: Optional[datetime]=None,
                          extended: Optional[bool]=None) -> requests.Response:
        params = {
            "username": user.username,
            "limit": limit,
            "page": page,
            "from": (from_ - datetime.utcfromtimestamp(0)).total_seconds() if from_ else None,
            "to": to.timestamp() if to else None,
            "extended": extended,
        }
        return self._get_request("user.getrecenttracks", params)

    def _map_recent_tracks(self, tracks: List[dict]) -> List[Song]:
        def map_response_track(track):
            try:
                now_playing = track["@attr"]["nowplaying"]
                if now_playing == "true":
                    return None
            except KeyError:
                pass
            return Song(track["name"], track["artist"]["#text"], track["album"]["#text"])
        return list(filter(partial(is_not, None), map(map_response_track, tracks)))

    def get_recent_tracks(self, user: User, limit: Optional[int]=200, page: Optional[int]=None,
                          from_: Optional[datetime]=None, to: Optional[datetime]=None,
                          extended: Optional[bool]=None):
        res = self._get_recent_tracks(user, limit, page, from_, to, extended)
        return self._map_recent_tracks(res["recenttracks"]["track"])

    def get_all_tracks(self, user: User) -> List[Song]:
        all_songs = []

        page = 1
        total_pages = 1
        while page <= total_pages:
            res = self._get_recent_tracks(user, page=page, from_=datetime.utcfromtimestamp(0))
            attr = res["recenttracks"]["@attr"]
            total_pages = int(attr["totalPages"])
            page = int(attr["page"]) + 1

            page_songs = self._map_recent_tracks(res["recenttracks"]["track"])
            all_songs.extend(page_songs)

        return all_songs
