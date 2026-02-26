from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Catch


class CatchForm(forms.ModelForm):
    # override length field to ensure proper numeric validation and allow blank
    length = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )

    class Meta:
        model = Catch
        fields = ['date', 'species', 'venue', 'method', 'bait', 'length', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_length(self):
        """Convert empty values to ``None`` so the model can handle nulls."""
        length = self.cleaned_data.get('length')
        if length in (None, ''):
            return None
        return length


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
