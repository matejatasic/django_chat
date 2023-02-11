from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import PublicMessage

import json


class PublicChatTests(TestCase):
    """
    Test public chat functionality
    """

    public_chat_url = reverse("public_chat")

    def test_entering_public_chat_as_anonymous_user_fails(self):
        """
        Test entering public chat while not logged in
        redirects to the login page
        """
        response = self.client.get(self.public_chat_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], reverse("login") + "?next=/public_chat")

class PublicChatApi(TestCase):
    public_chat_api_url = reverse("public-chat-api-list")

    def test_create_message_with_valid_data_successful(self):
        message = "some message"
        user = User.objects.create(username="some_user", password="123")

        response = self.client.post(self.public_chat_api_url, {"message": message, "user_id": user.id})
        new_message = PublicMessage.objects.latest("timestamp")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_message.message, message)
        self.assertEqual(new_message.user, user)

    def test_create_message_with_no_data_unsuccessful(self):
        response = self.client.post(self.public_chat_api_url, {})
        error_messages = json.loads(response.content)

        self.assertEqual(response.status_code, 400)

        for error_key in error_messages:
            error_message = error_messages[error_key][0]

            self.assertIn(error_key, ["message", "user_id"])
            self.assertEqual(error_message, "This field is required.")

    def test_create_message_with_invalid_user_id_unsuccessful(self):
        with self.assertRaises(Exception):
            message = "some message"

            self.client.post(self.public_chat_api_url, {"message": message, "user_id": 1})

    def test_list_all_messages(self):
        user_parameters = {
            "username": "some_user",
            "password": "123"
        }
        user = User.objects.create(username=user_parameters["username"], password=user_parameters["password"])

        message1 = "message1"
        message2 = "message2"

        # create messages
        self.client.post(self.public_chat_api_url, {"message": message1, "user_id": user.id})
        self.client.post(self.public_chat_api_url, {"message": message2, "user_id": user.id})

        response = self.client.get(self.public_chat_api_url)
        messages = json.loads(response.content)
        first_message = messages[0]
        second_message = messages[1]

        self.assertEqual(first_message["user"], user_parameters["username"])
        self.assertEqual(first_message["message"], message1)

        self.assertEqual(second_message["user"], user_parameters["username"])
        self.assertEqual(second_message["message"], message2)
