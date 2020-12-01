from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from contributions.models import Publication, Comment
from contributions.api.serializers import PublicationSerializer, CommentSerializer




class ItemsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer
    # Get all publications (all kinds)
    def get(self, request): 
        queryset = Publication.objects.all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    # Create a new publication
    def post(self, request):
        serializer_class = PublicationSerializer(data=request.data)
        # If form data is valid (all params set)
        if serializer_class.is_valid():
            # If the url is repeated
            if request.data['kind'] == '1' and Publication.objects.filter(url=request.data['url']).exists():
                return Response({'status': 'Error 409, url already exists'}, status=status.HTTP_409_CONFLICT)
            # Otherwise a completely new publication
            else:
                serializer_class.save()
                # TODO CommentAPI.post() <-- hipotesis POST 201
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
        else:
            return Response({'status': 'Error 400, bad request'}, status=status.HTTP_400_BAD_REQUEST)
        # TODO 401 authorization to create an item
        # TODO Look up the creation of asks -> not comment associated

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