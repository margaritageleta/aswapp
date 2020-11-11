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
        print(self.publications)
    
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



class ReplyView(FormView):
    form = CommentForm()
    template_name = 'reply_comment.html'
    context = {}
    
    def get(self, request, id):
        print(id)
        comment = Comment.objects.get(id=id)
        self.parent = comment
        context = {
            'comment': comment,
            'form': self.form,
            'type': 'comment'
        }
        return render(request, self.template_name, context)
        
    def post(self, request, id):
        reply_text = request.POST['comment']
        parent_comment = Comment.objects.get(id=id)
        parent_publication = parent_comment.referenced_publication
        new_reply = Comment(comment=reply_text, parent=parent_comment, referenced_publication=parent_publication)
        new_reply.save()

        # print("____________")
        # print(new_reply.parent.comment)
        # print("__________")

        return HttpResponseRedirect(reverse('show_contribution_view',args=[parent_publication.pk]))

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

    form = SubmissionForm()
    template_name = 'submit.html'
    context = {
        'form': form,
        'type': 'submit'
    }

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):                  
        
        title = request.POST['title']
        url = request.POST['url']
        text = request.POST['text']

        if url == '' or url is None:
            kind = 0 # Is an Ask publication
        else:
            kind = 1 # Is an Url publication          

        #If url publication exists in out system then redirect to that publication 
        if kind == 1 and Publication.objects.filter(url=url).exists(): 
            id = Publication.objects.get(url=url).id
            return HttpResponseRedirect('/item/' + str(id))
        

        else:
            #Create a new publication 
            new_publication = Publication(title=title, question=text, url=url, kind=kind)
            new_publication.save()
            # print(new_publication)

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
    comments = {}

    def get_replies(self, reply):
        # Obtains replies of comments recursively
        subcomments = {}
        subreplies = Comment.objects.filter(referenced_publication=self.publication, parent=reply)
        for subreply in subreplies:
            subcomments[subreply] = self.get_replies(subreply)
        return subcomments if subcomments else None

    def get(self, request, id, *args, **kwargs):
        # This method builds the client page newests.html with the 
        # publications sorted 
        try:
            self.publication = Publication.objects.filter(id=id).first()
            replies = Comment.objects.filter(referenced_publication=self.publication, parent=None)
            
            for reply in replies:
                self.comments[reply] = self.get_replies(reply)
        
        except Exception as e:
            # back to square one
            return HttpResponseRedirect(reverse('news_view'))

        context = {
            'contribution': self.publication,
            'form': CommentForm(),
            'replies': self.comments
        }
        # get_comment(request)
        return render(request, "contribution.html", context)
