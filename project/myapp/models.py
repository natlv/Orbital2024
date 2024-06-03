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