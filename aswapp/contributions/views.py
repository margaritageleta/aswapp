from django.shortcuts import render
from .models import Contribution, Url, Ask

# Create your views here.

def news_view(request, *args, **kwargs):
    print(request.user) # who is requesting

    urls = Url.objects.all()

    context = {
        'contributions': urls,
    }

    return render(request, "news.html", context) # the last is context

def newest_view(request, *args, **kwargs):
    print(request.user) # who is requesting

    contributions = Contribution.get_all()

    context = {
        'contributions': contributions,
    }

    return render(request, "newest.html", context) 

def submit_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "submit.html", {}) # the last is context