from django.core.serializers import serialize
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import PrivateDialog, PrivateMessage
from .serializers import PrivateMessageSerializer

import json
from typing import Union, List

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


class PrivateChatModelViewSet(ModelViewSet):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer
    allowed_methods = ("GET", "POST")

    def list(self, request: Request) -> Response:
        user1_id = request.user.id
        user2_id = request.GET["user2"]

        try:
            private_dialog: Union[QuerySet, List[PrivateDialog]] = PrivateDialog.objects.get(
                Q(user1__pk=user1_id, user2__pk=user2_id) | Q(user1__pk=user2_id, user2__pk=user1_id)
            )
        except:
            return Response({"status": "The requested dialog was not found!"}, status=status.HTTP_404_NOT_FOUND)

        messages = PrivateMessage.objects.filter(dialog=private_dialog)

        serialized_messages_list: list = PrivateMessageSerializer(messages, many=True).data

        return Response(serialized_messages_list)

    def create(self, request: Request):
        data: dict = request.data.copy()
        user1_id: str = request.user.id
        user2_id: str = data["user2"]
        dialog: PrivateDialog = self._get_or_create_dialog(user1_id, user2_id)

        data["dialog"]: PrivateDialog = dialog

        message: PrivateMessage = PrivateMessage.objects.create(message=data["message"], sender=request.user, dialog=data["dialog"])
        serialized_message: str = PrivateMessageSerializer(message).data

        return Response(serialized_message, status=status.HTTP_201_CREATED)

    def _get_or_create_dialog(self, user1_id: str, user2_id: str) -> PrivateDialog:
        try:
            dialog: Union[QuerySet, List[PrivateDialog]] = PrivateDialog.objects.get(
                Q(user1__pk=user1_id, user2__pk=user2_id) | Q(user1__pk=user2_id, user2__pk=user1_id),
            )
        except Exception:
            user1: User = User.objects.get(pk=user1_id)
            user2: User = User.objects.get(pk=user2_id)

            dialog: PrivateDialog = PrivateDialog.objects.create(user1=user1, user2=user2)

        return dialog