from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(blank=True)
    image_video = models.FileField(upload_to='users_post/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Post"
    