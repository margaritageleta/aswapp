from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.models import User
from users.models import Hacker
from users.forms import ProfileForm
from contributions.models import Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from contributions.models import VoteComment



# Create your views here.


class UserComments(View): 
    template_name = "comments.html"
    comments = {}

    def get_replies(self, comment):
        # Obtains replies of comments recursively
        subcomments = {}
        subreplies = Comment.objects.filter(parent=comment)
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

    def get(self, request, id): 
        hacker = Hacker.objects.get(id=id)
        # print(hacker.username)
        hacker_comments = hacker.get_comments()
        self.comments = {}

        try:
            for comment in hacker_comments:
                self.comments[comment] = self.get_replies(comment)

            votes_c = set()
            self.create_comment_set(votes_c, hacker, self.comments)
            
        except Exception as e:
            # Back to square one
            return HttpResponseRedirect(reverse('news_view'))

        context = {
            'replies': self.comments,
            'threads': True,
            'c_votes': votes_c
        }
        return render(request, self.template_name, context)

class UserContributions(View):
 
    template_name = "news.html"
    
    def get(self, request, id): 
        hacker = Hacker.objects.get(id=id)
        context = {
            'contributions': hacker.get_publications(),
        }
        return render(request, self.template_name, context)


class ProfileView(View): 
    # This class manages the display of the 
    # users' profiles
    template_name = "profile.html"
    context = {}
    # form = ProfileForm()

    def get(self, request, *args, **kwargs):
        # This method builds the client page profie.html 
        # with the requested user dataç
        
        user_name = request.user
        user = User.objects.get(username=user_name)
    
        # #See if the user has been registered in 
        if Hacker.objects.filter(user = user).count() == 0: 
            hacker = Hacker(user=user, username=user_name)
            hacker.save()
            
        else: 
            hacker = Hacker.objects.get(user=user)  

        print('PRE')
        print(f' HACKER {hacker.user.id}')

        context = {
            'hackerid': hacker.user.id,
            'username': hacker.get_username(),
            'karma': hacker.get_karma(),
            'joined': hacker.get_created_time(),
            'email': hacker.get_email(),  
            'description': hacker.get_description(),
            'form': ProfileForm(initial={'description': hacker.get_description()})        
        }

        print(context)

        return render(request, self.template_name, context)

    def post(self, request):
        new_description = request.POST['description']  
        user = User.objects.get(username=request.user)
        hacker = Hacker.objects.get(user=user)
        hacker.set_description(new_description)
        hacker.save()
        return HttpResponseRedirect(reverse('show_user_view', kwargs={'id':hacker.user.id}))
 

class UserView(View):

    # This class manages the display of the 
    # users' profiles
    template_name = "profile.html"
    context = {}
    def get(self, request, id):
        # This method builds the client page profie.html 
        # with the requested user data

        user = User.objects.get(id=id)

        # See if the user has been registered in 
        if Hacker.objects.filter(user = user).count() == 0: 
            hacker = Hacker(user=user, username=user.username)
            hacker.save()
            
        else: 
            hacker = Hacker.objects.get(user=user)
                 
        context = {
            'hackerid': hacker.user.id,
            'username': hacker.get_username(),
            'karma': hacker.get_karma(),
            'joined': hacker.get_created_time(),
            'email': hacker.get_email(),       
            'description': hacker.get_description(),
        }
        
        # if (str(hacker.get_username()) == str(request.user)): 
        #     return HttpResponseRedirect(reverse('show_user_view', kwargs={'id':hacker.user.id}))
        # else: 
        return render(request, self.template_name, context)

def logout(request):
    # end session
    do_logout(request)
    # deberia redireccionar a la misma donde se hace logout pero aun no se
    return redirect('/news')
