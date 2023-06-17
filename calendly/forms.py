from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Event


class EventCreationForm(forms.ModelForm):
    name = forms.CharField(label="Event title", max_length=150, required=True)
    max_amount_of_joiners = forms.IntegerField(
        min_value=1,
        max_value=32767,
        label="Maximum amount of invitees",
        initial=1,
    )

    class Meta:
        model = Event
        fields = ["name", "start_time", "end_time", "max_amount_of_joiners", "hidden"]
        widgets = {
            "start_time": DateTimePickerInput(
                options={
                    "showTodayButton": True,
                    "minDate": timezone.now().date(),
                }
            ),
            "end_time": DateTimePickerInput(
                options={
                    "showTodayButton": True,
                },
                range_from="start_time",
            ),
        }
        help_texts = {"hidden": "Should the event be hidden from users without link?"}

    def __init__(self, *args, **kwargs):
        self._user_created = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        if start_time and start_time < timezone.now():
            raise forms.ValidationError("Start time cannot be in the past.")

        return cleaned_data

    def save(self, commit=True):
        event = super().save(commit=False)
        event.user_created = self._user_created
        if commit:
            event.save()
        return event


class EventUpdatingForm(forms.ModelForm):
    name = forms.CharField(label="Event title", max_length=150, required=True)
    max_amount_of_joiners = forms.IntegerField(label="Maximum amount of invitees", initial=1)

    class Meta:
        model = Event
        fields = ["name", "start_time", "end_time", "max_amount_of_joiners", "hidden"]
        widgets = {
            "start_time": DateTimePickerInput(
                options={
                    "showTodayButton": True,
                }
            ),
            "end_time": DateTimePickerInput(
                options={
                    "showTodayButton": True,
                },
                range_from="start_time",
            ),
        }
        help_texts = {"hidden": "Should the event be hidden from users without link?"}

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        if start_time and start_time < timezone.now():
            raise forms.ValidationError("Start time cannot be in the past.")

        return cleaned_data


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
