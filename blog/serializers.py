from rest_framework import serializers
from .models import Category, Series, Season, Post, Event, Comment, Like
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class SeriesSerializer(serializers.ModelSerializer):
    """Serializer for Series model"""
    
    author = UserSerializer(read_only=True)
    episodes_count = serializers.ReadOnlyField()
    tags_list = serializers.ReadOnlyField()
    
    class Meta:
        model = Series
        fields = [
            'id', 'title', 'slug', 'subtitle', 'description', 'image',
            'icon', 'author', 'status', 'tags', 'tags_list', 'gradient',
            'accent_color', 'episodes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for Season model"""
    
    series = SeriesSerializer(read_only=True)
    episodes_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Season
        fields = [
            'id', 'title', 'slug', 'description', 'season_number',
            'series', 'episodes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post list view"""
    
    author = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    series_title = serializers.CharField(source='series.title', read_only=True)
    season_title = serializers.CharField(source='season.title', read_only=True)
    episode_number = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image', 'icon',
            'author', 'category_name', 'series_title', 'season_title',
            'episode_number', 'is_featured', 'read_time', 'views_count',
            'likes_count', 'gradient', 'post_type', 'published_at', 'created_at'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post detail view"""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'icon', 'author', 'category', 'series', 'season', 'status',
            'is_featured', 'read_time', 'views_count', 'likes_count',
            'gradient', 'post_type', 'comments_count', 'is_liked', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views_count', 'likes_count', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating posts"""
    
    class Meta:
        model = Post
        fields = [
            'title', 'excerpt', 'content', 'featured_image', 'icon',
            'category', 'series', 'status', 'is_featured', 'read_time', 'gradient', 'post_type'
        ]


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    
    organizer = UserSerializer(read_only=True)
    spots_left = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    price_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'event_type', 'date',
            'time', 'end_time', 'location', 'is_virtual', 'image',
            'price', 'price_display', 'is_free', 'max_attendees',
            'attendees_count', 'spots_left', 'gradient', 'accent_color',
            'organizer', 'is_past', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'attendees_count', 'created_at', 'updated_at']
    
    def get_price_display(self, obj):
        if obj.is_free:
            return 'Free'
        return f'${obj.price}'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    
    author = UserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'parent',
            'replies_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_replies_count(self, obj):
        return obj.replies.count()


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
