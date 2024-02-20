import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection established")
        
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket connection closed")

    async def receive(self, text_data):
        print("Message received:", text_data)


# class ChatConsumer(SyncConsumer):
#     def connect(self, event):
#         print("connect event is called")

#         self.send({
#             "type": "websocket.accept"
#         })

#     def disconnect(self, event):
#         print("disconnected")
#         print(event)


#     def receive(self, event):
#         print("New event is recieved")
#         print(event)