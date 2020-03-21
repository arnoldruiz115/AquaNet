from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


# Create your models here.
class Profile(models.Model):
    common_name = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail_url = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Modify model elements
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
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        # Modify model elements
        images_count = ProfileImage.objects.filter(profile=self.profile.pk).count()
        self.order = images_count
        super(ProfileImage, self).save(*args, **kwargs)

        # If profile has no images, first image will be the thumbnail. Do after image has been saved to get url
        if images_count == 0:
            self.profile.thumbnail_url = self.image.url
            self.profile.save()

    def __str__(self):
        if self.profile.common_name:
            return "{}-{} image {}".format(self.profile.author, self.profile.common_name, self.order)
        else:
            return "{}-{} image {}".format(self.profile.author, self.profile.species, self.order)
