from channels.consumer import SyncConsumer


class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connect event called")
        self.send(
            {
                "type": "websocket.accept"
            }
        )

    def websocket_receive(self, event):
        print("new evenet received")
        print(event)

    def websocket_disconnect(self, event):
        print("Disconnected connection")
        print(event)