from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Thread(models.Model):
    first_user = models.ForeignKey(User, related_name="first_user", on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name="second_user", on_delete=models.CASCADE)

    def __str__(self):
        return "Thread for {} and {}".format(self.first_user.username, self.second_user.username)


class Message(models.Model):
    # Message thread (converstation between two users) this message belongs to
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Message from {}".format(self.sender.username)


def get_or_create_thread(first_user, second_user):
    q1 = Thread.objects.filter(first_user=first_user, second_user=second_user)
    q2 = Thread.objects.filter(first_user=second_user, second_user=first_user)

    if q1 or q2:
        print("found existing thread")
        if q1:
            return q1.first()
        else:
            return q2.first()
    else:
        print("new thread")
        new_thread = Thread()
        new_thread.first_user = first_user
        new_thread.second_user = second_user
        new_thread.save()
        return new_thread

