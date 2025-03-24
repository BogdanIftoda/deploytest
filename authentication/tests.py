from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUser(APITestCase):

    def test_registration(self):
        data = {
            "username": "testuser",
            "email": "test_user@gmail.com",
            "password": "test_password",
        }
        with patch("authentication.tasks.send_activation_email.delay") as mock_task:
            response = self.client.post(reverse("authentication:register"), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_task.assert_called_once()
