from django import forms
from django.contrib import admin

from .external_client.shazam import ShazamSong
from .downloaders.from_yt import YTSong
from .models import Song


class SongAddForm(forms.ModelForm):
    url = forms.CharField()

    class Meta:
        model = Song
        fields = ['tip', 'url']  # Define your fields for "Add" view

    def save(self, commit=True):
        url = self.cleaned_data['url']
        yt = YTSong(url)
        yt.download()
        yt.convert_to_mp3()
        yt.copy_to_media()

        song = super().save(commit=False)
        yt.update_song(song)

        return song


class SongChangeForm(forms.ModelForm):
    genres = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Song
        fields = ['title', 'author', 'genres', 'tip', 'polish', 'drawn', 'audio_file']


@admin.action(description="Download genre for selected song")
def find_genres(modeladmin, request, queryset):
    for song in queryset:
        shazam = ShazamSong(song.title)
        song.genres = shazam.genres
        song.save()


class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genres', 'tip', 'polish', 'drawn']
    actions = [find_genres]

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return SongAddForm
        else:
            return SongChangeForm


admin.site.register(Song, SongAdmin)
