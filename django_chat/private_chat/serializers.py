from django.contrib.auth.models import User

from .models import PrivateMessage

from rest_framework import serializers


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username")

    class Meta():
        model = PrivateMessage
        fields = "__all__"