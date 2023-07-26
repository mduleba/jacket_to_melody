from django.shortcuts import render, redirect
from .models import Song, Game
from django.http import Http404
import random


def main_menu(request):
    scores = Game.objects.first()
    context = {
        'blue_score': scores.blue_team_score if scores else 0,
        'red_score': scores.red_team_score if scores else 0,
        'songs_left': Song.objects.filter(drawn=False).count(),
        'songs_total': Song.objects.all().count()
    }
    return render(request, 'main_menu.html', context)


def random_song(request):
    songs = Song.objects.filter(drawn=False)
    if len(songs) == 0:
        return redirect('main_menu')

    song = random.choice(songs)
    song.drawn = True
    song.save()

    game = Game.objects.first()
    if not game:
        game = Game.objects.create()
    context = {
        'song': song,
        'game': game,
        'songs_left': Song.objects.filter(drawn=False).count() + 1,
        'songs_total': Song.objects.all().count()
    }
    return render(request, 'random_song.html', context)


def increase_score(request, team):
    game = Game.objects.first()
    if team == "blue":
        game.blue_team_score += 1
    elif team == "red":
        game.red_team_score += 1
    game.save()
    return redirect('random_song')


def reset_score(request):
    scores = Game.objects.first()
    if scores:
        scores.blue_team_score = 0
        scores.red_team_score = 0
        scores.save()

    Song.objects.update(drawn=False)
    return redirect('main_menu')
