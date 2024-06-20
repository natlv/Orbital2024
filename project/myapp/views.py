from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import SignupForm, LoginForm, EventCreateForm, EventJoinForm, ProfileForm
from .models import Event, UserProfile, EventParticipants


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

# create event page 
class EventCreateView(LoginRequiredMixin, FormView):
    template_name = 'event_create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('event_create')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You must be logged in to create an event")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        event_start = form.cleaned_data['event_start']
        event_end = form.cleaned_data['event_end']
        if not event_end:
            event_end = event_start

        event = Event.objects.create(
            creator=form.cleaned_data['creator'],
            organisation=form.cleaned_data['organisation'],
            event_name=form.cleaned_data['event_name'],
            event_type=form.cleaned_data['event_type'],
            event_location=form.cleaned_data['event_location'],
            event_start=event_start,
            event_end=event_end
        )

        participant = EventParticipants.objects.create(
            user=self.request.user,
            event=event,
            name=self.request.user.username,
            email=self.request.user.email,
            is_staff=True
        )

        event.participants.add(self.request.user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# see joinable events page
class EventJoinView(LoginRequiredMixin, TemplateView):
    template_name = 'event_join.html'
    form_class = EventJoinForm
    success_url = reverse_lazy('event_join')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context

# join specific event page
class ChosenEventJoinView(LoginRequiredMixin, FormView):
    template_name = 'event_join_chosen.html'
    form_class = EventJoinForm
    success_url = reverse_lazy('event_join')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, event_id=self.kwargs['event_id'])
        return context

    def form_valid(self, form):
        event = get_object_or_404(Event, event_id=self.kwargs['event_id'])
        event.participants.add(self.request.user)
        participant = EventParticipants.objects.create(
            user=self.request.user,
            event=event,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email']
        )
        return super().form_valid(form)
    
# show all the events that user has created or joined
class MyEventsView(LoginRequiredMixin, TemplateView):
    template_name = 'my_events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['created_events'] = Event.objects.filter(creator=self.request.user.username)
        # context['joined_events'] = Event.objects.filter(participants=self.request.user).exclude(creator=self.request.user.username)
        context['joined_events'] = Event.objects.filter(participants=self.request.user)
        return context
    
# show marketplace for eco-friendly services
class MarketplaceView(LoginRequiredMixin, TemplateView):
    template_name = 'marketplace.html'

# show redeemable rewards for users
class RewardsView(LoginRequiredMixin, TemplateView):
    template_name = 'rewards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context

@login_required    
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

class ChosenEventParticipantsView(LoginRequiredMixin, TemplateView):
    model = EventParticipants
    template_name = 'event_participants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = EventParticipants.objects.all()
        return context