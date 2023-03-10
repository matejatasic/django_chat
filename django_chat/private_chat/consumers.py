import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        user_id: str = self.scope["session"]["_auth_user_id"]
        self.room_group_name: str = f"private_chat-{user_id}"

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
        user2_id: str = message["user2"]

        await self.channel_layer.group_send(
            f"private_chat-{user2_id}",
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
