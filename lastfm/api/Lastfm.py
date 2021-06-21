from lastfm.api.TrackMethods import TrackMethods
from lastfm.api.UserMethods import UserMethods


class Lastfm():
    def __init__(self, api_key: str) -> None:
        self.user = UserMethods(api_key)
        self.track = TrackMethods(api_key)
