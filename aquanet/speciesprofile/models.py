from django.db import models


# Create your models here.
class Profile(models.Model):
    common_name = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)

    def __str__(self):
        if self.common_name:
            return self.common_name
        else:
            return self.species
