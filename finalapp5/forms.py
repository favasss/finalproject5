from django import forms
from .models import Review
from finalapp5.models import Movie
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['name','year','actors','trailer_link','description','image','user','category']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
