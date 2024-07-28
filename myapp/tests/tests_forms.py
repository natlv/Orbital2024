from django.utils import timezone
from django.test import TestCase
from myapp.forms import (EventCreateForm, 
                         EventJoinForm, 
                         EventSearchForm,
                         ItemForm,
                         LoginForm,
                         ProfileForm, 
                         SignupForm)

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
        self.assertEqual(len(form.errors), 2)
    
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
            'email': 'testuser@example.com',
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
        self.assertEqual(len(form.errors), 8)
        self.assertIn("Event start time is required.",
                      form.errors['__all__'])

    def test_event_create_form_end_before_start(self):
        data = self.valid_data
        data['event_end'] = timezone.now() - timezone.timedelta(hours=1)
        form = EventCreateForm(data = data, request=self.request)
        self.assertFalse(form.is_valid())
        self.assertIn('Event end time cannot be before the start time.', 
                      form.errors['__all__'])
        
class TestEventJoinForm(TestCase):

    def test_event_join_form_valid_data(self):
        form = EventJoinForm(data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        })

        self.assertTrue(form.is_valid())

    def test_event_join_form_no_data(self):
        form = EventJoinForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

class TestEventSearchForm(TestCase):
    
    def test_event_search_form_valid_data(self):
        form = EventSearchForm(data = {
            'query': 'test',
            'event_type': 'cleanup',
        })
    
        self.assertTrue(form.is_valid())
    
    def test_event_search_form_no_data(self):
        form = EventSearchForm(data = {})
    
        self.assertTrue(form.is_valid())

class TestProfileForm(TestCase):
    
    def test_profile_form_valid_data(self):
        form = ProfileForm(data = {
            'bio': 'Test bio',
            'location': 'Test location',
            'birth_date': '1990-01-01',
        })
    
        self.assertTrue(form.is_valid())
    
    def test_profile_form_no_data(self):
        form = ProfileForm(data = {})
    
        self.assertTrue(form.is_valid())
    
    def test_profile_form_no_bio(self):
        form = ProfileForm(data = {
            'bio': '',
            'location': 'Test location',
            'birth_date': '1990-01-01',
        })
    
        self.assertTrue(form.is_valid())
    
    def test_profile_form_no_location(self):
        form = ProfileForm(data = {
            'bio': 'Test bio',
            'location': '',
            'birth_date': '1990-01-01',
        })
    
        self.assertTrue(form.is_valid())
    
    def test_profile_form_no_birth_date(self):
        form = ProfileForm(data = {
            'bio': 'Test bio',
            'location': 'Test location',
            'birth_date': '',
        })
    
        self.assertTrue(form.is_valid())
    
    def test_profile_form_invalid_birth_date(self):
        form = ProfileForm(data = {
            'bio': 'Test bio',
            'location': 'Test location',
            'birth_date': '01-01-1990',
        })
    
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
    
    def test_profile_form_future_birth_date(self):
        form = ProfileForm(data = {
            'bio': 'Test bio',
            'location': 'Test location',
            'birth_date': timezone.now().date() + timezone.timedelta(days=1),
        })
    
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

class TestItemForm(TestCase):
    def test_item_form_valid_data(self):
        form = ItemForm(data = {
            'name': 'Test Item',
            'description': 'Test description',
            'price': 100,
        })
    
        self.assertTrue(form.is_valid())

    def test_item_form_no_data(self):
        form = ItemForm(data = {})
    
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
