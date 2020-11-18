from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.views import View
from django.contrib.auth.models import User
from users.models import Hacker
from users.forms import ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



# Create your views here.


class UserComments(View): 
    template_name = "news.html"

    def get(self, request, id): 
        hacker = Hacker.objects.get(username=id)
        context = {
            'contributions': hacker.get_comments(),
        }
        return render(request, self.template_name, context)

class UserContributions(View):
 
    template_name = "news.html"
    
    def get(self, request, id): 
        hacker = Hacker.objects.get(username=id)
        context = {
            'contributions': hacker.get_publications(),
        }
        return render(request, self.template_name, context)


class ProfileView(View): 
    # This class manages the display of the 
    # users' profiles
    template_name = "profile.html"
    context = {}
    form = ProfileForm()

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

        context = {
            'username': hacker.get_username(),
            'karma': hacker.get_karma(),
            'joined': hacker.get_created_time(),
            'email': hacker.get_email(),  
            'description': hacker.get_description(),
            'form': self.form         

        }
        return render(request, self.template_name, context)

    def post(self, request):
        new_description = request.POST['description']  
        if (new_description != ""):    
            user = User.objects.get(username=request.user)
            hacker = Hacker.objects.get(user=user)
            hacker.set_description(new_description)
            hacker.save()
        return HttpResponseRedirect(reverse('profile_view'))
 

class UserView(View):

    # This class manages the display of the 
    # users' profiles
    template_name = "profile.html"
    context = {}
    def get(self, request, id):
        # This method builds the client page profie.html 
        # with the requested user dataç

    
        user = User.objects.get(id=id)
        

        #See if the user has been registered in 
        if Hacker.objects.filter(user = user).count() == 0: 
            hacker = Hacker(user=user, username=user.username)
            hacker.save()
            
        else: 
            hacker = Hacker.objects.get(user=user)
                 
        context = {
            'username': hacker.get_username(),
            'karma': hacker.get_karma(),
            'joined': hacker.get_created_time(),
            'email': hacker.get_email(),       

        }
        

        if (str(hacker.get_username()) == str(request.user)): 
            return HttpResponseRedirect(reverse('profile_view'))
        else: 
            return render(request, self.template_name, context)

def logout(request):
    #end session
    do_logout(request)
    #deberia redireccionar a la misma donde se hace logout pero aun no se
    return redirect('/news')
