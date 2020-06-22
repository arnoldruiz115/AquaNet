from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Thread, get_or_create_thread, user_exists, Message
from users.models import get_user_image_url
from .forms import MessageForm

@login_required
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


@login_required
def send_message(request):
    if request.method == 'GET':
        message_form = MessageForm()
        context = {'form': message_form}
        return render(request, 'userschat/message.html', context)
        
    if request.method == 'POST':
        active_user = request.user
        other_username = request.POST.get('other_username')
        other_user = User.objects.get(username=other_username)
        thread = get_or_create_thread(active_user, other_user)
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.cleaned_data['message']
            new_message = Message(thread=thread, sender=active_user, message=message)
            new_message.save()
            return redirect('userschat:threads')
            


class ThreadsView(LoginRequiredMixin, TemplateView):
    template_name = 'userschat/threads.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ThreadsView, self).get_context_data(**kwargs)

        self.threads = Thread.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))   
        context.update({'threads': self.threads})
        return context


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
        other_user_image = get_user_image_url(other_user)
        context.update({'room_name': thread.id, 'thread': thread, 'reciever_image': other_user_image, 'chat_messages': messages, 'reciever': other_user})
        return context

    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.first_user or self.request.user == thread.second_user:
            return True
        return False