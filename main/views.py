from telebot import types
from rest_framework.response import Response
from rest_framework.views import APIView
import config

from .main import bot

class UpdateBot(APIView):
    def post(self, request):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return Response({'code': 200})

bot.set_webhook(url=config.webhook_url)
