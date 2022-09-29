from .. import settings
from ..utils.get_file import _get_file
from ..utils.ruru_weather import _get_weather_image

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
                            { "type": "Image", "url": "https://bot.api.gedoy.cn/ruru/weather" },
                        ]
                    }, 'sendFriendMessage')
                    return
                if msg.get('text') == 'file cache':
                    bot.send_text(settings.ADMIN_QQ, str(_get_file.cache_info()))
                    return
                if msg.get('text') == 'weather cache':
                    bot.send_text(settings.ADMIN_QQ, str(_get_weather_image.cache_info()))
                    return
