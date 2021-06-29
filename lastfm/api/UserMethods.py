from datetime import datetime, timezone
from functools import partial
from operator import is_not
from typing import List, Optional

import requests

from lastfm.api.Methods import Methods
from lastfm.models.Listen import Listen
from lastfm.models.Song import Song
from lastfm.models.User import User


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

    def _map_recent_tracks(self, user: User, tracks: List[dict]) -> List[Listen]:
        def map_response_track(track: dict) -> Optional[Listen]:
            try:
                now_playing = track["@attr"]["nowplaying"]
                if now_playing == "true":
                    return None
            except KeyError:
                pass
            song = Song(track["name"], track["album"]["#text"], track["artist"]["#text"])
            return Listen(user, song, datetime.fromtimestamp(int(track["date"]["uts"]), timezone.utc))
        return list(filter(partial(is_not, None), map(map_response_track, tracks)))

    def get_recent_tracks(self, user: User, limit: Optional[int]=200, page: Optional[int]=None,
                          from_: Optional[datetime]=None, to: Optional[datetime]=None,
                          extended: Optional[bool]=None) -> List[Listen]:
        res = self._get_recent_tracks(user, limit, page, from_, to, extended)
        return self._map_recent_tracks(user, res["recenttracks"]["track"])

    def get_all_tracks(self, user: User) -> List[Listen]:
        all_songs = []

        page = 1
        total_pages = 1
        while page <= total_pages:
            res = self._get_recent_tracks(user, page=page, from_=datetime.utcfromtimestamp(0))
            attr = res["recenttracks"]["@attr"]
            total_pages = int(attr["totalPages"])
            page = int(attr["page"]) + 1

            page_songs = self._map_recent_tracks(user, res["recenttracks"]["track"])
            all_songs.extend(page_songs)

        user.listens.update(all_songs)
        return all_songs
