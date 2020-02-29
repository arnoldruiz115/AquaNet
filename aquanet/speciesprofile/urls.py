from django.urls import path
from . import views

app_name = 'speciesprofile'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('species/<int:pk>/', views.DetailView.as_view(), name='detail'),
]
