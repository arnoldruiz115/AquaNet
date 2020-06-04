from django.urls import path

from . import views

app_name = 'userschat'
urlpatterns = [
    path('joinroom/', views.index, name='joinroom'),
    path('messages/<str:room_name>/', views.room, name='room'),
]