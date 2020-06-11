from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user-images', blank=True)

    def __str__(self):
        return f"{self.user.username} image"

def get_user_image_url(user):
    if UserImage.objects.filter(user=user):
        img = UserImage.objects.get(user=user)
        return img.user_image.url
    else:
        return "/media/species-images/default.jpg"