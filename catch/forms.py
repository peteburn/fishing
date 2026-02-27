from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Catch


class CatchForm(forms.ModelForm):
    # override length field to ensure proper numeric validation and allow blank
    length = forms.DecimalField(
        required=True,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )

    class Meta:
        model = Catch
        fields = ['date', 'species', 'venue', 'method', 'bait', 'length', 'weight', 'picture', 'comments']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add any comments (optional)'}),
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
    accept_rules = forms.BooleanField(
        required=True,
        label="I confirm that I have read and accept the rules of the challenge",
        error_messages={
            'required': 'You cannot register until you have accepted the rules.'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'accept_rules']
