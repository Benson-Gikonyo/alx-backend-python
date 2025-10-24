from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.CharField(max_length=30, unique=True, null=False)
    password_hash = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=30, null=True)
    role = models.CharField(
        max_length=10, choices=Role.choices, null=False, blank=False
    )
    created_at = models.DateField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_index=True, editable=False
    )
    sender_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="received_messages"
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, db_index=True
    )
    participants_id = models.ForeignKey("user", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
