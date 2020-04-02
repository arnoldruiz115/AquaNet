from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Profile, ProfileImage
from .forms import SpeciesProfileForm, ImagesFormset


# Create your views here.
class IndexView(ListView):
    template_name = 'speciesprofile/index.html'
    context_object_name = 'species_list'

    def get_queryset(self):
        return Profile.objects.order_by('-publish_date')[:4]


class SearchResultView(ListView):
    template_name = 'speciesprofile/searchresults.html'
    context_object_name = 'result_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context.update({'search': self.kwargs['common_name']})
        return context

    def get_queryset(self):
        search = self.kwargs['common_name']
        return Profile.objects.filter(Q(common_name__contains=search) | Q(species__contains=search))


def search_form_page(request):
    if request.method == 'GET':
        return render(request, 'speciesprofile/searchresults.html')
    if request.method == 'POST':
        search = request.POST['SearchSpecies']
        if not search:
            messages.warning(request, 'Can not search empty string.')
            return render(request, 'speciesprofile/searchresults.html')
        return redirect('speciesprofile:search', search)


def search_advanced(request):
    return render(request, 'speciesprofile/advancedsearch.html')


class SpeciesDetailView(DetailView):
    model = Profile
    template_name = 'speciesprofile/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpeciesDetailView, self).get_context_data(**kwargs)
        profile = self.get_object()
        images = ProfileImage.objects.filter(profile=profile.pk)
        context.update({'images': images})
        return context


class SpeciesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'speciesprofile/update.html'

    fields = ['common_name', 'species', 'max_size', 'water_type']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpeciesUpdateView, self).get_context_data(**kwargs)
        profile = self.get_object()
        formset = ImagesFormset(instance=profile)
        context.update({'formset': formset})
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = SpeciesProfileForm(request.POST, instance=profile)
        formset = ImagesFormset(request.POST, request.FILES, instance=profile)
        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
        return redirect('speciesprofile:detail', profile.id)

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
