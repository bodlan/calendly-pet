from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import generic
from .models import Event

from .forms import NewUserForm, EventCreationForm
import logging

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = "calendly/index.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(hidden=False, expired=False).order_by("-id")[:5]


class EventDetailsView(generic.DetailView):
    model = Event
    template_name = "calendly/event_detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        url = self.kwargs["hash_url"]
        try:
            e_obj = Event.objects.get(hash_url=url)
        except Event.DoesNotExist:
            logger.info("Event does not exist with url: %s", url)
            e_obj = None
        except Exception as e:
            logger.warning(e)
            raise Exception
        return e_obj


class UserDetailsView(generic.DetailView):
    model = User
    template_name = "calendly/user_details.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        name = self.kwargs["name"]
        try:
            u_obj = User.objects.get(username=name)
        except Exception as e:
            logger.warning(e)
            u_obj = None
        return u_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(user_created=context["user"])
        logger.info(context)
        return context


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("calendly:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="calendly/register.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("calendly:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="calendly/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("calendly:index")


def explore(request):
    return render(request=request, template_name="calendly/explore.html")


# TODO: rewrite to generic editing view
def create_event(request):
    if not request.user.is_authenticated:
        return redirect("calendly:register")
    if request.method == "POST":
        event_form = EventCreationForm(request.POST, user=request.user)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event created successfully!")
            # Getting the latest event created by this user
            event = request.user.event_set.order_by("-id")[0]
            return redirect(event)
        else:
            messages.error(request, "Error validating form!")
            return redirect("calendly:create_event")
    event_form = EventCreationForm(user=request.user)
    return render(request=request, template_name="calendly/create_event.html", context={"event_form": event_form})
