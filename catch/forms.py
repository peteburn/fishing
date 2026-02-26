from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Catch


class CatchForm(forms.ModelForm):
    class Meta:
        model = Catch
        fields = ['date', 'species', 'venue', 'method', 'bait', 'length', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
