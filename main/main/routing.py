from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from .consumer import LiveScoreConsumer

websockets = URLRouter([
    path(
        "ws/chat", LiveScoreConsumer.as_asgi(),
        name="get-good",
    ),
])
application = ProtocolTypeRouter({
    "websocket": websockets,
})
