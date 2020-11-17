from django.contrib import admin

# Register your models here.
from contributions import models

admin.site.register(models.Publication)
admin.site.register(models.Comment)
admin.site.register(models.VotePublication)
admin.site.register(models.VoteComment)

