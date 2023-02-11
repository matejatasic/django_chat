from django.contrib.auth.models import User

from .models import PublicMessage

from rest_framework.serializers import ModelSerializer, IntegerField, CharField


class PublicMessageSerializer(ModelSerializer):
    user_id = IntegerField()
    user = CharField(source="user.username", required=False)

    class Meta():
        model = PublicMessage
        fields = ["id", "message", "user_id", "user", "timestamp"]

    def create(self, validated_data: dict) -> PublicMessage:
        user: User = User.objects.filter(pk=validated_data["user_id"])

        if not user.exists():
            user_id: str = validated_data["user_id"]

            raise Exception(f"User with the id {user_id} does not exist!")

        validated_data.pop("user_id")
        validated_data["user"] = user.first()

        return PublicMessage.objects.create(**validated_data)
