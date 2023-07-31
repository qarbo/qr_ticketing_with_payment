import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm

from booking.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        del self.fields['password1']
        # self.fields['password1'].help_text = None
        # self.fields['username'].help_text = None

    def clean_username(self):
        return self.cleaned_data['email']

    def save(self, commit=True):
        # Perform additional actions or custom logic here
        instance = super().save(commit=False)
        instance.username = uuid.uuid4()

        if commit:
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number']
