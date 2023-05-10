from django.urls import path
from . import views

app_name = "calendly"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("user/<slug:name>", views.UserDetailsView.as_view(), name="user_detail"),
    path("event/<slug:hash_url>/", views.EventDetailsView.as_view(), name="event_detail"),
    path("event/new", views.create_event, name="create_event"),
    path("event/add", views.new_event, name="event_add"),
]
