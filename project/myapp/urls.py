from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import EventCreateView, EventJoinView, ChosenEventJoinView, MyEventsView, MarketplaceView, RewardsView, profile, edit_profile, claim_reward

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('event_create/', EventCreateView.as_view(), name='event_create'),
    path('event_join/', EventJoinView.as_view(), name='event_join'),
    path('event_join/<str:event_id>/', ChosenEventJoinView.as_view(), name='event_join_chosen'),
    path('my_events/', MyEventsView.as_view(), name='my_events'),
    path('marketplace/', MarketplaceView.as_view(), name='marketplace'),
    path('rewards/', RewardsView.as_view(), name='rewards'),
    path('claim_reward/<int:reward_id>/', claim_reward, name='claim_reward'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 