from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Event, User
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    events = Event.objects.order_by("name").filter(hidden=False, expired=False)
    context = {"events": events}
    return render(request, "calendly/index.html", context)


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
    return HttpResponseRedirect(e.get_absolute_url())


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
