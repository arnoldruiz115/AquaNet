from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    image = models.ImageField(upload_to='species-images', blank=True)
    common_name = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.common_name:
            return self.common_name
        else:
            return self.species
