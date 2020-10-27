from django.db import models

# Create your models here.


class UserInfo(models.Model):

    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Passage(models.Model):

    colum = models.CharField(max_length=64)
    title = models.CharField(max_length=256, primary_key=True)
    content = models.TextField()
