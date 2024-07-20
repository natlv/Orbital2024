from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignupForm, LoginForm, EventCreateForm, EventJoinForm, EventSearchForm, ProfileForm, ItemForm, MessageForm
from .models import Event, UserProfile, Rewards, EventParticipants, UserRewards, Item, Message



# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    error_message = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error_message = "Please correct the errors below."
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

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
        form = EventSearchForm(self.request.GET or None)
        events = Event.objects.filter(event_end__gte=timezone.now())
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            event_type = form.cleaned_data.get('event_type')
            
            if query:
                events = events.filter(event_name__icontains=query)
            if event_type and event_type != 'any':
                events = events.filter(event_type=event_type)

        context['events'] = events
        context['form'] = form
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
        EventParticipants.objects.create(
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
        context['joined_events'] = Event.objects.filter(participants=self.request.user)
        return context

# show redeemable rewards for users
class RewardsView(LoginRequiredMixin, TemplateView):
    template_name = 'rewards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        rewards = Rewards.objects.all()
        context['profile'] = profile
        context['rewards'] = rewards
        return context

@login_required    
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_pic_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if user_profile.profile_pic:
        return HttpResponse(user_profile.profile_pic, content_type="image/png")

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

@login_required
def claim_reward(request, reward_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    reward = get_object_or_404(Rewards, id=reward_id)

    if profile.points >= reward.points_cost:
        profile.points -= reward.points_cost
        UserRewards.objects.create(user=request.user, reward=reward)
        profile.save()
        messages.success(request, f'You have successfully claimed {reward.name}!')
    else:
        messages.error(request, 'You do not have enough points to claim this reward.')

    return redirect('rewards')

@login_required
def user_rewards(request):
    user_rewards = UserRewards.objects.filter(user=request.user)
    rewards = [user_reward.reward for user_reward in user_rewards]
    return render(request, 'user_rewards.html', {'rewards': rewards})
    
class ChosenEventParticipantsView(LoginRequiredMixin, TemplateView):
    model = EventParticipants
    template_name = 'event_participants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['participants'] = EventParticipants.objects.filter(event_id=event_id)
        return context
    
@csrf_exempt
def update_attendance(request, event_id):
    if request.method == 'POST':
        for participant in EventParticipants.objects.filter(event_id=event_id):
            checkbox_name = f'attended_{participant.id}'
            participant.attended = checkbox_name in request.POST
            participant.save()
        return redirect(reverse('event_participants_chosen', args=[event_id]))
    else:
        # Handling GET requests to view the participants if necessary
        participants = EventParticipants.objects.filter(event_id=event_id)
        return render(request, 'event_participants.html', {'participants': participants, 'event_id': event_id})
    
    
# show marketplace for eco-friendly services
@login_required
def marketplace_sell(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('marketplace')
    else:
        form = ItemForm()
    return render(request, 'marketplace_sell.html', {'form': form})

@login_required
def item_image_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.image:
        return HttpResponse(item.image, content_type="image/png")

def marketplace(request):
    items = Item.objects.all()
    return render(request, 'marketplace.html', {'items': items})

def send_message(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = item.seller
            message.item = item
            message.save()
            return redirect('marketplace')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form, 'item': item})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})

@transaction.atomic
def close_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    attendances = EventParticipants.objects.filter(event=event, attended=True)
    
    for attendance in attendances:
        user = attendance.user
        user_profile = UserProfile.objects.get(user=user)
        # user_profile.points += 10
        user_profile.save()
    
    event.delete()
    
    return redirect('home')

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('my_events')