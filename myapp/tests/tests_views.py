from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import (Event, EventParticipants, Item,
                          Message, UserProfile, UserRewards)
from django.utils import timezone
import json

class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')        
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'partials/_header.html')
        self.assertTemplateUsed(response, 'partials/_footer.html')

class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_login_view(self):
        login_url = reverse('login')

        login_data = {
            'username': 'testuser',
            'password': 'password',
        }

        response = self.client.post(login_url, data=login_data)

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

        home_url = reverse('home')
        
        self.assertRedirects(response, home_url)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_login_view_invalid_credentials(self):
        login_url = reverse('login')

        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        response = self.client.post(login_url, login_data, follow=True)

        self.assertEqual(response.status_code, 200)

        user = response.context['user']
        self.assertFalse(user.is_authenticated)