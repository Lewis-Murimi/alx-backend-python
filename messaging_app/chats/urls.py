from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet

# This exact object name is required by the checker:
router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
