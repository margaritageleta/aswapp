from django.conf.urls import url
from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView
from django.urls import include
from aswapp import settings
from users import views


urlpatterns =[
    path(r'^logout/$', views.logout, name='logout'),
    path (r'^profile/$', views.ProfileView.as_view(), name='profile_view'),
    path (r'^profile_user/(?P<id>[0-9A-Za-z_\-]+)/$', views.UserView.as_view(), name='show_user_view'),
    path (r'^profile_user/(?P<id>[0-9A-Za-z_\-]+)/contributions/$', views.UserContributions.as_view(), name='show_contributions_user'),
    path (r'^^profile_user/(?P<id>[0-9A-Za-z_\-]+)/comments/$', views.UserComments.as_view(), name='show_comments_user'),
    path('', include('social_django.urls', namespace='social')),

    

]