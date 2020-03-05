from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Profile


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'speciesprofile/index.html'
    context_object_name = 'species_list'

    def get_queryset(self):
        return Profile.objects.order_by('-publish_date')[:8]


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'speciesprofile/detail.html'
