from django.db import models

# Create your models here.


class ShironekoGatcha(models.Model):
    time = models.DateTimeField(unique=True)
    star = models.IntegerField()
