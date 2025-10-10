from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


# Create your tests here.
class MessageNotificationTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="ben", password="1234")
        self.receiver = User.objects.create_user(username="alice", password="1234")

    def test_notification_created_on_messsage(self):
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello Alice"
        )
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)
