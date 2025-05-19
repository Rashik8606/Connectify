from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
from inbox.models import Notification
from .models import UserPosts, Like , Share
from django.contrib.auth.models import User
from .forms import UserPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import EditUserProfile, CommentForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from inbox.models import Message

# Create your views here.

@login_required
def index(request):
    user_profile = UserProfile.objects.get(user = request.user)
    followed_profile = user_profile.following.all()
    followed_users = [profile.user for profile in followed_profile]

    posts = UserPosts.objects.filter(user__in = followed_users).order_by('-created_at').prefetch_related('comments')

    for post in posts:
        post.liked_by_user = Like.objects.filter(user = request.user, post = post).exists()

    followers = user_profile.followers.all()

    shared_post = Share.objects.filter(sender=request.user).select_related('original_post').order_by('-share_at')

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

    context = {
        'users':UserProfile.objects.all(),
        'form':form,
        'posts':posts,
        'followers':followers,
        'shared_post':shared_post
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

    return redirect(request.META.get('HTTP_REFERER','home:index'))
     
@login_required
def user_profile(request):
    profile = UserProfile.objects.get(user = request.user)

    followers = profile.followers.all()
    following = profile.following.all()
    post_count = UserPosts.objects.filter(user = request.user).count()
    user_post = UserPosts.objects.filter(user = request.user)

    context = {
         'profile':profile,
         'followers':followers,
         'following':following,
         'post_count':post_count,
         'user_post':user_post
    }
    return render(request, 'user-profile.html',context)


@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user = request.user)

    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.error(request, 'Profile Updated')
            return redirect('home:user-profile')
    else:
        form = EditUserProfile(instance=profile)
    return render(request, 'profile-edit.html', {'form':form})


@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(UserPosts, id = post_id)

        like, created = Like.objects.get_or_create(user = user, post = post)


        if created :
            if post.user != user:
                Notification.objects.create(
                    sender = user,
                    recipient = post.user,
                    post = post,
                    notification_type = 'like',
                    message = f'{user.username} liked your post'
                )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = post.like_count
        return JsonResponse({
            'liked':liked,
            'like_count':like_count
        })
    else:
        return JsonResponse({'error':'invalid request method'}, status = 400)

@require_POST
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(UserPosts, id = post_id)
    form = CommentForm(request.POST)
    print("Form valid:", form.is_valid())  # Log form validation
    print("POST data:", request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()


        if post.user != request.user:
            Notification.objects.create(
                sender = request.user,
                recipient = post.user,
                post = post,
                notification_type = 'comment',
                message = f'{request.user.username} commented on your post '
            )
        return JsonResponse({
            'success':True,
            'text':comment.text,
            'username':comment.user.username
        })
    else:
        return JsonResponse({'success':False, 'error':'Empty comment'})

@login_required
def share_post(request,post_id):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')

        if not recipient_id:
            messages.error(request, 'No recipient selected')
            return redirect('home:index')

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            messages.error(request,'Recipient Not Found..')
            return redirect('home:index')

        post = get_object_or_404(UserPosts, id=post_id)
        sender = request.user

        Share.objects.get_or_create(sender=sender, recipient=recipient, original_post=post)
        

        message_text = f'/post/{post_id}'
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            context=message_text,
            post = post
        )
        messages.error(request, 'post shared Successfully ..')
        return redirect('home:index')

    return redirect('home:index')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(UserPosts, id=post_id)
    return render(request, 'index.html', {'post': post})


# class based views.........

from django.views.generic import ListView
from django.db.models import Q


class UserSearchView(ListView):
    model = UserProfile
    template_name = 'search-user.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UserProfile.objects.filter(Q(user__username__icontains = query))
        return UserProfile.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_profile = UserProfile.objects.get(user = self.request.user)
        context['following_ids'] = current_user_profile.following.values_list('id',flat=True)
        return context