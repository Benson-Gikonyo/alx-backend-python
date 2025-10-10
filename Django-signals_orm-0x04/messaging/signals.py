from django.db.models import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
