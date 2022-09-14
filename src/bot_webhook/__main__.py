import asyncio
from .bot import Bot
from .flask import app
from . import settings

bot = Bot()
bot.schedule(settings.URL, settings.VERIFY, settings.BOT)
bot.start()

app.run()
asyncio.get_event_loop().run_forever()