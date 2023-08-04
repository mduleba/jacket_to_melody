from django.db import models
from dataclasses import dataclass
from functools import cached_property

import requests
import json


class Song(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='songs/')
    drawn = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Game(models.Model):
    blue_team_score = models.IntegerField(default=0)
    red_team_score = models.IntegerField(default=0)


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
