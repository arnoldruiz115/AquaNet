from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile


# Create your views here.
class IndexView(ListView):
    template_name = 'speciesprofile/index.html'
    context_object_name = 'species_list'

    def get_queryset(self):
        return Profile.objects.order_by('-publish_date')[:4]


class SpeciesDetailView(DetailView):
    model = Profile
    template_name = 'speciesprofile/detail.html'


class SpeciesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'speciesprofile/update.html'

    fields = ['common_name', 'species', 'max_size', 'water_type', 'image', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SpeciesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'speciesprofile/delete.html'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.request.user.username})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
