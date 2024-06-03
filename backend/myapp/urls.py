from django.urls import path
from . import views
from .views import EventCreateView, EventJoinView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('event_create/', EventCreateView.as_view(), name='event_create'),
    path('event_join/', EventJoinView.as_view(), name='event_join'),
]