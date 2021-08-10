from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):

    def test_not_logged_in(self):
        """
        tests whether a user can access the main page
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in")
