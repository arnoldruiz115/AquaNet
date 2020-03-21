from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from . models import Profile, ProfileImage


class SpeciesProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['common_name', 'species', 'max_size', 'water_type']


class SpeciesImageForm(ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
