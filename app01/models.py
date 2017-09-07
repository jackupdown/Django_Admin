from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=32)
    info = models.TextField()

    def __str__(self):
        return self.name
