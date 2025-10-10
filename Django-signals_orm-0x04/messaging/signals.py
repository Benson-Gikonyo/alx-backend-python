from django.db.models import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """log its old content into message history if its being edited before saving a message."""

    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=instance.edited_by,
            )
            instance.edited = True
            instance.edited_at = timezone.now()
