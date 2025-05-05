from django import forms
from .models import UserPosts,Comment
from login.models import UserProfile


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPosts
        fields = ['description','image_video']


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['college_name', 'bio', 'profile_pic']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']