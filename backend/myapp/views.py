from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignupForm, LoginForm, EventCreateForm, EventJoinForm
from .models import Event

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
class EventCreateView(FormView):
    template_name = 'event_create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('event_create')

    def form_valid(self, form):
        Event.objects.create(
            creator=form.cleaned_data['creator'],
            organisation=form.cleaned_data['organisation'],
            event_name=form.cleaned_data['event_name'],
            event_type=form.cleaned_data['event_type'],
            event_location=form.cleaned_data['event_location']
        )
        return super().form_valid(form)

# join event page
class EventJoinView(TemplateView):
    template_name = 'event_join.html'
    form_class = EventJoinForm
    success_url = reverse_lazy('event_join')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()  # Add all events to the context
        return context

    def form_valid(self, form):
        # Handle the form submission
        # For simplicity, just print the form data or save to a different model if needed
        print("User joined event:", form.cleaned_data)
        return super().form_valid(form)