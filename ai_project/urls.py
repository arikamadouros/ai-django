from django.contrib import admin
from django.urls import path, include
from bot.views import BotMessageView  # Correct path if located in bot/views.py


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', BotMessageView, name="bot-message"),
    path('api/openai/', include('openai_integration.urls')),
    path('api/searchai/', include('searchai_integration.urls')),
    path('api/integration/', include('ai_integration.urls')),
]
