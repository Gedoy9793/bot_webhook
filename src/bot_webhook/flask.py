import datetime
import requests
from io import BytesIO
from flask import Flask, request, send_file, make_response
from flask_cors import cross_origin
from .bot import Bot
from . import settings
from .utils.ruru_weather import get_weather_image

bot = Bot()
bot.schedule(settings.URL, settings.VERIFY, settings.BOT)
bot.start()

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
commit: {data.get('head_commit').get('id')[:7]}
message: {data.get('head_commit').get('message')}
author: {data.get('head_commit').get('author').get('name')}"""
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
commit: {data.get('GIT_COMMIT')[:7] if data.get('GIT_COMMIT') else None}
result: {data.get('BUILD_STATUS')}"""
    bot.send_group_text(msg)
    return "OK"

@app.route('/ruru/weather')
def ruru_weather():
    res = BytesIO(get_weather_image())

    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    tomorrow = today + datetime.timedelta(days=1)
    res = make_response(send_file(res, mimetype='image/jpeg', max_age=(tomorrow - now).seconds))
    res.headers["Expires"] = tomorrow.strftime('%a, %d %b %Y %H:%M:%S GMT+0800 (CST)')
    return res

@app.route('/redirect', methods=['GET', 'POST'])
@cross_origin()
def redirect():
    headers = dict(request.headers)
    headers.pop('Host', None)
    headers.pop('Origin', None)
    headers.pop('Sec-Fetch-Site', None)
    headers.pop('Sec-Fetch-Mode', None)
    headers.pop('Sec-Fetch-Dest', None)
    headers.pop('Sec-Fetch-User', None)

    res =  requests.request(method=request.method, url=request.values.get('url'), data=request.data, headers=headers)
    return res.content

@app.route('/webhook/staticFileUpdate', methods=["POST"])
def staticFileUpdate():
    print(request.get_json())
    data = request.get_json().get("fileList")
    msg = "Static File Update\n"
    for path in list(data.keys())[:min(8, len(data))]:
        msg += f"\n{path} : {data[path]}"
    if len(data) > 8:
        msg += f"\n...(total: {len(data)})"
    # bot.send_group_text(msg)
    print(msg)
    return "OK"