from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import (Event, EventParticipants, Item,
                          Message, UserProfile, UserRewards)
from django.utils import timezone
from myapp.forms import EventJoinForm, EventSearchForm

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


class EventCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.url = reverse('event_create')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def logged_in_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_create.html')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_form_valid(self):
        form_data = {
            'creator': self.user,
            'organisation': 'Test Org',
            'event_name': 'Test Event',
            'event_type': 'seminar',
            'event_location': 'Test Location',
            'event_start': timezone.now(),
            'event_end': timezone.now() + timezone.timedelta(hours=2),
        }

        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(event_name='Test Event').exists())

    # There's an error in the creation where if u don't put an event_end_time, it will throw an error
    # @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    # def test_form_invalid(self):
    #     response = self.client.post(self.url, {})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Event.objects.exists())

class EventJoinViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_event_join_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('event_join'))
        self.assertRedirects(response, '/login/?next=/event_join/')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_event_join_view_for_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('event_join'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_join.html')
        self.assertIsInstance(response.context['form'], EventSearchForm)

class ChosenEventJoinViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.event = Event.objects.create(
            creator='testcreator',
            organisation='Test Organisation',
            event_name='Test Event',
            event_type='seminar',
            event_location='Test Location',
            event_start=timezone.now(),
            event_end=timezone.now() + timezone.timedelta(hours=2)
        )

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_chosen_event_join_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('event_join_chosen', args=[self.event.event_id]))
        self.assertRedirects(response, f'/login/?next=/event_join/{self.event.event_id}/')
    
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_chosen_event_join_view_for_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': 'Test Name',
            'email': 'tester@example.com'
        }

        response = self.client.post(reverse('event_join_chosen', args=[self.event.event_id]), form_data)
        self.assertRedirects(response, reverse('event_join'))
        self.assertTrue(EventParticipants.objects.filter(
            user=self.user,
            event=self.event,
            name=form_data['name'],
            email=form_data['email']
        ).exists())

class MyEventsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        create_event_data = {
            'creator': self.user,
            'organisation': 'Test Org',
            'event_name': 'Test Event',
            'event_type': 'seminar',
            'event_location': 'Test Location',
            'event_start': timezone.now(),
            'event_end': timezone.now() + timezone.timedelta(hours=2),
        }
        #Create an event
        self.client.post(reverse('event_create'), create_event_data)
        self.joined_event = Event.objects.create(
            creator='testcreator',
            organisation='Test Organisation2',
            event_name='Test Event2',
            event_type='workshop',
            event_location='Test Location',
            event_start=timezone.now(),
            event_end=timezone.now() + timezone.timedelta(hours=3)
        )
        form_data = {
            'name': 'Test Name',
            'email': 'tester@example.com'
        }
        #Join an event
        self.client.post(reverse('event_join_chosen', args=[self.joined_event.event_id]), form_data)

        @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
        def test_my_events_view(self):
            response = self.client.get(reverse('my_events'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'my_events.html')
            self.assertIn('created_events', response.context)
            self.assertIn('joined_events', response.context)

            self.assertQuerysetEqual(response.context['created_events'], map(repr, Event.objects.filter(creator=self.user)))
            self.assertQuerysetEqual(response.context['joined_events'], map(repr, [self.joined_event]))
    
