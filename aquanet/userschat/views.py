from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Thread, get_or_create_thread, user_exists, Message

@require_http_methods(["POST"])
def get_room(request):
    other_username = request.POST.get('other_username')
    active_user = request.user
    if user_exists(other_username):
        reciever = User.objects.get(username=other_username)
        thread = get_or_create_thread(active_user, reciever)
        if not thread:
            return HttpResponseForbidden()
        url = reverse('userschat:room', kwargs={'pk': thread.id})
        return HttpResponseRedirect(url)
    return HttpResponseForbidden()


class RoomView(LoginRequiredMixin, UserPassesTestMixin, DetailView): 
    model = Thread
    template_name = 'userschat/room.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        thread = self.get_object()
        messages = Message.objects.filter(thread=thread)

        if thread.first_user == self.request.user:
            other_user = thread.second_user
        else:
            other_user = thread.first_user
        context.update({'room_name': thread.id, 'thread': thread, 'chat_messages': messages, 'reciever': other_user})
        return context

    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.first_user or self.request.user == thread.second_user:
            return True
        return False