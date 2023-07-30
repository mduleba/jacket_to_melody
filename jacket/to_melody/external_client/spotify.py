from dataclasses import dataclass
from functools import cached_property

import requests
import json

from requests import Response


class SpotifyClient:

    url = "https://spotify23.p.rapidapi.com/search/"

    # https://rapidapi.com/Glavier/api/spotify23
    headers = {
        "X-RapidAPI-Key": "585bcd3644mshb5fe0ff59afa106p12c81ejsn723fd5d7e60d",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    def get(self, q: str, **kwargs):
        querystring = {
            "type": "multi",
            "offset": "0",
            "limit": "10",
            "numberOfTopResults": "5"
        }
        querystring.update(kwargs)
        querystring['q'] = q
        return requests.get(self.url, headers=self.headers, params=querystring)


@dataclass
class SpotifyData:
    response: Response

    @cached_property
    def data(self):
        return json.loads(self.response.text)
