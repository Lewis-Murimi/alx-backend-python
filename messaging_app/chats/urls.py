from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# This exact object name is required by the checker:
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
