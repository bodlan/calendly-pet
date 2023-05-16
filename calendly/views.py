from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.views import generic
from .models import Event, User
from .forms import NewUserForm
import logging

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = "calendly/index.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(hidden=False, expired=False).order_by("name")


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


def create_event(request):
    current_user = User.objects.get(username="bodlan")
    context = {
        "user": current_user,
    }
    return render(request, "calendly/create_event.html", context=context)


def new_event(request):
    current_user = User.objects.get(username="bodlan")
    data = request.POST
    if "hidden" in data:
        hidden = True
    else:
        hidden = False
    try:
        e = Event(
            user_created=current_user,
            name=data["ename"],
            start_time=data["sdate"],
            end_time=data["edate"],
            hidden=hidden,
        )
        e.save()
    except Exception as e:
        logger.error("Couldn't create event: %s", e)
        return render(
            request,
            "calendly/create_event.html",
            context={
                "user": current_user,
                "error_message": "Something went wrong try again!",
            },
        )
    logger.info("Event created")
    return HttpResponseRedirect(reverse("calendly:event_detail", args=(e.hash_url,)))


def user_details(request, name):
    user = get_object_or_404(User, username=name)
    events = user.event_set.all()
    context = {
        "user": user,
        "events": events,
    }
    return render(request, "calendly/user_details.html", context=context)


def event_detail_view(request, hashed_url):
    path = request.path
    event = get_object_or_404(Event, url=path)
    return render(request, "calendly/event_detail.html", context={"event": event})
