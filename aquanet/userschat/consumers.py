import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import get_or_create_thread, Thread, Message
from django.contrib.auth.models import User
import datetime
from django.utils import dateformat
from users.models import get_user_image_url

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # TODO: create function to get thread/room name for two users, then make room_name = result
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        usr = self.scope['user']
        self.sender = await database_sync_to_async(User.objects.get)(username=usr)
        self.thread = await database_sync_to_async(Thread.objects.get)(id=self.room_name)
        self.sender_image = await database_sync_to_async(get_user_image_url)(self.sender)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.sender.username
        sender_img_url = self.sender_image
        time_now = dateformat.format(datetime.datetime.now(), 'F j, Y, P')
        await self.create_message(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'sender_img_url': sender_img_url,
                'time_now': time_now
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_img_url = event['sender_img_url']
        time_now = event['time_now']
        if sender == self.sender.username:
            sender = "self"
        else:
            sender = "other"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_img_url': sender_img_url,
            'time_now': time_now
        }))

    @database_sync_to_async
    def create_message(self, message):
        thread = self.thread
        return Message.objects.create(thread=thread, sender=self.sender, message=message)