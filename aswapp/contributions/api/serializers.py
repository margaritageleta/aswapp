from rest_framework import serializers

from contributions.models import Publication, Comment, VotePublication

class PublicationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Publication
        fields = [
            'id',
            'author',
            'number_votes',
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
            'author',
            'comment',
            'referenced_publication',
            'parent',         
        ]

