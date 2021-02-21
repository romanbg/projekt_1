from django.db import models

# Create your models here.

class Jana2006Document(models.Model):
    file = models.FileField(upload_to='constrain_file')

class HklDocument(models.Model):
    title = models.CharField(max_length=64)
    h_column = models.IntegerField()
    k_column = models.IntegerField()
    l_column = models.IntegerField()
    intensity = models.FloatField()