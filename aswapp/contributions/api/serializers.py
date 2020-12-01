from rest_framework import serializers

from contributions.models import Publication, Comment

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = [
            'id',
            'comment',
            'created_at',
            'referenced_publication',
            'parent',         
        ]