from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone = models.IntegerField(null=True)
    image = models.URLField(max_length=200, default="https://picsum.photos/id/1025/200/300")
    country = models.CharField(max_length=80, null=True) #unsure why it is requesting a default value for country when running makemigrations 
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
