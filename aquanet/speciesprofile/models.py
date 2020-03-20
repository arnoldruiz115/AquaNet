from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


# Create your models here.
class Profile(models.Model):
    image = models.ImageField(upload_to='species-images', blank=True)
    common_name = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Modify model elements
        self.water_type += "water"
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        if self.common_name:
            return self.common_name
        else:
            return self.species

    def get_absolute_url(self):
        return reverse('speciesprofile:detail', kwargs={'pk': self.pk})


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='species-images', blank=True)

    def __str__(self):
        if self.profile.common_name:
            return self.profile.common_name + " image"
        else:
            return self.profile.species + " image"
