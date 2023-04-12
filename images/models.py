from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Imagen(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - por' + self.user.username
    
    class Meta:
        db_table = "images_imagen"