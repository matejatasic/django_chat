from django.test import TestCase
from django.urls import reverse


class PublicChatTests(TestCase):
    """
    Test public chat functionality
    """

    public_chat_url = reverse("public_chat")

    def test_entering_public_chat_as_anonymous_user_fails(self):
        """
        Test entering public chat while not logged in
        returns an error
        """
        response = self.client.get(self.public_chat_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], reverse("login") + "?next=/public_chat")
