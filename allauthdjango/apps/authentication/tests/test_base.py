
"""Base file containing setup"""


from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


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
