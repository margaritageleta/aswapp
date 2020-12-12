from django.conf.urls import url
from contributions import views



urlpatterns = [
    url(r'^$', views.NewsView.as_view(), name='news_view'),
    url(r'news/$', views.NewsView.as_view(), name='news_view'),
    url(r'newest/$', views.NewestView.as_view(), name='newest_view'),
    url(r'submit/$', views.SubmitView.as_view(), name='submit_contribution_view'),
    url(r'ask/$', views.AskView.as_view(), name='ask_view'),
    url(r'^item/(?P<id>[0-9A-Za-z_\-]+)/$', views.PublicationView.as_view(), name='show_contribution_view'),
    url(r'^item/(?P<id>[0-9A-Za-z_\-]+)/comment/$', views.CommentView.as_view(), name = 'comment_view'),
    url(r'^item/(?P<id>[0-9A-Za-z_\-]+)/comment/add/$', views.ReplyView.as_view(), name = 'reply_view'),
    url(r'^delete/(?P<id>[0-9A-Za-z_\-]+)/$', views.DeleteView.as_view(), name='delete_publication_view'),
    url(r'^vote/(?P<kind>[-\w]+)/(?P<id>[0-9A-Za-z_\-]+)/$', views.VoteView.as_view(), name='vote_publication_view'),
    url(r'^unvote/(?P<kind>[-\w]+)/(?P<id>[0-9A-Za-z_\-]+)/$', views.UnvoteView.as_view(), name='unvote_publication_view'),

]
