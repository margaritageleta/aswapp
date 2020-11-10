from django.shortcuts import render
from .models import Publication, Comment
# from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from .forms import SubmissionForm
# from django.contrib import messages
# from django.urls import reverse
from django import forms



# Create your views here.




class NewsView(): 
    #This class manages to show all the Url publications, sorted by the number of votes
    pass
    
    def get_url_publications(): 
    #This method gets all the publications type url
        pass
    def sort_url_publications():
    #This method return the publications sorted by number of votes
        pass
    def show():
    #This method build the html news.html with the url publications sorted. 
        pass
    pass

class NewestView(): 
    #This class manages to show all Publications, sorted by descendent creation date 
    pass 
class SubmitView(): 
    #This class manages to ahow a form for creating a new Publication, and creates the publication with its features.
    pass
class PublicationView(): 
    #This class manages to show a particular publication (Url or Ask) and show its comments and the replies to each comment. 
    pass

def news_view(request, *args, **kwargs):

    
    
    contributions = Publication.objects.all() 
    contributions = sorted(contributions, key = lambda x: x.created_at, reverse=True)

    return render(request, "news.html", {'contributions': contributions})
    # contributions = []
    # for subclass in Contribution.__subclasses__():
    #     for instance in subclass.objects.all():
    #         contributions.append(instance)
    # contributions.sort(key=lambda x: x.created_at, reverse=True)

    # context = {
    #   'contributions': contributions,
    # }
    
    # print('NEWS')

    # return render(request, "news.html", context) # the last is context

def newest_view(request, *args, **kwargs):
    pass
    # contributions = []
    # for subclass in Contribution.__subclasses__():
    #     for instance in subclass.objects.all():
    #         contributions.append(instance)
    # contributions.sort(key=lambda x: x.created_at, reverse=True)

    # context = {
    #   'contributions': contributions,
    # }
    
    # print('NEWEST')

    # return render(request, "newest.html", context) 

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}), max_length=160)
   
    

def show_contribution_view (request, kind, id):
    
     # get the contrib from the db
    try:
        # if kind == 'ask':
        #     contribution = Ask.objects.filter(id = id).first()
        # elif kind == 'url':
        #     contribution = Url.objects.filter(id = id).first()
        # else:
        #     print('nonsense')
        #     raise Exception
        p = Publication.objects.filter(id = 1).first()
        replies = Comment.objects.filter(referenced_publication=p, parent=None)

    except:
        contribution = None
    
    # # back to square one
    # if contribution is None:
    #     return HttpResponseRedirect(reverse('news_view'))

    context = {
        'contribution': replies,
        'form': CommentForm()

    }
    # get_comment(request)
    return render(request, "contribution.html", context)
    
# class ContributionView(FormView): 
#     pass
#     form_class = CommentForm
#     template_name = 'contribution.html'
#     context = {}

#     def form_valid(self, form): 
#         data = form.cleaned_data
#         text = data['comment']
        
#         new_comment = Comment(title=' ', content=text)

#         new_comment.save()
        

#         return HttpResponseRedirect(reverse('news_view'))
    
   

class SubmitView(FormView):
    # pass
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
        
        if url is '' or url is None:
            kind = 0 #Is an Ask publication
        else:
            kind = 1 #Is an Url publication          

        
        new_publication = Publication(title=title, question=text, url=url, kind=kind)
        new_publication.save()

        #If it is a URL publications and has a comment associated
        #Create the comment and associate with publication
        if kind == 1 and (text is not '' or text is not None): 
            new_comment = Comment(comment=text, referenced_publication=new_publication)
            new_comment.save()
        
            new_reply = Comment(comment="Hi, i'm a reply", parent=new_comment)
            new_reply.save()
        


       

        # if url is not '': #An url submission 

        #     if (Url.objects.filter(url=url).count() == 1):#it already exists
        #         # print("Hey i entered")  
        #         my_id = Url.objects.get(url=url).id #id of the references contribution
        #         # print(my_id)            
        #         uri = r"/url/" + str(my_id)
        #         return HttpResponseRedirect(uri)   
        #     else: 
        #         print("Im in the URL CZONE")
        #         contrib = Url(title = title, url = url) 

        #         if text is not '': #With a comment associated
        #             # contrib.addComment(text)
        #             pass
                
        #         contrib.save()

        # else: #An ask submission
        #     print("Im in the ask CZONE")
        #     contrib = Ask(title=title, content=text)
        #     contrib.save() 
        
        return HttpResponseRedirect("/news")        


        





