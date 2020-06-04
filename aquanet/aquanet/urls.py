from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('speciesprofile.urls')),
    path('', include('userschat.urls')),
    path('', include('users.urls')),
]
