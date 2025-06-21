from django.contrib import admin
from .models import SevoCampaign


@admin.register(SevoCampaign)
class SevoCampaignAdmin(admin.ModelAdmin):
    """Admin interface for SEvO Campaign model."""
    
    list_display = [
        'brand_name', 'main_content_topic', 'campaign_goal', 
        'master_content_format', 'submission_timestamp', 'webhook_sent'
    ]
    
    list_filter = [
        'campaign_goal', 'master_content_format', 'audience_knowledge_level',
        'visual_style', 'webhook_sent', 'submission_timestamp'
    ]
    
    search_fields = [
        'brand_name', 'main_content_topic', 'campaign_goal_other',
        'master_content_format_other', 'seed_keywords'
    ]
    
    readonly_fields = [
        'submission_timestamp', 'webhook_sent', 'webhook_response'
    ]
    
    fieldsets = (
        ('Campaign Goal & Core Topic', {
            'fields': ('campaign_goal', 'campaign_goal_other', 'main_content_topic')
        }),
        ('Content Format & Keywords', {
            'fields': ('master_content_format', 'master_content_format_other', 'seed_keywords')
        }),
        ('Content Details & Audience', {
            'fields': ('target_word_count', 'audience_knowledge_level', 'audience_characteristics')
        }),
        ('Platforms & Linking', {
            'fields': ('target_platforms', 'avoid_platforms', 'internal_linking_pages')
        }),
        ('Brand Foundation', {
            'fields': ('website_url', 'brand_name')
        }),
        ('Brand Voice & E-E-A-T', {
            'fields': ('brand_voice_tone', 'other_voice_descriptors', 'eeat_highlights', 'top_content_urls')
        }),
        ('Visual Preferences', {
            'fields': ('visual_style', 'aesthetic_requirements', 'logo_url')
        }),
        ('Metadata', {
            'fields': ('submission_timestamp', 'webhook_sent', 'webhook_response'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual campaign creation in admin."""
        return False 