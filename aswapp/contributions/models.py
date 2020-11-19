from django.db import models
from django.utils import timezone
from django.apps import apps
from users.models import Hacker

# Create your models here.

class Contribution(models.Model):
    

    author = models.ForeignKey(Hacker, on_delete=models.CASCADE, blank=False, null=False) 
    number_votes = models.IntegerField(default=1, null=False)
    voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now(), null=False)
    modified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

    objects = models.Manager()

    def add_votes(self): 
        self.number_votes += 1

    def delete_votes(self): 
        self.number_votes -= 1
    
    def get_votes(self):
        return self.number_votes


class Publication(Contribution):

    class PublicationTypes(models.IntegerChoices):
       ASK = 0
       URL = 1
    

    title = models.CharField(max_length=80, null=False)
    question = models.TextField(blank=True)
    url = models.URLField(blank=True)
    kind = models.IntegerField(max_length=1, choices=PublicationTypes.choices) 

    def get_title(self):
        return self.title


class Comment(Contribution):
    #If parent is None then is the first comment, else is a reply to a existing comment
    #If parent is None references_publication is not None
    
    comment = models.TextField(null=False)    
    referenced_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name="reply", null=True)
    created_at = models.DateTimeField(default=timezone.now(), null=False)


class Vote(models.Model):
    voter = models.ForeignKey(Hacker, on_delete=models.CASCADE, blank=False, null=False) 
    
    class Meta:
        abstract = True

    objects = models.Manager()

class VotePublication(Vote):
    contribution =  models.ForeignKey(Publication, on_delete=models.CASCADE, blank=False, null=False) 

    class Meta:
        unique_together = (("voter", "contribution"),)


class VoteComment(Vote):
    contribution =  models.ForeignKey(Comment, on_delete=models.CASCADE, blank=False, null=False) 

    class Meta:
        unique_together = (("voter", "contribution"),)



    
 
    



    