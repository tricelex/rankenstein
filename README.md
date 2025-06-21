# Rankenstein SEvO Configuration Wizard

A sophisticated, multi-step conversational SEvO (Search Engine and Voice Optimization) Wizard application built with Django. This application guides users through a comprehensive configuration process for their SEvO campaigns, collects detailed information, and submits this data to a specified webhook upon completion.

## Features

- **Modern Dark Theme**: Sleek, professional dark theme with glassmorphism effects
- **Multi-Step Form**: 10-step conversational flow with progress tracking
- **Responsive Design**: Fully responsive for desktop, tablet, and mobile devices
- **Real-time Validation**: Form validation with user-friendly error messages
- **Platform Recommendations**: Intelligent platform suggestions based on user inputs
- **Webhook Integration**: Automatic data submission to configurable webhook endpoint
- **Admin Interface**: Django admin panel for campaign management
- **CSRF Protection**: Secure form submission with CSRF tokens

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Styling**: Custom CSS with glassmorphism effects
- **Icons**: Font Awesome 6.0
- **Fonts**: Inter (Google Fonts)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rankenstein
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   WEBHOOK_URL=https://your-webhook-endpoint.com/webhook
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Configuration

### Webhook Setup

The application sends campaign data to a webhook endpoint. Configure the webhook URL in your `.env` file:

```env
WEBHOOK_URL=https://your-webhook-endpoint.com/webhook
```

### Webhook Payload Format

The webhook receives a JSON payload with the following structure:

```json
{
  "campaignGoal": "increase_brand_awareness",
  "campaignGoalOther": null,
  "mainContentTopic": "Benefits of Filtered Showerheads",
  "masterContentFormat": "blog_post_article",
  "masterContentFormatOther": null,
  "seedKeywords": "best shower filters, hard water solution",
  "targetWordCount": 1500,
  "audienceKnowledgeLevel": "beginner",
  "audienceCharacteristics": "Key problems and interests...",
  "internalLinkingPages": "yoursite.com/page1, yoursite.com/page2",
  "targetPlatforms": ["wordpress", "linkedin", "google"],
  "avoidPlatforms": "TikTok, Facebook",
  "websiteURL": "https://www.yourwebsite.com",
  "brandName": "Your Brand Name",
  "brandVoiceTone": ["Professional", "Educational"],
  "otherVoiceDescriptors": "Additional voice descriptors",
  "eeatHighlights": "10+ years experience, Certified...",
  "topContentURLs": "yoursite.com/best-article-1\nyoursite.com/another-piece",
  "visualStyle": "modern_clean",
  "aestheticRequirements": "Blue, white, #0000FF",
  "logoURL": "https://www.yourwebsite.com/logo.png",
  "submissionTimestamp": "2024-01-15T10:30:00Z"
}
```

## Form Flow

The wizard consists of 10 steps:

1. **Campaign Goal & Core Topic**: Define campaign objectives and main content topic
2. **Content Format & Keywords**: Choose content format and initial keywords
3. **Content Details & Audience Knowledge**: Specify word count and audience expertise level
4. **Audience Characteristics & Internal Linking**: Describe audience and internal linking strategy
5. **Platform Recommendation & Target Selection**: Choose target platforms with intelligent recommendations
6. **Platforms to AVOID**: Specify platforms to exclude
7. **Brand Foundation**: Provide website URL and brand name
8. **Brand Voice & E-E-A-T**: Define brand voice and establish authority
9. **Visual Preferences**: Specify visual style and aesthetic requirements
10. **Final Submission**: Review and submit campaign

## API Endpoints

- `GET /`: Main application interface
- `POST /api/submit-campaign/`: Submit campaign data
- `GET /api/campaign-options/`: Get available form options
- `GET /admin/`: Django admin interface

## Customization

### Styling

The application uses a custom CSS file located at `static/css/style.css`. The design features:

- Dark theme with blue gradient background
- Glassmorphism effects on form cards
- Smooth animations and transitions
- Responsive design for all devices

### Form Fields

To add or modify form fields:

1. Update the `SevoCampaign` model in `sevo_wizard/models.py`
2. Modify the form template in `templates/sevo_wizard/index.html`
3. Update the JavaScript validation in `static/js/wizard.js`
4. Run database migrations

### Platform Options

Platform recommendations are generated in the `getPlatformRecommendations()` method in `static/js/wizard.js`. Modify this method to change the recommendation logic.

## Deployment

### Production Settings

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving with WhiteNoise or a CDN
4. Configure your webhook URL
5. Set up proper logging

### Environment Variables

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
WEBHOOK_URL=https://your-production-webhook.com/webhook
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.

## Changelog

### Version 1.0.0
- Initial release
- 10-step SEvO configuration wizard
- Dark theme with glassmorphism design
- Webhook integration
- Django admin interface
- Responsive design
- Real-time form validation 