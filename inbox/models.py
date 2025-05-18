from django.db import models
from login.models import User,UserProfile
from home.models import UserPosts
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    context = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    post = models.ForeignKey(UserPosts, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'From {self.sender} to {self.recipient}' 
    

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like' , 'Like'),
        ('comment','Comment'),
        ('following', 'Following')
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notification')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_notification')
    post = models.ForeignKey(UserPosts, on_delete=models.CASCADE, null=True , blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} {self.notification_type} to {self.recipient}'