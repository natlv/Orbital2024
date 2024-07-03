from django.contrib import admin
from .models import Event, UserProfile, Rewards, EventParticipants

# Register your models here.
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Rewards)
admin.site.register(EventParticipants)