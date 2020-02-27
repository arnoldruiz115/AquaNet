from django.shortcuts import render, get_object_or_404
from .models import Profile


# Create your views here.
def index(request):
    species_list = Profile.objects.order_by('publish_date')
    context = {'species_list': species_list}
    return render(request, 'speciesprofile/index.html', context)


def species_detail(request, species_id):
    # species = Profile.objects.get(pk=species_id)
    species = get_object_or_404(Profile, pk=species_id)
    context = {'species': species}
    return render(request, 'speciesprofile/detail.html', context)
