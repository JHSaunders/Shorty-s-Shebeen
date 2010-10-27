from django.forms import ModelForm

from models import *

class StoryForm(ModelForm):
    class Meta:
        model = Story

class AuthenticationDetailsForm(ModelForm):
    class Meta:
        model = User 
        fields = ("first_name","last_name","email")

class AuthorProfileForm(ModelForm):
    class Meta:
        model = AuthorProfile
