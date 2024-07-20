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

class SignUpTest(TestCase):

    def setUp(self):
        self.client = Client()

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_signup_view(self):
        signup_url = reverse('signup')

        """Case 1: Valid signup data"""
        valid_signup_data = {
            'username': 'testuser',
            'password1': 'password1234$',
            'password2': 'password1234$',
        }

        response = self.client.post(signup_url, data=valid_signup_data)

        self.assertEqual(response.status_code, 302)

        login_url = reverse('login')
        self.assertRedirects(response, login_url)

        """Case 2: Missing field"""
        invalid_signup_data = {
            'username': '',
            'password1': 'password1234$',
            'password2': 'password1234$',
        }

        response = self.client.post(signup_url, data=invalid_signup_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below.')
        
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

        """Case 3: Password mismatch"""
        invalid_signup_data_mismatch = {
            'username': 'testuser1',
            'password1': 'password123#',
            'password2': 'password1234$',
        }

        response = self.client.post(signup_url, data=invalid_signup_data_mismatch)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below.')
        
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        """Case 4: Username already taken"""
        invalid_signup_data_taken = {
            'username': 'testuser',
            'password1': 'password1234$',
            'password2': 'password1234$',
        }

        response = self.client.post(signup_url, data=invalid_signup_data_taken)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below.')

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertContains(response, 'This username is already taken.')


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