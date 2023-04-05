from django.db import models

# Create your models here.

class Imagen(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "images_imagen"
5