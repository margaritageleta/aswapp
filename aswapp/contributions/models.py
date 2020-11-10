from django.db import models
from django.utils import timezone
from django.apps import apps


# Create your models here.

class Contribution(models.Model):
    
    number_votes = models.IntegerField(default=0, null=False)
    voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now(), null=False)
    modified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

    objects = models.Manager()



class Publication(Contribution):

    class PublicationTypes(models.IntegerChoices):
       ASK = 0
       URL = 1
    

    title = models.CharField(max_length=80, null=False)
    question = models.CharField(max_length=80, blank=True)
    url = models.URLField(blank=True)
    kind = models.IntegerField(max_length=1, choices=PublicationTypes.choices) 


class Comment(Contribution):
    #If parent is None then is the first comment, else is a reply to a existing comment
    #If parent is None references_publication is not None
    
    comment = models.CharField(max_length=80, null=False)    
    referenced_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name="reply", null=True)




    
 
    



    