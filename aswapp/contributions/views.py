from django.shortcuts import render
from .models import Contribution, Url, Ask



# Create your views here.

def news_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    urls = Contribution.objects.instance_of(Url)
    print(urls)

    context = {
      'contributions': urls,
    }
    print("-------------------------------------------")
    print(context)

    return render(request, "news.html", context) # the last is context

def newest_view(request, *args, **kwargs):
    print(request.user) # who is requesting

    contributions = Url.objects.all()
    contributions.append(Ask.objects.all())

    context = {
        'contributions': contributions,
    }
    print("Newest - - - - ")
    print("-------------------------------------------")
    print(context)

    return render(request, "newest.html", context) 

def submit_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "submit.html", {}) # the last is context
