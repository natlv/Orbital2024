from django.contrib.auth.models import User
from django.test import TestCase
from myapp.models import Item, Message, UserProfile
from PIL import Image

class TestUserProfile(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123#')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            bio='This is a test bio',
            location='Test City'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.bio, 'This is a test bio')
        self.assertEqual(self.user_profile.location, 'Test City')
        self.assertIsNone(self.user_profile.birth_date)
        self.assertIsNone(self.user_profile.profile_pic)
        self.assertEqual(self.user_profile.points, 20)

    def test_save_profile_pic(self):
        image = Image.new('RGB', (100, 100), color='red')
        self.user_profile.save_profile_pic(image)
        self.user_profile.save()

        self.assertIsNotNone(self.user_profile.profile_pic)

    def tearDown(self):
        self.user.delete()
        self.user_profile.delete()

class TestItem(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123#')
        self.item = Item.objects.create(
            seller=self.user,
            name='Test Item',
            description='This is a test item',
            price=100
        )

    def test_item_creation(self):
        self.assertEqual(self.item.seller, self.user)
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.description, 'This is a test item')
        self.assertEqual(self.item.price, 100)
        self.assertIsNone(self.item.image)

    def test_save_image(self):
        image = Image.new('RGB', (100, 100), color='red')
        self.item.save_image(image)
        self.item.save()

        self.assertIsNotNone(self.item.image)

    def tearDown(self):
        self.user.delete()
        self.item.delete()

class TestMessage(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')
        
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Description',
            price=10.0,
            seller=self.sender,
        )

        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            item=self.item,
            email='test@example.com',
            message='This is a test message.'
        )

    def test_message_creation(self):
        self.assertEqual(str(self.message), f'Message from {self.sender} to {self.recipient} about {self.item.name}')
        self.assertEqual(self.message.sender.username, 'sender')
        self.assertEqual(self.message.recipient.username, 'recipient')
        self.assertEqual(self.message.item.name, 'Test Item')
        self.assertEqual(self.message.email, 'test@example.com')
        self.assertEqual(self.message.message, 'This is a test message.')

    def tearDown(self):
        self.message.delete()
        self.item.delete()
        self.sender.delete()
        self.recipient.delete()