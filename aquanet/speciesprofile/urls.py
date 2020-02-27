from django.urls import path
from . import views

app_name = 'speciesprofile'
urlpatterns = [
    path('', views.index, name='index'),
    path('species/<int:species_id>/', views.species_detail, name='detail'),
]
