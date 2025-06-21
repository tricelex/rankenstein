import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.conf import settings
import requests
from .models import SevoCampaign
from .serializers import SevoCampaignSerializer, SevoCampaignWebhookSerializer

logger = logging.getLogger(__name__)


def index(request):
    """Render the main SEvO Wizard interface."""
    return render(request, 'sevo_wizard/index.html')


@csrf_exempt
@require_http_methods(["POST"])
def submit_campaign(request):
    """Handle campaign submission and webhook delivery."""
    try:
        data = json.loads(request.body)
        
        # Create campaign instance
        campaign = SevoCampaign()
        
        # Map form data to model fields
        campaign.campaign_goal = data.get('campaignGoal')
        campaign.campaign_goal_other = data.get('campaignGoalOther')
        campaign.main_content_topic = data.get('mainContentTopic')
        campaign.master_content_format = data.get('masterContentFormat')
        campaign.master_content_format_other = data.get('masterContentFormatOther')
        campaign.seed_keywords = data.get('seedKeywords')
        campaign.target_word_count = data.get('targetWordCount')
        campaign.audience_knowledge_level = data.get('audienceKnowledgeLevel')
        campaign.audience_characteristics = data.get('audienceCharacteristics')
        campaign.internal_linking_pages = data.get('internalLinkingPages')
        campaign.target_platforms = data.get('targetPlatforms', [])
        campaign.avoid_platforms = data.get('avoidPlatforms')
        campaign.website_url = data.get('websiteURL')
        campaign.brand_name = data.get('brandName')
        campaign.brand_voice_tone = data.get('brandVoiceTone', [])
        campaign.other_voice_descriptors = data.get('otherVoiceDescriptors')
        campaign.eeat_highlights = data.get('eeatHighlights')
        campaign.top_content_urls = data.get('topContentURLs')
        campaign.visual_style = data.get('visualStyle')
        campaign.aesthetic_requirements = data.get('aestheticRequirements')
        campaign.logo_url = data.get('logoURL')
        
        # Validate the campaign
        campaign.full_clean()
        campaign.save()
        
        # Send webhook
        webhook_success = send_webhook(campaign)
        
        if webhook_success:
            return JsonResponse({
                'success': True,
                'message': 'Campaign submitted successfully!',
                'campaign_id': campaign.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Campaign saved but webhook delivery failed.',
                'campaign_id': campaign.id
            }, status=500)
            
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': 'Validation error',
            'errors': e.message_dict
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error submitting campaign: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Internal server error'
        }, status=500)


def send_webhook(campaign):
    """Send campaign data to webhook endpoint."""
    try:
        webhook_url = getattr(settings, 'WEBHOOK_URL', None)
        if not webhook_url:
            logger.warning("No webhook URL configured")
            return False
        
        # Prepare webhook payload
        payload = campaign.get_webhook_payload()
        
        # Send webhook
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Update campaign with webhook status
        campaign.webhook_sent = True
        campaign.webhook_response = {
            'status_code': response.status_code,
            'response_text': response.text,
            'success': response.status_code in [200, 201, 202]
        }
        campaign.save()
        
        if response.status_code in [200, 201, 202]:
            logger.info(f"Webhook sent successfully for campaign {campaign.id}")
            return True
        else:
            logger.error(f"Webhook failed with status {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook request failed: {str(e)}")
        campaign.webhook_sent = False
        campaign.webhook_response = {'error': str(e)}
        campaign.save()
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending webhook: {str(e)}")
        return False


@require_http_methods(["GET"])
def get_campaign_options(request):
    """Return available options for form fields."""
    return JsonResponse({
        'campaign_goals': dict(SevoCampaign.CAMPAIGN_GOAL_CHOICES),
        'content_formats': dict(SevoCampaign.MASTER_CONTENT_FORMAT_CHOICES),
        'audience_levels': [
            {'value': 'beginner', 'label': 'Beginner (Little to no prior knowledge)'},
            {'value': 'intermediate', 'label': 'Intermediate (Some familiarity)'},
            {'value': 'advanced', 'label': 'Advanced (High expertise)'},
            {'value': 'mixed_audience', 'label': 'Mixed Audience'},
        ],
        'visual_styles': [
            {'value': 'modern_clean', 'label': 'Modern & Clean'},
            {'value': 'professional_corporate', 'label': 'Professional & Corporate'},
            {'value': 'creative_artistic', 'label': 'Creative & Artistic'},
            {'value': 'minimal_simple', 'label': 'Minimal & Simple'},
            {'value': 'bold_vibrant', 'label': 'Bold & Vibrant'},
            {'value': 'elegant_sophisticated', 'label': 'Elegant & Sophisticated'},
            {'value': 'fun_playful', 'label': 'Fun & Playful'},
            {'value': 'technical_data_driven', 'label': 'Technical & Data-driven'},
        ],
        'platforms': [
            {'value': 'wordpress', 'label': 'WordPress (Master Content Destination)', 'description': 'Primary publishing platform, e.g., Blog Post / Article'},
            {'value': 'youtube', 'label': 'YouTube (Full Video Script, Shorts Ideas)', 'description': 'Video Content, Shorts'},
            {'value': 'linkedin', 'label': 'LinkedIn (Article/Pulse Post, Shorter Updates)', 'description': 'Professional Content, Articles'},
            {'value': 'google', 'label': 'Google', 'description': 'Google Search, Discover, News Feed Optimization'},
            {'value': 'ai_llm', 'label': 'AI / LLM Optimization', 'description': 'Optimizing for ChatGPT, Gemini, Perplexity AI responses'},
            {'value': 'twitter', 'label': 'X / Twitter (Thread Outline, Individual Tweet Ideas)', 'description': 'Short Updates, Threads'},
            {'value': 'tiktok', 'label': 'TikTok (Short Video Scripts/Ideas, Hashtag Suggestions)', 'description': 'Short-form Video, Trends'},
            {'value': 'pinterest', 'label': 'Pinterest (Pin Titles & Descriptions, Visual Concepts)', 'description': 'Visual Discovery, Idea Pins'},
            {'value': 'reddit', 'label': 'Reddit', 'description': 'Community Engagement, Niche Forums'},
            {'value': 'quora', 'label': 'Quora', 'description': 'Q&A Content, Thought Leadership'},
            {'value': 'podcast', 'label': 'Podcast (Key Talking Points, Segment Outline)', 'description': 'Audio Content, Episodes'},
            {'value': 'ecommerce', 'label': 'E-commerce Platforms (Amazon, Etsy, etc.)', 'description': 'Product Descriptions, Marketplace Content'},
        ],
        'brand_voice_options': [
            'Professional', 'Authoritative', 'Educational', 'Friendly', 
            'Witty / Humorous', 'Inspiring / Motivational', 'Casual / Conversational', 
            'Technical / Formal'
        ]
    }) 