import base64
from io import BytesIO
from .. import settings
from ..utils.ruru_weather import get_weather_image

def hook(bot, data):
    qq = data.get('sender').get('group').get('id')
    if str(qq) == settings.QQ_GROUP:
        for msg in data.get('messageChain'):
            if msg.get('type') == 'Plain':
                if msg.get('text') == '天气':
                    bot.send({
                        "target":settings.QQ_GROUP,
                        "messageChain":[
                            { "type": "Image", "url": "http://106.52.73.51:18002/ruru/weather" },
                        ]
                    }, 'sendGroupMessage')
                    return
