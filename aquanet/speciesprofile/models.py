from django.db import models
from django.utils import timezone


# Create your models here.
class Profile(models.Model):
    common_name = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.common_name:
            return self.common_name
        else:
            return self.species
