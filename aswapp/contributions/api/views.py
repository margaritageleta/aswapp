from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from contributions.models import Publication
from contributions.api.serializers import PublicationSerializer




class ItemsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer

    def get(self, request): 
        queryset = Publication.objects.all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    def item_existing(self, url): 
        return Publication.objects.filter(url=url).count()

    def post(self,request):
        serializer_class = PublicationSerializer(data=request.data)
        if serializer_class.is_valid():
            if request.data['kind'] == '1' and Publication.objects.filter(url=request.data['url']).exists():
                return Response({'status': 'Error 409, url already exists'}, status=status.HTTP_409_CONFLICT)
            else:
                serializer_class.save()
                # CommentAPI.post() <-- hipotesis POST 201
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)  
        else:
            return Response({'status': 'Error 400, bad request'}, status=status.HTTP_400_BAD_REQUEST)
        # TODO 401
        # TODO Look up the creation of asks -> not comment associated

class ItemsAsksListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer

    def get(self, request): 
        queryset = Publication.objects.filter(kind=0).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemUrlsListAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer

    def get(self, request): 
        queryset = Publication.objects.filter(kind=1).all()
        serializer_class = PublicationSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class ItemAPIView(ListAPIView):
    queryset = ''
    serializer_class = PublicationSerializer

    def get(self, request, id, format=None):
        queryset = Publication.objects.filter(id=id).first()
        serializer_class = PublicationSerializer(queryset, many=False)
        if queryset:
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error 404, item not found'}, status=status.HTTP_404_NOT_FOUND)

class ItemCommentsListAPIView(ListAPIView):
    pass
class CommentAPIView(ListAPIView):
    pass