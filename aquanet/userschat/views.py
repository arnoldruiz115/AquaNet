from django.shortcuts import render

def index(request):
    return render(request, 'userschat/index.html')

def room(request, room_name):
    return render(request, 'userschat/room.html', {
        'room_name': room_name
    })