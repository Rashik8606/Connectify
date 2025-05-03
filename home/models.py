from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.


class UserPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(blank=True)
    image_video = models.FileField(upload_to='users_post/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Post"
    
    @property
    def is_image(self):
        ext = os.path.splitext(self.image_video.name)[1].lower()
        return ext in ['.jpg', '.png', '.jpeg', '.gif']
    @property
    def is_video(self):
        ext = os.path.splitext(self.image_video.name)[1].lower()
        return ext in ['.mp4', '.webm', 'ogg']
    