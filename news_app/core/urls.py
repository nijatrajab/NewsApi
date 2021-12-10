from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("news", views.NewsViewSet)
router.register("^news/(?P<news_id>.+)/comment", views.CommentViewSet)

app_name = "core"

urlpatterns = [path("", include(router.urls))]
