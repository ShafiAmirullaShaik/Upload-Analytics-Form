from django.db import models

# Create your models here.


class filesData(models.Model):
    filename = models.CharField(max_length = 50)
    extension = models.CharField(max_length = 10)
    createdAt = models.DateField(auto_now_add=True)