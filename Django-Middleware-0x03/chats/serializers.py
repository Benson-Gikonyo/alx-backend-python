from .models import User, Message, Conversation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=True)
    # email = serializers.CharField(required=True)
    # password_hash = serializers.CharField(required=True)
    # phone_number = serializers.CharField(required=True)
    # role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(source="sender_id", read_only=True)
    message_body = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["message_id", "sender_id", "message_body"]

    def validate_message_body(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Message body must be at least 2 characters long"
            )
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(source="participants_id", read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id"]
