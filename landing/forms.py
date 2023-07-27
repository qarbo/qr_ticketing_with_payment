from django import forms
from django.contrib.auth.forms import UserCreationForm

from booking.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_username(self):
        return self.cleaned_data['email']

    def save(self, commit=True):
        # Perform additional actions or custom logic here
        instance = super().save(commit=False)
        instance.username = instance.email

        if commit:
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']
