from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.utils import timezone
from rest_framework_api_key.models import APIKey

class Hacker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=80)
    api_key = models.CharField(max_length=128, null=True, blank=True)
    karma = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now(), null=False)
    description = models.CharField(default="",max_length=500)

    objects = models.Manager()    

    
    def get_username(self):
        return self.user.username 
        
    def get_publications(self):
        Publication = apps.get_model('contributions', 'Publication') #This is done due circular imports
        return Publication.objects.filter(author=self)
    
    def get_comments(self):
        Comment = apps.get_model('contributions', 'Comment')
        return Comment.objects.filter(author=self, parent=None)

    def get_created_time(self):
        return self.user.date_joined
    
    def get_email(self):
        return self.user.email

    def add_upvotes(self): 
        self.upvotes += 1
        self.calculate_karma()
    
    def remove_upvotes(self):
        self.upvotes -= 1
        self.calculate_karma()
    
    def add_downvotes(self):
        self.downvotes += 1
        self.calculate_karma()

    def remove_downvotes(self):
        self.downvotes -= 1
        self.calculate_karma()

    def set_username(self, new_username):
        self.user.username = new_username
        self.user.save()
    
    def calculate_karma(self): 
        self.karma = self.upvotes-self.downvotes
    
    def get_karma(self):
        self.calculate_karma()
        return self.karma

    def get_description(self):
        return self.description

    def set_description(self, new_description):
        self.description = new_description
