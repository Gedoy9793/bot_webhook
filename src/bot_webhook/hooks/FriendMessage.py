from .. import settings

def hook(bot, data):
    qq = data.get('sender').get('id')
    if str(qq) == settings.ADMIN_QQ:
        for msg in data.get('messageChain'):
            if msg.get('type') == 'Plain':
                if msg.get('text') == 'ping':
                    bot.send_text(settings.ADMIN_QQ, 'pong')
                    return
