from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from contributions.models import Publication, Comment, VotePublication, Hacker, VoteComment
from contributions.api.serializers import PublicationSerializer, CommentSerializer

class ItemsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]

    # Get all publications (all kinds)
    def get(self, request): 
        """
        Get all the publications.

        Return all the publications regardless it's a url or ask publication
        ---
        responseMessages:
                - code: 200
                    description: 'OK'
        """
        
        permission_classes = [AllowAny]
        queryset = Publication.objects.all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    # Create a new publication
    def post(self, request):
        """
        Post a new publications.

        Return all the publications regardless it's a url or ask publication
        ---  
        """
        
        self.permission_classes = [HasAPIKey]
        serializer_class = PublicationSerializer(data=request.data)
        key = request.META["HTTP_AUTHORIZATION"].split()[1]

        # Check for authorization
        if Hacker.objects.filter(api_key=key).exists():
            # If form data is valid (all params set)
            if serializer_class.is_valid():
                # If is url
                if request.data['author'] != Hacker.objects.filter(api_key=key).first().id:
                    return Response({'status': 'Error 403, author does not match with id'}, status=status.HTTP_403_FORBIDDEN)     
                else:
                    if request.data['kind'] == '1':
                        #If repeated
                        if Publication.objects.filter(url=request.data['url'], kind=1).exists():
                            return Response({'status': 'Error 409, url already exists'}, status=status.HTTP_409_CONFLICT)
                        else: 
                            if len(request.data['url']) > 0:
                                if len(request.data['question']) > 0: 
                                    return Response({'status': 'Error 409, question must be empty in a url kind publication'}, status=status.HTTP_409_CONFLICT)
                                else: 
                                    serializer_class.save()
                                    return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
                            else: 
                                return Response({'status': 'Error 409, url must not be empty in a url kind publication'}, status=status.HTTP_409_CONFLICT)
                    # Otherwise a completely new publication
                    else:
                        if len(request.data['url']) > 0:
                            return Response({'status': 'Error 409, url must be empty in a ask kind publication'}, status=status.HTTP_409_CONFLICT)
                        else:
                            serializer_class.save()
                            return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
            else:
                return Response({'status': 'Error 400, bad request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class ItemsAsksListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]

    # Get all publications of type ASK
    def get(self, request): 
        """
        Get all the publications of type ask.

        Return all the ask publications in the system.
        ---  
        """
        queryset = Publication.objects.filter(kind=0).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemUrlsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]

    # Get all publications of type URL
    def get(self, request): 
        """
        Get all publications of type URL.

        Return all publications of type URL.
        ---  
        """
        queryset = Publication.objects.filter(kind=1).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]

    # Get an item by id
    def get(self, request, id, format=None):
        """
        Get an item by id.

        Return an item identified by an id.
        ---  
        """
        permission_classes = [AllowAny]

        queryset = Publication.objects.filter(id=id).first()
        serializer_class = PublicationSerializer(queryset, many=False)
        # If items exists, return JSON
        if queryset:
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)

    
    # Delete an item by id
    def delete(self, request, id, format=None):
        """
        Delete an item by id.

        Delete from the system an item indentified by an id.
        ---  
        """
        self.permission_classes = [HasAPIKey]
        queryset = Publication.objects.filter(id=id).first()
        key = request.META["HTTP_AUTHORIZATION"].split()[1]

        # Check for authorization
        if Hacker.objects.filter(api_key=key).exists():
            # If deleted item author id marches with api key 
            if queryset.author.id == Hacker.objects.filter(api_key=key).first().id:
                # On successful delete, return no content
                if queryset:
                    queryset.delete()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                # Otherwise return error
                else:
                    return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
               return Response({'status': 'Error 403, forbidden to delete this item'}, status=status.HTTP_403_FORBIDDEN)      
        else:
            return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # TODO How to update votes?
class ItemVotesAPIView(ListAPIView):
    #Votar y desvotar
    permission_classes = ''
    def post(self, request, id, format=None): 
        """
        Vote/Unvote a publication by id.

        Vote and unvote a publication identified by an id.
        ---  
        """
        permission_classes = [HasAPIKey]
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
    
        if Publication.objects.filter(id=id).exists():
            c = Publication.objects.get(id=id) 
            if c.author.api_key != key:
                if  Hacker.objects.filter(api_key=key).exists():
                    h = Hacker.objects.get(api_key=key)
                    if VotePublication.objects.filter(voter=h, contribution=c).exists():
                        VotePublication.objects.get(voter=h, contribution=c).delete()
                        return Response({'status': '202, publication unvoted'}, status=status.HTTP_404_NOT_FOUND)
                    else: 
                        VotePublication(voter=h, contribution=c).save()
                        return Response({'status': '202, publication voted'}, status=status.HTTP_404_NOT_FOUND)
                else: 
                    return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            else: 
                return Response({'status': 'Error 409, cannot vote your own publication'}, status=status.HTTP_409_CONFLICT)

        else: 
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)

class ItemCommentsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    # Get all comments of a given publication
    def get(self, request, id, format=None): 
        """
        Get comments of a publication.

        Get all comments of a given publication, indentified by the publication id.
        ---  
        """
        permission_classes = [AllowAny]

        ref_publication = Publication.objects.filter(id=id).first()
        queryset = Comment.objects.filter(referenced_publication=ref_publication).all()
        # If referenced publication exists
        if queryset:
            serializer_class = CommentSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, item of comment not found'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, id, format=None):
        """
        Post a comment in a publication.

        Create a new comment for a publication identified by the publication id.
        ---  
        """
        queryset = Comment.objects.none()
        serializer_class = CommentSerializer
        permission_classes = [HasAPIKey]
        key = request.META["HTTP_AUTHORIZATION"].split()[1]


        if Hacker.objects.filter(api_key = key).exists(): 
            serializer_class = CommentSerializer(data=request.data)
            # If form data is valid (all params set)
            if serializer_class.is_valid():
                
                ref_publication = Publication.objects.get(id=request.data['referenced_publication'])
                # author = Hacker.objects.get(api_key=key)
                

                # If publication referenced does not exist 
                if not ref_publication:
                    return Response({'status': 'Error 404, referenced publication must be specified'}, status=status.HTTP_404_NOT_FOUND)
                # Otherwise, create comment to that publication
                else:
                    # If match save, otherwise return conflict
                        serializer_class.save()
                        return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
            else:
                return Response({'status': 'Error 400, bad request'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class CommentListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    # Get all comments
    def get(self, request, format=None):
        """
        Get all comments.

        Return all the existing comments.
        ---  
        """
        permission_classes = [AllowAny]

        queryset = Comment.objects.all()
        serializer_class = CommentSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Post a comment.

        Create a new comment.
        ---  
        """
        serializer_class = CommentSerializer(data=request.data)
        # If form data is valid (all params set)
        if serializer_class.is_valid():

            ref_publication = request.data['referenced_publication']   
            parent = request.data['parent'] 

            parent_comment = Comment.objects.filter(id=parent).first()
            # If parent comment does not exist 
            if not parent_comment:
                return Response({'status': 'Error 404, parent does not exist'}, status=status.HTTP_404_NOT_FOUND)
            # Otherwise, check parent comment matches referenced publication
            else:
                # If match save, otherwise return conflict
                if Comment.objects.filter(id=parent, referenced_publication=ref_publication).exists():
                    serializer_class.save()
                    return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
                else:
                    return Response({'status': 'Error 409, parent does not match item'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'status': 'Error 400, bad request'}, status=status.HTTP_400_BAD_REQUEST)
        # TODO 401 authorization to create an item
        
class CommentAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    # Get a comment by id
    def get(self, request, id, format=None):
        """
        Get a comment by id

        Return a comment identified by the comment id.
        ---  
        """
        permission_classes = [AllowAny]

        queryset = Comment.objects.filter(id=id).first()
        serializer_class = CommentSerializer(queryset, many=False)
        # If comment exists, return JSON
        if queryset:
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete a comment by id
    def delete(self, request, id, format=None):
        """
        Delete a comment by id

        Delete a comment identified by the comment id.
        ---  
        """
        self.permission_classes = [HasAPIKey]
        self.queryset = Comment.objects.filter(id=id).first()
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        # Check for authorization
        if Hacker.objects.filter(api_key=key).exists():
            print(":"*100)
            # If deleted item author id marches with api key 
            if self.queryset.author.id == Hacker.objects.filter(api_key=key).first().id:
                # On successful delete, return no content
                if self.queryset:
                    Comment.objects.get(id=id).delete()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                # Otherwise return error
                else:
                    return Response({'status': 'Error 404, comment not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
               return Response({'status': 'Error 403, forbidden to delete this comment'}, status=status.HTTP_403_FORBIDDEN)      
        else:
            return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    # TODO How to update votes?
    
class CommentVotesAPIView(ListAPIView):
    #Votar y desvotar
    permission_classes = ''
    def post(self, request, id, format=None): 
        """
        Vote/Unvote a comment.

        Vote and unvote a comment identified by the comment id.
        ---  
        """
        permission_classes = [HasAPIKey]
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
    
        if Comment.objects.filter(id=id).exists():
            c = Comment.objects.get(id=id) 
            if c.author.api_key != key:
                if  Hacker.objects.filter(api_key=key).exists():
                    h = Hacker.objects.get(api_key=key)
                    if VoteComment.objects.filter(voter=h, contribution=c).exists():
                        VoteComment.objects.get(voter=h, contribution=c).delete()
                        return Response({'status': '202, comment unvoted'}, status=status.HTTP_404_NOT_FOUND)
                    else: 
                        VoteComment(voter=h, contribution=c).save()
                        return Response({'status': '202, comment voted'}, status=status.HTTP_404_NOT_FOUND)
                else: 
                    return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            else: 
                return Response({'status': 'Error 409, cannot vote your own comment'}, status=status.HTTP_409_CONFLICT)

        else: 
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)