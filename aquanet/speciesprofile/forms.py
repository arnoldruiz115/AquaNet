from django.forms import ModelForm, Form
from django.forms import inlineformset_factory, formset_factory
from . models import Profile, ProfileImage


class SpeciesProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['common_name', 'species', 'max_size', 'water_type']


class SpeciesImageForm(ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']


ProfileImageFormset = formset_factory(form=SpeciesImageForm, extra=1)
ImagesFormset = inlineformset_factory(Profile, ProfileImage, fields=['image'], extra=1)
