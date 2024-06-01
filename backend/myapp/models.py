from django.db import models

# For creating and joining events
class Event(models.Model):
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
    
    def __str__(self):
        return self.event_name