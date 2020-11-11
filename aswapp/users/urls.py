from django.conf.urls import url
from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView
from django.urls import include
from aswapp import settings
from users import views


urlpatterns =[
    # path(r'register', views.register, name='register_view'),
    # path(r'login', views.login, name='login_view'),
    # path(r'forgot', views.forgot, name='forgot_view'),
    # path('logout/',
    #    LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),
    #    name='logout'
    # ),
    path (r'profile', views.ProfileView.as_view(), name='profile_view'),
    path('', include('social_django.urls', namespace='social')),
    

]