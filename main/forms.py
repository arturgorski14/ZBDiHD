from django import forms
from .models import *


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'director', 'cast', 'description', 'release_date', 'image')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewG
        fields = ('comment', 'rating')


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'studio', 'platform', 'description', 'release_date', 'image')
