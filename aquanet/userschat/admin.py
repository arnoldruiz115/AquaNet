from django.contrib import admin
from .models import Thread, Message

# Register your models here.

admin.site.register(Thread)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'sender', 'thread')

admin.site.register(Message, MessageAdmin)