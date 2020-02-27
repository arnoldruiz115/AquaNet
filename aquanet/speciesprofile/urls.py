from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('species/<int:species>/', views.species_detail, name='species-detail'),
]
