from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from contributions.models import Publication, Comment
from users.models import Hacker
from users.api.serializers import HackerSerializer


class UsersAPIView(ListAPIView):
    pass

class UserAPIView(ListAPIView):
    pass

class UserItemsListAPIView(ListAPIView):
    pass

class UserCommentsListAPIView(ListAPIView):
    pass

class UserVotedItemsListAPIView(ListAPIView):
    pass

class UserVotedCommentsListAPIView(ListAPIView):
    pass
