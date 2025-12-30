from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models

from .models import Category, Series, Season, Post, Event, Comment, Like
from .serializers import (
    CategorySerializer,
    SeriesSerializer,
    SeasonSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    EventSerializer,
    CommentSerializer,
    LikeSerializer
)
from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SeriesViewSet(viewsets.ModelViewSet):
    """ViewSet for Series model"""
    
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'updated_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Get all posts in a series"""
        series = self.get_object()
        posts = series.posts.filter(status='published')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class SeasonViewSet(viewsets.ModelViewSet):
    """ViewSet for Season model"""
    
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['series']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'season_number']
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def episodes(self, request, slug=None):
        """Get all episodes in a season"""
        season = self.get_object()
        posts = season.posts.filter(status='published').order_by('episode_number')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    
    queryset = Post.objects.filter(status='published')
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'series', 'is_featured', 'post_type']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'created_at', 'views_count', 'likes_count']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Show user's own drafts
            queryset = Post.objects.filter(
                models.Q(status='published') | models.Q(author=self.request.user)
            )
        return queryset
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
            post.save()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        """Like/Unlike a post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            post.likes_count -= 1
            message = 'Post unliked'
        else:
            post.likes_count += 1
            message = 'Post liked'
        
        post.save()
        return Response({
            'message': message,
            'is_liked': created,
            'likes_count': post.likes_count
        })
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts"""
        posts = self.get_queryset().filter(is_featured=True)[:3]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event model"""
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'is_virtual', 'is_free']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        events = self.get_queryset().filter(date__gte=timezone.now().date())
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past events"""
        events = self.get_queryset().filter(date__lt=timezone.now().date())
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'parent']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
