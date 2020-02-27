from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile


# Create your views here.
def index(request):
    species_list = Profile.objects.order_by('publish_date')
    context = {'species_list': species_list}
    return render(request, 'speciesprofile/index.html', context)


def species_detail(request, species):
    response = 'Detail of %s.'
    return HttpResponse(response % species)
