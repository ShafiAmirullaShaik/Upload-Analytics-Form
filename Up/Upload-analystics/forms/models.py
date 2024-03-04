from django.db import models

# Create your models here.


class fileData(models.Model):
    filename = models.CharField(max_length = 100)
    extension = models.CharField(max_length = 10)
    createdAt = models.DateField(auto_now_add=True)


class testingUploadModel(models.Model):
    dataSource = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    filePath = models.TextField()