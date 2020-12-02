from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from contributions.models import Publication, Comment
from users.models import Hacker
from users.api.serializers import HackerSerializer


class UserAPIView(ListAPIView):
    queryset = ''
    serializer_class = HackerSerializer
    # Get an user by id
    def get(self, request, id, format=None):
        queryset = Hacker.objects.filter(id=id).first()
        serializer_class = HackerSerializer(queryset, many=False)
        # If user exists, return JSON
        if queryset:
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, user not found'}, status=status.HTTP_404_NOT_FOUND)

class UserItemsListAPIView(ListAPIView):
    pass

class UserCommentsListAPIView(ListAPIView):
    pass

class UserVotedItemsListAPIView(ListAPIView):
    pass

class UserVotedCommentsListAPIView(ListAPIView):
    pass
