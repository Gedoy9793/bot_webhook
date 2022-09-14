from .flask import app as application 
from . import settings
from .bot import Bot

bot = Bot()
bot.schedule(settings.URL, settings.VERIFY, settings.BOT)
bot.start()
