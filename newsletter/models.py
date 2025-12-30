from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):
    """Model to store newsletter subscribers"""
    
    email = models.EmailField(unique=True, max_length=254)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    trial_expires_at = models.DateTimeField(null=True, blank=True)
    has_upgraded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
    
    def __str__(self):
        return self.email
    
    def set_trial_period(self, days=24):
        """Set the trial expiration date"""
        self.trial_expires_at = timezone.now() + timezone.timedelta(days=days)
        self.save()
    
    def is_trial_active(self):
        """Check if trial period is still active"""
        if self.trial_expires_at is None:
            return False
        return timezone.now() < self.trial_expires_at
