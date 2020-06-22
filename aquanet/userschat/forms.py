from django.forms import ModelForm, Form
from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']