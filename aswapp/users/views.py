from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login

# Create your views here.
# def welcome(request):
#     if request.user.is_authenticated:
#         return render(request)

#login y register en la misma pagina y luego pagina register para errores
def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request,user)
                return redirect('/')
    return render(request, "users/login.html", {'form': form})

def register(request):
    return render(request, "users/register.html")

def forgot(request):
    return render(request, "users/forgot.html")

def logout(request):
    #end session
    do_logout(request)
    #deberia redireccionar a la misma donde se hace logout pero aun no se
    return redirect('/news')

