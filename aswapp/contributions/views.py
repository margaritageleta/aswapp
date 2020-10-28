from django.shortcuts import render

# Create your views here.

def news_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "news.html", {}) # the last is context

def newest_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "news.html", {}) # the last is context

def contact_view(request, *args, **kwargs):
    print(request.user) # who is requesting
    return render(request, "contact.html", {}) # the last is context

