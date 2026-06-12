from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=32,null=True, blank=True)
    validators = [MinLengthValidator(2),MaxLengthValidator(32)]
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','full_name']

    def save(self, *args, **kwargs):
        
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
