from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, UserProfile, Item, Message
from PIL import Image
import io

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': "Please enter your username.",
                'unique': "This username is already taken.",
            },
            'password1': {
                'required': "Please enter a password.",
            },
            'password2': {
                'required': "Please confirm your password.",
            },
        }

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
            raise forms.ValidationError("Event end time cannot be before the start time.")
        
        if not event_start:
            raise forms.ValidationError("Event start time is required.")
        
        elif not event_end:
            event_end = event_start
            cleaned_data['event_end'] = event_end
        
        if event_end < timezone.now():
            raise forms.ValidationError("Event end time cannot be before the current date and time.")

        return cleaned_data

class EventJoinForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    email = forms.EmailField(label="Your email")

class EventSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Keyword')
    event_type = forms.ChoiceField(
        required=False,
        choices=[
        ['any', 'Any'],
        ('cleanup', 'Environmental Clean-up'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('planting', 'Tree Planting'),
        ('recycling', 'Recycling / Composting'),
        ('other', 'Other'),
    ], label='Event Type'
    )

class ProfileForm(forms.ModelForm):
    upload_pic = forms.FileField(required=False) 

    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']  

    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=False)
        upload_pic = self.cleaned_data.get('upload_pic')

        if upload_pic:
            image = Image.open(upload_pic)
            instance.save_image(image)

        if commit:
            instance.save()
        return instance

class ItemForm(forms.ModelForm):
    upload_image = forms.FileField(required=False) 

    class Meta:
        model = Item
        fields = ['name', 'description', 'price']
 
    def save(self, commit=True):
        instance = super(ItemForm, self).save(commit=False)
        upload_image = self.cleaned_data.get('upload_image')

        if upload_image:
            image = Image.open(upload_image)
            instance.save_image(image)

        if commit:
            instance.save()
        return instance

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }