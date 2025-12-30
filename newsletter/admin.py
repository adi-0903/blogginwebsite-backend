from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active', 'is_trial_active', 'has_upgraded']
    list_filter = ['is_active', 'has_upgraded', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    
    def is_trial_active(self, obj):
        return obj.is_trial_active()
    is_trial_active.short_description = 'Trial Active'
    is_trial_active.boolean = True
