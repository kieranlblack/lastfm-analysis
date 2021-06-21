from typing import Optional

import requests


class Methods():
    _ROOT_API_URL = " http://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def _get_request(self, api_method: str, params: Optional[dict]=None) -> requests.Response:
        if params is None:
            params = {}
        params["api_key"] = self._api_key
        params["method"] = api_method
        params["format"] = "json"

        res = {}
        try:
            res = requests.get(self._ROOT_API_URL, params).json()
        except (requests.RequestException, ValueError) as err:
            print(err)

        if error := res.get("error", None):
            print(error)

        return res
