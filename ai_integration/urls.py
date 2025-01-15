from django.urls import path
from . import views

urlpatterns = [
  path('', views.integrate_search_and_summarize, name='ai-integration-view'),
  path('search_and_summarize/', views.integrate_search_and_summarize, name='search-and-summarize'),
]