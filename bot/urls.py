from django.urls import path
from .views import BotMessageView

urlpatterns = [
    path('', BotMessageView.as_view(), name='bot-messages'),
]