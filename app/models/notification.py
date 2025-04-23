from django.db import models


class MessageLog(models.Model):
    EMAIL = 'email'
    SMS = 'sms'
    MESSAGE_TYPE_CHOICES = [
        (EMAIL, 'Email'),
        (SMS, 'SMS'),
    ]
    send_by = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.message_type} to {self.recipient} at {self.sent_at}"