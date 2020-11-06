from django.shortcuts import render
from .models import Contribution, Url, Ask
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from .forms import SubmissionForm
from django.contrib import messages
from django.urls import reverse
from django import forms



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

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}), max_length=160)

def show_contribution_view (request, kind, id):
     # get the contrib from the db
    try:
        if kind == 'ask':
            contribution = Ask.objects.filter(id = id).first()
        elif kind == 'url':
            contribution = Url.objects.filter(id = id).first()
        else:
            print('nonsense')
            raise Exception
    except:
        contribution = None
    
    # back to square one
    if contribution is None:
        return HttpResponseRedirect(reverse('news_view'))

    context = {
        'contribution': contribution,
        'form': CommentForm()
    }

    return render(request, "contribution.html", context)
    

class SubmitView(FormView):
    form_class = SubmissionForm
    template_name = 'submit.html'
    context = {}

    def form_valid(self, form):
        data = form.cleaned_data
        #print("_________________")
        #print(data)
        #print("_________________")
        title = data['title']
        url = data['url']
        text = data['text']     

        #print("Hey i entered")

        if url is not '': #An url submission 
            print("Im in the URL CZONE")
            contrib = Url(title = title, url = url) 
            if text is not '': #With a comment associated
                contrib.addComment(text)
            contrib.save()
        else: #An ask submission
            print("Im in the ask CZONE")
            contrib = Ask(title=title, content=text)
            contrib.save() 
        
        return HttpResponseRedirect('/news')        


        





