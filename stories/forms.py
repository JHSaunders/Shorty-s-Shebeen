from django.forms import ModelForm 
from django.forms import CheckboxSelectMultiple,ModelMultipleChoiceField
from models import *

class StoryForm(ModelForm):
    competitions =  ModelMultipleChoiceField(queryset=Competition.objects.filter(active=True),widget=CheckboxSelectMultiple,required=False)
    class Meta:
        model = Story
        widgets = {
            'genre': CheckboxSelectMultiple,
        }

class AuthenticationDetailsForm(ModelForm):
    class Meta:
        model = User 
        fields = ("first_name","last_name","email")

class AuthorProfileForm(ModelForm):
    class Meta:
        model = AuthorProfile
