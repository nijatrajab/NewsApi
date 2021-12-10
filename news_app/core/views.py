from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core import serializers
from core.models import News, Comment

from core.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    @action(detail=True)
    def upvote(self, request, *args, **kwargs):
        news = self.get_object()
        news.up_votes += 1
        news.save()
        return Response()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        news = self.kwargs["news_id"]
        return Comment.objects.filter(news__id=news)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
