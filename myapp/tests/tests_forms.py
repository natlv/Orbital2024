from django.utils import timezone
from django.test import TestCase
from myapp.forms import EventCreateForm, LoginForm, SignupForm

class TestSignupForm(TestCase):

    def test_signup_form_valid_data(self):
        form = SignupForm(data = {
            'username': 'testuser',
            'password1': 'testpassword123#',
            'password2': 'testpassword123#',
        })

        self.assertTrue(form.is_valid())

    def test_signup_form_no_data(self):
        form = SignupForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

class TestLoginForm(TestCase):

    def test_login_form_valid_data(self):
        form = LoginForm(data = {
            'username': 'testuser',
            'password': 'testpassword123#',
        })

        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
    
    def test_login_form_no_username(self):
        form = LoginForm(data = {
            'username': '',
            'password': 'testpassword123#',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_login_form_no_password(self):
        form = LoginForm(data = {
            'username': 'testuser',
            'password': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

class TestEventCreateForm(TestCase):

    def setUp(self):
        self.valid_data = {
            'organisation': 'Green Earth',
            'event_name': 'Community Cleanup',
            'event_type': 'cleanup',
            'event_location': 'City Park',
            'event_start': timezone.now() + timezone.timedelta(),
            'event_end': timezone.now() + timezone.timedelta(days=1, hours=2),
        }
        self.request = type('Request', (), {'user': type('User', (), {'username': 'testuser'})})
        
    def test_event_create_form_valid_data(self):
        form = EventCreateForm(data = self.valid_data, request=self.request)
        self.assertTrue(form.is_valid())

    def test_event_create_form_no_data(self):
        form = EventCreateForm(data = {}, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)

    def test_event_create_form_end_before_start(self):
        data = self.valid_data
        data['event_end'] = timezone.now() - timezone.timedelta(hours=1)
        form = EventCreateForm(data = data, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertIn('Event end time cannot be before the start time.', 
                      form.errors['__all__'])