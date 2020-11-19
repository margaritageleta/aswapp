from django.db import models
from django.utils import timezone
from django.apps import apps


# Create your models here.

class Contribution(models.Model):
    
    
    title = models.CharField(max_length=80)
    content = models.TextField()
    url = models.URLField(null=True, unique=True)
    created_at = models.DateTimeField(default=timezone.now())  

    comments = []
    
    class Meta:
        abstract = True

    objects = models.Manager()
    def addComment(self, comment): 
        self.comments.append(comment)

class Ask(Contribution):
    kind = 'ask'       
    url = None
class Url(Contribution): 
    kind = 'url'

    def exists(self, url):
        if Url.objects.exists.url == url: return True
        return False 
    
 
    



    