from django.urls import path
from . import views

app_name = 'sevo_wizard'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/submit-campaign/', views.submit_campaign, name='submit_campaign'),
    path('api/campaign-options/', views.get_campaign_options, name='campaign_options'),
] 