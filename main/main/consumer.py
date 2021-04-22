import json


from channels.generic.websocket import AsyncWebsocketConsumer


from .models import get_good_amount


class LiveScoreConsumer(AsyncWebsocketConsumer):
    groups = ['boradvase']
    async def connect(self):
        print("accept")
        await self.accept()


    async def receive(self, text_data):

        good_name = json.loads(text_data).get('good_name')

        message = await get_good_amount(good_name)
        await self.send(text_data=json.dumps({
            "message": message,
        }))
