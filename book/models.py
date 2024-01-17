from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser


class Books(models.Model):
    AVAILABLE = 'available'
    ORDERED = 'ordered'
    STATUS = (
       (AVAILABLE, _('available')),
       (ORDERED, _('ordered')),
       )
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    published_year = models.CharField(max_length=4)
    status = models.CharField(max_length=9, choices=STATUS, default=AVAILABLE)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)


class BookCart(models.Model):
   name = models.CharField(max_length=128)
   author = models.CharField(max_length=128)
   published_year = models.CharField(max_length=4)
   added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)