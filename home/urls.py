from django.urls import path
from .import views 
from django.conf.urls.static import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('',views.index,name='index'),
    path('follow/<int:user_id>/',views.follow_toggle,name='follow_toggle'),
    path('user-profile/',views.user_profile,name='user-profile'),
    path('edit-profile/',views.edit_profile,name='user-profile-edit'),
    path('like/<int:post_id>/', views.like_post,name='like-post'),
    path('comment/<int:post_id>', views.comment_post,name='comment-post'),
    
]
