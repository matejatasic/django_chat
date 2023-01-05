from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

import base64
import os

from django_chat.settings import MEDIA_ROOT
from .models import UserProfile


public_chat_url = reverse("public_chat")

class RegistrationTests(TestCase):
    """
    Test registration functionality
    """

    registration_url = reverse("register")

    def test_registration_valid_user_success(self):
        """
        Test registration with valid payload is successfull
        """
        payload = {
            "username": "newUser",
            "email": "new-user@test.com",
            "password1": "testpass123",
            "password2": "testpass123"
        }

        response = self.client.post(self.registration_url, payload)
        users = User.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], public_chat_url)
        self.assertEqual(users.count(), 1)

    def test_user_registration_creates_profile(self):
        """
        Test registration with valid payload creates user profile
        """
        payload = {
            "username": "newUser",
            "email": "new-user@test.com",
            "password1": "testpass123",
            "password2": "testpass123"
        }

        response = self.client.post(self.registration_url, payload)
        user_profiles = UserProfile.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], public_chat_url)
        self.assertEqual(user_profiles.count(), 1)

    def test_user_upload_image_success(self):
        """
        Test user uploads an image successfully
        """
        image_content = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUA" + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO" + "9TXL0Y4OHwAAAABJRU5ErkJggg==")
        image_name = "img_avatar.png"
        image = SimpleUploadedFile(image_name, image_content, "image/png")
        payload = {
            "username": "newUser",
            "email": "new-user@test.com",
            "password1": "testpass123",
            "password2": "testpass123",
            "image": image
        }

        response = self.client.post(self.registration_url, payload)
        new_user_profile = UserProfile.objects.all()[0]

        # remove the image that was uploaded while testing
        user_images_folder = os.path.join(MEDIA_ROOT, "user_images")
        last_uploaded_image = os.listdir(user_images_folder)[-1]
        os.remove(os.path.join(user_images_folder, last_uploaded_image))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], public_chat_url)
        self.assertNotEqual(new_user_profile.image, None)
        self.assertIn(image_name, new_user_profile.image.name)

    def test_invalid_input_returns_errors(self):
        """
        Test registration with invalid input
        returns the validation errors
        """
        payload = {
            "username": "",
            "email": "",
            "password1": "testpass123",
            "password2": "testpass123",
        }

        response = self.client.post(self.registration_url, payload)

        form_errors = response.context["form"].errors.as_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(form_errors), 2)

        for error in form_errors:
            error_message = form_errors[error][0].message

            self.assertEqual(error_message, "This field is required.")

class LoginTests(TestCase):
    """
    Test login functionality
    """

    login_url = reverse("login")
    registration_url = reverse("register")

    def test_login_with_valid_user(self):
        """
        Test login is successfull with valid user
        """
        register_payload = {
            "username": "newUser",
            "email": "new-user@test.com",
            "password1": "testpass123",
            "password2": "testpass123"
        }
        login_payload = {
            "username": register_payload["username"],
            "password": register_payload["password1"]
        }

        self.client.post(self.registration_url, register_payload)
        response = self.client.post(self.login_url, login_payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], public_chat_url)

    def test_login_with_invalid_input_returns_errors(self):
        """
        Test login with invalid input returns errors
        """
        login_payload = {
            "username": "unknownUser",
            "password": "invalidPassword"
        }

        response = self.client.post(self.login_url, login_payload)

        form_errors = response.context["form"].errors.as_data()
        error_message = form_errors["__all__"][0].message

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(form_errors), 1)
        self.assertEqual(error_message, "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.")

class LogoutTests(TestCase):
    """
    Test logout functionality
    """

    logout_url = reverse("logout")
    login_url = reverse("login")
    registration_url = reverse("register")

    def test_logout_successfull(self):
        """
        Test logout is successfull
        """
        register_payload = {
            "username": "newUser",
            "email": "new-user@test.com",
            "password1": "testpass123",
            "password2": "testpass123"
        }
        login_payload = {
            "username": register_payload["username"],
            "password": register_payload["password1"]
        }

        self.client.post(self.registration_url, register_payload)
        self.client.post(self.login_url, login_payload)
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], reverse("homepage"))
