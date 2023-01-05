from django.test import TestCase
from django.urls import reverse


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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], reverse("login") + "?next=/private_chat")