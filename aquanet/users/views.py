from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import formset_factory
from .forms import UserRegisterForm
from speciesprofile.forms import SpeciesProfileForm, SpeciesImageForm
from speciesprofile.models import Profile, ProfileImage


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created! You can now login {username}.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_profile(request, username):
    ProfileImageFormset = formset_factory(form=SpeciesImageForm, extra=3)
    user = get_object_or_404(User, username=username)
    if Profile.objects.filter(author=user):
        posts = Profile.objects.filter(author=user).order_by('-publish_date')
    else:
        posts = None
    if request.method == 'POST':
        form = SpeciesProfileForm(request.POST)
        formset = ProfileImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            form.instance.author = request.user
            form.save()
            for image_form in formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    photo = ProfileImage(profile=form.instance, image=image)
                    photo.save()
            id = form.instance.pk
            return redirect('speciesprofile:detail', id)
    else:
        form = SpeciesProfileForm()
        formset = ProfileImageFormset()
    context = {'profile_user': user, 'form': form, 'formset': formset, 'posts': posts}
    return render(request, 'users/userprofile.html', context)
