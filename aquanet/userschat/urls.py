from django.urls import path
from . import views

app_name = 'userschat'
urlpatterns = [
    path('joinroom/', views.get_room, name='joinroom'),
    path('messages/<int:pk>/', views.RoomView.as_view(), name='room'),
]