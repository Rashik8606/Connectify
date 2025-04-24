from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = 'login'

urlpatterns = [
    path('signup/',views.user_signup,name='signup-page'),
    path('login/',views.login_user,name='login-page'),
    path('logout/',auth_views.LogoutView.as_view(next_page = '/login/'),name='logout')
]