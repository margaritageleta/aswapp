from rest_framework import serializers

from users.models import Hacker


class HackerSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Hacker
        fields = [
            'username',
            'karma',
            'upvotes',
            'downvotes',
            'created_at',
            'description'           
        ]