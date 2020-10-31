from django.shortcuts import render
from .models import Contribution, Url, Ask
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import FormView
from .forms import SubmissionForm




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
    context = {}
    return render(request, "submit.html", context) # the last is context


class SubmitView(FormView):
    form_class = SubmissionForm
    template_name = 'submit.html'

    def form_valid(self, form):
        data = form.cleaned_data 
        if (data['title'] is None): return HttpResponse('That is not a valid title')
        else:            
            # if data['url'] is not None: 
            #     contrib = Url.objects.create(
            #         title = data['title'],            
            #         content = data['text'],
            #         url = data['url']

            #     )
            # else: 
            #     contrib = Ask.objects.create(
            #         title = data['title'],            
            #         content = data['text']
                # )
            contrib = Url.objects.create(
            title = data['title'],            
            content = data['text'], )
        contrib.save()
        return HttpResponse(contrib)