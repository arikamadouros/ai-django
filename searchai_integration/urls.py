from django.urls import path
from . import views

urlpatterns = [
  path('', views.query_search_ai, name='openai-search'),
  path('query-search-ai/', views.query_search_ai, name='search_ai'),
]