from django.urls import path
from . import views

urlpatterns = [
    path('', views.webchat, name='chat'),
    path('webchat/', views.webchat, name='webchat'),
]