from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from bot.views import BotMessageView
from web_frontend.views import webchat


urlpatterns = [
  # Route for the frontend
  path('', TemplateView.as_view(template_name="web_frontend/index.html"), name='home'),

  path('admin/', admin.site.urls),
  path('bot/', BotMessageView, name="bot-message"),
  
  # API endpoint for chat search
  path('api/openai/', include('openai_integration.urls')),
  path('api/searchai/', include('searchai_integration.urls')),
  path('api/integration/', include('ai_integration.urls')),
  path('api/webchat/', webchat, name='webchat'),
]
