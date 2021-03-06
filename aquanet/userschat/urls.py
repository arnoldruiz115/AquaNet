from django.urls import path
from . import views

app_name = 'userschat'
urlpatterns = [
    path('joinroom/', views.get_room, name='joinroom'),
    path('message/', views.send_message, name='send-message'),
    path('messages', views.ThreadsView.as_view(), name='threads'),
    path('messages/<int:pk>/', views.RoomView.as_view(), name='room'),
]