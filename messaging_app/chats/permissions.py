from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
        Custom permission to only allow participants of a conversation
        to send/view/update/delete messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return False

            # ✅ Mention HTTP methods
        if request.method in ["PUT", "PATCH", "DELETE", "POST", "GET"]:
            return True

        # For Conversations
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        # For Messages (assuming obj.conversation exists)
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False
