from flask import Flask, request
from .bot import Bot
from . import settings

bot = Bot()
bot.schedule(settings.URL, settings.VERIFY, settings.BOT)
bot.start()

# bot.send_text('gunicorn process starting...')

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github():
    event = request.headers.get('X-GitHub-Event')
    if event == 'ping':
        data = request.get_json()
        msg = f"GitHub Webhook set at {data.get('repository').get('name')}"
        bot.send_group_text(msg)

    if event == 'push':
        data = request.get_json()
        msg = f"""GitHub Push at {data.get('repository').get('name')}
ref: {data.get('ref')}
commit: {data.get('head_commit').get('id')[-7:]}
message: {data.get('head_commit').get('message')}
author: {data.get('head_commit').get('author').get('name')}
"""
        bot.send_group_text(msg)

    return "OK"

@app.route('/webhook/codesign', methods=['POST'])
def codesign():
    data = request.get_json()
    if data.get('event') == 'ping':
        bot.send_group_text(f"CoDesign Webhook set")
        return 'pong'

@app.route('/webhook/jenkins', methods=['POST'])
def jenkins():
    data = request.get_json()
    msg = f"""Jenkins Build at {data.get('JOB_NAME')}
build_id: {data.get('BUILD_DISPLAY_NAME')}
ref: {data.get('GIT_BRANCH')}
commit: {data.get('GIT_COMMIT')[-7:] if data.get('GIT_COMMIT') else None}
result: {data.get('BUILD_STATUS')}
"""
    bot.send_group_text(msg)
