# Generated by Django 4.2.7 on 2025-06-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SevoCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_goal', models.CharField(choices=[('increase_brand_awareness', 'Increase Brand Awareness'), ('drive_website_traffic', 'Drive Website Traffic'), ('generate_leads', 'Generate Leads'), ('boost_sales_conversions', 'Boost Sales/Conversions'), ('improve_seo_rankings', 'Improve SEO Rankings'), ('build_thought_leadership', 'Build Thought Leadership'), ('customer_education', 'Customer Education'), ('product_launch', 'Product Launch'), ('crisis_management', 'Crisis Management'), ('other', 'Other')], max_length=50)),
                ('campaign_goal_other', models.CharField(blank=True, max_length=255, null=True)),
                ('main_content_topic', models.CharField(max_length=500)),
                ('master_content_format', models.CharField(choices=[('blog_post_article', 'Blog Post / Article'), ('video_content', 'Video Content'), ('podcast_episode', 'Podcast Episode'), ('infographic', 'Infographic'), ('case_study', 'Case Study'), ('how_to_guide', 'How-to Guide'), ('product_review', 'Product Review'), ('interview', 'Interview'), ('webinar', 'Webinar'), ('white_paper', 'White Paper'), ('email_newsletter', 'Email Newsletter'), ('social_media_post', 'Social Media Post'), ('other', 'Other')], max_length=50)),
                ('master_content_format_other', models.CharField(blank=True, max_length=255, null=True)),
                ('seed_keywords', models.TextField(blank=True, null=True)),
                ('target_word_count', models.IntegerField(blank=True, null=True)),
                ('audience_knowledge_level', models.CharField(choices=[('beginner', 'Beginner (Little to no prior knowledge)'), ('intermediate', 'Intermediate (Some familiarity)'), ('advanced', 'Advanced (High expertise)'), ('mixed_audience', 'Mixed Audience')], max_length=20)),
                ('audience_characteristics', models.TextField(blank=True, null=True)),
                ('internal_linking_pages', models.TextField(blank=True, null=True)),
                ('target_platforms', models.JSONField(default=list)),
                ('avoid_platforms', models.CharField(blank=True, max_length=500, null=True)),
                ('website_url', models.URLField()),
                ('brand_name', models.CharField(max_length=255)),
                ('brand_voice_tone', models.JSONField(blank=True, default=list)),
                ('other_voice_descriptors', models.CharField(blank=True, max_length=500, null=True)),
                ('eeat_highlights', models.TextField(blank=True, null=True)),
                ('top_content_urls', models.TextField(blank=True, null=True)),
                ('visual_style', models.CharField(blank=True, choices=[('modern_clean', 'Modern & Clean'), ('professional_corporate', 'Professional & Corporate'), ('creative_artistic', 'Creative & Artistic'), ('minimal_simple', 'Minimal & Simple'), ('bold_vibrant', 'Bold & Vibrant'), ('elegant_sophisticated', 'Elegant & Sophisticated'), ('fun_playful', 'Fun & Playful'), ('technical_data_driven', 'Technical & Data-driven')], max_length=50, null=True)),
                ('aesthetic_requirements', models.CharField(blank=True, max_length=500, null=True)),
                ('logo_url', models.URLField(blank=True, null=True)),
                ('submission_timestamp', models.DateTimeField(auto_now_add=True)),
                ('webhook_sent', models.BooleanField(default=False)),
                ('webhook_response', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'SEvO Campaign',
                'verbose_name_plural': 'SEvO Campaigns',
                'ordering': ['-submission_timestamp'],
            },
        ),
    ]
