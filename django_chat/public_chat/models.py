from django.db import models
from django.contrib.auth.models import User


class PublicMessage(models.Model):
    """
    This is a model for messages that
    are sent to the public chat
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)