from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("event/<str:hashed_url>/", views.event_detail_view, name='event_detail'),
]