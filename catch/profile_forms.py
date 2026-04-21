from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class ProfilePasswordChangeForm(PasswordChangeForm):
    pass

from .models import Profile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
        labels = {'picture': 'Profile Picture'}
