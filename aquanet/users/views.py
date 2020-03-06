from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from speciesprofile.forms import SpeciesProfileForm
from speciesprofile.models import Profile


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
    user = get_object_or_404(User, username=username)
    if Profile.objects.filter(author=user):
        posts = Profile.objects.filter(author=user).order_by('-publish_date')
    else:
        posts = None
    if request.method == 'POST':
        form = SpeciesProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('speciesprofile:index')
    else:
        form = SpeciesProfileForm()
    context = {'profile_username': user.username, 'form': form, 'posts': posts}
    return render(request, 'users/userprofile.html', context)
