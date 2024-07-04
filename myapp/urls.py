from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import EventCreateView, EventJoinView, ChosenEventJoinView, MyEventsView, RewardsView, profile, edit_profile, claim_reward, ChosenEventParticipantsView, update_attendance

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('event_create/', EventCreateView.as_view(), name='event_create'),
    path('event_join/', EventJoinView.as_view(), name='event_join'),
    path('event_join/<str:event_id>/', ChosenEventJoinView.as_view(), name='event_join_chosen'),
    path('my_events/', MyEventsView.as_view(), name='my_events'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/sell/', views.marketplace_sell, name='marketplace_sell'),
    path('message/send/<int:item_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('rewards/', RewardsView.as_view(), name='rewards'),
    path('claim_reward/<int:reward_id>/', claim_reward, name='claim_reward'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('event_participants/<str:event_id>/', ChosenEventParticipantsView.as_view(), name='event_participants_chosen'),
    path('update_attendance/<str:event_id>/', update_attendance, name='update_attendance'),
    path('user_rewards/', views.user_rewards, name='user_rewards'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 