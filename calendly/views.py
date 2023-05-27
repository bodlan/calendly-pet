from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.views import generic
from .models import Event
from .forms import NewUserForm, EventCreationForm, EventUpdatingForm
import logging

from .utils import generate_calendar

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = "calendly/index.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(hidden=False, expired=False).order_by("-id")[:5]

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(hidden=False, expired=False)
        user_count = User.objects.annotate(event_count=Count("event")).filter(event_count__gt=0).count()
        current_time = timezone.now()
        active_events = events.filter(start_time__lte=current_time, end_time__gt=current_time)
        context = {
            "events": self.get_queryset(),
            "events_count": events.count(),
            "active_events": active_events.count(),
            "users_count": user_count,
        }
        return render(request, self.template_name, context=context)


class CalendarEventsView(generic.View):
    login_url = "calendly:login"
    template_name = "calendly/explore.html"

    def get(self, request, *args, **kwargs):
        if "range" in kwargs:
            calendar_range = kwargs["range"].title()
        else:
            calendar_range = "month".title()

        now = timezone.now()
        year = now.year
        month = now.month
        calendar_data = generate_calendar(year, month)
        events = Event.objects.filter(hidden=False, expired=False)
        context = {
            "events": events,
            "calendar_data": calendar_data,
            "range": calendar_range,
        }
        return render(request, self.template_name, context=context)


def day_view(request):
    events = Event.objects.filter(start_time__date=timezone.now().date())
    print(events)
    return render(request, "calendly/day_view.html", {"events": events})


def week_view(request):
    events = Event.objects.filter(start_time__date=timezone.now().date())
    print(events)
    return render(request, "calendly/week_view.html", {"events": events})


def month_view(request):
    events = Event.objects.filter(start_time__month=timezone.now().month)
    print(events)
    return render(request, "calendly/month_view.html", {"events": events})


def year_view(request):
    events = Event.objects.filter(start_time__year=timezone.now().year)
    print(events)
    return render(request, "calendly/year_view.html", {"events": events})


class EventDetailsView(generic.DetailView):
    model = Event
    template_name = "calendly/event_detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        url = self.kwargs["hash_url"]
        e_obj = get_object_or_404(Event, hash_url=url)
        return e_obj


class UpdateEventView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventUpdatingForm
    template_name = "calendly/update_event_form.html"

    def get_object(self, queryset=None):
        url = self.kwargs["hash_url"]
        e_obj = get_object_or_404(Event, hash_url=url)
        return e_obj

    def dispatch(self, request, *args, **kwargs):
        event_object = self.get_object()  # Retrieve the object being updated

        # Check if the user is the specific user or an admin
        if not (request.user == event_object.user_created or request.user.is_staff):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class DeleteEventView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = "calendly/delete_event.html"
    success_url = "/"

    def get_object(self, queryset=None):
        url = self.kwargs["hash_url"]
        e_obj = get_object_or_404(Event, hash_url=url)
        return e_obj

    def dispatch(self, request, *args, **kwargs):
        event_object = self.get_object()  # Retrieve the object being updated

        # Check if the user is the specific user or an admin
        if not (request.user == event_object.user_created or request.user.is_staff):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


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
