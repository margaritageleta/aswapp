from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from contributions.models import Publication, Comment, VotePublication, Hacker
from contributions.api.serializers import PublicationSerializer, CommentSerializer, VoteItemSerializer

class ItemsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    permission_classes = [HasAPIKey]

    # Get all publications (all kinds)
    def get(self, request): 
        queryset = Publication.objects.all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    # Create a new publication
    def post(self, request):
        serializer_class = PublicationSerializer(data=request.data)
        key = request.META["HTTP_AUTHORIZATION"].split()[1]

        # Check for authorization
        if Hacker.objects.filter(api_key=key).exists():
            # If form data is valid (all params set)
            if serializer_class.is_valid():
                # If is url
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
    # Get all publications of type ASK
    def get(self, request): 
        queryset = Publication.objects.filter(kind=0).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemUrlsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    # Get all publications of type URL
    def get(self, request): 
        queryset = Publication.objects.filter(kind=1).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    # Get an item by id
    def get(self, request, id, format=None):
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
        queryset = Publication.objects.filter(id=id).first()
        # On successful delete, return no content
        if queryset:
            queryset.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        # Otherwise return error
        else:
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)
        # TODO 403 forbidden to delete not yours
        # TODO 401 authorization to delete yours
    
    # TODO How to update votes?
class ItemVotesAPIView(ListAPIView):
    """
    queryset = ''
    serializer_class = PublicationSerializer
    user, voter = 'rita.geleta', 1 # hardcoded

    def get(self, request, id, format=None):
        queryset = VotePublication.objects.filter(contribution=id, voter=self.voter).first() # hardcoded
        serializer_class = VoteItemSerializer(queryset, many=False)



        if self.user == 'rita.geleta': # autheticated
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        else: # not autheticated
            return Response({'status': 'Error 401, unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, id, format=None):


        print(request.META["HTTP_AUTHORIZATION"])
        
        print(request)
        print(request.data)
        print(request.GET.get('api_key'))
        return Response({'status' : 'hello'}, status=status.HTTP_200_OK)
    """
    pass

    """
    def patch(self, request, id, format=None):
        queryset = Publication.objects.filter(id=id).first()
        serializer_class = PublicationSerializer(queryset, many=False)
        # On successful delete, return no content
        if queryset and serializer_class.is_valid():
            ...
        # Otherwise return error
        else:
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)
        # TODO 403 forbidden to delete not yours
        # TODO 401 authorization to delete yours
    """

class ItemCommentsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    # Get all comments of a given publication
    def get(self, request, id, format=None): 
        ref_publication = Publication.objects.filter(id=id).first()
        queryset = Comment.objects.filter(referenced_publication=ref_publication).all()
        # If referenced publication exists
        if queryset:
            serializer_class = CommentSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        # Otherwise, it does not exist, return error
        else:
            return Response({'status': 'Error 404, item of comment not found'}, status=status.HTTP_404_NOT_FOUND)

class CommentListAPIView(ListAPIView):
    queryset = ''
    serializer_class = CommentSerializer
    # Get all comments of a given publication
    def get(self, request, format=None): 
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
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
    # Get a comment by id
    def get(self, request, id, format=None):
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
        queryset = Comment.objects.filter(id=id).first()
        # On successful delete, return no content
        if queryset:
            queryset.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        # Otherwise return error
        else:
            return Response({'status': 'Error 404, comment not found'}, status=status.HTTP_404_NOT_FOUND)
        # TODO 403 forbidden to delete not yours
        # TODO 401 authorization to delete yours
    
    # TODO How to update votes?
    """
    def patch(self, request, id, format=None):
        queryset = Publication.objects.filter(id=id).first()
        serializer_class = PublicationSerializer(queryset, many=False)
        # On successful delete, return no content
        if queryset and serializer_class.is_valid():
            ...
        # Otherwise return error
        else:
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)
        # TODO 403 forbidden to delete not yours
        # TODO 401 authorization to delete yours
    """