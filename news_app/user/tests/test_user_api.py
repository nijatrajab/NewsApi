from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def register_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the users API(public)"""

    def setUp(self):
        self.client = APIClient()

    def test_register_valid_user_success(self):
        """user registering with valid payload is successful"""
        payload = {
            "email": "test@gmail.com",
            "password": "strongpass",
            "name": "Test Person",
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """test registered user that already exists fails"""
        payload = {
            "email": "test@gmail.com",
            "password": "testpass",
        }
        register_user(**payload)

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_test_password_too_short(self):
        """test that password must be more than 8 char"""
        payload = {"email": "test@gmail.com", "password": "test"}
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_test_password_entirely_numeric(self):
        """test that password must not be entirely numeric"""
        payload = {"email": "test@gmail.com", "password": "123456789"}
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_test_password_similar_name(self):
        """test that password must not be similar to name"""
        payload = {
            "email": "test@gmail.com",
            "password": "testpass",
            "name": "Test Person",
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that a token is created for the user"""
        payload = {"email": "test@gmail.com", "password": "testpass"}
        register_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test that token is not created if invalid credentials are given"""
        register_user(email="test@gmail.com", password="testpass")
        payload = {"email": "test@gmail.com", "password": "passtest"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that token is not created if user doesn't exists"""
        payload = {"email": "test@gmail.com", "password": "testpass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersApiTest(TestCase):
    """test api request that require authentication"""

    def setUp(self):
        self.user = register_user(
            email="test@gmail.com", password="testpass", name="Test Person"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name,
                                    "email": self.user.email})

    def test_post_me_not_allowed(self):
        """test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating the user profile for authenticated user"""
        payload = {"name": "New Person", "password": "passtest"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
