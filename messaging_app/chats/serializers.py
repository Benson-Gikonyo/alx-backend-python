from .models import User, Message, Conversation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender_id", "message_body"]


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id"]
