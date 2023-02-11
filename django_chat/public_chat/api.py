from django.core.serializers import serialize
from django.contrib.auth.models import User

from .models import PublicMessage
from .serializers import PublicMessageSerializer

import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request


class PublicChatModelViewSet(ModelViewSet):
    queryset = PublicMessage.objects.all()
    serializer_class = PublicMessageSerializer
    allowed_methods = ("GET", "POST")

    def list(self, request: Request) -> Response:
        serialized_data: str = serialize("json", PublicMessage.objects.all())
        messages_list: list = self._add_user_data_to_message(serialized_data)

        return Response(messages_list)

    def _add_user_data_to_message(self, messages: list) -> list:
        messages: list = json.loads(messages)
        newResult: list = []

        for message in messages:
            message_fields: dict = message["fields"]

            user: User = User.objects.get(pk=message_fields["user"])
            message_fields["user"]: str = user.username

            newResult.append(message_fields)

        return newResult
