from userschat.models import Thread
from django.db.models import Q

def get_unread_threads(request):
    unread_threads = 0
    active_user = request.user
    if active_user.is_authenticated:
        threads = Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        for thread in threads:
            if active_user == thread.first_user:
                if thread.notify_first_user:
                    unread_threads += 1
            else:
                if thread.notify_second_user:
                    unread_threads += 1
    return {'unread_threads': unread_threads}