from django import forms
from django.contrib import admin

from .downloaders.from_yt import YTSong
from .models import Song


class SongAddForm(forms.ModelForm):
    url = forms.CharField()

    class Meta:
        model = Song
        fields = ['url']  # Define your fields for "Add" view

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
    class Meta:
        model = Song
        fields = ['title', 'author', 'drawn', 'audio_file']


class SongAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return SongAddForm
        else:
            return SongChangeForm


admin.site.register(Song, SongAdmin)
