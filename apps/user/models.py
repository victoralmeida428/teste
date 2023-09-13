from django.db import models

# Create your models here.
class PixImage(models.Model):
    valor = models.IntegerField()
    pix = models.ImageField()

