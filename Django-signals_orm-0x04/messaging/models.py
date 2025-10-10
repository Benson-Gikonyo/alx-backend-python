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
    edited = models.BooleanField(default=False)
    edited_at = models.DateField(auto_now_add=True)
    edited_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages",
    )

    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:30]}"

    def get_thread(self):
        replies = self.replies.select_related("sender", "reciever").all()
        thread = []
        for reply in replies:
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread


class Notification(models.Model):
    user = models.ForeignKey(
        "user", on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="notifications"
    )
    created_at = models.DateField(auto_now_add=True)


class MessageHistory(models.Model):
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="message_edits",
    )
