from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
import re


class CustomCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phonenumber = forms.CharField(max_length=15)
    profile_pic = forms.ImageField(required=False)
    college_name = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username','email','password1','password2','profile_pic','phonenumber','college_name','bio']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already registered . Please use another one ')
        return email
    
    def clean_phonenumber(self):
        phone = self.cleaned_data.get('phonenumber')
        digit_only = re.sub(r'\D','', phone)
        if len(phone)!=10:
            raise forms.ValidationError('phone number must be 10 digit ')
        return digit_only

    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user = user,
                phonenumber = self.cleaned_data['phonenumber'],
                profile_pic = self.cleaned_data.get('profile_pic'),
                college_name = self.cleaned_data.get('college_name'),
                bio = self.cleaned_data.get('bio')
            )
        return user
    

    


