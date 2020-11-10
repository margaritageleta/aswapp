from django.shortcuts import render
from .models import Publication, Comment
# from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from .forms import SubmissionForm
from django.views import View
# from django.contrib import messages
from django.urls import reverse
from django import forms
from contributions.forms import CommentForm

# Create your views here.

class NewsView(View): 
    # This class manages the display of the 
    # URL publications, sorted by the number of votes
    template_name = "news.html"
    publications = []
    
    def get_url_publications(self): 
        # This method gets all the publications of type URL
        self.publications = Publication.objects.filter(kind = 1).all() 
    
    def sort_url_publications(self):
        # This method returns the publications sorted by number of votes
        self.publications = sorted(self.publications, key = lambda x: x.created_at, reverse=True)
        
    def get(self, request, *args, **kwargs):
        # This method builds the client page news.html with the URL publications sorted 
        
        self.get_url_publications()
        self.sort_url_publications()
        
        context = {'contributions': self.publications}
    
        return render(request, self.template_name, context)

class NewestView(View): 
    # This class manages the display of 
    # all Publications, sorted by descendent creation date
    template_name = "newest.html"
    publications = []
    
    def get_publications(self): 
        # This method gets all the publications
        self.publications = Publication.objects.all() 
    
    def sort_publications(self):
        # This method returns the publications sorted by number of votes
        self.publications = sorted(self.publications, key = lambda x: x.created_at, reverse=True)
        
    def get(self, request, *args, **kwargs):
        # This method builds the client page newests.html with the publications sorted 
        
        self.get_publications()
        self.sort_publications()
        
        context = {'contributions': self.publications}
        print(context)
        return render(request, self.template_name, context) 



class CommentView(FormView):
    form_class = CommentForm
    template_name = 'contribution.html'
    context = {} 


    def post(self, request, id): 
        publication =  Publication.objects.get(id=id)
        text = request.POST['comment']
        new_comment = Comment(comment=text, referenced_publication=publication)
        new_comment.save()         

        return HttpResponseRedirect('/item/' + str(id))

            
   

class SubmitView(FormView):
    # This class manages the display of a form for 
    # creating a new Publication, and creates the 
    # publication with its features.

    form_class = SubmissionForm
    template_name = 'submit.html'
    context = {}

    def form_valid(self, form):
        data = form.cleaned_data

        title = data['title']
        url = data['url']
        text = data['text']             
        
        if url == '' or url is None:
            kind = 0 # Is an Ask publication
        else:
            kind = 1 # Is an Url publication          

        if kind == 1 and Publication.objects.filter(url=url).exists(): 
            id = Publication.objects.get(url=url)
            HttpResponseRedirect('/item/' + str(id))
        
            return HttpResponseRedirect("/news")   

        else:
            new_publication = Publication(title=title, question=text, url=url, kind=kind)
            new_publication.save()

            # If it is a URL publications and has a comment associated
            # Create the comment and associate with publication

            if kind == 1 and (text is not '' or text is not None): 
                new_comment = Comment(comment=text, referenced_publication=new_publication)
                new_comment.save()            
        
            return HttpResponseRedirect("/news")   


class PublicationView(View): 
    # This class manages to show a particular publication 
    # (URL or Ask) and show its comments and the replies to each comment 

    template_name = "contribution.html"
    publication = None

    def get(self, request, id, *args, **kwargs):
        # This method builds the client page newests.html with the publications sorted 
        try:
            publication = Publication.objects.filter(id=id).first()
            replies = Comment.objects.filter(referenced_publication=self.publication, parent=None)
        except Exception as e:
            # back to square one
            return HttpResponseRedirect(reverse('news_view'))

        context = {
            'contribution': publication,
            'form': CommentForm(),
            'replies': replies
        }
        # get_comment(request)
        return render(request, "contribution.html", context)
