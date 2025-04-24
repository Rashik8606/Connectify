from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pic/',default='profile_pic/default.jpg',blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return f'{self.user.username}'

