from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
from .models import UserPosts
from django.contrib.auth.models import User
from .forms import UserPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

@login_required
def index(request):
    users_profile = UserProfile.objects.get(user = request.user)
    followed_profile = users_profile.following.all()
    followed_users = [profile.user for profile in followed_profile]

    posts = UserPosts.objects.filter(user__in = followed_users).order_by('-created_at')

    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            print(f"User: {request.user}") 
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home:index') 
    else:
        form = UserPostForm()

    for post in posts:
            if post.image_video:
                ext = post.image_video.url.split('.')[-1].lower()
                post.is_video = ext in ['mp4', 'webm', 'ogg']
            else:
                 post.image_video = False

    context = {
        'users':UserProfile.objects.all(),
        'form':form,
        'posts':posts
        }
    
    return render(request,'index.html',context)



def follow_toggle(request, user_id):
    current_user_profile = UserProfile.objects.get(user=request.user)
    target_user = get_object_or_404(User, id=user_id)
    target_profile = UserProfile.objects.get(user = target_user)
    current_user = request.user

    if target_profile in current_user_profile.following.all():
        current_user_profile.following.remove(target_profile)
    else:
         current_user_profile.following.add(target_profile)

    return HttpResponseRedirect(reverse('home:index'))
     
@login_required
def user_profile(request):
     
     return render(request, 'user-profile.html',{'user':request.user})