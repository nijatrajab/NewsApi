from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import News
from core.serializers import NewsSerializer

NEWS_URLS = reverse("core:news-list")


def detail_url(news_id):
    """return news detail url"""
    return reverse("core:news-detail", args=[news_id])


def sample_news(user, **params):
    """create and return a sample news"""
    defaults = {
        "title": "Sample news",
        "link": "https://sample.com",
    }
    defaults.update(params)

    return News.objects.create(author=user, **defaults)


class PublicNewsApiTests(TestCase):
    """test unauthenticated news api access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test that auth is required"""
        res = self.client.get(NEWS_URLS)

        self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNewsApiTests(TestCase):
    """test auth news API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_news(self):
        """test retrieving a list of news"""

        sample_news(user=self.user)
        sample_news(user=self.user)
        sample_news(user=self.user)
        sample_news(user=self.user)
        sample_news(user=self.user)

        res = self.client.get(NEWS_URLS)

        news = News.objects.all().order_by("id")
        serializer = NewsSerializer(news, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_news_detail(self):
        """test viewing a news detail"""
        news = sample_news(user=self.user)

        url = detail_url(news.id)
        res = self.client.get(url)

        serializer = NewsSerializer(news)

        self.assertEqual(res.data, serializer.data)

    def test_full_update_news(self):
        """test full update a news"""
        news = sample_news(user=self.user)
        payload = {
            "title": "New sample news",
            "link": "https://newsample.com",
        }
        url = detail_url(news.id)

        self.client.put(url, payload)

        news.refresh_from_db()
        self.assertEqual(news.title, payload["title"])
        self.assertEqual(news.link, payload["link"])

    def test_full_update_news_only_author(self):
        """test only author can full update a news"""
        news = sample_news(user=self.user)
        payload = {
            "title": "New sample news",
            "link": "https://newsample.com",
        }
        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        news.refresh_from_db()
        self.assertNotEqual(news.title, payload["title"])
        self.assertNotEqual(news.link, payload["link"])

    def test_partial_update_news(self):
        """test updating news with patch"""
        news = sample_news(user=self.user)
        payload = {"title": "Sample news", "link": "https://newsample.com"}
        url = detail_url(news.id)

        self.client.patch(url, payload)

        news.refresh_from_db()
        self.assertEqual(news.link, payload["link"])

    def test_partial_update_news_only_author(self):
        """test only author can update news with patch"""
        news = sample_news(user=self.user)
        payload = {"title": "Sample news", "link": "https://newsample.com"}

        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        news.refresh_from_db()
        self.assertNotEqual(news.link, payload["link"])

    def test_delete_news(self):
        """test delete news"""
        news = sample_news(user=self.user)
        url = detail_url(news.id)
        old_news = news.id

        self.client.delete(url)

        news_exists = News.objects.filter(id=old_news).exists()
        self.assertFalse(news_exists)

    def test_delete_news_only_author(self):
        """test only author can delete news"""
        news = sample_news(user=self.user)

        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)
        old_news = news.id

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        news.refresh_from_db()
        news_exists = News.objects.filter(id=old_news).exists()
        self.assertTrue(news_exists)
