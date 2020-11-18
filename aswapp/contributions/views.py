from django.shortcuts import render
from .models import Contribution, Publication, Comment
# from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from .forms import SubmissionForm
from django.views import View
# from django.contrib import messages
from django.urls import reverse
from django import forms
from contributions.forms import CommentForm
from users.models import Hacker
from django.contrib.auth.models import User
from contributions.models import VotePublication, VoteComment

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

        if request.user.is_authenticated and request.user.username != 'root':
            hacker = Hacker.objects.get(user=request.user)

            #voted_publications = VotePublication.objects.filter(voter=hacker).all()
            #print(voted_publications)

            context['hacker'] = hacker

            votes = set()
            for c in self.publications:
                if VotePublication.objects.filter(voter=hacker, contribution=c).exists():
                    votes.add(c.id)
            
            context['votes'] = votes
            print(votes)

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

        if request.user.is_authenticated and request.user.username != 'root':
            hacker = Hacker.objects.get(user=request.user)
            context['hacker'] = hacker

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
        user = User.objects.get(username=request.user)
        hacker = Hacker.objects.get(user=user)

        new_reply = Comment(comment=reply_text, parent=parent_comment, referenced_publication=parent_publication, author=hacker)
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
        user = User.objects.get(username=request.user)
        hacker = Hacker.objects.get(user=user)


        new_comment = Comment(comment=text, referenced_publication=publication, author=hacker)

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

        user = User.objects.get(username=request.user)
        hacker = Hacker.objects.get(user=user)

        kind = 0 if url == '' or url is None else 1


        #Url Publication Options
        if kind == 1: 
            #If already exists: redirect to existing post
            if Publication.objects.filter(url=url).exists(): 
                id = Publication.objects.get(url=url).id
                return HttpResponseRedirect('/item/' + str(id))
            #Else, create a new Publication type Url
            else: 
                new_publication = Publication(title=title, url=url, kind=kind, author=hacker)
                new_publication.save()
                #If has text associated - it is a comment associated to the publication
                print(text.isspace())
                if len(text) > 0:
                    new_comment = Comment(comment=text, referenced_publication=new_publication, author=hacker)
                    new_comment.save() 
        #Ask Submission
        else:  
            new_publication = Publication(title=title, kind=kind, author=hacker, question=text)
            new_publication.save()

            if len(text) > 0:
                new_comment = Comment(comment=text, referenced_publication=new_publication, author=hacker)
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

    def create_comment_set(self, setc, voter, comments):
        for c, v in comments.items():
            print(f'{c}={v}')
            if VoteComment.objects.filter(voter=voter, contribution=c).exists():
                setc.add(c.id)
                print(c.id)
            if v != None: 
                self.create_comment_set(setc, voter, v)
            else: 
                pass

    def get(self, request, id, *args, **kwargs):
        # This method builds the client page newests.html with the 
        # publications sorted 
        
        # Reset comments dict
        self.comments = {}

        try:
            self.publication = Publication.objects.filter(id=id).first()
            replies = Comment.objects.filter(referenced_publication=self.publication, parent=None)
            # Get comments recursively
            for reply in replies:
                self.comments[reply] = self.get_replies(reply)
            
        except Exception as e:
            # Back to square one
            return HttpResponseRedirect(reverse('news_view'))

        context = {
            'contribution': self.publication,
            'form': CommentForm(),
            'replies': self.comments,
        }

        if request.user.is_authenticated and request.user.username != 'root':
            hacker = Hacker.objects.get(user=request.user)
            context['publi_vote'] = VotePublication.objects.filter(voter=hacker, contribution=self.publication).exists()

            votes_c = set()
            self.create_comment_set(votes_c, hacker, self.comments)
            
            context['c_votes'] = votes_c
        return render(request, "contribution.html", context)

class DeleteView(View):

    def get(self, request, id):
        if Publication.objects.filter(id=id).exists():
            Publication.objects.get(id=id).delete()
            return HttpResponseRedirect('/news')

        else:
            id_pub = Comment.objects.get(id=id).referenced_publication.id
            Comment.objects.get(id=id).delete() 
            return HttpResponseRedirect("/item/" + str(id_pub))         

class VoteView(View):

    def get(self, request, kind, id):
        
        if request.user.is_authenticated and request.user.username != 'root':
            hacker = Hacker.objects.get(user=request.user)

            if kind == 'publication' and Publication.objects.filter(id=id).exists():
                publi = Publication.objects.get(id=id) 

                # If the publication is not voted by hacker
                if VotePublication.objects.filter(voter=hacker, contribution=publi).count() == 0:
                    
                    # Create a new vote and update the votes in both
                    # the author (to recompute karma) & publication's
                    vote = VotePublication.objects.create(voter=hacker, contribution=publi)
                    
                    publi.author.add_upvotes()
                    publi.author.save()

                    publi.add_votes()
                    publi.save()
                   
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            elif kind == 'comment' and Comment.objects.filter(id=id).exists():
                comment = Comment.objects.get(id=id) 
                
                # If the comment is not voted by hacker
                if VoteComment.objects.filter(voter=hacker, contribution=comment).count() == 0:
                    
                    # Create a new vote and update the votes 
                    # the author (to recompute karma) 
                    vote = VoteComment.objects.create(voter=hacker, contribution=comment)
                    
                    comment.author.add_upvotes()
                    comment.author.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
            return HttpResponseRedirect('/login/google-oauth2') # TODO


class UnvoteView(View):

    def get(self, request, kind, id):

        if request.user.is_authenticated and request.user.username != 'root':
            hacker = Hacker.objects.get(user=request.user)

            if kind == 'publication' and Publication.objects.filter(id=id).exists():
                publi = Publication.objects.get(id=id) 

                # If the publication is voted by hacker
                if VotePublication.objects.filter(voter=hacker, contribution=publi).count() > 0:
                    
                    # Delete the vote and update the votes in both
                    # the author (to recompute karma) & publication's
                    VotePublication.objects.get(voter=hacker, contribution=publi).delete()
                    
                    publi.author.remove_upvotes()
                    publi.author.save()

                    publi.delete_votes()
                    publi.save()
                    
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
            elif kind == 'comment' and Comment.objects.filter(id=id).exists():
                comment = Comment.objects.get(id=id)

                # If the comment is voted by hacker
                if VoteComment.objects.filter(voter=hacker, contribution=comment).count() > 0:
                    
                    # Delete the vote and update the votes 
                    # the author (to recompute karma) 
                    VoteComment.objects.get(voter=hacker, contribution=comment).delete()
                    
                    comment.author.remove_upvotes()
                    comment.author.save()
                    
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            return HttpResponseRedirect('/login/google-oauth2') # TODO
