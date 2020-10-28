from django.contrib import admin

# Register your models here.
from contributions import models

admin.site.register(models.Url)
admin.site.register(models.Ask)