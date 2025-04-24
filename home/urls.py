from django.urls import path
from .import views 
from django.conf.urls.static import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('',views.index,name='index'),
    path('follow/<int:user_id>/',views.follow_toggle,name='follow_toggle'),
    
]
