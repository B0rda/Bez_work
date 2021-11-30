from django.db import models

class MainData(models.Model):
    num = models.CharField(max_length=200)
    hashn = models.CharField(max_length=1000)
# Create your models here.
