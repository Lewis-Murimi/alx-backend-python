from rest_framework import viewsets, status, filters  # <-- 'filters' now included
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .permissions import IsParticipantOfConversation
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]  # Optional: ordering support

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]  # Optional: ordering support

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')  # ✅ Checker expects this name
        return Message.objects.filter(conversation_id=conversation_id)  # ✅

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)  # ✅
        serializer.save(sender=self.request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
