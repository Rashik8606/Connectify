from django.urls import path
from .views import InboxAndSendMessageView,NotificationPage



urlpatterns = [
    path('notification/',NotificationPage.as_view(),name='notifications'),
    path('',InboxAndSendMessageView.as_view(),name='inbox-default'),
    path('<str:username>/',InboxAndSendMessageView.as_view(),name='inbox'),
    

]