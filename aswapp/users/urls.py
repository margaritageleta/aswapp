from django.conf.urls import url
from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView
from django.urls import include
from aswapp import settings
from users import views


urlpatterns =[

    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile_view'),
    url(r'^profile/(?P<id>[0-9A-Za-z_\-]+)/$', views.UserView.as_view(), name='show_user_view'),
    url(r'^profile/(?P<id>[0-9A-Za-z_\-]+)/contributions/$', views.UserContributions.as_view(), name='show_contributions_user'),
    url(r'^profile/(?P<id>[0-9A-Za-z_\-]+)/comments/$', views.UserComments.as_view(), name='show_comments_user'),
    url(r'^profile/(?P<id>[0-9A-Za-z_\-]+)/upvoted/(?P<kind>[-\w]+)/$', views.UpvotedView.as_view(), name='upvoted_contributions_view'),
    path('', include('social_django.urls', namespace='social')),

]