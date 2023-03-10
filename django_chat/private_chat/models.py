from django.db import models
from django.contrib.auth.models import User


class PrivateDialog(models.Model):
    """
    This is a model for a dialog
    between two users
    """

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", db_index=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", db_index=True)

    def __str__(self) -> str:
        return f"Dialog between: {self.user1} and {self.user2}"

class PrivateMessage(models.Model):
    """
    This is a model for the messages
    that are sent between two users
    """

    dialog = models.ForeignKey(PrivateDialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)