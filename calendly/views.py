from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event
# Create your views here.
def index(request):
    return HttpResponse("Hello")
def event_detail_view(request, hashed_url):
    path = request.get_full_path()
    instance = get_object_or_404(Event, url=path)
    context = {"instance":instance}
    # return render(request,'.html', context=context)
    return HttpResponse(context['instance'])