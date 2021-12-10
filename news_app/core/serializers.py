from rest_framework import serializers

from core.models import News, Comment


class NewsSerializer(serializers.ModelSerializer):
    """Serialize news"""

    author = serializers.StringRelatedField(many=False, read_only=True)
    comment_news = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "created_at",
            "author",
            "link",
            "up_votes",
            "comment_news",
        )
        read_only_fields = (
            "id",
            "created_at",
            "author",
            "up_votes",
            "comment_news"
        )


class CommentSerializer(serializers.ModelSerializer):
    """Serialize news"""

    author = serializers.StringRelatedField(many=False, read_only=True)

    def update(self, instance, validated_data):
        validated_data.pop("news", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = ("id", "author", "news", "content", "created_at")
        read_only_fields = ("id", "author", "created_at")
