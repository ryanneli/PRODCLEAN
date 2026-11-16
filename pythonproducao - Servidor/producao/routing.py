from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # A barra no final é importante se o seu log mostra /ws/chat/1/
    re_path(r'ws/chat/(?P<grupo_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]