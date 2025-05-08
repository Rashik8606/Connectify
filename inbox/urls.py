from django.urls import path
from .views import InboxAndSendMessageView



urlpatterns = [
    path('inbox/',InboxAndSendMessageView.as_view(),name='inbox-default'),
    path('inbox/<str:username>/',InboxAndSendMessageView.as_view(),name='inbox'),

]