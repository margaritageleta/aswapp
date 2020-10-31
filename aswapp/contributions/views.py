from django.shortcuts import render
from .models import Contribution, Url, Ask
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from .forms import SubmissionForm
from django.contrib import messages




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


class SubmitView(FormView):
    form_class = SubmissionForm
    template_name = 'submit.html'
    context = {}

    def form_valid(self, form):
        data = form.cleaned_data
        # print("_________________")
        # print(data)
        # print("_________________")
        title = data['title']
        url = data['url']
        text = data['text']     

        if url is not '' and text is not '': #Throw Error
            contrib = Ask(title = title, content = text)
            return HttpResponseRedirect('/submit/badsubmission')
        else: #An Url submission
            contrib = Url(title=title, content=text, url=url)
            return HttpResponseRedirect('/news')        
        contrib.save()

        





