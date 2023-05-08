from django.shortcuts import render, get_object_or_404
from .models import Event, User


# Create your views here.
def index(request):
    events = Event.objects.order_by("name")
    context = {"events": events}

    return render(request, "calendly/index.html", context)


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
