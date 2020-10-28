from django.db import models
from django.utils import timezone
from django.apps import apps


# Create your models here.

class Contribution(models.Model):
    
    title = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())  
    
    class Meta:
        abstract = True

    objects = models.Manager()
   
    # @classmethod
    # def get_subclasses(self, abstract_class):
    #     result = []
    #     for model in apps.get_app_config('contributions').get_models():
    #         if issubclass(model, abstract_class) and model is not abstract_class:
    #             result.append(model)
    #     return result

class Ask(Contribution):
    kind = 'ask'          
class Url(Contribution):   
    kind = 'url'
    



    