from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


def upload_image_path(instance, filename):
    todays_date_string = str(datetime.now())
    new_filename = todays_date_string + filename

    return f"user_images/{new_filename}"

class UserProfile(models.Model):
    """
        A custom user profile model that extends the builtin User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path)

    def __str__(self):
        return self.user.username