from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventCreateForm(forms.Form):
    creator = forms.CharField(label="Your name", max_length=100)
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

class EventJoinForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    email = forms.EmailField(label="Your email")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), label="Select an event to join")