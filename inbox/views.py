from django.shortcuts import render,redirect
from .models import Message
from .forms import MessageForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView
from django.views import View
from login.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from home.models import UserPosts


# Create your views here.



class InboxAndSendMessageView(LoginRequiredMixin,View):
    template_name = 'inbox.html'

    def get(self, request, username = None):
        form = MessageForm()
        user_profile = UserProfile.objects.get(user = request.user)
        followings = user_profile.following.select_related('user')

        selected_user = None
        messages = []

        if username:
            selected_user = get_object_or_404(User, username=username)
            messages = Message.objects.filter(
                (models.Q(sender=request.user) & models.Q(recipient = selected_user)) |
                (models.Q(sender = selected_user) & models.Q(recipient = request.user))
            ).order_by('timestamp')

        shared_post_ids = []
        for msg in messages:
            if msg.context and '/post/' in msg.context:
                try:
                    post_id = int(msg.context.split('/post/')[1])
                    shared_post_ids.append(post_id)
                except:
                    continue

        shared_posts = UserPosts.objects.filter(id__in=shared_post_ids)
        shared_posts_dict = {str(post.id):post for post in shared_posts}

        return render(request, self.template_name,{
            'form':form,
            'user_profile':user_profile,
            'followings':followings,
            'selected_user':selected_user,
            'messages':messages,
            'shared_posts_dict':shared_posts_dict
        })
    
    def post(self, request,username=None):
        form = MessageForm(request.POST)
        user_profile = UserProfile.objects.get(user = request.user)
        followings = user_profile.following.select_related('user')
        selected_user = None

        if username:
            selected_user = get_object_or_404(User, username = username)

        if form.is_valid() and selected_user:
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = selected_user
            message.save()
            print('message',message.content)
            return redirect('inbox', selected_user.username)
        
        messages = []
        if selected_user:
            messages = Message.objects.filter(
                (models.Q(sender = request.user) & models.Q(recipient = selected_user)) |
                (models.Q(sender = selected_user) & models.Q(recipient = request.user))
            ).order_by('-timestamp')

        received_message = Message.objects.filter(recipient = request.user).order_by('-timestamp')
        return render(request, self.template_name, {
            'form':form,
            'user_profile':user_profile,
            'followings':followings,
            'messages':messages,
            'selected_user':selected_user

        })

    
    

# class SendMessageView(LoginRequiredMixin, CreateView):
#     model = Message
#     form_class = MessageForm
#     template_name = 'inbox.html'
#     success_url = reverse_lazy('inbox')

#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         return super().form_valid(form)
