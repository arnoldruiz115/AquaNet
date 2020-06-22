from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import get_user_image_url


# Create your models here.
class Profile(models.Model):
    common_name = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200)
    max_size = models.FloatField()
    water_type = models.CharField(max_length=50)
    for_sale = models.BooleanField(default=False)
    price = models.FloatField(null=True, blank=True, default=None)
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='species-images', blank=True, default=None)
    thumbnail_aspect_ratio = models.FloatField(null=True, blank=True, default=None)

    def get_author_image_url(self):
        return get_user_image_url(self.author)

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
    order = models.IntegerField(default=-1)
    aspect_ratio = models.FloatField(null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        # Modify model elements
        images_count = self.get_image_count()
        self.aspect_ratio = self.image.width / self.image.height
        if self.order == -1:
            self.order = images_count
        super(ProfileImage, self).save(*args, **kwargs)

        # If profile has no images, first image will be the thumbnail. Do after image has been saved to get url
        if images_count == 0:
            self.profile.thumbnail = self.image
            self.profile.thumbnail_aspect_ratio = self.aspect_ratio
            self.profile.save()

    def delete(self, using=None, keep_parents=False):
        position = self.order
        super(ProfileImage, self).delete()
        # If the first (thumbnail) image is being deleted, make the next image the thumbnail, if there is a next image
        if position == 0:
            if ProfileImage.objects.filter(profile=self.profile.pk, order=1):
                next_image = ProfileImage.objects.get(profile=self.profile.pk, order=1)
                self.profile.thumbnail = next_image.image
                self.profile.thumbnail_aspect_ratio = next_image.aspect_ratio
                self.profile.save()
            else:
                self.profile.thumbnail.delete()
                self.profile.thumbnail_aspect_ratio.delete()
                self.profile.save()
        # change order of remaining images
        while position < self.get_image_count():
            position += 1
            next_image = ProfileImage.objects.get(profile=self.profile.pk, order=position)
            next_image.order = position - 1
            next_image.save()

    def get_image_count(self):
        images_count = ProfileImage.objects.filter(profile=self.profile.pk).count()
        return images_count

    def __str__(self):
        if self.profile.common_name:
            return "{}-{} image {}".format(self.profile.author, self.profile.common_name, self.order)
        else:
            return "{}-{} image {}".format(self.profile.author, self.profile.species, self.order)
