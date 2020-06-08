from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Thread, get_or_create_thread

@require_http_methods(["POST"])
def get_room(request):
    other_username = request.POST.get('other_username')
    active_user = request.user
    reciever = User.objects.get(username=other_username)
    thread = get_or_create_thread(active_user, reciever)
    url = reverse('userschat:room', kwargs={'pk': thread.id})
    return HttpResponseRedirect(url)


class RoomView(LoginRequiredMixin, UserPassesTestMixin, DetailView): 
    model = Thread
    template_name = 'userschat/room.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        thread = self.get_object()
        context.update({'room_name': thread.id, 'thread': thread})
        return context

    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.first_user or self.request.user == thread.second_user:
            return True
        return False