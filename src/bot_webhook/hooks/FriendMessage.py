import base64
from io import BytesIO
from .. import settings
from ..utils.ruru_weather import get_weather_image

def hook(bot, data):
    qq = data.get('sender').get('id')
    if str(qq) == settings.ADMIN_QQ:
        for msg in data.get('messageChain'):
            if msg.get('type') == 'Plain':
                if msg.get('text') == 'ping':
                    bot.send_text(settings.ADMIN_QQ, 'pong')
                    return
                if msg.get('text') == '天气':
                    bot.send({
                        "target":settings.ADMIN_QQ,
                        "messageChain":[
                            { "type": "Image", "url": "http://106.52.73.51:18002/ruru/weather" },
                        ]
                    }, 'sendFriendMessage')
                    return
