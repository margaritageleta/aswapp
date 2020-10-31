from django.shortcuts import render
from .models import Contribution, Url, Ask

# Create your views here.

def news_view(request, *args, **kwargs):
    
    contributions = []
    for subclass in Contribution.__subclasses__():
        for instance in subclass.objects.all():
            contributions.append(instance)
    contributions.sort(key=lambda x: x.created_at, reverse=True)

    context = {
      'contributions': contributions,
    }
    
    print('NEWS')

    return render(request, "news.html", context) # the last is context

def newest_view(request, *args, **kwargs):
    print(request.user) # who is requesting

    contributions = []
    for subclass in Contribution.__subclasses__():
        for instance in subclass.objects.all():
            contributions.append(instance)
    contributions.sort(key=lambda x: x.created_at, reverse=True)

    context = {
      'contributions': contributions,
    }
    
    print('NEWEST')

    return render(request, "newest.html", context) 

def submit_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "submit.html", {}) # the last is context
