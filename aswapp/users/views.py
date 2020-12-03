from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.views import View
from django.contrib.auth.models import User
from users.models import Hacker

# Create your views here.

class ProfileView(View): 
    # This class manages the display of the 
    # users' profiles
    template_name = "profile.html"

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
            

        }
        print("_____________________________")
        return render(request, self.template_name, context)

# class LoginView(View): 
#     template_name = "profile.html"
#     def get(self, request, *args, **kwargs):



#login y register en la misma pagina y luego pagina register para errores

def logout(request):
    #end session
    do_logout(request)
    #deberia redireccionar a la misma donde se hace logout pero aun no se
    return redirect('/news')

class UserContributionsView(View): 
    # This class manages the display of the 
    # URL publications, sorted by the number of votes
    template_name = "user_contributions.html"
    publications = []
    
    def get_url_publications(self): 
        # This method gets all the publications of type URL
        self.publications = self.hacker.get_publications()
        # print(self.publications)
    
    def sort_url_publications(self):
        # This method returns the publications sorted by number of votes
        self.publications = sorted(self.publications, key = lambda x: x.created_at, reverse=True)
        
    def get(self, request, id):
        # This method builds the client page news.html with the URL publications sorted 
        self.hacker = Hacker.objects.get(username=id)
        print(self.hacker)
        self.get_url_publications()
        self.sort_url_publications()
        return render(request, self.template_name, self.publications)
