from django.urls import path
from .views import PrivateChatView

urlpatterns = [
    path("", PrivateChatView.as_view(), name="private_chat"),
]