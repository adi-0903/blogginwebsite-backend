from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    SeriesViewSet,
    SeasonViewSet,
    PostViewSet,
    EventViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'series', SeriesViewSet, basename='series')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'events', EventViewSet, basename='event')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
