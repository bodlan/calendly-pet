from django.urls import path
from . import views

app_name = "calendly"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("user/<slug:name>", views.UserDetailsView.as_view(), name="user_detail"),
    path("event/<slug:hash_url>/", views.EventDetailsView.as_view(), name="event_detail"),
    path("event/new", views.create_event, name="create_event"),
    path("event/<slug:hash_url>/update", views.UpdateEventView.as_view(), name="update_event"),
    path("event/<slug:hash_url>/delete", views.DeleteEventView.as_view(), name="delete_event"),
    path("explore", views.CalendarEventsView.as_view(), name="explore"),
    path("explore/day/", views.day_view, name="day_view"),
    path("explore/week/", views.week_view, name="week_view"),
    path("explore/month/", views.month_view, name="month_view"),
    path("explore/year/", views.year_view, name="year_view"),
]
