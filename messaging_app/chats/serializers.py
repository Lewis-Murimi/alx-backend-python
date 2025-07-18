from rest_framework import serializers
from .models import User, Message, Conversation

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

# Conversation Serializer with Nested Messages and Participants
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

# Optional: Create Serializer for POST requests with participant IDs
class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source='participants'
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
