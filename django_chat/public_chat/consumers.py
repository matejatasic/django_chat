import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.room_group_name: str = "public_chat"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code: any) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data: str) -> None:
        message: dict = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "receive_new_message",
                "message": message
            }
        )

    async def receive_new_message(self, event: dict) -> None:
        message: str = event["message"]

        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": message
        }))
