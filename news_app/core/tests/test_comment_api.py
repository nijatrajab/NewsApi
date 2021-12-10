from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import News, Comment
from core.serializers import CommentSerializer

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


def sample_comment(user, news, **params):
    """create and return a sample comment"""
    defaults = {"content": "Sample comment"}
    defaults.update(params)

    return Comment.objects.create(author=user, news=news, **defaults)


class PublicCommentApiTests(TestCase):
    """test unauthenticated comment api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="testpass",
        )

    def test_auth_required(self):
        """test that auth is required"""
        # res = self.client.get(NEWS_URLS)
        news = sample_news(user=self.user)
        sample_comment(user=self.user, news=news)
        url = detail_url(news.id)
        res = self.client.get(f"{url}comment", follow=True)
        self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNewsApiTests(TestCase):
    """test auth comments API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_comments(self):
        """test retrieving a list of comments"""

        news = sample_news(user=self.user)
        sample_comment(user=self.user, news=news)
        sample_comment(user=self.user, news=news)
        sample_comment(user=self.user, news=news)
        sample_comment(user=self.user, news=news)

        url = detail_url(news.id)
        res = self.client.get(f"{url}comment", follow=True)
        comment = Comment.objects.filter(news=news).order_by("id")
        serializer = CommentSerializer(comment, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_comment_detail(self):
        """test viewing a comment detail"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)
        url = detail_url(news.id)
        res = self.client.get(f"{url}comment/{comment.id}", follow=True)

        serializer = CommentSerializer(comment)

        self.assertEqual(res.data, serializer.data)

    def test_full_update_comment(self):
        """test full update a comment"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)
        payload = {"content": "New sample comment", "news": news.id}
        url = detail_url(news.id)
        self.client.put(f"{url}comment/{comment.id}/", payload, follow=True)
        comment.refresh_from_db()
        self.assertEqual(comment.content, payload["content"])

    def test_full_update_comment_only_author(self):
        """test only author can full update a comment"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)
        payload = {"content": "New sample comment", "news": news.id}
        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)
        res = self.client.put(f"{url}comment/{comment.id}/",
                              payload, follow=True)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertNotEqual(comment.content, payload["content"])

    def test_partial_update_comment(self):
        """test updating comment with patch"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)

        payload = {
            "content": "New sample comment",
        }
        url = detail_url(news.id)

        self.client.patch(f"{url}comment/{comment.id}/", payload, follow=True)
        comment.refresh_from_db()

        self.assertEqual(comment.content, payload["content"])

    def test_partial_update_comment_only_author(self):
        """test only author can update comment with patch"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)
        payload = {
            "content": "New sample comment",
        }
        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)

        res = self.client.patch(
            f"{url}comment/{comment.id}/",
            payload,
            follow=True
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        comment.refresh_from_db()
        self.assertNotEqual(comment.content, payload["content"])

    def test_delete_comment(self):
        """test delete comment"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)
        url = detail_url(news.id)
        old_comment = comment.id

        self.client.delete(f"{url}comment/{comment.id}/", follow=True)

        comment_exists = Comment.objects.filter(id=old_comment).exists()
        self.assertFalse(comment_exists)

    def test_delete_comment_only_author(self):
        """test only author can delete comment"""
        news = sample_news(user=self.user)
        comment = sample_comment(user=self.user, news=news)

        user2 = get_user_model().objects.create_user(
            email="other@mail.com", password="otherpass"
        )
        self.client.force_authenticate(user2)
        url = detail_url(news.id)
        old_comment = comment.id

        res = self.client.delete(f"{url}comment/{comment.id}/", follow=True)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        comment.refresh_from_db()
        comment_exists = Comment.objects.filter(id=old_comment).exists()
        self.assertTrue(comment_exists)
