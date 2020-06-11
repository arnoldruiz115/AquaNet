from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from .forms import UserRegisterForm, UserImageForm
from speciesprofile.forms import SpeciesProfileForm, ProfileImageFormset
from speciesprofile.models import Profile, ProfileImage
from .models import UserImage, get_user_image_url


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
    if request.method == 'GET':
        if Profile.objects.filter(author=user):
            posts = Profile.objects.filter(author=user).order_by('-publish_date')
        else:
            posts = None
        form = SpeciesProfileForm()
        formset = ProfileImageFormset()
        user_image = get_user_image_url(user)
    context = {'profile_user': user, 'user_image': user_image, 'form': form, 'formset': formset, 'posts': posts}
    return render(request, 'users/userprofile.html', context)


class UpdateUserProfile(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    slug_field = 'username'
    template_name = 'users/edituserprofile.html'
    context_object_name = 'userprofile'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        image_form = UserImageForm(request.POST, request.FILES, instance=user)

        if image_form.is_valid():
                clean_data = image_form.cleaned_data
                image = clean_data['user_image']
                if image:
                    if UserImage.objects.filter(user=user):
                        photo = UserImage.objects.get(user=user)
                        photo.user_image = image
                        photo.save()
                    else:
                        photo = UserImage(user=user, user_image=image)
                        photo.save()

        return redirect('users:profile', user.username)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpdateUserProfile, self).get_context_data(**kwargs)
        image_form = UserImageForm()
        user_image = get_user_image_url(self.get_object())
        context.update({'form': image_form, 'user_image': user_image})
        return context

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False