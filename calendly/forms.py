from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event


class EventCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    start_time = forms.DateTimeField(required=True)
    end_time = forms.DateTimeField(required=True)

    # TODO: rewrite datetime field to satisfy needs of calendly app
    class Meta:
        model = Event
        fields = ("name", "start_time", "end_time", "hidden")


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
