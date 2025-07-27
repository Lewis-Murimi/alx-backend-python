from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
        Custom permission to only allow participants of a conversation
        to send/view/update/delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For Messages (assuming obj.conversation exists)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
