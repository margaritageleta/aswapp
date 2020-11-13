from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

# Create your models here.
class Hacker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=80)
    karma = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    objects = models.Manager()

    

    def get_publications(self):
        Publication = apps.get_model('contributions', 'Publication') #This is done due circular imports
        return Publication.objects.filter(author=self)

    def add_upvotes(self): 
        self.upvotes += 1
        self.calculate_karma()
    
    def remove_upvotes(self):
        self.upvotes += 1
        self.calculate_karma()
    
    
    def add_downvotes(self):
        self.downvotes += 1
        self.calculate_karma()

    def remove_downvotes(self):
        self.downvotes -= 1
        self.calculate_karma

    def set_username(self, new_username):
        self.username = new_username
    
    def calculate_karma(self): 
        self.karma = self.upvotes-self.downvotes

    