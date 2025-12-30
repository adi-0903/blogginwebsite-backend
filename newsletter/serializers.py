from rest_framework import serializers
from .models import NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    """Serializer for newsletter subscribers"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at', 'is_active', 'trial_expires_at', 'has_upgraded']
        read_only_fields = ['id', 'subscribed_at', 'trial_expires_at']


class NewsletterSubscribeSerializer(serializers.Serializer):
    """Serializer for newsletter subscription endpoint"""
    
    email = serializers.EmailField()
