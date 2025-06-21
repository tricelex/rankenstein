// SEvO Configuration Wizard JavaScript
class SevoWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 10;
        this.formData = {};
        this.platformOptions = [];
        this.init();
    }

    init() {
        this.loadPlatformOptions();
        this.bindEvents();
        
        // Delay the initial validation to ensure DOM is ready
        setTimeout(() => {
            this.updateProgress();
            this.updateNavigationButtons();
        }, 100);
    }

    async loadPlatformOptions() {
        try {
            const response = await fetch('/api/campaign-options/');
            const data = await response.json();
            console.log(data);
            this.platformOptions = data.platforms;
            this.populatePlatformCheckboxes();
        } catch (error) {
            console.error('Error loading platform options:', error);
        }
    }

    bindEvents() {
        // Navigation buttons
        document.getElementById('nextBtn').addEventListener('click', () => this.nextStep());
        document.getElementById('backBtn').addEventListener('click', () => this.previousStep());
        document.getElementById('submitBtn').addEventListener('click', () => this.submitForm());
        document.getElementById('createAnotherBtn').addEventListener('click', () => this.resetForm());

        // Form field events
        this.bindFormEvents();
        
        // Slider events
        this.bindSliderEvents();
        
        // Conditional field events
        this.bindConditionalEvents();
    }

    bindFormEvents() {
        // Real-time validation for required fields
        const requiredFields = document.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('input', () => {
                this.saveCurrentStepData();
                this.validateCurrentStep();
                this.updateNavigationButtons();
            });
            field.addEventListener('change', () => {
                this.saveCurrentStepData();
                this.validateCurrentStep();
                this.updateNavigationButtons();
            });
        });

        // Checkbox events for platforms
        document.addEventListener('change', (e) => {
            if (e.target.name === 'targetPlatforms') {
                this.saveCurrentStepData();
                this.validateCurrentStep();
                this.updateNavigationButtons();
            }
        });
    }

    bindSliderEvents() {
        const wordCountSlider = document.getElementById('targetWordCount');
        const wordCountValue = document.getElementById('wordCountValue');
        
        if (wordCountSlider && wordCountValue) {
            wordCountSlider.addEventListener('input', (e) => {
                const value = e.target.value;
                wordCountValue.textContent = `${value} words`;
                this.formData.targetWordCount = parseInt(value);
            });
        }
    }

    bindConditionalEvents() {
        // Campaign goal other field
        const campaignGoal = document.getElementById('campaignGoal');
        const campaignGoalOther = document.getElementById('campaignGoalOtherField');
        
        if (campaignGoal) {
            campaignGoal.addEventListener('change', (e) => {
                this.saveCurrentStepData();
                if (e.target.value === 'other') {
                    campaignGoalOther.style.display = 'block';
                    document.getElementById('campaignGoalOther').required = true;
                } else {
                    campaignGoalOther.style.display = 'none';
                    document.getElementById('campaignGoalOther').required = false;
                    document.getElementById('campaignGoalOther').value = '';
                }
                this.validateCurrentStep();
                this.updateNavigationButtons();
            });
        }

        // Content format other field
        const contentFormat = document.getElementById('masterContentFormat');
        const contentFormatOther = document.getElementById('masterContentFormatOtherField');
        
        if (contentFormat) {
            contentFormat.addEventListener('change', (e) => {
                this.saveCurrentStepData();
                if (e.target.value === 'other') {
                    contentFormatOther.style.display = 'block';
                    document.getElementById('masterContentFormatOther').required = true;
                } else {
                    contentFormatOther.style.display = 'none';
                    document.getElementById('masterContentFormatOther').required = false;
                    document.getElementById('masterContentFormatOther').value = '';
                }
                this.validateCurrentStep();
                this.updateNavigationButtons();
            });
        }
    }

    populatePlatformCheckboxes() {
        const container = document.getElementById('platformCheckboxes');
        if (!container) return;

        container.innerHTML = '';
        
        this.platformOptions.forEach(platform => {
            const card = document.createElement('div');
            card.className = 'checkbox-card';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `platform_${platform.value}`;
            checkbox.name = 'targetPlatforms';
            checkbox.value = platform.value;
            
            const label = document.createElement('label');
            label.htmlFor = `platform_${platform.value}`;
            label.innerHTML = `
                <span class="checkbox-label-content">
                    <span class="checkbox-label-title">${platform.label}</span>
                    <span class="checkbox-label-description">${platform.description}</span>
                </span>
            `;
            
            card.appendChild(checkbox);
            card.appendChild(label);
            container.appendChild(card);
        });
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            this.saveCurrentStepData();
            
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.showStep(this.currentStep);
                this.updateProgress();
                this.updateNavigationButtons();
                
                // Special handling for step 5 (platforms)
                if (this.currentStep === 5) {
                    this.generatePlatformRecommendations();
                }
                
                // Special handling for step 10 (summary)
                if (this.currentStep === 10) {
                    this.generateSummary();
                }
            }
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showStep(this.currentStep);
            this.updateProgress();
            this.updateNavigationButtons();
        }
    }

    showStep(stepNumber) {
        // Hide all steps
        const steps = document.querySelectorAll('.step');
        steps.forEach(step => {
            step.style.display = 'none';
        });

        // Show current step
        const currentStepElement = document.getElementById(`step${stepNumber}`);
        if (currentStepElement) {
            currentStepElement.style.display = 'block';
            currentStepElement.classList.add('fade-in');
        }
    }

    updateProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        if (progressFill) {
            const percentage = (this.currentStep / this.totalSteps) * 100;
            progressFill.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = `Step ${this.currentStep} of ${this.totalSteps}`;
        }
    }

    updateNavigationButtons() {
        const backBtn = document.getElementById('backBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');

        // Show/hide back button
        if (backBtn) {
            backBtn.style.display = this.currentStep > 1 ? 'flex' : 'none';
        }

        // Show/hide next and submit buttons
        if (nextBtn && submitBtn) {
            if (this.currentStep === this.totalSteps) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'flex';
            } else {
                nextBtn.style.display = 'flex';
                submitBtn.style.display = 'none';
            }
        }

        // Disable next button if current step is not valid
        if (nextBtn) {
            nextBtn.disabled = !this.validateCurrentStep();
        }
    }

    validateCurrentStep() {
        const currentStepElement = document.getElementById(`step${this.currentStep}`);
        if (!currentStepElement) return true;

        const requiredFields = currentStepElement.querySelectorAll('[required]');
        let isValid = true;

        console.log(`Validating step ${this.currentStep}, found ${requiredFields.length} required fields`);

        requiredFields.forEach(field => {
            const fieldValue = field.value.trim();
            console.log(`Field ${field.name}: "${fieldValue}"`);
            
            // Special handling for conditional "Other" fields
            if (field.name === 'campaignGoalOther' && this.formData.campaignGoal !== 'other') {
                // Skip validation if "Other" is not selected
                this.clearFieldError(field);
                return;
            }
            
            if (field.name === 'masterContentFormatOther' && this.formData.masterContentFormat !== 'other') {
                // Skip validation if "Other" is not selected
                this.clearFieldError(field);
                return;
            }
            
            if (field.type === 'checkbox') {
                // For checkboxes, check if at least one is selected
                const checkboxes = currentStepElement.querySelectorAll(`input[name="${field.name}"]`);
                const checkedBoxes = Array.from(checkboxes).filter(cb => cb.checked);
                if (checkedBoxes.length === 0) {
                    isValid = false;
                    this.showFieldError(field, 'This field is required');
                } else {
                    this.clearFieldError(field);
                }
            } else {
                if (!fieldValue) {
                    isValid = false;
                    this.showFieldError(field, 'This field is required');
                } else {
                    this.clearFieldError(field);
                }
            }
        });

        console.log(`Step ${this.currentStep} validation result:`, isValid);
        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('error');
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorMessage = field.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    saveCurrentStepData() {
        const currentStepElement = document.getElementById(`step${this.currentStep}`);
        if (!currentStepElement) return;

        // Collect form data from current step
        const formElements = currentStepElement.querySelectorAll('input, select, textarea');
        
        formElements.forEach(element => {
            if (element.name) {
                if (element.type === 'checkbox') {
                    if (element.checked) {
                        if (!this.formData[element.name]) {
                            this.formData[element.name] = [];
                        }
                        this.formData[element.name].push(element.value);
                    }
                } else {
                    this.formData[element.name] = element.value;
                }
            }
        });
    }

    generatePlatformRecommendations() {
        const recommendationList = document.getElementById('recommendationList');
        if (!recommendationList) return;

        // Generate recommendations based on previous inputs
        const recommendations = this.getPlatformRecommendations();
        
        recommendationList.innerHTML = '';
        recommendations.forEach(rec => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            item.textContent = rec;
            recommendationList.appendChild(item);
        });

        // Pre-select recommended platforms
        recommendations.forEach(rec => {
            const checkbox = document.querySelector(`input[value="${rec.toLowerCase()}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }

    getPlatformRecommendations() {
        const recommendations = [];
        const contentFormat = this.formData.masterContentFormat;
        const campaignGoal = this.formData.campaignGoal;

        // Base recommendations
        recommendations.push('wordpress', 'google');

        // Content format specific
        if (contentFormat === 'video_content') {
            recommendations.push('youtube', 'tiktok');
        } else if (contentFormat === 'blog_post_article') {
            recommendations.push('linkedin', 'ai_llm');
        } else if (contentFormat === 'podcast_episode') {
            recommendations.push('podcast', 'linkedin');
        }

        // Campaign goal specific
        if (campaignGoal === 'build_thought_leadership') {
            recommendations.push('linkedin', 'quora');
        } else if (campaignGoal === 'generate_leads') {
            recommendations.push('linkedin', 'ai_llm');
        }

        return recommendations.slice(0, 5); // Limit to 5 recommendations
    }

    generateSummary() {
        const summaryContainer = document.getElementById('campaignSummary');
        if (!summaryContainer) return;

        const summaryData = this.getSummaryData();
        
        summaryContainer.innerHTML = '';
        summaryData.forEach(item => {
            const summaryItem = document.createElement('div');
            summaryItem.className = 'summary-item';
            summaryItem.innerHTML = `
                <div class="summary-label">${item.label}</div>
                <div class="summary-value">${item.value}</div>
            `;
            summaryContainer.appendChild(summaryItem);
        });
    }

    getSummaryData() {
        return [
            { label: 'Campaign Goal', value: this.getDisplayValue('campaignGoal', this.formData.campaignGoal) },
            { label: 'Main Topic', value: this.formData.mainContentTopic || 'Not specified' },
            { label: 'Content Format', value: this.getDisplayValue('masterContentFormat', this.formData.masterContentFormat) },
            { label: 'Target Platforms', value: this.formData.targetPlatforms ? this.formData.targetPlatforms.length + ' platforms selected' : 'None selected' },
            { label: 'Brand Name', value: this.formData.brandName || 'Not specified' },
            { label: 'Website', value: this.formData.websiteURL || 'Not specified' }
        ];
    }

    getDisplayValue(fieldName, value) {
        if (!value) return 'Not specified';
        
        const displayMaps = {
            campaignGoal: {
                'increase_brand_awareness': 'Increase Brand Awareness',
                'drive_website_traffic': 'Drive Website Traffic',
                'generate_leads': 'Generate Leads',
                'boost_sales_conversions': 'Boost Sales/Conversions',
                'improve_seo_rankings': 'Improve SEO Rankings',
                'build_thought_leadership': 'Build Thought Leadership',
                'customer_education': 'Customer Education',
                'product_launch': 'Product Launch',
                'crisis_management': 'Crisis Management',
                'other': this.formData.campaignGoalOther || 'Other'
            },
            masterContentFormat: {
                'blog_post_article': 'Blog Post / Article',
                'video_content': 'Video Content',
                'podcast_episode': 'Podcast Episode',
                'infographic': 'Infographic',
                'case_study': 'Case Study',
                'how_to_guide': 'How-to Guide',
                'product_review': 'Product Review',
                'interview': 'Interview',
                'webinar': 'Webinar',
                'white_paper': 'White Paper',
                'email_newsletter': 'Email Newsletter',
                'social_media_post': 'Social Media Post',
                'other': this.formData.masterContentFormatOther || 'Other'
            }
        };

        return displayMaps[fieldName]?.[value] || value;
    }

    async submitForm() {
        if (!this.validateCurrentStep()) {
            return;
        }

        this.saveCurrentStepData();
        
        // Show loading overlay
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }

        try {
            const response = await fetch('/api/submit-campaign/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(this.formData)
            });

            const result = await response.json();

            if (result.success) {
                this.showConfirmation();
            } else {
                this.showError(result.message || 'Submission failed');
            }
        } catch (error) {
            console.error('Submission error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            // Hide loading overlay
            if (loadingOverlay) {
                loadingOverlay.style.display = 'none';
            }
        }
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    showConfirmation() {
        const confirmationStep = document.getElementById('confirmation');
        if (confirmationStep) {
            // Hide all other steps
            const steps = document.querySelectorAll('.step');
            steps.forEach(step => {
                if (step.id !== 'confirmation') {
                    step.style.display = 'none';
                }
            });

            // Show confirmation
            confirmationStep.style.display = 'block';
            confirmationStep.classList.add('fade-in');

            // Hide navigation buttons
            const navigationButtons = document.querySelector('.navigation-buttons');
            if (navigationButtons) {
                navigationButtons.style.display = 'none';
            }
        }
    }

    showError(message) {
        // Create and show error notification
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
            z-index: 1001;
            animation: slideInRight 0.3s ease;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    resetForm() {
        // Reset form data
        this.formData = {};
        this.currentStep = 1;

        // Reset all form fields
        const formElements = document.querySelectorAll('input, select, textarea');
        formElements.forEach(element => {
            if (element.type === 'checkbox') {
                element.checked = false;
            } else {
                element.value = '';
            }
        });

        // Reset progress and navigation
        this.showStep(1);
        this.updateProgress();
        this.updateNavigationButtons();

        // Show navigation buttons again
        const navigationButtons = document.querySelector('.navigation-buttons');
        if (navigationButtons) {
            navigationButtons.style.display = 'flex';
        }

        // Clear any error states
        const errorFields = document.querySelectorAll('.error');
        errorFields.forEach(field => {
            field.classList.remove('error');
        });

        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(message => {
            message.remove();
        });
    }
}

// Initialize the wizard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SevoWizard();
});

// Add slide-in animation for error notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style); 