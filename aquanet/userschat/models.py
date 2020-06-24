from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import get_user_image_url

# Create your models here.

class Thread(models.Model):
    first_user = models.ForeignKey(User, related_name="first_user", on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name="second_user", on_delete=models.CASCADE)
    last_update = models.DateTimeField(default=timezone.now)

    def get_last_message(self):
        last_message = Message.objects.filter(thread=self.id).last()
        if last_message:
            return last_message.message

    def get_first_user_image(self):
        return get_user_image_url(self.first_user)

    def get_second_user_image(self):
        return get_user_image_url(self.second_user)

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
    
    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        print(timezone.now())
        self.thread.last_update = timezone.now()
        self.thread.save()



def get_or_create_thread(first_user, second_user):
    if first_user == second_user:
        return False

    q1 = Thread.objects.filter(first_user=first_user, second_user=second_user)
    q2 = Thread.objects.filter(first_user=second_user, second_user=first_user)

    if q1 or q2:
        if q1:
            return q1.first()
        else:
            return q2.first()
    else:
        new_thread = Thread()
        new_thread.first_user = first_user
        new_thread.second_user = second_user
        new_thread.save()
        return new_thread


def does_thread_exist(first_user, second_user):
    if first_user == second_user:
        return False
    q1 = Thread.objects.filter(first_user=first_user, second_user=second_user)
    q2 = Thread.objects.filter(first_user=second_user, second_user=first_user)

    if q1 or q2:
        return True
    else:
        return False


def user_exists(username):
    q = User.objects.filter(username=username)
    if q:
        return True
    else:
        return False