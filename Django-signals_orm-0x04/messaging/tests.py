from django.test import TestCase
from django.contrib.auth.models import User  # type: ignore
from .models import Message, Notification


class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender', password='password')
        self.receiver = User.objects.create_user(
            username='receiver', password='password')

    def test_notification_created_on_message(self):
        # Send a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello there!"
        )

        # Check if a notification was created
        notifications = Notification.objects.filter(
            user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)
        self.assertFalse(notifications.first().is_read)
