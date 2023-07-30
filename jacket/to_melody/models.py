from django.db import models


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
