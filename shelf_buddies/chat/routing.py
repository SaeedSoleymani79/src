from django.urls import path , include, re_path
from . import consumers
 
# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
#    path("" , consumers.ChatConsumer.as_asgi()) , 
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.Chat_Consumer.as_asgi()),
]