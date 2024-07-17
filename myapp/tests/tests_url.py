from django.test import SimpleTestCase
from django.urls import resolve, reverse
from myapp.views import *

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, index)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)
    
    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, user_signup)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, user_logout)
    
    def test_event_create_url_resolves(self):
        url = reverse('event_create')
        self.assertEqual(resolve(url).func.view_class, EventCreateView)

    def test_event_join_url_resolves(self):
        url = reverse('event_join')
        self.assertEqual(resolve(url).func.view_class, EventJoinView)

    def test_event_join_chosen_url_resolves(self):
        url = reverse('event_join_chosen', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ChosenEventJoinView)

    def test_my_events_url_resolves(self):
        url = reverse('my_events')
        self.assertEqual(resolve(url).func.view_class, MyEventsView)

    def test_delete_event_url_resolves(self):
        url = reverse('delete_event', args=['1'])
        self.assertEqual(resolve(url).func, delete_event)

    def test_event_participants_chosen_url_resolves(self):
        url = reverse('event_participants_chosen', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ChosenEventParticipantsView)

    def test_update_attendance_url_resolves(self):
        url = reverse('update_attendance', args=['1'])
        self.assertEqual(resolve(url).func, update_attendance)

    def test_marketplace_url_resolves(self):
        url = reverse('marketplace')
        self.assertEqual(resolve(url).func, marketplace)

    def test_marketplace_sell_url_resolves(self):
        url = reverse('marketplace_sell')
        self.assertEqual(resolve(url).func, marketplace_sell)

    def test_message_send_url_resolves(self):
        url = reverse('send_message', args=['1'])
        self.assertEqual(resolve(url).func, send_message)

    def test_inbox_url_resolves(self):
        url = reverse('inbox')
        self.assertEqual(resolve(url).func, inbox)

    def test_rewards_url_resolves(self):
        url = reverse('rewards')
        self.assertEqual(resolve(url).func.view_class, RewardsView)

    def test_rewards_url_resolves(self):
        url = reverse('rewards')
        self.assertEqual(resolve(url).func.view_class, RewardsView)

    def test_reward_claim_url_resolves(self):
        url = reverse('claim_reward', args=['1'])
        self.assertEqual(resolve(url).func, claim_reward)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_user_rewards_url_resolves(self):
        url = reverse('user_rewards')
        self.assertEqual(resolve(url).func, user_rewards)

    def test_close_event_url_resolves(self):
        url = reverse('close_event', args=['1'])
        self.assertEqual(resolve(url).func, close_event)

    def test_profile_pic_url_resolves(self):
        url = reverse('profile_pic', args=['1'])
        self.assertEqual(resolve(url).func, profile_pic_view)

    def test_item_image_url_resolves(self):
        url = reverse('item_image', args=['1'])
        self.assertEqual(resolve(url).func, item_image_view)