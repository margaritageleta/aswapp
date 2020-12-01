from rest_framework import serializers

from contributions.models import Publication

class PublicationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Publication
        fields = [
            'id',
            'author',
            'created_at',
            'title',
            'question',
            'url',
            'kind'           
        ]