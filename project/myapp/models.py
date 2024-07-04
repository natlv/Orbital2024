import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# For generating unique event id
def generate_event_id():
    return uuid.uuid4().hex[:9]

# For creating and joining events
class Event(models.Model):
    event_id = models.CharField(max_length=9, unique=True, default=generate_event_id)
    creator = models.CharField(max_length=100)
    organisation = models.CharField(max_length=150)
    event_name = models.CharField(max_length=150)
    event_type = models.CharField(max_length=50, choices=[
        ('cleanup', 'Environmental Clean-up'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('planting', 'Tree Planting'),
        ('recycling', 'Recycling / Composting'),
        ('other', 'Other'),
    ])
    event_location = models.CharField(max_length=150)
    event_start = models.DateTimeField(default=timezone.now)
    event_end = models.DateTimeField(default=timezone.now)
    participants = models.ManyToManyField(User, related_name='joined_events', blank=True)
    
    def __str__(self):
        return self.event_name

class EventParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    contact_number = models.CharField(max_length=15, default='')
    attended = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + ' joined ' + self.event.event_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='myapp/files/profile_pics', null=True, blank=True)
    points = models.IntegerField(default=20)

class Rewards(models.Model):
    points = models.IntegerField(default=20)
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_cost = models.IntegerField()
    image = models.ImageField(upload_to='myapp/files/reward_pics', null=True, blank=True)

    def __str__(self):
        return self.name

class UserRewards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Rewards, on_delete=models.CASCADE)
    date_claimed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' claimed ' + self.reward.name

class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='myapp/files/marketplace_pics/')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} about {self.item.name}'