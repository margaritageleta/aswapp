from django.db import models
from django.utils import timezone

# Create your models here.

class Contribution(models.Model):

    title = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

class Url(Contribution):
    kind = 'url'

class Ask(Contribution):
    kind = 'ask'


    