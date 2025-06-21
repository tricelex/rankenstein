from rest_framework import serializers
from .models import SevoCampaign


class SevoCampaignSerializer(serializers.ModelSerializer):
    """Serializer for SEvO Campaign model."""
    
    class Meta:
        model = SevoCampaign
        fields = '__all__'
        read_only_fields = ('submission_timestamp', 'webhook_sent', 'webhook_response')
    
    def validate(self, data):
        """Custom validation for the serializer."""
        # Validate campaign goal other field
        if data.get('campaign_goal') == 'other' and not data.get('campaign_goal_other'):
            raise serializers.ValidationError(
                'Please specify the campaign goal when "Other" is selected.'
            )
        
        # Validate master content format other field
        if data.get('master_content_format') == 'other' and not data.get('master_content_format_other'):
            raise serializers.ValidationError(
                'Please specify the content format when "Other" is selected.'
            )
        
        # Validate target platforms
        if not data.get('target_platforms'):
            raise serializers.ValidationError(
                'At least one target platform must be selected.'
            )
        
        return data


class SevoCampaignWebhookSerializer(serializers.ModelSerializer):
    """Serializer for webhook payload format."""
    
    class Meta:
        model = SevoCampaign
        fields = [
            'campaign_goal', 'campaign_goal_other', 'main_content_topic',
            'master_content_format', 'master_content_format_other', 'seed_keywords',
            'target_word_count', 'audience_knowledge_level', 'audience_characteristics',
            'internal_linking_pages', 'target_platforms', 'avoid_platforms',
            'website_url', 'brand_name', 'brand_voice_tone', 'other_voice_descriptors',
            'eeat_highlights', 'top_content_urls', 'visual_style', 'aesthetic_requirements',
            'logo_url', 'submission_timestamp'
        ]
    
    def to_representation(self, instance):
        """Convert to webhook payload format."""
        data = super().to_representation(instance)
        
        # Convert field names to camelCase for webhook
        webhook_data = {
            'campaignGoal': data['campaign_goal'],
            'campaignGoalOther': data['campaign_goal_other'],
            'mainContentTopic': data['main_content_topic'],
            'masterContentFormat': data['master_content_format'],
            'masterContentFormatOther': data['master_content_format_other'],
            'seedKeywords': data['seed_keywords'],
            'targetWordCount': data['target_word_count'],
            'audienceKnowledgeLevel': data['audience_knowledge_level'],
            'audienceCharacteristics': data['audience_characteristics'],
            'internalLinkingPages': data['internal_linking_pages'],
            'targetPlatforms': data['target_platforms'],
            'avoidPlatforms': data['avoid_platforms'],
            'websiteURL': data['website_url'],
            'brandName': data['brand_name'],
            'brandVoiceTone': data['brand_voice_tone'],
            'otherVoiceDescriptors': data['other_voice_descriptors'],
            'eeatHighlights': data['eeat_highlights'],
            'topContentURLs': data['top_content_urls'],
            'visualStyle': data['visual_style'],
            'aestheticRequirements': data['aesthetic_requirements'],
            'logoURL': data['logo_url'],
            'submissionTimestamp': data['submission_timestamp'],
        }
        
        return webhook_data 