from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, UserProfile, EventParticipants

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventCreateForm(forms.Form):
    organisation = forms.CharField(label="Your organisation", max_length=150)
    event_name = forms.CharField(label="Name of event", max_length=150)
    event_type = forms.ChoiceField(choices=[
        ('cleanup', 'Environmental Clean-up'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('planting', 'Tree Planting'),
        ('recycling', 'Recycling / Composting'),
        ('other', 'Other'),
    ], required=True, label='Type of Event')
    event_location = forms.CharField(label="Event Location", max_length=150)
    event_start = forms.DateTimeField(label="From (Date and Time)", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    event_end = forms.DateTimeField(label="To (Date and Time)", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EventCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['creator'] = self.request.user.username
        event_start = cleaned_data.get('event_start')
        event_end = cleaned_data.get('event_end')

        if event_start and event_end and event_end < event_start:
            raise ValidationError("Event end time cannot be before the start time.")
        
        return cleaned_data

class EventJoinForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    email = forms.EmailField(label="Your email")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), label="Select an event to join")
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date', 'profile_pic']