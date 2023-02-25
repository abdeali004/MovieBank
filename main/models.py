from django.db import models
from django.conf import settings
# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    gender = models.CharField(max_length=10, default="male")
    age = models.CharField(max_length=10, default="low")
    movieType = models.TextField()
    lang = models.TextField()
    genre = models.TextField()
    newUser = models.BooleanField(default=True)
    dateJoined = models.DateField()

    def __str__(self):
        return self.username
