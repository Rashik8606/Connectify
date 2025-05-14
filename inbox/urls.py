from django.urls import path
from .views import InboxAndSendMessageView



urlpatterns = [
    path('',InboxAndSendMessageView.as_view(),name='inbox-default'),
    path('<str:username>/',InboxAndSendMessageView.as_view(),name='inbox'),

]