from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class SevoCampaign(models.Model):
    """Model to store SEvO campaign configuration data."""
    
    # Campaign Goal & Core Topic
    CAMPAIGN_GOAL_CHOICES = [
        ('increase_brand_awareness', 'Increase Brand Awareness'),
        ('drive_website_traffic', 'Drive Website Traffic'),
        ('generate_leads', 'Generate Leads'),
        ('boost_sales_conversions', 'Boost Sales/Conversions'),
        ('improve_seo_rankings', 'Improve SEO Rankings'),
        ('build_thought_leadership', 'Build Thought Leadership'),
        ('customer_education', 'Customer Education'),
        ('product_launch', 'Product Launch'),
        ('crisis_management', 'Crisis Management'),
        ('other', 'Other'),
    ]
    
    campaign_goal = models.CharField(max_length=50, choices=CAMPAIGN_GOAL_CHOICES)
    campaign_goal_other = models.CharField(max_length=255, blank=True, null=True)
    main_content_topic = models.CharField(max_length=500)
    
    # Content Format & Keywords
    MASTER_CONTENT_FORMAT_CHOICES = [
        ('blog_post_article', 'Blog Post / Article'),
        ('video_content', 'Video Content'),
        ('podcast_episode', 'Podcast Episode'),
        ('infographic', 'Infographic'),
        ('case_study', 'Case Study'),
        ('how_to_guide', 'How-to Guide'),
        ('product_review', 'Product Review'),
        ('interview', 'Interview'),
        ('webinar', 'Webinar'),
        ('white_paper', 'White Paper'),
        ('email_newsletter', 'Email Newsletter'),
        ('social_media_post', 'Social Media Post'),
        ('other', 'Other'),
    ]
    
    master_content_format = models.CharField(max_length=50, choices=MASTER_CONTENT_FORMAT_CHOICES)
    master_content_format_other = models.CharField(max_length=255, blank=True, null=True)
    seed_keywords = models.TextField(blank=True, null=True)
    
    # Content Details & Audience Knowledge
    target_word_count = models.IntegerField(blank=True, null=True)
    audience_knowledge_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner (Little to no prior knowledge)'),
        ('intermediate', 'Intermediate (Some familiarity)'),
        ('advanced', 'Advanced (High expertise)'),
        ('mixed_audience', 'Mixed Audience'),
    ])
    
    # Audience Characteristics & Internal Linking
    audience_characteristics = models.TextField(blank=True, null=True)
    internal_linking_pages = models.TextField(blank=True, null=True)
    
    # Platform Selection
    target_platforms = models.JSONField(default=list)
    avoid_platforms = models.CharField(max_length=500, blank=True, null=True)
    
    # Brand Foundation
    website_url = models.URLField()
    brand_name = models.CharField(max_length=255)
    
    # Brand Voice & E-E-A-T
    brand_voice_tone = models.JSONField(default=list, blank=True)
    other_voice_descriptors = models.CharField(max_length=500, blank=True, null=True)
    eeat_highlights = models.TextField(blank=True, null=True)
    top_content_urls = models.TextField(blank=True, null=True)
    
    # Visual Preferences
    visual_style = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('modern_clean', 'Modern & Clean'),
        ('professional_corporate', 'Professional & Corporate'),
        ('creative_artistic', 'Creative & Artistic'),
        ('minimal_simple', 'Minimal & Simple'),
        ('bold_vibrant', 'Bold & Vibrant'),
        ('elegant_sophisticated', 'Elegant & Sophisticated'),
        ('fun_playful', 'Fun & Playful'),
        ('technical_data_driven', 'Technical & Data-driven'),
    ])
    aesthetic_requirements = models.CharField(max_length=500, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    
    # Metadata
    submission_timestamp = models.DateTimeField(auto_now_add=True)
    webhook_sent = models.BooleanField(default=False)
    webhook_response = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-submission_timestamp']
        verbose_name = 'SEvO Campaign'
        verbose_name_plural = 'SEvO Campaigns'
    
    def __str__(self):
        return f"{self.brand_name} - {self.main_content_topic}"
    
    def clean(self):
        """Custom validation for the model."""
        if self.campaign_goal == 'other' and not self.campaign_goal_other:
            raise ValidationError('Please specify the campaign goal when "Other" is selected.')
        
        if self.master_content_format == 'other' and not self.master_content_format_other:
            raise ValidationError('Please specify the content format when "Other" is selected.')
        
        if not self.target_platforms:
            raise ValidationError('At least one target platform must be selected.')
    
    def get_webhook_payload(self):
        """Return the data in the format expected by the webhook."""
        return {
            'campaignGoal': self.campaign_goal,
            'campaignGoalOther': self.campaign_goal_other,
            'mainContentTopic': self.main_content_topic,
            'masterContentFormat': self.master_content_format,
            'masterContentFormatOther': self.master_content_format_other,
            'seedKeywords': self.seed_keywords,
            'targetWordCount': self.target_word_count,
            'audienceKnowledgeLevel': self.audience_knowledge_level,
            'audienceCharacteristics': self.audience_characteristics,
            'internalLinkingPages': self.internal_linking_pages,
            'targetPlatforms': self.target_platforms,
            'avoidPlatforms': self.avoid_platforms,
            'websiteURL': self.website_url,
            'brandName': self.brand_name,
            'brandVoiceTone': self.brand_voice_tone,
            'otherVoiceDescriptors': self.other_voice_descriptors,
            'eeatHighlights': self.eeat_highlights,
            'topContentURLs': self.top_content_urls,
            'visualStyle': self.visual_style,
            'aestheticRequirements': self.aesthetic_requirements,
            'logoURL': self.logo_url,
            'submissionTimestamp': self.submission_timestamp.isoformat(),
        } 