"""Authentication test for ku-polls."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse


class AuthenticationTest(TestCase):
    """Test for authenticated."""

    def setUp(self):
        """Initialize the user."""
        self.user = {
            'username': 'test',
            'password': 'password'
        }
        User.objects.create_user(**self.user)

    def test_login(self):
        """Test user login."""
        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['user'].is_authenticated, True)
        self.assertContains(response, f'Welcome back, {self.user["username"]}')

    def test_logout(self):
        """Test user logout."""
        self.client.post(reverse('login'), self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['user'].is_authenticated, False)
