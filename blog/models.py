from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    """Category model for blog posts"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Series(models.Model):
    """Series model for grouping related posts"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='series/', null=True, blank=True)
    icon = models.CharField(max_length=10, default='📚')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    gradient = models.CharField(max_length=200, blank=True)
    accent_color = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def episodes_count(self):
        return self.posts.count()
    
    @property
    def tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Season(models.Model):
    """Season model for organizing series episodes"""
    
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='seasons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    season_number = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('series', 'season_number')
        ordering = ['season_number']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}"
    
    @property
    def episodes_count(self):
        return self.posts.count()


class Post(models.Model):
    """Blog post model with image support"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    POST_TYPE_CHOICES = [
        ('blog', 'Blog'),
        ('journal', 'Journal'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='posts/', null=True, blank=True)
    icon = models.CharField(max_length=10, default='📝')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    season = models.ForeignKey('Season', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    episode_number = models.PositiveIntegerField(null=True, blank=True, help_text='Episode number within the season')
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='blog')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    read_time = models.IntegerField(default=5, help_text='Estimated read time in minutes')
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    gradient = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Event(models.Model):
    """Event model for workshops, meetups, etc."""
    
    TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('masterclass', 'Masterclass'),
        ('meetup', 'Meetup'),
        ('webinar', 'Webinar'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='workshop')
    
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    is_virtual = models.BooleanField(default=False)
    
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=True)
    
    max_attendees = models.IntegerField(null=True, blank=True)
    attendees_count = models.IntegerField(default=0)
    
    gradient = models.CharField(max_length=200, blank=True)
    accent_color = models.CharField(max_length=50, blank=True)
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def spots_left(self):
        if self.max_attendees:
            return max(0, self.max_attendees - self.attendees_count)
        return None
    
    @property
    def is_past(self):
        from django.utils import timezone
        return self.date < timezone.now().date()


class Comment(models.Model):
    """Comment model for blog posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    """Like model for posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
