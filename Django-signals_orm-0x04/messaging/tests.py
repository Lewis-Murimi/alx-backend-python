from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.
class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello!'
        )
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertFalse(notification.is_read)
