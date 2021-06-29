from collections import namedtuple
from typing import List, Optional

from lastfm.models.Album import Album
from lastfm.models.Artist import Artist
from lastfm.models.Song import Song
from lastfm.models.User import User
from mongo.Cacheable import Cacheable
from mongo.Mongo import Mongo


LoadedResults = namedtuple("LoadedResults", "artists albums songs users")


def _load(class_: Cacheable) -> List[Cacheable]:
    raw_items = Mongo.instance.find_all(class_.COLLECTION_NAME)
    items = []
    for raw_item in raw_items:
        items.append(class_.load(raw_item))
    return items


def load_artists() -> List[Artist]:
    print("loading artists...")
    return _load(Artist)


def load_albums() -> List[Album]:
    print("loading albums...")
    return _load(Album)


def load_songs() -> List[Song]:
    print("loading songs...")
    return _load(Song)


def load_users() -> List[User]:
    print("loading users...")
    return _load(User)

def load_user(username: str) -> Optional[User]:
    print(f"loading {username}...")
    raw_user = Mongo.instance.find(User.COLLECTION_NAME, {"username": username})
    return User.load(raw_user)


def load_all():
    return LoadedResults(load_artists(), load_albums(), load_songs(), load_users())
