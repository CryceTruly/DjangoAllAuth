
"""Base file containing setup"""


from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from .test_data.test_data import mytestcode


class BaseTest(APITestCase):
    """Contains test setup method."""

    def setUp(self):
        self.client = APIClient()
        self.email_url = reverse('authentication:emailauth')
        self.linkedin_url = reverse('authentication:linkedin')

    def test_welcome(self):
        response = self.client.get(self.email_url, format="json")
        message = response.data['msg']
        self.assertEqual(message, "Welcome email")

    def test_linked_in_auth(self):
        response = self.client.get(
            self.linkedin_url+"?code="+mytestcode, format="json")
        self.assertEqual(response.status_code, 400)
