from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import PrivateDialog, PrivateMessage

import json
from rest_framework import status


class PrivateChatTests(TestCase):
    """
    Test private chat functionality
    """

    private_chat_url = reverse("private_chat")

    def test_entering_private_chat_as_anonymous_user_fails(self):
        """
        Test entering private chat while not logged in
        returns an error
        """
        response = self.client.get(self.private_chat_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["location"], reverse("login") + "?next=/private_chat")

class PrivateChatApiTests(TestCase):
    """
    Test private chat API functionality
    """

    private_chat_api_url = reverse("private-chat-api-list")

    def test_create_message_with_valid_data_successful(self):
        message = "some message"
        user1 = User.objects.create(username="some_user", password="123")
        user2 = User.objects.create(username="some_user2", password="123")

        self.client.force_login(user1)

        response = self.client.post(self.private_chat_api_url, {"message": message, "user2": user2.id})
        new_message = PrivateMessage.objects.first()
        dialog = PrivateDialog.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_message.message, message)
        self.assertEqual(new_message.dialog.id, dialog.id)
        self.assertEqual(dialog.user1.id, user1.id)
        self.assertEqual(dialog.user2.id, user2.id)

    def test_add_message_to_dialog_if_exists(self):
        message = "some_message"
        user1 = User.objects.create(username="some_user", password="123")
        user2 = User.objects.create(username="some_user2", password="123")

        private_dialog = PrivateDialog.objects.create(user1=user1, user2=user2)

        self.client.force_login(user1)

        self.client.post(self.private_chat_api_url, {"message": message, "user2": user2.id})

        new_message = PrivateMessage.objects.first()

        self.assertEqual(private_dialog, new_message.dialog)

    def test_create_message_with_invalid_data_unsuccessful(self):
        message = "some message"

        with self.assertRaises(Exception):
            self.client.post(self.private_chat_api_url, {"message": message, "user2": 2})

    def test_list_all_messages_from_a_dialog(self):
        message1 = "some_message"
        message2 = "some_message_2"
        user1 = User.objects.create(username="some_user", password="123")
        user2 = User.objects.create(username="some_user2", password="123")
        user3 = User.objects.create(username="some_user3", password="123")

        self.client.force_login(user1)

        self.client.post(self.private_chat_api_url, {"message": message1, "user2": user2.id})
        self.client.post(self.private_chat_api_url, {"message": message2, "user2": user2.id})
        self.client.post(self.private_chat_api_url, {"message": message1, "user2": user3.id})
        self.client.post(self.private_chat_api_url, {"message": message2, "user2": user3.id})

        response1 = self.client.get(self.private_chat_api_url,  {"user2": user2.id})
        response2 = self.client.get(self.private_chat_api_url,  {"user2": user3.id})
        dialog1_messages = json.loads(response1.content)
        dialog2_messages = json.loads(response2.content)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(dialog1_messages), 2)
        self.assertEqual(len(dialog2_messages), 2)

