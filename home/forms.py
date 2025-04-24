from django import forms
from .models import UserPosts


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPosts
        fields = ['description','image_video']