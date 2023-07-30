from dataclasses import dataclass
from functools import cached_property

import requests
import json

from requests import Response


class ShazamClient:
    urls = {
        'search': "https://shazam.p.rapidapi.com/search",
        'get': "https://shazam.p.rapidapi.com/songs/get-details"
    }

    headers = {
        "X-RapidAPI-Key": "585bcd3644mshb5fe0ff59afa106p12c81ejsn723fd5d7e60d",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    def search(self, term, **kwargs):
        params = {
            "locale": "en-US", "offset": "0", "limit": "5"
        }
        params.update(kwargs)
        params['term'] = term
        return requests.get(self.urls['search'], headers=self.headers, params=params)

    def get(self, key, **kwargs):
        params = {
            'locale': 'en-US'
        }
        params.update(kwargs)
        params['key'] = key
        return requests.get(self.urls['get'], headers=self.headers, params=params)


class ShazamSong:

    def __init__(self, name: str):
        self.name = name
        self.client = ShazamClient()

    @cached_property
    def search_results(self):
        response = self.client.search(self.name)
        return response.json()

    @property
    def track(self):
        tracks = self.search_results['tracks']
        hits = tracks['hits']
        return hits[0]['track']

    @property
    def key(self):
        return self.track['key']

    @cached_property
    def details(self):
        response = self.client.get(self.key)
        return response.json()




