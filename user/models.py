from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    OWNER = 'owner'
    VENDOR = 'vendor'
    CUSTOMER = 'customer'
    ROLE = (
       (OWNER, _('owner')),
       (VENDOR, _('vendor')),
       (CUSTOMER, _('customer')),
       )
    
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=8, choices=ROLE, default=CUSTOMER)
    phone = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [phone]

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'