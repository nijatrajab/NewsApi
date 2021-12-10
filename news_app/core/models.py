from django.conf import settings
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="comment_author",
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="comment_news",
        blank=False,
        null=False,
    )
    content = models.CharField(max_length=144, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}'s comment: {self.content}"
