from django.db import models
from django.utils import timezone

# Create your models here.

class Contribution(models.Model):

    title = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True
    
    objects = models.Manager()

    # def get_all (self):
    #    rel_objs = self._meta.get_all_related_objects()
    #    return [getattr(self, x.get_accessor_name()) for x in rel_objs if x.model != type(self)]

class Url(Contribution):
    kind = 'url'

class Ask(Contribution):
    kind = 'ask'


    