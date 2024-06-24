import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Message, Thread, User



class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection established")
        self.room_name = "broadcast"
        await self.accept()
        (self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'[{self.channel_name}] - you are connected')

    async def disconnect(self, close_code):
        print("WebSocket connection closed")
        await (self.channel_layer.group_discard)(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def message(self, event):
        text_data_json = json.loads(event)
        message = text_data_json['message']
        print(f'[{self.channel_name}] - Received - {message}')
        self.send({
            "type": "websocket.send",
            "text": message
        })


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        me = self.scope["user"]
        other_username = self.scope["url_route"]["kwargs"]["username"]
        other_user = await sync_to_async(User.objects.get)(username=other_username)
        self.thread_obj = await sync_to_async(Thread.objects.get_or_create_personal_thread)(me, other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.send({
            "type": "websocket.accept"
        })
        print(f'[{self.channel_name}] - you are connected')


    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        msg = json.dumps({
            "text": event.get("text"),
            "username": self.scope["user"].username
        })

        await self.store_messages(event.get("text"))

        await (self.channel_layer.group_send)(self.room_name, {
            "type": "websocket.message",
            "text": msg
        }) 

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - message sent - {event["text"]}')
        await self.send({
            "type": "websocket.send",
            "text": event.get("text")
        })


    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - disconnected')
        await (self.channel_layer.group_discard)(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_messages(self, text):
        Message.objects.create(
            thread = self.thread_obj,
            sender = self.scope["user"],
            text = text
        )

