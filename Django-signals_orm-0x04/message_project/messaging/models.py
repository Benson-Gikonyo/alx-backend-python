from django.db import models
import uuid


# Create your models here.
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    sender = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateField(auto_now_add=False)


class Notification(models.Model):
    user = models.ForeignKey(
        "user", on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="notifications"
    )
    created_at = models.DateField(auto_now_add=True)
