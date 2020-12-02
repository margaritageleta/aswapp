from django.conf.urls import url

from users.api import views


urlpatterns = [
    #url(r'^$', views.UsersAPIView.as_view(), name='users'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/$', views.UserAPIView.as_view(), name='user'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/items/$', views.UserItemsListAPIView.as_view(), name='user_items'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/comments/$', views.UserCommentsListAPIView.as_view(), name='user_comments'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/votedItems/$', views.UserVotedItemsListAPIView.as_view(), name='user_voted_items'),
    url(r'^(?P<id>[0-9A-Za-z_\-]+)/votedComments/$', views.UserVotedCommentsListAPIView.as_view(), name='user_voted_comments'),
]