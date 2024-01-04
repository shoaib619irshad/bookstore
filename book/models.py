from django.db import models

from user.models import CustomUser


class Books(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    published_year = models.CharField(max_length=4)
    issued_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)