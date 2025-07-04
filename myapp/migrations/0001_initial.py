# Generated by Django 3.2.25 on 2024-07-03 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import myapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(default=myapp.models.generate_event_id, max_length=9, unique=True)),
                ('creator', models.CharField(max_length=100)),
                ('organisation', models.CharField(max_length=150)),
                ('event_name', models.CharField(max_length=150)),
                ('event_type', models.CharField(choices=[('cleanup', 'Environmental Clean-up'), ('seminar', 'Seminar'), ('workshop', 'Workshop'), ('planting', 'Tree Planting'), ('recycling', 'Recycling / Composting'), ('other', 'Other')], max_length=50)),
                ('event_location', models.CharField(max_length=150)),
                ('event_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('event_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('participants', models.ManyToManyField(blank=True, related_name='joined_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rewards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('points_cost', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='myapp/files/reward_pics')),
            ],
        ),
        migrations.CreateModel(
            name='UserRewards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_claimed', models.DateTimeField(auto_now_add=True)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rewards')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='myapp/files/profile_pics')),
                ('points', models.IntegerField(default=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='myapp/files/marketplace_pics/')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('contact_number', models.CharField(default='', max_length=15)),
                ('attended', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
