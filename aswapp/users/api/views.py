from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from contributions.models import Publication, Comment, VoteComment, VotePublication
from contributions.api.serializers import PublicationSerializer, CommentSerializer
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
    queryset = ''
    serializer_class = PublicationSerializer
    # Get an user by id
    def get(self, request, id, format=None):
        author = Hacker.objects.get(id=id)
               
        # If there are publications, return JSON
        if Publication.objects.filter(author=author).exists():
            queryset = Publication.objects.filter(author=author).all()
            serializer_class = PublicationSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, user does not any publications'}, status=status.HTTP_404_NOT_FOUND)

class UserCommentsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    # Get an user by id
    def get(self, request, id, format=None):
        author = Hacker.objects.get(id=id)
               
        # If there are publications, return JSON
        if Comment.objects.filter(author=author).exists():
            queryset = Comment.objects.filter(author=author).all()
            serializer_class = CommentSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, user does not has any comments'}, status=status.HTTP_404_NOT_FOUND)

class UserVotedItemsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    # Get an user by id
    def get(self, request, id, format=None):
        author = Hacker.objects.get(id=id)
               
        # If there are voted publications, return JSON
        if VotePublication.objects.filter(voter=author).exists():
            data = []
            for vp in VotePublication.objects.filter(voter=author).all():
                data.append({
                    'id': vp.contribution.id,
                    'author': vp.contribution.author,
                    'created_at': vp.contribution.created_at,
                    'number_votes': vp.contribution.number_votes,
                    'title': vp.contribution.title,
                    'question': vp.contribution.question,
                    'url': vp.contribution.url,
                    'kind': vp.contribution.kind 
                })

            queryset = data
            serializer_class = PublicationSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, user does not has any voted publications'}, status=status.HTTP_404_NOT_FOUND)

class UserVotedCommentsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    # Get an user by id
    def get(self, request, id, format=None):
        author = Hacker.objects.get(id=id)
               
        # If there are voted publications, return JSON
        if VoteComment.objects.filter(voter=author).exists():
            data = []
            for vp in VoteComment.objects.filter(voter=author).all():
                data.append({
                    'id': vp.contribution.id,
                    'author': vp.contribution.author,
                    'comment': vp.contribution.comment,
                    'created_at': vp.contribution.created_at,
                    'referenced_publication': vp.contribution.referenced_publication,
                    'parent': vp.contribution.parent, 
                })

            queryset = data
            serializer_class = CommentSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, user does not has any voted comments'}, status=status.HTTP_404_NOT_FOUND)
