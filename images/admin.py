from django.contrib import admin
from django.db import models
from .models import Imagen

# Register your models here.
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img')

admin.site.register(Imagen, ImagenAdmin)