from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'speciesprofile'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.search_advanced, name='search-advanced'),
    path('search/<str:common_name>', views.SearchResultView.as_view(), name='search'),
    path('empty-search/', views.search_form_page, name='search-name'),
    path('advanced-search/', views.search_form_page, name='advanced-search'),
    path('species/<int:pk>/', views.SpeciesDetailView.as_view(), name='detail'),
    path('species/<int:pk>/update/', views.SpeciesUpdateView.as_view(), name='update'),
    path('species/<int:pk>/update/images', views.SpeciesImagesFormset.as_view(), name='images-formset'),
    path('species/<int:pk>/delete/', views.SpeciesDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
