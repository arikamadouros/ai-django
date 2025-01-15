from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_ai_response, name='openai-view'),
  path('get-ai-response/', views.get_ai_response, name='get_ai_response'),
]